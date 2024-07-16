# Knowledge Graph Based Music Recommendation System with LLMs and neo4j



## Introduction:
The explosive growth of social media platforms has revolutionized the way music is discovered and consumed, offering both opportunities and challenges for aspiring musicians. Among these platforms, TikTok has emerged as a powerhouse for viral content and music promotion, yet many talented artists struggle to break through the noise and gain visibility.

- Complex Data Representation
- Enhanced Querying and Analysis


## Team:

- Krishna J
- Bhargavi S

  
## Dataset Insights

The dataset used for this project categorizes song attributes, metadata, and user interactions, facilitating personalized recommendations and enhancing music discovery on TikTok.

### Key Features

1. **Song Attributes**: Danceability, Acousticness, Energy, etc.
2. **Metadata**: Genre, Year, Artist, Likes, etc.
3. **User Interactions**: Tags, User, Playcount, etc.


### Pipe Line:

<img width="461" alt="Screenshot 2024-07-16 at 1 59 33 PM" src="https://github.com/user-attachments/assets/8d18eb81-ecd6-436a-8cd9-bdd376c215c7">


### Challenges

- **Limited Exposure**: Despite TikTok's vast user base, many new artists find it difficult to gain traction.
- **Content Diversity**: Dominance of popular genres and established artists limits exposure to diverse musical styles.
- **Viral Promotion**: Mechanisms for promoting new music and nurturing artist-fan relationships are underdeveloped.
- **Community Engagement**: Engagement features for artists are relatively nascent compared to other platforms.

## Dataset Insights

The dataset used for this project categorizes song attributes, metadata, and user interactions, facilitating personalized recommendations and enhancing music discovery on TikTok.

### Key Features

1. **Song Attributes**: Danceability, Acousticness, Energy, etc.
2. **Metadata**: Genre, Year, Artist, Likes, etc.
3. **User Interactions**: Tags, User, Playcount, etc.


### Node properties:

Song {name: STRING}

Genre {name: STRING}

Year {name: STRING}

Artist {name: STRING}

Likes {name: STRING}

Tag {name: STRING}

User {name: STRING}

Danceability {name: STRING}

Acousticness {name: STRING}

Energy {name: STRING}

Liveness {name: STRING}

Tempo {name: STRING}

Valence {name: STRING}



Relationship properties:

The relationships:

(:Song)-[:HAS_TAG]->(:Tag)

(:Song)-[:LISTEN_BY]->(:User)

(:Song)-[:PERFORMED_BY]->(:Artist)

(:Song)-[:HAS_DANCEABILITY]->(:Danceability)

(:Song)-[:HAS_ACOUSTICNESS]->(:Acousticness)

(:Song)-[:HAS_ENERGY]->(:Energy)

(:Song)-[:HAS_LIVENESS]->(:Liveness)

(:Song)-[:HAS_TEMPO]->(:Tempo)

(:Song)-[:HAS_VALENCE]->(:Valence)

(:Song)-[:RELEASED_IN]->(:Year)

(:Song)-[:HAS_GENRE]->(:Genre)

(:Song)-[:TOTAL_LIKES]->(:Likes)

(:Artist)-[:HAS_GENRE]->(:Genre)

## Implementation Strategies

### Enhanced Exposure

- **Objective**: Increase visibility for emerging musicians.
- **Proposed Solutions**: Algorithmic boosts, cross-promotion with influencers, and artist spotlight features.

### Diverse Content Discovery

- **Objective**: Enable exploration of diverse music genres.
- **Proposed Solutions**: Genre-based channels, personalized recommendations, and user-generated content promotion.

### Viral Potential

- **Objective**: Enhance organic spread of music content.
- **Proposed Solutions**: Trend identification, challenge integration, and user-generated viral content promotion.

## Strategy Development Roadmap

### Utilizing Features for Recommendation Strategies

1. **Popularity-Based Recommendation**: Utilizes engagement metrics like 'Likes'.
2. **Collaborative Filtering**: Recommends based on user or item similarity.
3. **Matrix Factorization**: Uses latent factors for precise recommendations.

### Enhancing Music Exploration with Knowledge Graphs

- **Graph Data Model for Music**: Represents relationships between songs, artists, genres, etc.
- **Semantic Relationships**: Enriches understanding of music attributes and interactions.
- **User-Centric Recommendations**: Tailors recommendations based on user preferences.



## Conclusion

This proposal outlines a comprehensive strategy to enhance music discovery and engagement on TikTok by leveraging advanced recommendation algorithms and knowledge graphs. By prioritizing new artists, promoting diverse content, and fostering community engagement, the project aims to transform the way users interact with music on the platform.

### Future Works

Future developments include integrating with external platforms, enhancing NLP capabilities, analyzing user interactions, ensuring scalability, and improving visualization tools.

## References and Articles

- [Understanding Music Recommendations](Link)
- [Spotify: A Case Study of Music Recommendation Systems](Link)
- [Knowledge Graphs for Music Recommendation](Link)
- [Mel-frequency Cepstral Coefficients (MFCC) Tutorial](Link)
- [The Role of User Interactions in Music Recommendation](Link)
- [Graph-Based Methods for Music Recommendation](Link)
- [Evaluating Music Recommendation Systems](Link)
- [Natural Language Processing in Music Recommendation](Link)
- [Exploring the Use of Knowledge Graphs in Recommender Systems](Link)
- [Building Scalable and High-Performance Recommendation Systems](Link)

