# Serper tool definition.

import os
from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
load_dotenv()

def get_university_urls(query:str):
    """
    Finds the most relevant university/program URLs using Serper tool.
    """
    # Initialise the wrapper. 
    search=GoogleSerperAPIWrapper()

    # We use .results() to get structured dictionary.
    results=search.results(query)

    urls=[item['link'] for item in results.get('organic',[])[:3]]
    return urls

# # --- Testing snippet ---
# if __name__ == "__main__":
#     # Test with a specific query
#     test_query = "NYU MS in Computer Science admission requirements official"
#     links = get_university_urls(test_query)
#     print(f"Search Results for: {test_query}")
#     for i, link in enumerate(links, 1):
#         print(f"{i}. {link}")