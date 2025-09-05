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
from .ai_client import ai_client

vector_store = VectorStore()
docs_folder = os.path.join(settings.BASE_DIR, 'documents')

vector_store.load_from_folder(docs_folder)



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
        stats = vector_store.get_stats()
        return Response(stats, status=status.HTTP_200_OK)


class AIProviderStatusView(APIView):
    """Get status information about available AI providers."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        status_info = ai_client.get_provider_status()
        return Response(status_info, status=status.HTTP_200_OK)