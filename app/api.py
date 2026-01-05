import sys
import asyncio
if sys.platform=='win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI, HTTPException
from app.utils import agent_app
import uvicorn
from app.schemas import ChatRequest, ResearchRequest
from agents.graph import agent_app2

app = FastAPI(title="CollegeInfoBot API")

@app.post("/run-agent")
async def run_agent(request: ChatRequest):
    # Mapping the UI message to the Agent's expected 'user_input' key
    initial_state = {
        "user_input": request.message,
        "university": None,
        "program": None,
        "status": "started"
    }
    
    try: 
        print(f"DEBUG: API received: {request.message}")
        
        # FIX: Use .ainvoke() instead of .invoke()
        final_state = await agent_app.ainvoke(initial_state)
        
        print(f"DEBUG: Agent extracted: {final_state.get('university')}")
        return final_state
        
    except Exception as e:
        # This will print the error to your terminal so you can see it
        print(f"ERROR: {str(e)}") 
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/start-research")
async def start_research(request: ResearchRequest):
    """
    Triggers the Agentic Hierarchy (manager->scraper->strategist)
    to generate the professional applicant guide. 
    """
    initial_state={
        "university": request.university,
        "program": request.program,
        "level": request.level,
        "user_input": request.background, # Their profile info
        "status": "research_starting",
        "university_data": "" # To be filled by scrapper.
    }
    try:
        print(f"Research Started!")
        final_state = await agent_app2.ainvoke(initial_state)
        return {"status":"success","report":final_state.get("user_input")}
    except Exception as e: 
        print(f"AGENT ERROR:{str(e)}")
        raise HTTPException(status_code=500,detail=f"Agent Failed {str(e)}")


if __name__ == "__main__":
    uvicorn.run("app.api:app", host="127.0.0.1", port=8001, reload=False)