import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
movies_df = pd.read_csv("data/movies.csv")
ratings_df = pd.read_csv("data/ratings.csv")

# 1. Analyze the most popular movies based on average ratings
def analyze_popular_movies(top_n=10):
    movie_ratings = ratings_df.groupby('movieId')['rating'].mean().reset_index()
    movie_ratings = movie_ratings.merge(movies_df, on='movieId')
    popular_movies = movie_ratings.sort_values(by='rating', ascending=False).head(top_n)

    # Print clean output
    print(f"\n🎬 Top {top_n} Highest Rated Movies 🎯\n")
    print(popular_movies[['title', 'rating']].to_string(index=False))

    # Save to CSV and HTML
    popular_movies[['title', 'rating']].to_csv('data/top_movies.csv', index=False)
    popular_movies[['title', 'rating']].to_html('data/top_movies.html', index=False)

# 2. Visualize movie counts by genre
def visualize_genre_distribution():
    genres = movies_df['genres'].str.split('|', expand=True).stack().reset_index(drop=True)
    genre_counts = genres.value_counts()

    # Plot and save
    plt.figure(figsize=(12, 6))
    genre_counts.plot(kind='bar')
    plt.title('Count of Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('data/genre_distribution.png')
    plt.show()

# 3. Recommend top-rated movies in a specific genre
def recommend_movies_by_genre(genre, top_n=5):
    genre_movies = movies_df[movies_df['genres'].str.contains(genre, case=False, na=False)]
    genre_ratings = ratings_df.groupby('movieId')['rating'].mean().reset_index()
    genre_movies = genre_movies.merge(genre_ratings, on='movieId')
    recommendations = genre_movies.sort_values(by='rating', ascending=False).head(top_n)

    # Print clean recommendations
    print(f"\n🎭 Top {top_n} {genre} Movies 🎬\n")
    print(recommendations[['title', 'rating']].to_string(index=False))

    # Save to CSV and HTML
    recommendations[['title', 'rating']].to_csv(f'data/{genre}_recommendations.csv', index=False)
    recommendations[['title', 'rating']].to_html(f'data/{genre}_recommendations.html', index=False)

# Run functions
analyze_popular_movies()
visualize_genre_distribution()
recommend_movies_by_genre('Comedy')

print("\n✅ Recommendation system completed successfully!")
