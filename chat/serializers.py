from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import ChatMessage

class ChatMessageSerializer(ModelSerializer):
    user = StringRelatedField(read_only=True)
    class Meta:
        model = ChatMessage
        fields = ["user", "message", "response", "created_at"]
