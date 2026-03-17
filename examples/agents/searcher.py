import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

def searcher_agent(state: dict) -> dict:
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    all_results = []
    for sub_q in state["sub_questions"]:
        try:
            response = client.search(sub_q, max_results=3)
            for r in response["results"]:
                all_results.append({
                    "sub_question": sub_q,
                    "title": r.get("title", ""),
                    "content": r.get("content", ""),
                    "url": r.get("url", "")
                })
        except Exception as e:
            print(f"Search error: {e}")

    print(f"✅ Searcher Done: {len(all_results)} results")
    return {"search_results": all_results, "status": "searched"}