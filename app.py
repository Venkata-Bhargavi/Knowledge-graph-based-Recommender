import streamlit as st
from utils import *

# ------------------------------------------- Config --------------------------------------------------------------
# Loading Local env variables
load_dotenv()

# The code below is for the layout of the page
st.set_page_config(  # Alternate names: setup_page, page, layout
    layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
    initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
    page_title='Knowledge Graph Recommendation System',  # String or None. Strings get appended with "• Streamlit".
    page_icon=None,  # String, anything supported by st.image, or None.
)

# ------------------------------------------- Configurations --------------------------------------------------------------

dataset_path = "data/sampled_cleaned_movies_data_with_embeddings_30.csv"

### Model Names
embedding_model_name = 'all-minilm' # model name in - Ollama
text_to_cypher_llm_model_name = "tomasonjo/llama3-text2cypher-demo" ## Model name in - Ollama

## 1. Load the Neo4J graph db
def load_neo4j_graph_db():
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI") ,
        username=os.getenv("NEO4J_USERNAME") ,
        password=os.getenv("NEO4J_PASSWORD") 
    )

    graph.refresh_schema()
    # print(f"Here is the Graph DB Schema:\n\n{graph.schema}")
    return graph


# Define the session state keys for models and data
if 'graph_db' not in st.session_state:
    st.session_state.graph_db = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'text_to_cypher_llm' not in st.session_state:
    st.session_state.text_to_cypher_llm = None

# ------------------------------------------- Functions --------------------------------------------------------------

def load_resources():
    # Load the Graph - Load required Models -- Fetch results --> Failed --> entities --> Fetch results
    with st.spinner("Loading Data and Graph!"):
        # 1. Load Graph and Data
        st.session_state.graph_db = load_neo4j_graph_db()
        print("Initiated Graph")

        st.session_state.df = load_base_dataset(dataset_path)
        ## Generate the embeddings on tagline column
        st.session_state.df = generate_embeddings_for_data(st.session_state.df)
        print("Loaded data")

        # ## 2. Function to update the graph DB
        update_graph_db_with_new_data(st.session_state.graph_db, st.session_state.df)
        print("Updated Graph DB with Data!")

        # ## 3. Create a Vector Index on embeddings column
        create_vector_index_in_graph_db(st.session_state.graph_db, st.session_state.df)
        print("Created Vector Index in Graph DB")

        ## Load the LLM Model
        st.session_state.text_to_cypher_llm = load_llm_model(text_to_cypher_llm_model_name)
        print("Loaded LLM model!")

def main():
    col1, col2, col3 = st.columns([0.5,2,0.4])
    with col2:
        st.header("Knowledge Graph based Movie Recommendation System :robot_face:")
        st.markdown("")

    if st.session_state.graph_db is None or st.session_state.df is None or st.session_state.text_to_cypher_llm is None:
        load_resources()

    # ------------------------------------------- Response Page  --------------------------------------------------------------

    if user_query := st.chat_input("Ask me anything about Movies? Ex: Who was the cast of the movie Road House?"):

        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Generating the response..."):
                try:
                    response = extract_entites_using_cypher_model(st.session_state.graph_db, st.session_state.text_to_cypher_llm, user_query)
                    st.markdown(f"\n{response}\n")
                except Exception as e:
                    improved_response = embed_question_to_improve_search_results(st.session_state.graph_db, st.session_state.text_to_cypher_llm, user_query) 
                    st.markdown(f"\n{improved_response}\n")

if __name__ == "__main__":
    main()

