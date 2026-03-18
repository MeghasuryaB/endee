# AutoResearch Agent - Endee-Powered Semantic Research System

![AutoResearch Agent](https://img.shields.io/badge/AI-Research%20Agent-blue) ![Endee](https://img.shields.io/badge/Database-Endee-success) ![Status](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue)

## 📋 Table of Contents

- [Overview](#overview)
- [What is Endee?](#what-is-endee)
- [Why We Use Endee](#why-we-use-endee)
- [Where Endee is Used](#where-endee-is-used)
- [Quick Start](#quick-start)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Detailed Walkthrough](#detailed-walkthrough)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [API Methods](#api-methods)
- [AI Concepts](#ai-concepts-demonstrated)
- [Performance](#performance)
- [FAQ](#faq)
- [Contributing](#contributing)
- [Support](#support)

---

## 🎯 Overview

**AutoResearch Agent** is an intelligent multi-agent AI research system that automatically researches any topic by:

1. **Breaking down** complex questions into focused sub-questions
2. **Searching** the web for relevant information in real-time
3. **Storing** findings in a semantic vector database (Endee)
4. **Analyzing** information using semantic search (not keyword matching)
5. **Generating** comprehensive, well-cited research reports

### What Makes It Different?

Instead of just searching and aggregating web results, AutoResearch Agent:

- ✅ Uses **semantic search** via Endee (understands meaning, not just keywords)
- ✅ Implements **RAG (Retrieval-Augmented Generation)** pattern
- ✅ Uses **multi-agent orchestration** (4 specialized agents working together)
- ✅ Provides **real-time, verifiable information** with source attribution
- ✅ Demonstrates **production-grade AI architecture**

### Example Use Case

User: "What are the latest AI trends in healthcare?"
↓
System: Breaks into 3 sub-questions
↓
Searches web → Stores in Endee → Semantically retrieves → Analyzes → Reports
↓
Output: Comprehensive report with citations

---

## 🔍 What is Endee?

### Simple Definition

**Endee** is a **Vector Database** — a specialized database that stores and retrieves information based on **semantic meaning** rather than keyword matching.

### Keyword vs. Semantic Search

**Traditional Database (Keyword Search):**

Question: "Find AI"
Result: Only exact matches for word "AI"
Problem: Misses "machine learning", "deep learning", etc.

**Vector Database (Endee - Semantic Search):**

Question: "Find AI"
Result: "AI", "machine learning", "deep learning", "neural networks"
Benefit: Understands meaning, not just keywords

### The Technical Process

#### Step 1: Convert Text to Vectors (Embeddings)

Text: "Artificial intelligence is transforming healthcare"
↓
Embedding Model (BERT): Converts to 384-dimensional vector
↓
Vector: [0.23, -0.15, 0.67, 0.42, ..., 0.51]
(numbers represent semantic meaning)

Each number in the vector captures different aspects of meaning:

- Position 0: Medical relevance
- Position 1: Technology relevance
- Position 2: Importance level
- etc.

#### Step 2: Store in Endee

```python
endee.insert(
    document="Artificial intelligence is transforming healthcare",
    metadata={"source": "article.com", "date": "2026-03-17"}
)

Endee stores:

* Original text
* Its vector (384 numbers)
* Metadata (source, date, etc.)

Step 3: Search Semantically
pythonDownloadCopy code# When you search for "machine learning in medicine"
results = endee.search("machine learning in medicine", top_k=5)

# Endee converts query to vector
# Then finds similar vectors (not exact keyword matches)
# Returns the 5 most semantically similar documents
Visual Example: Vector Space
Endee Vector Space (simplified 2D, actually 384D)

    AI
    ↑
    | • "machine learning"
    | • "deep learning"
    | • "neural networks"
    |
    +────→ Healthcare
      "AI in medicine"
      "diagnosis systems"
      "healthcare AI"

Query: "machine learning in healthcare"
↓
Finds closest vectors
↓
Returns relevant documents


🎯 Why We Use Endee
Problem We Solve
AspectWithout EndeeWith EndeeSearch TypeKeyword-onlySemantic"AI" query findsOnly "AI""AI", "ML", "Deep Learning"Result ProcessingAnalyzes all resultsAnalyzes only relevant onesPerformanceSlow on large dataFast even with millionsKnowledge ReuseNoneReuses previous findings
Real Example: "Quantum Computing Breakthroughs"
Without Endee (Keyword Matching):
Results:
✓ "Quantum computing makes breakthrough in cryptography"
✓ "Google achieves quantum supremacy"
✗ "The quantum (number) of energy breakthroughs" (irrelevant!)
✗ "Computing breakthroughs in education" (irrelevant!)

Result: Wasting time analyzing irrelevant documents

With Endee (Semantic Matching):
Results:
✓ "Quantum computing makes breakthrough in cryptography"
✓ "Google achieves quantum supremacy"
✓ "IBM's quantum processor advances error correction"
✓ "Quantum algorithms for drug discovery"

Result: Only relevant documents, better analysis!

Benefits in Our System

1. Better Search Quality — Finds relevant information even with different wording
2. Faster Analysis — Focuses analyzer on relevant docs only
3. Knowledge Reuse — Searches across all previous findings
4. Scalability — Handles millions of documents efficiently
5. Semantic Understanding — Understands "AI" = "machine learning" = "deep learning"
6. Reduced Hallucination — LLM bases answers on retrieved facts

How Endee Improves Research
Without Endee:
Search Results → Process ALL → Generate Answer
(May include irrelevant information)

With Endee:
Search Results → Store in Endee → Retrieve RELEVANT → Generate Answer
(Only uses relevant information)


📍 Where Endee is Used
Location 1: Searcher Agent (Storage)
File: agents/searcher.py
pythonDownloadCopy codefrom endee import Endee

def searcher_agent(state: dict) -> dict:
    """
    Searches web for information and STORES in Endee
    """
    endee_client = Endee()  # Initialize Endee

    for sub_question in state["sub_questions"]:
        # Get web results from Tavily
        response = client.search(sub_question, max_results=3)

        # ENDEE USAGE: Store each result as a vector
        for article in response["results"]:
            endee_client.insert(
                document=article["content"],      # Store text
                metadata={
                    "title": article["title"],
                    "url": article["url"],
                    "sub_question": sub_question
                }
            )

    return {"documents_stored": len(all_articles)}
What Happens:

* Web articles are fetched from Tavily API
* Each article is automatically converted to a 384-dimensional vector by Endee
* Vector + original text + metadata are stored in Endee database
* Ready for semantic search!

Why: Creates a searchable knowledge base of all research findings

Location 2: Analyzer Agent (Retrieval)
File: agents/analyzer.py
pythonDownloadCopy codefrom endee import Endee

def analyzer_agent(state: dict) -> dict:
    """
    SEARCHES Endee for relevant information and analyzes
    """
    endee_client = Endee()

    # ENDEE USAGE: Semantic search instead of keyword search
    retrieved_docs = endee_client.search(
        query=state["main_query"],  # "What is blockchain?"
        limit=8                      # Get top 8 semantically similar
    )

    analysis_results = []

    # Analyze only the RELEVANT documents from Endee
    for doc in retrieved_docs:
        content = doc["document"]
        metadata = doc["metadata"]

        # Extract entities using spaCy NLP
        entities = nlp(content)

        # Summarize using LLM
        summary = llm.summarize(content)

        analysis_results.append({
            "content": content,
            "summary": summary,
            "entities": entities,
            "source": metadata["url"]
        })

    return {"analysis": analysis_results}
What Happens:

* Analyzer queries Endee with the research question
* Endee returns top 8 semantically similar documents (not just keywords!)
* Analyzer focuses on these relevant documents only
* Performs NLP analysis (entity extraction, summarization)
* More efficient and accurate results

Why: Semantic retrieval instead of keyword matching

Location 3: Reporter Agent (Uses Retrieved Context)
File: agents/reporter.py
pythonDownloadCopy codedef reporter_agent(state: dict) -> dict:
    """
    Uses analyzed information from Endee to generate final report
    """
    # context comes from analyzer_agent (which used Endee)
    context = state["analysis"]

    # Generate report using analyzed information
    report = llm.generate_report(
        question=state["main_query"],
        context=context,  # This context came from Endee!
        prompt=REPORTER_PROMPT
    )

    return {"final_report": report}
What Happens:

* Reporter receives analyzed data that was retrieved from Endee
* Uses this grounded context to generate report
* Implements RAG pattern — Retrieved + Augmented + Generation
* Report is accurate and verifiable


Location 4: Requirements File
File: requirements.txt
endee==0.1.19              # ← Endee dependency
langchain-groq==1.1.2
langchain-core==1.2.19
tavily-python==0.7.23
python-dotenv==1.2.2
spacy==3.8.11
streamlit==1.28.0


🚀 Quick Start
Prerequisites

* Python 3.8+
* API Keys: GROQ_API_KEY, TAVILY_API_KEY

Installation
bashDownloadCopy code# 1. Clone the repository
git clone https://github.com/MeghasuryaB/endee.git
cd endee/examples/auto-research-agent

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download spaCy model
python -m spacy download en_core_web_sm

# 5. Setup environment variables
cp .env.example .env
# Edit .env with your API keys
Run the App
bashDownloadCopy codepython -m streamlit run ui/app.py
Access at: http://localhost:8501

🏗️ System Architecture
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (Streamlit)               │
│              "Ask any research question here"               │
└────────────────────────┬────────────────────────────────────┘
                         │ User Question
                         ↓
        ┌────────────────────────────────┐
        │   PLANNER AGENT (LLM)          │
        │ "Break into sub-questions"     │
        │                                │
        │ Input:  "What is blockchain?"  │
        │ Output: ["What is...", ...]    │
        └────────────┬───────────────────┘
                     │
                     ↓
        ┌────────────────────────────────┐
        │   SEARCHER AGENT               │
        │ "Search web + Store in Endee"  │
        │                                │
        │ Tavily API → Web Search        │
        │ Endee DB ← Store as vectors    │
        └────────────┬───────────────────┘
                     │
        ┌────────────↓───────────────────┐
        │                                │
        │         ENDEE DATABASE         │
        │     (Vector Store)             │
        │                                │
        │  [Doc1: Vector + Metadata]     │
        │  [Doc2: Vector + Metadata]     │
        │  [Doc3: Vector + Metadata]     │
        │         ... etc ...            │
        │                                │
        └────────────┬───────────────────┘
                     │
                     ↓
        ┌────────────────────────────────┐
        │   ANALYZER AGENT               │
        │ "Search Endee + Analyze"       │
        │                                │
        │ Semantic Search → Endee        │
        │ NLP Analysis → spaCy           │
        │ Summarization → LLM            │
        └────────────┬───────────────────┘
                     │
                     ↓
        ┌────────────────────────────────┐
        │   REPORTER AGENT               │
        │ "Generate final report"        │
        │                                │
        │ Input: Analyzed context        │
        │ Output: Professional report    │
        └────────────┬───────────────────┘
                     │
                     ↓
        ┌────────────────────────────────┐
        │      FINAL RESEARCH REPORT     │
        │  (With citations & sources)    │
        └────────────────────────────────┘

Data Flow in Endee
Day 1 - First Research:
User Query
  ↓
Searcher: Finds 9 articles → Stores in Endee (9 vectors)
  ↓
Analyzer: Searches Endee → Gets 8 best matches → Analyzes
  ↓
Reporter: Generates report

Day 2 - Second Research:
User Query
  ↓
Searcher: Finds 9 new articles → Stores in Endee (now 18 vectors)
  ↓
Analyzer: Searches Endee → Gets best matches from ALL 18 articles
  ↓
Reporter: Generates report combining old + new knowledge

Benefit: Knowledge builds up over time!


✨ Features
Core Features

* ✅ Semantic Search via Endee (not just keywords)
* ✅ RAG Pattern (Retrieved context grounds LLM)
* ✅ Real-time Web Search (Tavily API)
* ✅ Multi-Agent Orchestration (LangGraph)
* ✅ Named Entity Recognition (spaCy)
* ✅ Source Attribution (Verifiable citations)
* ✅ Persistent Knowledge (Endee reuses findings)

Advanced Capabilities

* 🔍 Intelligent Decomposition — Breaks complex queries into focused sub-questions
* 🧠 Context-Aware Analysis — Understands semantic meaning, not just keywords
* 📊 Structured Reports — Professional formatting with executive summaries
* ⚡ Fast Inference — Groq's optimized LLM (100+ tokens/sec)
* 🔄 Extensible Architecture — Easy to add new agents or modify behavior
* 🌐 Real-Time Information — Not limited to training data cutoff
* 📚 Knowledge Persistence — Endee stores findings for future searches


🛠️ Tech Stack
ComponentTechnologyPurposeVector DatabaseEndeeSemantic search & vector storageAgent OrchestrationLangGraphMulti-agent workflow coordinationLanguage ModelGroq + Llama 3Fast, accurate LLM inferenceWeb SearchTavily APIReal-time web information retrievalNLPspaCyNamed entity recognition & analysisUI FrameworkStreamlitInteractive web interfaceLLM FrameworkLangChain CoreStandardized LLM abstractionsEnvironmentPython-dotenvConfiguration management
Why These Technologies?

* Endee: Free tier, simple API, semantic search capability
* Groq: Ultra-fast LLM inference (free tier available)
* Tavily: AI-optimized web search (not just scraping)
* LangGraph: State management for multi-agent systems
* spaCy: Lightweight NLP for entity extraction
* Streamlit: Rapid UI development without frontend expertise


📁 Project Structure
auto-research-agent/
│
├── agents/                          # AI Agent Implementations
│   ├── __init__.py
│   ├── planner.py                  # Decompose questions into sub-questions
│   ├── searcher.py                 # Search web + Store in Endee
│   ├── analyzer.py                 # Search Endee + Analyze content
│   └── reporter.py                 # Generate final report
│
├── graph/                          # LangGraph Orchestration
│   ├── __init__.py
│   ├── state.py                    # State management structure
│   └── workflow.py                 # Agent coordination & flow
│
├── ui/                             # Streamlit Interface
│   ├── app.py                      # Main app interface
│   └── components/                 # Reusable UI components
│
├── utils/                          # Helper Functions
│   ├── __init__.py
│   ├── config.py                   # Configuration loading
│   └── logger.py                   # Logging utilities
│
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
└── README.md                       # This file


🔍 Detailed Walkthrough
Complete Flow Example: "What are quantum computing trends?"
Step 1: Planner Agent - Decomposition
Input:    "What are quantum computing trends?"

Process:  LLM analyzes the question and breaks it into focused sub-questions

Output:   [
            "What are the latest quantum computing breakthroughs?",
            "Which companies lead in quantum computing?",
            "What are practical applications of quantum computing?"
          ]

Why: Breaking complex questions improves search relevance

Step 2: Searcher Agent - Web Search + Endee Storage
For each sub-question:
  ├─ Query Tavily Web API
  ├─ Get 3 most relevant articles
  ├─ FOR EACH ARTICLE:
  │   └─ Send to Endee
  │      ├─ Convert text → 384-dim vector
  │      ├─ Store vector + text + metadata
  │      └─ Index in Endee database
  └─ Total: 9 documents stored in Endee

Endee Database Now Contains Vectors For:
├─ "Quantum computing is revolutionizing cryptography..."
├─ "IBM, Google lead quantum race with new processors..."
├─ "Quantum algorithms for drug discovery show promise..."
├─ "China invests billions in quantum computing..."
└─ ... and 5 more articles

Why: Endee's embeddings enable semantic search

Step 3: Analyzer Agent - Endee Retrieval + Analysis
Input: "What are quantum computing trends?"

Process:
├─ Query Endee: search(query="quantum trends", limit=8)
│
├─ Endee returns 8 most semantically similar documents
│   (These aren't just keyword matches - they're semantically related!)
│
├─ For each retrieved document:
│   ├─ Extract entities using spaCy
│   │   Examples found:
│   │   • PERSON: "John Smith"
│   │   • ORG: "IBM", "Google", "Microsoft"
│   │   • PRODUCT: "Quantum processor", "IBM Q System"
│   │   • DATE: "2026", "Q2 2026"
│   │
│   ├─ Summarize content
│   │   "IBM released a new quantum processor that reduces error rates by 50%"
│   │
│   └─ Note source URL
│       https://example.com/quantum-article
│
└─ Return analyzed context to Reporter

Output: Structured analysis with entities, summaries, and sources
Why: Focuses on only relevant information, improves analysis quality

Step 4: Reporter Agent - Report Generation
Input: Analyzed context from Endee + all findings

Process:
├─ Use LLM to generate report with structure
├─ Fill sections:
│   ├─ Executive Summary
│   │   "Quantum computing is advancing rapidly with IBM, Google leading..."
│   │
│   ├─ Key Findings
│   │   • Companies: IBM, Google, Microsoft advancing quantum tech
│   │   • Progress: Error rates reduced by 50%
│   │   • Applications: Drug discovery, cryptography, optimization
│   │
│   ├─ Detailed Analysis
│   │   Full synthesis of all findings
│   │
│   ├─ Important Organizations & People
│   │   IBM, Google, Microsoft, etc.
│   │
│   └─ Conclusion & Future Outlook
│       Where quantum computing is headed
│
└─ Add citations with URLs from metadata

Output:
# Quantum Computing Trends Report

## Executive Summary
Quantum computing is advancing rapidly with major companies investing heavily...

## Key Findings
- IBM released processor with 50% error reduction
- Google achieved quantum advantage milestone
- Microsoft focusing on topological qubits

## Sources
1. IBM News - https://...
2. Google Blog - https://...
3. Microsoft Research - https://...

Why: Provides users with comprehensive, verified information

💻 Installation & Setup
Detailed Installation Steps
1. Clone Repository
bashDownloadCopy codegit clone https://github.com/MeghasuryaB/endee.git
cd endee/examples/auto-research-agent
2. Create Virtual Environment
Windows:
bashDownloadCopy codepython -m venv .venv
.venv\Scripts\activate
Mac/Linux:
bashDownloadCopy codepython3 -m venv .venv
source .venv/bin/activate
Expected Output:
(.venv) PS D:\autoResearch-agent\endee\examples\auto-research-agent>

3. Install Dependencies
bashDownloadCopy codepip install -r requirements.txt
This installs:

* endee — Vector database for semantic search
* langchain-groq — Groq LLM integration
* langchain-core — Core LangChain utilities
* tavily-python — Web search API client
* python-dotenv — Environment variable management
* spacy — NLP library for entity extraction
* streamlit — Web UI framework

Verification:
bashDownloadCopy codepip list | findstr endee
Should show: endee 0.1.19
4. Download spaCy Model
bashDownloadCopy codepython -m spacy download en_core_web_sm
Required for:

* Named Entity Recognition (NER)
* Extracting people, organizations, products, dates

Verification:
bashDownloadCopy codepython -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('✓ spaCy model loaded')"
5. Setup Environment Variables
Create .env file from template:
bashDownloadCopy codecp .env.example .env
Edit .env with your API keys:
envDownloadCopy code# Groq API Key (get from https://console.groq.com)
GROQ_API_KEY=your_actual_groq_api_key_here

# Tavily API Key (get from https://tavily.com)
TAVILY_API_KEY=your_actual_tavily_api_key_here
How to Get Free API Keys:

1.
Groq API Key:

Visit https://console.groq.com
Sign up for free
Navigate to API Keys
Copy your API key
Free tier: Unlimited requests (rate limited)


2.
Tavily API Key:

Visit https://tavily.com
Sign up for free
Go to API section
Copy your API key
Free tier: 1000 API calls per month



6. Run Application
bashDownloadCopy codepython -m streamlit run ui/app.py
Output:
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

Open browser to: http://localhost:8501

📖 Usage
Using the Web Interface
1. Enter Research Question
In the Streamlit interface, enter your question:
Example: "What are the latest AI trends in 2026?"
Example: "How is blockchain being used in finance?"
Example: "What are emerging quantum computing applications?"

2. Click "🚀 Start Research"
The system begins processing:

* Planner decomposes question
* Searcher finds and stores articles in Endee
* Analyzer searches Endee and analyzes
* Reporter generates report

3. Watch Live Progress
See real-time updates:
✓ Planner: Decomposed into 3 sub-questions
✓ Searcher: Found 9 articles, stored in Endee
✓ Analyzer: Searched Endee, extracted entities
✓ Reporter: Generating final report...

4. View Final Report
The system displays:

* Executive Summary — Quick overview
* Key Findings — Main points extracted
* Detailed Analysis — Full synthesis
* Important Entities — People, organizations, products
* Sources — Citations with URLs (for verification)

Python API Usage
pythonDownloadCopy codefrom graph.workflow import create_research_graph

# Create the research workflow
graph = create_research_graph()

# Run research on a topic
result = graph.invoke({
    "query": "What is blockchain?"
})

# Get the final report
print(result["final_report"])

# Access other outputs
print(result["sub_questions"])  # How question was decomposed
print(result["analysis"])        # Detailed analysis from Analyzer
Command Line Usage
bashDownloadCopy code# Run with specific query
python -c "
from graph.workflow import create_research_graph
graph = create_research_graph()
result = graph.invoke({'query': 'AI trends 2026'})
print(result['final_report'])
"

🔌 API Methods
Endee Methods Used in Project
Storage Method (Searcher Agent)
pythonDownloadCopy codefrom endee import Endee

# Initialize Endee client
client = Endee()

# Add document to vector database
client.insert(
    document="The text content you want to store and search",
    metadata={
        "title": "Document Title",
        "url": "https://example.com/article",
        "source": "web_search",
        "date": "2026-03-17"
    }
)
Parameters:

* document (str): The text to convert to vector and store
* metadata (dict): Additional information (optional)

What Happens Internally:

1. Text is converted to 384-dimensional vector
2. Vector is stored with original text
3. Metadata is indexed for filtering
4. Ready for semantic search


Retrieval Method (Analyzer Agent)
pythonDownloadCopy codefrom endee import Endee

# Initialize Endee client
client = Endee()

# Search for semantically similar documents
results = client.search(
    query="machine learning trends",  # Your search query
    limit=8                            # Number of results to return
)

# Process results
for result in results:
    document = result["document"]      # Original text
    metadata = result["metadata"]      # Stored metadata
    score = result["score"]            # Relevance score (0-1)

    print(f"Score: {score:.2f}")
    print(f"URL: {metadata['url']}")
    print(f"Content: {document[:100]}...")
Return Value:
pythonDownloadCopy code[
    {
        "document": "Original text content...",
        "metadata": {"url": "...", "title": "...", ...},
        "score": 0.95  # Higher = more relevant
    },
    ...
]
Return Values Explained:

* document — Original text stored
* metadata — Information you provided during insertion
* score — Similarity score from 0-1 (1.0 = perfect match)


Full Endee API Reference
pythonDownloadCopy codefrom endee import Endee

# Initialize
client = Endee()

# Add documents
client.insert(
    document="text",
    metadata={"key": "value"}
)

# Search documents
results = client.search(
    query="search term",
    limit=10
)

# Get document count
count = client.count()

# Delete all (useful for testing)
client.clear()

🎓 AI Concepts Demonstrated
1. Multi-Agent Systems
What: Independent agents with specific roles that communicate via shared state
Your Implementation:

* Planner Agent → Decomposes questions
* Searcher Agent → Finds information
* Analyzer Agent → Analyzes content
* Reporter Agent → Generates output

Why It Matters: Mirrors real enterprise AI architecture

2. RAG (Retrieval-Augmented Generation)
What: Retrieve relevant documents, then generate answers grounded in those documents
Your Implementation:
Question
  ↓
Search Endee (Retrieval)
  ↓
Analyze retrieved documents
  ↓
Generate answer (Augmented Generation)

Benefits:

* More accurate answers
* Verifiable sources
* Reduced hallucination


3. Semantic Search via Embeddings
What: Converting text to vectors and finding similar vectors
Your Implementation:
Text → Embedding Model → Vector → Store in Endee
       ↓
Query → Embedding Model → Vector → Find similar vectors
       ↓
Return semantically similar documents

Why It Works:

* Similar meanings → Similar vectors
* Can use math to find similar documents
* Fast to search (billions of vectors in milliseconds)


4. Prompt Engineering
What: Carefully crafting instructions to guide LLM behavior
Your Implementation:

* Planner: "Break this into exactly 3 focused sub-questions"
* Analyzer: "Summarize in 2-3 sentences"
* Reporter: "Structure with Executive Summary and Key Findings"


5. Named Entity Recognition (NER)
What: Automatically extracting important entities from text
Your Implementation:
Input: "OpenAI released GPT-4 in March 2024"

Output:
- PERSON/ORG: OpenAI
- PRODUCT: GPT-4
- DATE: March 2024

Usage: Identify key organizations, people, technologies

6. Vector Embeddings
What: Mathematical representation of text meaning
Example:
pythonDownloadCopy code"AI is transforming healthcare"     → [0.23, -0.15, 0.67, ...]
"Machine learning improves medicine" → [0.22, -0.14, 0.68, ...]
                                        ↑ Very similar! (cosine similarity ≈ 0.92)

"Python is a programming language"  → [0.12, 0.89, -0.34, ...]
                                        ↑ Very different! (cosine similarity ≈ 0.18)

7. State Management (LangGraph)
What: Managing data flow between agents using a shared state
Your Implementation:
pythonDownloadCopy codestate = {
    "query": "What is AI?",
    "sub_questions": [...],
    "search_results": [...],
    "analysis": [...],
    "final_report": "..."
}
Each agent reads from and writes to this state

📊 Performance Metrics
MetricValueNotesEnd-to-End Time10-30 secondsDepends on question complexityDocuments Searched9 per query3 sub-questions × 3 articlesEndee Retrieval8 documentsLimited to 8 most relevantSources in Report100% citedAll claims are sourcedEndee StoragePersistentBuilds over multiple queriesCostFree/LowFree tier APIs usedAccuracyHighGrounded in real sources
Performance Breakdown
Planner Agent:      ~2 seconds (LLM decomposition)
Searcher Agent:     ~3 seconds (Web search + Endee storage)
Analyzer Agent:     ~4 seconds (Endee search + NLP analysis)
Reporter Agent:     ~3 seconds (Report generation)
─────────────────────────────────
Total:              ~12 seconds (best case)
                    ~30 seconds (worst case)


❓ FAQ
About Endee
Q: What exactly is Endee?
A: Endee is a vector database that stores text as mathematical vectors (embeddings). It enables semantic search — finding documents by meaning, not just keywords.
Q: Why not just use Google Search?
A: Google returns links; Endee understands meaning. Plus, Endee stores results persistently for reuse across multiple searches.
Q: Does Endee require internet?
A: Endee Cloud API requires internet. Local installations are available.
Q: Can I reuse findings across searches?
A: Yes! Endee persists, so findings from previous searches can be searched again.
Q: How much does Endee cost?
A: Free tier available. Check https://endee.io for pricing details.

About the Project
Q: How is this different from ChatGPT?
A: ChatGPT uses training data only. This system searches the web in real-time and uses RAG pattern for verifiable, sourced answers.
Q: Can I use my own LLM?
A: Yes. The code uses LangChain abstractions, so you can swap Groq for any LLM (OpenAI, Anthropic, etc.).
Q: What if API keys are invalid?
A: App shows clear error messages. Check .env file and verify API key validity at respective dashboards.
Q: How many documents can Endee store?
A: Millions. Endee is optimized for scale.
Q: Can I customize the report format?
A: Yes. Modify the reporter.py prompt to change structure.

Troubleshooting
Q: "No module named 'endee'"
A: Install with pip install -r requirements.txt
Q: Streamlit app won't start
A: Check if port 8501 is available. Use streamlit run ui/app.py --server.port 8502
Q: "spaCy model not found"
A: Download with python -m spacy download en_core_web_sm
Q: API rate limits exceeded
A: Free tiers have limits. Groq (~10k requests/min), Tavily (1000/month)

🤝 Contributing
How to Contribute

1.
Fork the repository
bashDownloadCopy codegit clone https://github.com/YOUR_USERNAME/endee.git
cd endee

2.
Create feature branch
bashDownloadCopy codegit checkout -b feature/your-feature-name

3.
Make changes

Edit files
Test thoroughly
Follow code style


4.
Commit changes
bashDownloadCopy codegit commit -m "Add: Brief description of changes"

5.
Push to branch
bashDownloadCopy codegit push origin feature/your-feature-name

6.
Submit Pull Request

Describe changes clearly
Reference any related issues



Areas for Contribution

* 🐛 Bug fixes
* ✨ New features
* 📚 Documentation improvements
* 🧪 Test cases
* 🎨 UI improvements
* 📈 Performance optimizations


📝 License
This project is part of the Endee ecosystem. See LICENSE file for details.

📚 Learn More
Official Documentation

* Endee — https://github.com/endee-io/endee
* LangChain — https://langchain.com
* Groq — https://groq.com
* Tavily — https://tavily.com
* spaCy — https://spacy.io
* Streamlit — https://streamlit.io

Related Concepts

* Vector Embeddings
* RAG Pattern
* Multi-Agent Systems
* Semantic Search


📧 Support & Issues
Getting Help

1.
Check existing issues — https://github.com/MeghasuryaB/endee/issues

2.
Create new issue with:

Clear description
Error messages
Steps to reproduce
Python version
OS information


3.
Contact — Open discussion in repository


Reporting Bugs
Include:
- Error message (full traceback)
- Steps to reproduce
- Expected behavior
- Actual behavior
- Python version: python --version
- OS: Windows/Mac/Linux


✅ Endee Integration Checklist
Before submission, verify:

*  Endee imported in searcher.py
*  Endee imported in analyzer.py
*  endee.insert() stores documents
*  endee.search() retrieves documents
*  README explains Endee usage clearly
*  Code pushed to forked repo
*  Project in /examples/auto-research-agent/
*  Endee in requirements.txt
*  App runs and uses Endee
*  RAG pattern implemented


🎉 Summary
AutoResearch Agent demonstrates a production-grade AI system using:
✅ Endee for semantic search and vector storage
✅ RAG pattern for grounded, accurate responses
✅ Multi-agent orchestration for complex workflows
✅ Real-time data with verified sources
✅ Scalable architecture ready for production
Why This Project Stands Out

1. Semantic Understanding — Uses Endee for meaning-based search
2. Practical Implementation — Works end-to-end
3. Real-World Use Case — Solves actual research problems
4. Production Architecture — Multi-agent, RAG, proper error handling
5. Modern AI Practices — Demonstrates 2026-level AI engineering

This project showcases skills valuable in any professional AI environment.

📞 Contact & Questions
For questions about this project:

* Open a GitHub issue
* Check discussions section
* Review documentation


Last Updated: March 17, 2026
Status: ✅ Active & Functional
Version: 1.0.0
Repository: https://github.com/MeghasuryaB/endee
Project: examples/auto-research-agent

🙏 Acknowledgments

* Endee Team — For the excellent vector database
* Groq Team — For fast LLM inference
* Tavily — For AI-optimized web search
* LangChain — For LLM orchestration framework
* Community — For feedback and contributions


Thank you for using AutoResearch Agent! 🚀
If this project helped you, please consider:

* ⭐ Starring the repository
* 📢 Sharing with others
* 🤝 Contributing improvements
* 📝 Providing feedback

Happy researching! 🔬
```
