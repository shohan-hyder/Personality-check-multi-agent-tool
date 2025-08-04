from langchain_groq import ChatGroq
from services.config import Config

def get_llm():
    return ChatGroq(
        model=Config.MODEL_NAME,
        temperature=Config.TEMPERATURE,
        api_key=Config.GROQ_API_KEY
    )