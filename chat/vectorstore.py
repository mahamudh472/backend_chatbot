import faiss
import numpy as np
from django.conf import settings
import os
from .gemini_client import embed_text

class VectorStore:
    def __init__(self, dim=768):
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []

    def add_document(self, doc_text: str, metadata: dict = None):
        vec = np.array([embed_text(doc_text)], dtype="float32")
        self.index.add(vec)
        self.documents.append({"text": doc_text, "metadata": metadata})

    def search(self, query: str, top_k=3):
        query_vec = np.array([embed_text(query)], dtype="float32")
        distances, indices = self.index.search(query_vec, top_k)
        results = [self.documents[i] for i in indices[0] if i < len(self.documents)]
        return results

    def load_from_folder(self, folder_path: str):
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                    text = f.read()
                self.add_document(text, metadata={"filename": filename})
