import os
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class EmbeddingManager:
    def __init__(self):
        key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=key)
        self.embeddings = {}

    def get_embedding(self, text):
        response = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding

    def add_document(self, doc_id, text):
        self.embeddings[doc_id] = self.get_embedding(text)

    def find_most_similar(self, query, top_k=3):
        query_embedding = self.get_embedding(query)
        similarities = {}
        for doc_id, doc_embedding in self.embeddings.items():
            similarity = cosine_similarity([query_embedding], [doc_embedding])[0][0]
            similarities[doc_id] = similarity
        
        sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        return [doc_id for doc_id, _ in sorted_similarities[:top_k]]

embedding_manager = EmbeddingManager()