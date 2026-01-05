# Python function for each node (manager, scraper, etc.)
# Each func takes state: AgentState as an argument and returns a dictionary to update that state.
# Define your model here. 

import os
from langchain_groq import ChatGroq
from app.schemas import AgentState
from agents.prompts import MANAGER_PROMPT,SCRAPER_PROMPT,STRATEGIST_PROMPT
from tools.custom_scraper import  UniversityScraper
from tools.search_tool import get_university_urls

llm=ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1,
    groq_api_key=os.getenv("GROQ_API_KEY")
)
scraper_tool=UniversityScraper()

# Node functions.
async def manager_node(state:AgentState):
    """
    Decides the next steps in research process.
    """
    prompt=MANAGER_PROMPT.format(
        university=state.get("university"),
        program=state.get("program"),
        background=state.get("background"),
        level=state.get("level"),
        status=state.get("status")
    )
    # If no data exists go to search.
    if not state.get("university_data"):
        return {"status":"needs_search"}
    return {"status":"ready_for_strategy"}

async def search_node(state:AgentState):
    """Uses serper tool ot search for URLs."""
    query=f"{state['university']} {state['program']} admissions requirements."
    urls=get_university_urls(query)
    return {"status":"url_found","background":urls[0] if urls else ""}

async def scraper_node(state:AgentState):
    """Uses crawl4ai to read the page."""
    url=state.get("background")
    content=await scraper_tool.scrape_university(url)
    return {"university_data":content,"status":"scraped"}

async def strategist_node(state:AgentState):
    """Analyzes data using Llama-3.1-70B"""
    response=llm.invoke(STRATEGIST_PROMPT.format(
        background=state.get("user_input"),
        level=state.get("level"),
        university_data=state.get("university_data")
    ))
    return {"status":"completed","user_input":response.content}
