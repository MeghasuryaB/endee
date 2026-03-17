import os
import spacy
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

nlp = spacy.load("en_core_web_sm")

def analyzer_agent(state: dict) -> dict:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = ChatPromptTemplate.from_template("""
Summarize this content in 2-3 sentences to answer: {sub_question}

Content: {content}

Be concise and factual.
""")
    chain = prompt | llm

    analyzed = []
    for result in state["search_results"]:
        # NLP: Named Entity Recognition with spaCy
        doc = nlp(result["content"][:1000])
        entities = list(set([(ent.text, ent.label_) for ent in doc.ents]))[:8]

        # Summarize with LLM
        try:
            summary = chain.invoke({
                "sub_question": result["sub_question"],
                "content": result["content"][:2000]
            })
            summary_text = summary.content
        except:
            summary_text = result["content"][:300]

        analyzed.append({
            "sub_question": result["sub_question"],
            "title": result["title"],
            "url": result["url"],
            "summary": summary_text,
            "entities": entities
        })

    print(f"✅ Analyzer Done: {len(analyzed)} sources analyzed")
    return {"analysis": analyzed, "status": "analyzed"}