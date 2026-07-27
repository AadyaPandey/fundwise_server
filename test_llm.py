from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)

try:
    response = llm.invoke("Say hello in one sentence.")
    print("\nSUCCESS!")
    print(response.content)
except Exception as e:
    print("\nERROR:")
    print(e)