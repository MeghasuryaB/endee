import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.workflow import build_workflow
from fpdf import FPDF

st.set_page_config(page_title="AutoResearch Agent", page_icon="🔬", layout="wide")

st.title("🔬 AutoResearch Agent")
st.caption("Multi-Agent AI System • LangGraph + Groq + Tavily + spaCy")
st.divider()

query = st.text_input("Enter your research question:",
    placeholder="e.g. What is the future of quantum computing in 2025?")

start = st.button("🚀 Start Research", type="primary")

def render_status(done=[], running=None, extra=""):
    agents = [("📋", "Planner Agent"), ("🔍", "Searcher Agent"),
              ("🧠", "Analyzer Agent"), ("✍️", "Report Writer")]
    md = ""
    for icon, name in agents:
        if name in done:
            md += f"✅ **{icon} {name}** — Done\n\n"
        elif name == running:
            md += f"⏳ **{icon} {name}** — Running...\n\n"
        else:
            md += f"⬜ {icon} {name}\n\n"
    return md + extra

def generate_pdf(text, question):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Research Report", ln=True, align="C")
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 8, f"Topic: {question[:80]}", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    clean = text.replace("**","").replace("##","").replace("#","").replace("*","")
    for line in clean.split("\n"):
        try:
            pdf.multi_cell(0, 6, txt=line.encode('latin-1','replace').decode('latin-1'))
        except:
            pass
    return bytes(pdf.output())

if start and query.strip():
    st.divider()
    left, right = st.columns([1, 2])

    with left:
        st.subheader("🤖 Agent Pipeline")
        status_box = st.empty()

    with right:
        st.subheader("📄 Live Report")
        report_box = st.empty()

    status_box.markdown(render_status(running="Planner Agent"))

    try:
        workflow = build_workflow()
        initial_state = {
            "question": query, "sub_questions": [],
            "search_results": [], "analysis": [],
            "report": "", "status": "starting"
        }

        done_agents = []

        for step in workflow.stream(initial_state):
            node = list(step.keys())[0]
            data = step[node]

            if node == "planner":
                subs = data.get("sub_questions", [])
                done_agents.append("Planner Agent")
                extra = "\n**Sub-questions:**\n" + "\n".join([f"• {q}" for q in subs])
                status_box.markdown(render_status(done_agents, "Searcher Agent", extra))

            elif node == "searcher":
                n = len(data.get("search_results", []))
                done_agents.append("Searcher Agent")
                status_box.markdown(render_status(done_agents, "Analyzer Agent",
                    f"\n📊 **{n} sources** retrieved"))

            elif node == "analyzer":
                done_agents.append("Analyzer Agent")
                status_box.markdown(render_status(done_agents, "Report Writer"))

            elif node == "reporter":
                done_agents.append("Report Writer")
                report = data.get("report", "")
                status_box.markdown(render_status(done_agents, extra="\n\n🎉 **Research Complete!**"))
                report_box.markdown(report)

                st.divider()
                st.download_button(
                    "📥 Download as PDF",
                    data=generate_pdf(report, query),
                    file_name="research_report.pdf",
                    mime="application/pdf"
                )

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Check your API keys in the .env file")

elif start:
    st.warning("Please enter a research question!")