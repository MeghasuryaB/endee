import os
from endee import Endee
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

def searcher_agent(state: dict) -> dict:
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    
    # Initialize Endee for vector storage
    endee_client = Endee()

    all_results = []
    documents_to_store = []
    
    for sub_q in state["sub_questions"]:
        try:
            response = client.search(sub_q, max_results=3)
            for r in response["results"]:
                result_dict = {
                    "sub_question": sub_q,
                    "title": r.get("title", ""),
                    "content": r.get("content", ""),
                    "url": r.get("url", "")
                }
                all_results.append(result_dict)
                
                # Prepare document for Endee storage
                documents_to_store.append({
                    "text": r.get("content", ""),
                    "metadata": {
                        "sub_question": sub_q,
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "source": "tavily"
                    }
                })
        except Exception as e:
            print(f"Search error: {e}")

    # Store all search results in Endee vector database
    try:
        for doc in documents_to_store:
            endee_client.add_document(
                text=doc["text"],
                metadata=doc["metadata"]
            )
        print(f"✅ Stored {len(documents_to_store)} documents in Endee")
    except Exception as e:
        print(f"Endee storage error: {e}")

    print(f"✅ Searcher Done: {len(all_results)} results collected and stored")
    return {"search_results": all_results, "status": "searched"}