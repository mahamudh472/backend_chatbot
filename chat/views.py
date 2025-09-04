from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from django.conf import settings
from .vectorstore import VectorStore
import os
from .gemini_client import chat_with_context

vector_store = VectorStore()
docs_folder = os.path.join(settings.BASE_DIR, 'documents')

vector_store.load_from_folder(docs_folder)

# Correct OpenRouter base URL
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY,
)

def ask_ai(prompt: str, model: str = "mistralai/mistral-7b-instruct") -> str:
    """
    Send a prompt to OpenRouter and get the response.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content




class MessageListView(ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ChatMessage.objects.filter(user=self.request.user)


class ChatMessageCreateView(APIView):
    def post(self, request, *args, **kwargs):
        message = request.data.get('message')
        if not message:
            return Response({"error": "Message content is required"}, status=status.HTTP_400_BAD_REQUEST)
        docs = vector_store.search(message, top_k=2)
        context = "\n".join([doc['text'] for doc in docs])
        response = chat_with_context(message, context)

        print("User Message:", message)
        print("Context Retrieved:", context)
        print("AI Response:", response)
        # data ={
        #     'message': message,
        #     'response': "This is a static response.",
        #     'user': request.user.id
        # }
        # serializer = ChatMessageSerializer(data=data)
        # response = ask_ai(message)
        # print("AI Response:", response)
        # if serializer.is_valid():
        #     serializer.save(user=request.user)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"response": response}, status=status.HTTP_200_OK)