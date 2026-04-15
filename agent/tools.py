from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

def get_search_tool():
    return TavilySearchResults(
        max_results=3,
        name="tavily_search",
        description="Search the internet for study resources, syllabus, and exam information."
    )