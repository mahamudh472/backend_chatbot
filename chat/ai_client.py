from django.conf import settings
from .gemini_client import embed_text as gemini_embed, chat_with_context as gemini_chat
from .openai_client import OpenAIClient
import logging

logger = logging.getLogger(__name__)

class AIClient:
    """
    Unified AI client that prioritizes Google (Gemini) over OpenAI.
    Priority: Google > OpenAI
    """
    
    def __init__(self):
        self.google_available = bool(settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY.strip())
        self.openai_available = bool(settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip())
        
        self.openai_client = None
        if self.openai_available:
            try:
                self.openai_client = OpenAIClient()
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                self.openai_available = False
        
        if not self.google_available and not self.openai_available:
            raise ValueError("No AI API keys configured. Please set GOOGLE_API_KEY or OPENAI_API_KEY.")
    
    def get_active_provider(self):
        """Returns the name of the currently active AI provider."""
        if self.google_available:
            return "Google Gemini"
        elif self.openai_available:
            return "OpenAI"
        else:
            return "None"
    
    def embed_text(self, text: str):
        """
        Generate text embeddings using the available provider.
        Priority: Google > OpenAI
        """
        if self.google_available:
            try:
                return gemini_embed(text)
            except Exception as e:
                logger.error(f"Google embedding failed: {e}")
                if self.openai_available:
                    logger.info("Falling back to OpenAI for embeddings")
                    try:
                        return self.openai_client.embed_text(text)
                    except Exception as e2:
                        logger.error(f"OpenAI embedding fallback failed: {e2}")
                        raise e2
                else:
                    raise e
        
        elif self.openai_available:
            try:
                return self.openai_client.embed_text(text)
            except Exception as e:
                logger.error(f"OpenAI embedding failed: {e}")
                raise e
        
        else:
            raise ValueError("No AI provider available for embeddings")
    
    def chat_with_context(self, prompt: str, context: str):
        """
        Generate chat response using the available provider.
        Priority: Google > OpenAI
        """
        if self.google_available:
            try:
                response = gemini_chat(prompt, context)
                logger.info(f"Response generated using Google Gemini")
                return response
            except Exception as e:
                logger.error(f"Google chat failed: {e}")
                if self.openai_available:
                    logger.info("Falling back to OpenAI for chat")
                    try:
                        response = self.openai_client.chat_with_context(prompt, context)
                        logger.info(f"Response generated using OpenAI (fallback)")
                        return response
                    except Exception as e2:
                        logger.error(f"OpenAI chat fallback failed: {e2}")
                        raise e2
                else:
                    raise e
        
        elif self.openai_available:
            try:
                response = self.openai_client.chat_with_context(prompt, context)
                logger.info(f"Response generated using OpenAI")
                return response
            except Exception as e:
                logger.error(f"OpenAI chat failed: {e}")
                raise e
        
        else:
            raise ValueError("No AI provider available for chat")
    
    def get_provider_status(self):
        """Returns status information about available providers."""
        return {
            "google_available": self.google_available,
            "openai_available": self.openai_available,
            "active_provider": self.get_active_provider(),
            "google_api_key_set": bool(settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY.strip()),
            "openai_api_key_set": bool(settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip())
        }

# Global instance
ai_client = AIClient()
