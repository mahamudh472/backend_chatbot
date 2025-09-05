import openai
from django.conf import settings

class OpenAIClient:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def embed_text(self, text: str):
        """Generate embeddings using OpenAI's latest embedding model."""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def chat_with_context(self, prompt: str, context: str):
        """Generate chat response using OpenAI's latest chat model."""
        full_prompt = f"""
        You are a helpful assistant that represents our company. 
        Always answer as if you are the company itself, not an AI model. 
        Do not say things like "based on the provided text" or mention context. 
        If the answer is not directly in the context, respond politely but 
        stay in character as the company.

        Context:
        {context}

        User: {prompt}
        Company Assistant:
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Latest and most cost-effective model
            messages=[
                {"role": "system", "content": "You are a helpful company assistant."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
