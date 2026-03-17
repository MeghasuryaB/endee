import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def reporter_agent(state: dict) -> dict:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        api_key=os.getenv("GROQ_API_KEY")
    )

    context = ""
    sources = []
    seen_urls = set()
    all_entities = []

    for item in state["analysis"]:
        context += f"\nSub-topic: {item['sub_question']}\nSummary: {item['summary']}\n"
        all_entities.extend([e[0] for e in item["entities"]])
        if item["url"] not in seen_urls:
            sources.append(f"- [{item['title']}]({item['url']})")
            seen_urls.add(item["url"])

    unique_entities = list(set(all_entities))[:15]

    prompt = ChatPromptTemplate.from_template("""
Write a professional research report on: {question}

Research Summaries:
{context}

Use this exact markdown format:
## Executive Summary
## Key Findings
## Detailed Analysis
## Conclusion

Be detailed, insightful, and professional.
""")

    chain = prompt | llm
    report_response = chain.invoke({
        "question": state["question"],
        "context": context
    })

    entities_section = f"\n\n## Key Entities & Concepts\n{', '.join(unique_entities)}"
    sources_section = f"\n\n## Sources\n" + "\n".join(sources)
    final_report = report_response.content + entities_section + sources_section

    print(f"✅ Reporter Done: Report generated")
    return {"report": final_report, "status": "complete"}