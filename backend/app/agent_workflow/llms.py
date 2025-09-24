from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv

load_dotenv()

chatgpt_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
google_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=gemini_api_key
)
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")

