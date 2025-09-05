from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .vectorstore import VectorStore
import os
import sys
from .ai_client import ai_client

# Global variable to store the vector store instance
_vector_store = None

def get_vector_store():
    """
    Lazy-load the vector store only when needed and only for server operations.
    This prevents loading during management commands like migrate, makemigrations, etc.
    """
    global _vector_store
    
    # Check if we're in a management command context that shouldn't load vectorstore
    if len(sys.argv) > 1:
        command = sys.argv[1]
        # Commands that should NOT load vectorstore
        skip_commands = [
            'migrate', 'makemigrations', 'collectstatic', 'check', 
            'shell', 'createsuperuser', 'check_ai_status', 'showmigrations',
            'sqlmigrate', 'dbshell', 'inspectdb', 'flush', 'loaddata',
            'dumpdata', 'diffsettings', 'testserver'
        ]
        
        if command in skip_commands:
            return None
    
    if _vector_store is None:
        _vector_store = VectorStore()
        docs_folder = os.path.join(settings.BASE_DIR, 'documents')
        print("Loading vector store from documents folder...")
        _vector_store.load_from_folder(docs_folder)
        print("Vector store loaded successfully!")
    
    return _vector_store


def initialize_vector_store():
    """
    Initialize the vector store. This is called during app startup for runserver.
    """
    global _vector_store
    if _vector_store is None:
        get_vector_store()  # This will load it if appropriate



class MessageListView(ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatMessage.objects.filter(user=self.request.user)


class ChatMessageCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        message = request.data.get('message')
        if not message:
            return Response({"error": "Message content is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get vector store instance
        vector_store = get_vector_store()
        if vector_store is None:
            return Response({"error": "Vector store not available"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Search for relevant chunks (increased to 4 for better context)
        docs = vector_store.search(message, top_k=4)
        
        # Create context from chunks with metadata
        context_parts = []
        for doc in docs:
            metadata = doc.get('metadata', {})
            filename = metadata.get('filename', 'Unknown')
            chunk_info = f"(from {filename}"
            if 'chunk_index' in metadata and 'total_chunks' in metadata:
                chunk_info += f", part {metadata['chunk_index'] + 1}/{metadata['total_chunks']}"
            chunk_info += ")"
            
            context_parts.append(f"{chunk_info}:\n{doc['text']}")
        
        context = "\n\n---\n\n".join(context_parts)
        
        response = ai_client.chat_with_context(message, context)
        active_provider = ai_client.get_active_provider()
        
        data = {
            'message': message,
            'response': response,
            'user': request.user.id
        }
        serializer = ChatMessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "response": response,
                "provider": active_provider
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VectorStoreStatsView(APIView):
    """Get statistics about the vector store."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        vector_store = get_vector_store()
        if vector_store is None:
            return Response({"error": "Vector store not available"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        stats = vector_store.get_stats()
        return Response(stats, status=status.HTTP_200_OK)


class AIProviderStatusView(APIView):
    """Get status information about available AI providers."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        status_info = ai_client.get_provider_status()
        return Response(status_info, status=status.HTTP_200_OK)