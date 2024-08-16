# Knowledge Graph-Based Recommender System
**Developed By:**

> Venkata Bhargavi S (002724793) &
> 
> Krishnakanth J (002724795)

## Introduction

This project implements a knowledge graph-based recommender system using Large Language Models (LLMs), Neo4j for graph database management, and Streamlit for user interaction. The system aims to provide personalized recommendations by leveraging the power of knowledge graphs and advanced natural language processing techniques.



## Flow

1. User inputs a query through the Streamlit interface
2. The system processes the query using one of three approaches
3. The chosen approach interacts with the Neo4j knowledge graph
4. Results are retrieved and processed
5. Recommendations are presented to the user via the Streamlit app

## Architecture Diagram

![arch_diag](https://github.com/user-attachments/assets/0485025d-2102-469a-90b5-8adc91a84ce9)


## Technology Stack

1. **Neo4j**: Used to store and manage the knowledge graph, allowing us to efficiently query and traverse relationships between entities like movies, genres, and actors to provide relevant recommendations.

2. **Streamlit**: Implemented to build the interactive user interface, enabling users to input their queries and view personalized recommendations directly in a web browser.

3. **Large Language Models (LLMs)**: Utilized for natural language processing tasks such as converting user queries into Cypher queries, extracting relevant entities, and generating embeddings to match user inputs with the knowledge graph data.

4. **Ollama**: Employed to run pre-trained language models locally. Models like `all-minilm` and `llama3-text2cypher-demo` were used to generate vector embeddings for similarity searches and convert natural language questions into structured Cypher queries.

5. **Python**: Used as the core programming language for implementing the backend logic, integrating with Neo4j, processing user queries, and deploying the Streamlit application.

6. **Cypher**: Employed to interact with the Neo4j database by executing generated queries, allowing us to retrieve and manipulate graph data based on the user’s input.

7. **.env**: Used to securely store and manage environment variables, such as Neo4j credentials, ensuring that sensitive information remains protected and easily configurable.



## Approaches

### 1. Simple Graph Agent

- **Convert Question to Cypher Query:** The function uses a language model to convert a user's question into a Cypher query based on the graph database schema.
- **Execute the Query:** The generated Cypher query is run against the Neo4j graph database to fetch relevant results.
- **Format the Results:** The raw results from the database are then formatted by the language model into a more readable and understandable output for the user.

### 2. Embedding-Based Agent(Embed User Input + Graph Index Vector Search)
This process enhances search results in a Neo4j graph database by using an embedding-based approach
- **Question Embedding:** The user's question is converted into a vector embedding that captures its semantic meaning.
- **Vector Index Search:** The function queries the graph database using the question embedding. It compares the embedding against a pre-built vector index of movie taglines to find the most similar results.
- **Retrieve and Rank Results:** The database returns the top matching movie titles and taglines along with their similarity scores, based on the comparison of embeddings.
- **Result Formatting:** The raw search results are formatted by a language model into a clear and concise response, making the information easier to understand.
- **Final Output:** The function returns and prints a well-structured summary of the search results, providing a user-friendly presentation of the most relevant movies based on the question's context.

### 3. Entity Extraction Based Agent + LLM (Entities Extraction using Graph Schema + Query Generation)

- **Entity Extraction and Query Generation:** The function uses a language model to analyze the user's question and extract relevant entities (e.g., movie titles, genres). It then generates a Cypher query based on these entities using a predefined template.
- **Query Execution:** The generated Cypher query is executed against the Neo4j graph database to fetch the required data.
- **Result Formatting:** The raw results from the database are formatted by the language model into a clear and understandable response.
- **Final Output:** The function returns and prints a well-structured summary of the query results, making it easier for users to interpret the data.

### Graph Model

![image](https://github.com/user-attachments/assets/1e0cb867-9475-4cfa-b882-6656bc276657)


## Installation Guide

1. Clone the repository: `git clone https://github.com/Venkata-Bhargavi/Knowledge-graph-based-Recommender.git`

2. Add Neo4j credentials in `.env` file
   
   > NEO4J_URI =
   > 
   > NEO4J_USERNAME =
   > 
   > NEO4J_PASSWORD =

3. Download the Following Ollama models

   **Get local Ollama from the following Link: https://github.com/ollama/ollama**

   > Ollama pull all-minilm
   > 
   > ollama pull "tomasonjo/llama3-text2cypher-demo"
   
4. Install the required dependencies: `pip install -r requirements.txt`

5. run `streamlit app.py`

*Open your web browser and navigate to `http://localhost:8501` to access the Streamlit app*

## Evaluation Results:

![image](https://github.com/user-attachments/assets/a12740e9-cca4-46f1-a354-b5dfe605d48a)

**Purpose of Evaluation: **
The evaluation aims to assess how well the fine-tuned model can translate user requests (in natural language) into accurate Cypher queries that can be executed on the Neo4j database to retrieve movie recommendations.

**Evaluation Metric: **The metric used is "generated_queries_match proportion", which measures the similarity or accuracy between the generated Cypher queries and the actual (expected) Cypher queries.

**Results Interpretation:**

> True: 0.9 (90%)
> 
> False: 0.1 (10%)


## Challenges

1. **Short contextual data**: Dealing with limited context in user queries and knowledge graph entries.
2. **Cypher query generation**: Ensuring valid relationships and entities in generated Cypher queries.
3. **Open-source LLM limitations**: Managing API call restrictions when using open-source language models.
4. **Understanding User Queries**: Accurately mapping user input to entities and intents within the knowledge graph.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Reference:
