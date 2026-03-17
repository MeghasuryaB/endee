import os, ast
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def planner_agent(state: dict) -> dict:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = ChatPromptTemplate.from_template("""
You are a research planner. Break this question into exactly 3 focused sub-questions.

Research Question: {question}

Return ONLY a Python list of 3 strings. Example:
["sub-question 1", "sub-question 2", "sub-question 3"]
""")

    chain = prompt | llm
    result = chain.invoke({"question": state["question"]})

    try:
        sub_questions = ast.literal_eval(result.content.strip())
    except:
        sub_questions = [state["question"]]

    print(f"✅ Planner Done: {len(sub_questions)} sub-questions")
    return {"sub_questions": sub_questions, "status": "planned"}