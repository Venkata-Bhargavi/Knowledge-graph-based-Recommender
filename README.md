# Knowledge Graph-Based Recommendation System with LLMs and Neo4j



## Introduction

The rapid growth of digital platforms has revolutionized how content is consumed, offering both opportunities and challenges. In this project, we aim to develop a recommendation system leveraging knowledge graphs and large language models (LLMs) on the Million Songs dataset to provide personalized music recommendations. ![Dataset](https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm)

## Complex Data Representation

- Enhanced Querying and Analysis

## Team

- Krishna J (Building Knowledge Graph, Query Analysis using LLMs)
- Bhargavi S (Feature Extraction from Audio, Tags generation using Neural Networks, Prompt Enhancement)

  
## Dataset Insights

The dataset used for this project categorizes song attributes, metadata, and user interactions, facilitating personalized recommendations.

### Key Features

- **Song Attributes**: Danceability, Acousticness, Energy, etc.
- **Metadata**: Genre, Year, Artist, Likes, etc.
- **User Interactions**: Tags, User, Playcount, etc.


### Knowledge Graph Nodes and Relationships

- **Nodes**: Song, Genre, Year, Artist, Likes, Tag, User, Danceability, Acousticness, Energy, Liveness, Tempo, Valence
- **Relationships**:
  - (:Song)-[:HAS_TAG]->(:Tag)
  - (:Song)-[:LISTENED_BY]->(:User)
  - (:Song)-[:PERFORMED_BY]->(:Artist)
  - (:Song)-[:RELEASED_IN]->(:Year)
  - (:Song)-[:HAS_GENRE]->(:Genre)
  - (:Song)-[:TOTAL_LIKES]->(:Likes)
  - (:Song)-[:HAS_DANCEABILITY]->(:Danceability)
  - (:Song)-[:HAS_ACOUSTICNESS]->(:Acousticness)
  - (:Song)-[:HAS_ENERGY]->(:Energy)
  - (:Song)-[:HAS_LIVENESS]->(:Liveness)
  - (:Song)-[:HAS_TEMPO]->(:Tempo)
  - (:Song)-[:HAS_VALENCE]->(:Valence)


![image](https://github.com/user-attachments/assets/81e7e498-cce4-4baf-a68b-d621a8d1796e)



## Implementation Strategies

### Enhancing Recommendations with Knowledge Graphs

- **Graph Data Model for Music**: Represents relationships between songs, artists, genres, etc.
- **Semantic Relationships**: Enriches understanding of music attributes and interactions.
- **User-Centric Recommendations**: Tailors recommendations based on user preferences.

### Leveraging LLMs

- **Natural Language Understanding**: Process user queries to generate relevant recommendations.
- **Contextual Recommendations**: Use LLMs to understand user context and preferences for better recommendations.


## Evaluation Strategy

To evaluate the effectiveness of our recommendation system, we will use the following metrics:

- Normalized Discounted Cumulative Gain (NDCG): Measure the ranking quality of the retrieved items.
- Graph Coverage: Assess how much of the knowledge graph is utilized in responses

## Conclusion

This proposal outlines a strategy to develop a recommendation system that leverages advanced recommendation algorithms and knowledge graphs using LLMs and Neo4j. By focusing on personalized recommendations, the project aims to transform the way users interact with music on various platforms.

## Future Works

Future developments include integrating with external platforms, enhancing NLP capabilities, analyzing user interactions, ensuring scalability, and improving visualization tools.


