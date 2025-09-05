import faiss
import numpy as np
from django.conf import settings
import os
import re
from .ai_client import ai_client

class VectorStore:
    def __init__(self, dim=768, chunk_size=500, chunk_overlap=50):
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def _split_text_into_chunks(self, text: str, metadata: dict = None):
        """Split text into overlapping chunks while preserving sentence boundaries."""
        # Clean up text
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Split by sentences first
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            # If adding this sentence would exceed chunk_size, save current chunk
            if current_length + sentence_length > self.chunk_size and current_chunk:
                chunks.append({
                    "text": current_chunk.strip(),
                    "metadata": {
                        **(metadata or {}),
                        "chunk_index": len(chunks),
                        "total_chunks": None  # Will be set later
                    }
                })
                
                # Start new chunk with overlap
                overlap_text = self._get_overlap_text(current_chunk, self.chunk_overlap)
                current_chunk = overlap_text + " " + sentence if overlap_text else sentence
                current_length = len(current_chunk)
            else:
                # Add sentence to current chunk
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
                current_length = len(current_chunk)
        
        # Don't forget the last chunk
        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "metadata": {
                    **(metadata or {}),
                    "chunk_index": len(chunks),
                    "total_chunks": None
                }
            })
        
        # Update total_chunks count
        for chunk in chunks:
            chunk["metadata"]["total_chunks"] = len(chunks)
        
        return chunks

    def _get_overlap_text(self, text: str, overlap_size: int):
        """Get the last overlap_size characters from text, preferring word boundaries."""
        if len(text) <= overlap_size:
            return text
        
        # Try to find a good word boundary within the overlap region
        overlap_text = text[-overlap_size:]
        space_index = overlap_text.find(' ')
        
        if space_index != -1:
            return overlap_text[space_index:].strip()
        return overlap_text

    def add_document(self, doc_text: str, metadata: dict = None):
        """Add a document by splitting it into chunks and embedding each chunk."""
        chunks = self._split_text_into_chunks(doc_text, metadata)
        
        for chunk in chunks:
            vec = np.array([ai_client.embed_text(chunk["text"])], dtype="float32")
            self.index.add(vec)
            self.documents.append(chunk)

    def add_chunk(self, chunk_text: str, metadata: dict = None):
        """Add a single chunk directly without splitting."""
        vec = np.array([ai_client.embed_text(chunk_text)], dtype="float32")
        self.index.add(vec)
        self.documents.append({"text": chunk_text, "metadata": metadata})

    def search(self, query: str, top_k=3):
        """Search for the most relevant chunks."""
        query_vec = np.array([ai_client.embed_text(query)], dtype="float32")
        distances, indices = self.index.search(query_vec, top_k)
        results = []
        
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                result = self.documents[idx].copy()
                result["distance"] = float(distances[0][i])
                results.append(result)
        
        return results

    def load_from_folder(self, folder_path: str):
        """Load all text files from folder and split them into chunks."""
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                
                base_metadata = {
                    "filename": filename,
                    "file_path": file_path
                }
                
                self.add_document(text, metadata=base_metadata)
                print(f"Loaded and chunked: {filename}")

    def get_stats(self):
        """Get statistics about the vector store."""
        total_chunks = len(self.documents)
        files = set()
        
        for doc in self.documents:
            if doc.get("metadata", {}).get("filename"):
                files.add(doc["metadata"]["filename"])
        
        return {
            "total_chunks": total_chunks,
            "total_files": len(files),
            "files": list(files)
        }
