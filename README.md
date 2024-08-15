# Knowledge Graph-Based Recommender System
- By Venkata Bhargavi S & Krishnakanth J

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



## Approaches

### 1. Simple Graph Agent

This approach uses a straightforward graph traversal algorithm to generate recommendations based on direct relationships in the knowledge graph.

### 2. Embedding-Based

This method utilizes vector embeddings to capture semantic relationships between entities, enabling more nuanced recommendations.

### 3. Entity Extraction + LLM

This approach combines entity extraction techniques with a Large Language Model to understand user queries and generate context-aware recommendations.

## Installation Guide

1. Clone the repository:

2. Create a virtual environment (optional but recommended):

3. Install the required dependencies: `pip install -r requirements.txt`

4. run `streamlit app.py`

*Open your web browser and navigate to `http://localhost:8501` to access the Streamlit app*

## Challenges

1. **Short contextual data**: Dealing with limited context in user queries and knowledge graph entries.
2. **Cypher query generation**: Ensuring valid relationships and entities in generated Cypher queries.
3. **Open-source LLM limitations**: Managing API call restrictions when using open-source language models.
4. **Understanding User Queries**: Accurately mapping user input to entities and intents within the knowledge graph.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Reference:
