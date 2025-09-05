from django.core.management.base import BaseCommand
from chat.ai_client import ai_client

class Command(BaseCommand):
    help = 'Display AI provider status and configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== AI Provider Status ==='))
        
        status = ai_client.get_provider_status()
        
        self.stdout.write(f"Active Provider: {self.style.WARNING(status['active_provider'])}")
        self.stdout.write(f"Google Available: {'✅' if status['google_available'] else '❌'}")
        self.stdout.write(f"OpenAI Available: {'✅' if status['openai_available'] else '❌'}")
        self.stdout.write(f"Google API Key Set: {'✅' if status['google_api_key_set'] else '❌'}")
        self.stdout.write(f"OpenAI API Key Set: {'✅' if status['openai_api_key_set'] else '❌'}")
        
        # Test connectivity
        self.stdout.write(self.style.SUCCESS('\n=== Testing Connectivity ==='))
        try:
            test_response = ai_client.chat_with_context("Hello", "Test context")
            self.stdout.write(f"✅ Chat test successful with {ai_client.get_active_provider()}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Chat test failed: {e}"))
        
        try:
            embedding = ai_client.embed_text("Test text")
            self.stdout.write(f"✅ Embedding test successful (dimension: {len(embedding)})")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Embedding test failed: {e}"))
