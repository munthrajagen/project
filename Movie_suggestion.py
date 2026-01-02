import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import DBSCAN
from sklearn.ensemble import RandomForestRegressor

# Load dataset
df = pd.read_csv(r"Downloads\movies.csv")


# Encode genre
genre_encoder = LabelEncoder()
df['genre_encoded'] = genre_encoder.fit_transform(df['genre'])

# Features for clustering
X_cluster = df[['rating', 'views']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_cluster)

# DBSCAN clustering
dbscan = DBSCAN(eps=0.8, min_samples=2)
df['cluster'] = dbscan.fit_predict(X_scaled)

# Create popularity score (target for RF)
df['popularity_score'] = df['rating'] * 0.6 + (df['views'] / df['views'].max()) * 0.4

# Train Random Forest
X_rf = df[['rating', 'views', 'year', 'duration', 'genre_encoded']]
y_rf = df['popularity_score']

rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_rf, y_rf)

# User input
user_genre = input("Enter movie genre: ").strip()

if user_genre not in genre_encoder.classes_:
    print("Genre not found!")
else:
    encoded_genre = genre_encoder.transform([user_genre])[0]

    filtered = df[df['genre_encoded'] == encoded_genre]

    if filtered.empty:
        print("No movies available for this genre.")
    else:
        # Predict popularity
        filtered['predicted_score'] = rf.predict(
            filtered[['rating', 'views', 'year', 'duration', 'genre_encoded']]
        )

        recommendations = filtered.sort_values(
            by='predicted_score', ascending=False
        )

        print("\nRecommended Movies:\n")
        c = 0
        for _, row in recommendations.iterrows():
            print(f"{row['title']} | Rating: {row['rating']} | Views: {row['views']}")
            c+=1
        print(c)
