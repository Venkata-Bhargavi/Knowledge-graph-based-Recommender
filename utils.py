import streamlit as st
import base64
import os
from dotenv import load_dotenv
import pandas as pd
import langchain
from langchain_community.graphs import Neo4jGraph
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import ollama
from langchain.chains import GraphCypherQAChain
import re


# ------------------------------------------- Config --------------------------------------------------------------
# Loading Local env variables
load_dotenv()

# ------------------------------------------- Configurations --------------------------------------------------------------
dataset_name = "data/sampled_cleaned_movies_data_with_embeddings.csv"

### Model Names
embedding_model_name = 'all-minilm' # model name in - Ollama
text_to_cypher_llm_model_name = "tomasonjo/llama3-text2cypher-demo" ## Model nam in - Ollama

# ------------------------------------------- Functions --------------------------------------------------------------


## 2.1 Load Data to Graph DB 
def load_data_to_graph_db(graph_db, df):
    # Loop through each row in the DataFrame and add them to the Neo4j db
    # print(f"\nTotal Number of Records to push in Graph DB: {df.shape[0]}")

    for index, row in df.iterrows():

        graph_db.query(f'''
                MERGE (m:Movie {{title: '{row.title}'}})                             
                SET m.awards = {row.awards},                        
                    m.id = "{row.movie_id}",                                    
                    m.tagline = "{row.tagline}",                                
                    m.imdbRating = toFloat({(row.imdb_rating)}) 
                
                FOREACH (director IN split("{row.directors}", '|') |             
                    MERGE (p:Person {{name: trim(director)}})                  
                    MERGE (p)-[:DIRECTED]->(m))                             
                            
                FOREACH (actor IN split("{row.cast}", '|') |                  
                    MERGE (p:Person {{name: trim(actor)}})                     
                    MERGE (p)-[:ACTED_IN]->(m))                             
                            
                FOREACH (genre IN split("{row.genres}", '|') |                  
                    MERGE (g:Genre {{name: trim(genre)}})                      
                    MERGE (m)-[:IN_GENRE]->(g))                             
                            
                MERGE (l:Language {{name: trim("{row.languages}")}})
                MERGE (m)-[:WAS_RELEASED_IN]->(l)
                        
            ''')
    
    # print("\nPushed all the records to the graph db!")

## 2.2 update Data to Graph DB 

def update_graph_db_with_new_data(graph_db, df):
    graph_db.refresh_schema()
    if graph_db.schema == 'Node properties:\n\nRelationship properties:\n\nThe relationships:\n':
        # print("\nGraph DB is Empty!\n")
        load_data_to_graph_db(graph_db, df)
    else:
        # print("\nGraph DB is not empty, so deleting the records from DB!")

        ## Query to Delete all the nodes and relationship from the graph db
        graph_db.query('''
            MATCH (n)
            DETACH DELETE n
        ''')

        # print("\nPushing new data to Graph DB")
        load_data_to_graph_db(graph_db, df)

## 2.3 Create Vector Index on tagline_embeddings column
def create_vector_index_in_graph_db(graph_db, df):
    graph_db.query("""
        CREATE VECTOR INDEX movie_tagline_embeddings IF NOT EXISTS      // Create a vector index named 'movie_tagline_embeddings' if it doesn't already exist  
        FOR (m:Movie) ON (m.tagline_embedding)                           // Index the 'taglineEmbedding' property of Movie nodes 
        OPTIONS { indexConfig: {                                        // Set options for the index
            `vector.dimensions`: 384,                                    // Specify the dimensionality of the vector space (1536 dimensions)
            `vector.similarity_function`: 'cosine'                        // Specify the similarity function to be cosine similarity
        }}"""
    )

    # print(f"Updating the graph db with tagline embeddings") 
    for index, row in df.iterrows():
        title = row['title']
        embedding = row['tagline_embedding']
        graph_db.query(f"MATCH (m:Movie {{title: '{title}'}}) SET m.tagline_embedding = {embedding}")

    # print(f"Updated the graph db with tagline embeddings and here is the schema of the db:\n{graph_db.schema}") 

# 3. Generate Embeddings
def embed_text(text:str):
    response = ollama.embeddings(model= embedding_model_name, prompt=text)
    return response["embedding"]  

def generate_embeddings_for_data(df):
    df['tagline_embedding'] = df["tagline"].apply(lambda x: embed_text(x))
    return df

def load_llm_model(model_name):
    ## Initiate Cypher llm 
    return ChatOllama(model=model_name)

def load_base_dataset(dataset_path):
    df = pd.read_csv(dataset_path)
    df['title'] = df['title'].apply(lambda x: re.sub(r'[^A-Za-z0-9\s]', '', x))
    return df


# ------------------------------------------- Chat Prompt Templates and their Functions --------------------------------------------------------------

## 1. Function - to search the graph db
def simple_graph_db_search_by_generating_cypher_queries(graph_db, text_to_cypher_llm, question):

    # Template to convert Question to Cypher Query
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Given an input question, convert it to a Cypher query. No pre-amble.",
            ),
            (
                "human",
                (
                    "Based on the Neo4j graph schema below, write a Cypher query that would answer the user's question: "
                    "\n{schema} \nQuestion: {question} \nCypher query:"
                ),
            ),
        ]
    )

    # Chain
    cypher_query_chain = prompt | text_to_cypher_llm

    # Generate Cypher Query using Chain
    cypher_query_response = cypher_query_chain.invoke({"question": question, "schema": graph_db.schema}).content

    # Trigger the Graph db to fetch results
    result = graph_db.query(cypher_query_response)
    print(f"\nGraph DB response:\n{result}")  

    format_response = text_to_cypher_llm.invoke(f"Based on the following content, format it in a more readable and understandable output to make clear to the audience, {result}")
    print(f"\nImproved responses:\n{format_response.content}")  
    return format_response.content

## 1.1 Similar to above function - with langchain in-built function - GraphCypherQAChain    
def cypher_chain_graph_db_search_by_generating_cypher_queries(graph_db, text_to_cypher_llm, question):
    graphCypher_chain = GraphCypherQAChain.from_llm(graph=graph_db, llm=text_to_cypher_llm, validate_cypher=True)

    response = graphCypher_chain.invoke({"query": question})
    print(f"\nGraph Cypher Chain response:\n{response["result"]}")
    return response['result']


# ------------------------------------------- Function - to Improve Results Response --------------------------------------------------------------

### Index-Vector Search based on the Embeddings Approach 
def embed_question_to_improve_search_results(graph, text_to_cypher_llm, question):
    question_emb = embed_text(question)

    result = graph.query("""
            with $question_embedding as question_embedding      // Use the provided question embedding as 'question_embedding'
            CALL db.index.vector.queryNodes(                    // Call the vector index query function
                'movie_tagline_embeddings',                     // Name of the vector index to query against
                $top_k,                                         // Number of top results to retrieve
                question_embedding                              // The question embedding to compare against
                ) YIELD node AS movie, score                    // Yield each matched node and its similarity score
            RETURN movie.title, movie.tagline, score            // Return the title, tagline, and similarity score of each movie
            """,
            params={
                "question_embedding": question_emb,       # Pass the question embedding as a parameter
                "top_k": 3                                      # Specify the number of top results to retrieve
    })

    promt_improve_response = f"""Here is the graph db schema which has entities with properties and the relationship between entities
            {graph.schema}
            Here is the user question: {question}
            Here is the model output response: {result}

            format the model output response in a more readable and understandable way for clarity, without adding any additional information.
            Note:
            Do not include any text except the provided information.
            """

    improved_result = text_to_cypher_llm.invoke(promt_improve_response).content

    print(improved_result)
    return improved_result

## Function to Extract Entities + Generate Cypher Queries + Trigger DB
def extract_entites_using_cypher_model(graph_db, text_to_cypher_llm, question):    
    ENTITY_EXTRACTION_AND_CYPHER_GENERATION_TEMPLATE = f"""
                    Task: Breakdown the user input and Extract relevant entities from the user input and generate a Cypher query to retrieve the unknown entities using the known entities.
                    Instructions:
                    1. Identify and extract the known entities (e.g., movie title) from the user input.
                    2. Determine the unknown entities (e.g., cast, awards, genres, directors) that need to be retrieved from the graph database.
                    3. Use the known entities to generate a Cypher query that retrieves the values of the unknown entities and validate the generated Cypher query entities and relationships with the reference schema to ensure the query is valid.
                    Schema:
                    {graph_db.schema}
                    Note: Do not include any explanations or apologies in your responses.
                    Do not respond to any questions that might ask for anything other than extracting entities and generating a Cypher query.
                    Do not include any text except the extracted entities and the generated Cypher query.
                    Examples:

                    # Example user input: "Which genres does the movie Inception belong to and who directed it?"
                    Output:
                    MATCH (m:Movie {{title: "Inception"}})
                    OPTIONAL MATCH (m)-[:IN_GENRE]->(g:Genre)
                    OPTIONAL MATCH (p:Person)-[:DIRECTED]->(m)
                    RETURN collect(DISTINCT g.name) AS genres, collect(DISTINCT p.name) AS directors

                    # Example user input: "What is the IMDb rating of The Dark Knight, and in which language was it released?"
                    Output:
                    MATCH (m:Movie {{title: "The Dark Knight"}})
                    OPTIONAL MATCH (m)-[:WAS_RELEASED_IN]->(l:Language)
                    RETURN m.imdbRating AS imdbRating, collect(DISTINCT l.name) AS languages

                    # Example user input: "Who acted in the movie Titanic, and what is its tagline?"
                    Output:
                    MATCH (m:Movie {{title: "Titanic"}})
                    OPTIONAL MATCH (p:Person)-[:ACTED_IN]->(m)
                    RETURN collect(DISTINCT p.name) AS cast, m.tagline AS tagline

                    # Example user input: "Did the movie Avatar win any awards, and what is its IMDb rating?"
                    Output:
                    MATCH (m:Movie {{title: "Avatar"}})
                    RETURN m.awards AS awards, m.imdbRating AS imdbRating


                    # Example user input: "Which languages was the movie Parasite released in and who directed it?"
                    Output:
                    MATCH (m:Movie {{title: "Parasite"}})
                    OPTIONAL MATCH (m)-[:WAS_RELEASED_IN]->(l:Language)
                    OPTIONAL MATCH (p:Person)-[:DIRECTED]->(m)
                    RETURN collect(DISTINCT l.name) AS languages, collect(DISTINCT p.name) AS directors

                    # Example user input: "Recommend 3 movies with  atleast a award and should be in english language"
                    Output:
                    MATCH (m:Movie)-[:WAS_RELEASED_IN]->(l:Language)
                    WHERE l.name = 'English' AND m.awards > 1 
                    RETURN m.title
                    LIMIT 3

                    # Example user input: "Recommend 3 movies with imdb rating atleast 7 and atleast a award and should be in english language"
                    MATCH (m:Movie)-[:WAS_RELEASED_IN]->(l:Language)
                    WHERE l.name = 'English' AND m.awards > 1 and m.imdbRating >= 7.0
                    RETURN m.title
                    LIMIT 3

                    The question is:
                    {question}
        """


    entities_extracted_query = text_to_cypher_llm.invoke(ENTITY_EXTRACTION_AND_CYPHER_GENERATION_TEMPLATE).content
    print(f"\nModel Generated Cypher Query:\n\n{entities_extracted_query}")
    fetched_results = graph_db.query(f"""{entities_extracted_query}""")
    print(f"\n\nFetched Results:\n{fetched_results}")

    format_response = text_to_cypher_llm.invoke(f"""
                    Given the user question:\n{question} and the output response:\n{fetched_results}, 
                    format the response in a more readable and understandable way for clarity, without adding any additional information.
                    Note:
                    Do not include any text except the provided information.
                    """)

    # format_response = text_to_cypher_llm.invoke(f"Based on the following user question: \n{question} and output response: \n{fetched_results}, format it in a more readable and understandable output to make clear to the audience")
    print(f"\nImproved responses:\n{format_response.content}")  
    return format_response.content
