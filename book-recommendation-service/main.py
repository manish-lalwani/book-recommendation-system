import pandas as pd
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


app = Flask("Book Recommender")
#df = pd.read_csv("src/book_crud_service/book_recommender_model/dataset/BooksDataset.csv")
df = pd.read_csv("dataset/BooksDataset.csv")

#For temporary data have Remove books with null descriptions as it contains over 1 lakh rows and 30K are with null so
df = df[df['Description'].notnull()]
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
description_vectors = vectorizer.fit_transform(df["Description"])
nn = NearestNeighbors(metric='cosine', algorithm='brute')
nn.fit(description_vectors)


def get_description_from_title(title,df):
    result =  df[df['Title'].str.lower() == title.lower()]
    if not result.empty:
        return result.iloc[0]["Description"]
    else:
        return None


def get_recommendations_by_title(book_title,nn_model,df,n_neighbors=5):
    book_description = get_description_from_title(book_title, df)
    if not book_description:
        return f"Book titled '{book_title}' not found."

    input_vector = vectorizer.transform([book_description])
    distances, indices = nn_model.kneighbors(input_vector,n_neighbors=n_neighbors)

    recommended_books = df['Title'].iloc[indices.flatten()[1:]]

    return recommended_books


# book_title = "110%: 110 Strategies For Feeling Great Every Day"  # Replace with the user's input
# recommendations = get_recommendations_by_title(book_title, nn, df)
# print(recommendations)


@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    try:
        data = request.get_json()

        if 'title' not in data:
            return jsonify({"error": "Missing required parameter: title"}), 400

        book_title = data['title']
        n_neighbors = data.get('n_neighbors', 5)

        recommendations, error = get_recommendations_by_title(book_title, nn, df, n_neighbors)
        if error:
            return jsonify({"error": error}), 404

        return jsonify({"recommended_books": recommendations})

    except Exception as e:
        app.logger.error(f"Error occurred: {str(e)}")
        return jsonify({"Error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

