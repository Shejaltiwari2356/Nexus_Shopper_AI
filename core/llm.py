import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from core.settings import MODEL_NAME, TEMPERATURE

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=TEMPERATURE,
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)
