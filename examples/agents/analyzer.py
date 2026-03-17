import os
import spacy
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from endee import Endee
from dotenv import load_dotenv

load_dotenv()

nlp = spacy.load("en_core_web_sm")

def analyzer_agent(state: dict) -> dict:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    # Initialize Endee for semantic search
    endee_client = Endee()

    prompt = ChatPromptTemplate.from_template("""
Summarize this content in 2-3 sentences to answer: {sub_question}

Content: {content}

Be concise and factual.
""")
    chain = prompt | llm

    analyzed = []
    
    for result in state["search_results"]:
        # Search Endee for semantically similar documents
        sub_question = result["sub_question"]
        try:
            endee_results = endee_client.search(
                query=sub_question,
                top_k=3
            )
            # Use Endee-retrieved context if available
            retrieved_context = " ".join([doc.get("text", "") for doc in endee_results])
            content_to_analyze = retrieved_context if retrieved_context else result["content"]
        except Exception as e:
            print(f"Endee search error: {e}")
            content_to_analyze = result["content"]

        # NLP: Named Entity Recognition with spaCy
        doc = nlp(content_to_analyze[:1000])
        entities = list(set([(ent.text, ent.label_) for ent in doc.ents]))[:8]

        # Summarize with LLM
        try:
            summary = chain.invoke({
                "sub_question": sub_question,
                "content": content_to_analyze[:2000]
            })
            summary_text = summary.content
        except:
            summary_text = content_to_analyze[:300]

        analyzed.append({
            "sub_question": result["sub_question"],
            "title": result["title"],
            "url": result["url"],
            "summary": summary_text,
            "entities": entities,
            "endee_enhanced": True  # Flag showing Endee was used
        })

    print(f"✅ Analyzer Done: {len(analyzed)} sources analyzed with Endee retrieval")
    return {"analysis": analyzed, "status": "analyzed"}