# AutoResearch Agent - Built on Endee

An AI-powered research system using **Endee vector database** to store and retrieve research findings.

## Architecture

- **Planner**: Breaks down complex queries into sub-questions
- **Searcher**: Gathers info from Tavily → **stores vectors in Endee**
- **Analyzer**: **Searches Endee** for relevant context → synthesizes answers
- **Reporter**: Generates final research report

## Endee Integration

- Stores all research documents as embeddings
- Enables semantic retrieval between agents
- Acts as the shared knowledge base

## Quick Start

```bash
cd examples/auto-research-agent
pip install -r requirements.txt
streamlit run ui/app.py
```

## Tech Stack

- **Endee** (Vector Database)
- Groq + Llama 3
- LangGraph (Agentic Workflow)
- Tavily (Web Search)
- Streamlit (UI)
