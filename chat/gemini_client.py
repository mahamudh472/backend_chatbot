import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GOOGLE_API_KEY)

chat_model = genai.GenerativeModel("gemini-1.5-flash")
embed_model = genai.GenerativeModel("embedding-001")

def embed_text(text: str):
    result = genai.embed_content(
        model="models/embedding-001",
        content=text
    )
    return result["embedding"]

def chat_with_context(prompt: str, context: str):
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

    response = chat_model.generate_content(full_prompt)
    return response.text
