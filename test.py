from collections import OrderedDict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time
from backend.text2query.llm import write_nosql_query, write_nosql_query_no_pbac

# Function to calculate semantic similarity
def calculate_semantic_similarity(text1, text2):
    # Create a TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the texts into TF-IDF vectors
    vectors = vectorizer.fit_transform([text1, text2])

    # Compute the cosine similarity between the vectors
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])

    return similarity[0][0]

""" # Example inputs
text1 = "The cat sits on the mat."
text2 = "A feline is resting on a rug."

# Calculate similarity
similarity_score = calculate_semantic_similarity(text1, text2)
print(similarity_score) """

start = time.time()
a, q, _ = write_nosql_query_no_pbac("Count the umber of docs", "Research", 2)
print(time.time() - start)

from backend.pbac import re_write_query

print(re_write_query(q, a, "Research"))


