from django.apps import AppConfig
import sys


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    def ready(self):
        import chat.signals  # Ensure signals are imported to connect them
        
        # Initialize vector store only for runserver command
        if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
            from chat.views import initialize_vector_store
            initialize_vector_store()