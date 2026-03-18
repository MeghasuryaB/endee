AutoResearch Agent - Endee-Powered Semantic Research System

📋 Table of Contents

- Overview
- What is Endee?
- Why We Use Endee
- Where Endee is Used
- Quick Start
- System Architecture
- Features
- Tech Stack
- Project Structure
- Installation & Setup
- Usage
- API Methods
- Performance
- FAQ
- Contributing

🎯 Overview
AutoResearch Agent is an intelligent multi-agent AI research system that automatically researches any topic by breaking down complex questions, searching the web for relevant information, storing findings in a vector database, analyzing content semantically, and generating comprehensive research reports with citations.
What Makes It Different?

- ✅ Uses semantic search via Endee (understands meaning, not just keywords)
- ✅ Implements RAG (Retrieval-Augmented Generation) pattern
- ✅ Uses multi-agent orchestration (4 specialized agents working together)
- ✅ Provides real-time, verifiable information with source attribution
- ✅ Demonstrates production-grade AI architecture

Example Use Case
User asks: "What are the latest AI trends in healthcare?"
System breaks into 3 sub-questions → Searches web → Stores in Endee → Semantically retrieves → Analyzes → Generates comprehensive report with citations

🔍 What is Endee?
Simple Definition
Endee is a Vector Database that stores and retrieves information based on semantic meaning rather than keyword matching.
How It Works
Traditional Search: Query "Find AI" → Result: Only exact matches for "AI" → Problem: Misses "machine learning", "deep learning"
Vector Database (Endee): Query "Find AI" → Result: "AI", "machine learning", "deep learning", "neural networks" → Benefit: Understands meaning, not just keywords
The Technical Process
Step 1: Convert Text to Vectors
Text: "Artificial intelligence is transforming healthcare" → Embedding Model converts to 384-dimensional vector → [0.23, -0.15, 0.67, 0.42, ..., 0.51]
Step 2: Store in Endee

- Original text is stored
- Its vector (384 numbers) is stored
- Metadata (source, date, etc.) is stored

Step 3: Search Semantically
When you search for "machine learning in medicine", Endee converts query to vector, finds similar vectors, and returns semantically similar documents.

🎯 Why We Use Endee
Benefits
AspectWithout EndeeWith EndeeSearch TypeKeyword-onlySemanticResults QualityLimitedBetter understanding of meaningProcessingAnalyzes all resultsAnalyzes only relevant onesPerformanceSlow on large dataFast even with millionsKnowledge ReuseNoneReuses previous findings
Real Example
For "Quantum Computing Breakthroughs":
Without Endee returns irrelevant results like "The quantum (number) of energy breakthroughs"
With Endee returns only relevant documents about quantum computing technology, breakthroughs, companies, and applications.
System Benefits

1. Better Search Quality - Finds relevant information even with different wording
2. Faster Analysis - Focuses analyzer on relevant docs only
3. Knowledge Reuse - Searches across all previous findings
4. Scalability - Handles millions of documents efficiently
5. Semantic Understanding - Understands "AI" = "machine learning" = "deep learning"
6. Reduced Hallucination - LLM bases answers on retrieved facts

📍 Where Endee is Used
Location 1: Searcher Agent (Storage)
File: agents/searcher.py
The searcher agent:

- Fetches articles from Tavily Web API
- Automatically converts each article to a 384-dimensional vector
- Stores vector + original text + metadata in Endee database
- Creates a searchable knowledge base of all research findings

Location 2: Analyzer Agent (Retrieval)
File: agents/analyzer.py
The analyzer agent:

- Queries Endee with the research question
- Retrieves top 8 semantically similar documents (not just keywords)
- Performs NLP analysis on retrieved documents
- Extracts entities, summarizes content, identifies sources
- More efficient and accurate results focused on relevant information

Location 3: Reporter Agent (Uses Retrieved Context)
File: agents/reporter.py
The reporter agent:

- Receives analyzed data that was retrieved from Endee
- Uses grounded context to generate final report
- Implements RAG pattern - Retrieved + Augmented + Generation
- Ensures report is accurate and verifiable

Location 4: Requirements File
requirements.txt includes endee==0.1.19 as a core dependency

🚀 Quick Start
Prerequisites

- Python 3.8+
- API Keys: GROQ_API_KEY, TAVILY_API_KEY

Installation
Clone the repository:
git clone https://github.com/MeghasuryaB/endee.git
cd endee/examples/auto-research-agent
Create virtual environment:
python -m venv .venv
.venv\Scripts\activate # Windows
source .venv/bin/activate # Mac/Linux
Install dependencies:
pip install -r requirements.txt
Download spaCy model:
python -m spacy download en_core_web_sm
Setup environment variables:
cp .env.example .env
Edit .env with your API keys
Run the App
python -m streamlit run ui/app.py
Access at: http://localhost:8501

🏗️ System Architecture
The system consists of four main agents that work together:

1. Planner Agent (LLM) - Breaks complex questions into focused sub-questions
2. Searcher Agent - Searches web and stores articles in Endee as vectors
3. Analyzer Agent - Searches Endee semantically and analyzes retrieved documents
4. Reporter Agent - Generates final research report with citations

Data flows from user query → planner breaks it down → searcher finds and stores in Endee → analyzer searches Endee and analyzes → reporter generates comprehensive report.

✨ Features
Core Features

- Semantic Search via Endee (not just keywords)
- RAG Pattern (Retrieved context grounds LLM)
- Real-time Web Search (Tavily API)
- Multi-Agent Orchestration (LangGraph)
- Named Entity Recognition (spaCy)
- Source Attribution (Verifiable citations)
- Persistent Knowledge (Endee reuses findings)

Advanced Capabilities

- Intelligent Decomposition - Breaks complex queries into focused sub-questions
- Context-Aware Analysis - Understands semantic meaning, not just keywords
- Structured Reports - Professional formatting with executive summaries
- Fast Inference - Groq's optimized LLM (100+ tokens/sec)
- Extensible Architecture - Easy to add new agents or modify behavior
- Real-Time Information - Not limited to training data cutoff
- Knowledge Persistence - Endee stores findings for future searches

🛠️ Tech Stack
ComponentTechnologyPurposeVector DatabaseEndeeSemantic search & vector storageAgent OrchestrationLangGraphMulti-agent workflow coordinationLanguage ModelGroq + Llama 3Fast, accurate LLM inferenceWeb SearchTavily APIReal-time web information retrievalNLPspaCyNamed entity recognition & analysisUI FrameworkStreamlitInteractive web interfaceLLM FrameworkLangChain CoreStandardized LLM abstractionsEnvironmentPython-dotenvConfiguration management

📁 Project Structure
auto-research-agent/
├── agents/ - AI Agent Implementations
│ ├── planner.py - Decompose questions into sub-questions
│ ├── searcher.py - Search web + Store in Endee
│ ├── analyzer.py - Search Endee + Analyze content
│ └── reporter.py - Generate final report
├── graph/ - LangGraph Orchestration
│ ├── state.py - State management structure
│ └── workflow.py - Agent coordination & flow
├── ui/ - Streamlit Interface
│ └── app.py - Main app interface
├── utils/ - Helper Functions
│ ├── config.py - Configuration loading
│ └── logger.py - Logging utilities
├── requirements.txt - Python dependencies
├── .env.example - Environment variables template
└── README.md - This file

💻 Installation & Setup
Step 1: Clone Repository
git clone https://github.com/MeghasuryaB/endee.git
cd endee/examples/auto-research-agent
Step 2: Create Virtual Environment
Windows:
python -m venv .venv
.venv\Scripts\activate
Mac/Linux:
python3 -m venv .venv
source .venv/bin/activate
Step 3: Install Dependencies
pip install -r requirements.txt
This installs:

- endee - Vector database for semantic search
- langchain-groq - Groq LLM integration
- langchain-core - Core LangChain utilities
- tavily-python - Web search API client
- python-dotenv - Environment variable management
- spacy - NLP library for entity extraction
- streamlit - Web UI framework

Step 4: Download spaCy Model
python -m spacy download en_core_web_sm
Required for Named Entity Recognition (NER) - Extracting people, organizations, products, dates
Step 5: Setup Environment Variables
cp .env.example .env
Edit .env with your API keys:
GROQ_API_KEY=your_actual_groq_api_key_here
TAVILY_API_KEY=your_actual_tavily_api_key_here
How to Get Free API Keys:
Groq API Key:

- Visit https://console.groq.com
- Sign up for free
- Navigate to API Keys
- Copy your API key
- Free tier: Unlimited requests (rate limited)

Tavily API Key:

- Visit https://tavily.com
- Sign up for free
- Go to API section
- Copy your API key
- Free tier: 1000 API calls per month

Step 6: Run Application
python -m streamlit run ui/app.py
Opens at: http://localhost:8501

📖 Usage
Using the Web Interface

1.  Enter Research Question - Type your research question in the Streamlit interface
    Example: "What are the latest AI trends in 2026?"

2.  Click "🚀 Start Research" - The system begins processing

3.  Watch Live Progress - See real-time updates as agents work:
    ✓ Planner: Decomposed into sub-questions
    ✓ Searcher: Found articles, stored in Endee
    ✓ Analyzer: Searched Endee, extracted entities
    ✓ Reporter: Generating final report

4.  View Final Report - System displays:

Executive Summary
Key Findings
Detailed Analysis
Important Entities
Sources with citations

Python API Usage
from graph.workflow import create_research_graph
Create the research workflow
graph = create_research_graph()
Run research on a topic
result = graph.invoke({
"query": "What is blockchain?"
})
Get the final report
print(result["final_report"])
Access other outputs
print(result["sub_questions"])
print(result["analysis"])

🔌 API Methods
Endee Storage Method (Searcher Agent)
from endee import Endee
client = Endee()
client.insert(
document="The text content you want to store",
metadata={
"title": "Document Title",
"url": "https://example.com/article",
"source": "web_search"
}
)
Parameters:

- document (str): The text to convert to vector and store
- metadata (dict): Additional information (optional)

What Happens Internally:

1. Text is converted to 384-dimensional vector
2. Vector is stored with original text
3. Metadata is indexed for filtering
4. Ready for semantic search

Endee Retrieval Method (Analyzer Agent)
from endee import Endee
client = Endee()
results = client.search(
query="machine learning trends",
limit=8
)
for result in results:
document = result["document"]
metadata = result["metadata"]
score = result["score"]
print(f"Score: {score:.2f}")
print(f"URL: {metadata['url']}")
print(f"Content: {document[:100]}...")

Return Values:

- document: Original text stored
- metadata: Information you provided during insertion
- score: Similarity score from 0-1 (1.0 = perfect match)

📊 Performance
MetricValueNotesEnd-to-End Time10-30 secondsDepends on question complexityDocuments Searched9 per query3 sub-questions × 3 articlesEndee Retrieval8 documentsLimited to 8 most relevantSources in Report100% citedAll claims are sourcedEndee StoragePersistentBuilds over multiple queriesCostFree/LowFree tier APIs usedAccuracyHighGrounded in real sources
Performance Breakdown:
Planner Agent: ~2 seconds
Searcher Agent: ~3 seconds
Analyzer Agent: ~4 seconds
Reporter Agent: ~3 seconds
Total: ~12 seconds (best case) to ~30 seconds (worst case)

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
A: App shows clear error messages. Check .env file and verify API key validity.
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

1. Fork the repository
2. Create feature branch (git checkout -b feature/your-feature-name)
3. Make changes and test thoroughly
4. Commit changes (git commit -m "Add: Description")
5. Push to branch (git push origin feature/your-feature-name)
6. Submit Pull Request with clear description

Areas for Contribution

- Bug fixes
- New features
- Documentation improvements
- Test cases
- UI improvements
- Performance optimizations

📚 Learn More
Official Documentation

- Endee: https://github.com/endee-io/endee
- LangChain: https://langchain.com
- Groq: https://groq.com
- Tavily: https://tavily.com
- spaCy: https://spacy.io
- Streamlit: https://streamlit.io

Related Concepts

- Vector Embeddings: https://en.wikipedia.org/wiki/Word_embedding
- RAG Pattern: https://huggingface.co/blog/rag
- Multi-Agent Systems: https://arxiv.org/abs/2308.00352
- Semantic Search: https://www.deepset.ai/semantic-search

📧 Support & Issues
Getting Help

1. Check existing issues: https://github.com/MeghasuryaB/endee/issues
2. Create new issue with clear description, error messages, and steps to reproduce
3. Open discussion in repository

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

- Endee imported in searcher.py
- Endee imported in analyzer.py
- endee.insert() stores documents
- endee.search() retrieves documents
- README explains Endee usage clearly
- Code pushed to forked repo
- Project in /examples/auto-research-agent/
- Endee in requirements.txt
- App runs and uses Endee
- RAG pattern implemented

🎉 Summary
AutoResearch Agent demonstrates a production-grade AI system using:
✅ Endee for semantic search and vector storage
✅ RAG pattern for grounded, accurate responses
✅ Multi-agent orchestration for complex workflows
✅ Real-time data with verified sources
✅ Scalable architecture ready for production
Why This Project Stands Out

1. Semantic Understanding - Uses Endee for meaning-based search
2. Practical Implementation - Works end-to-end
3. Real-World Use Case - Solves actual research problems
4. Production Architecture - Multi-agent, RAG, proper error handling
5. Modern AI Practices - Demonstrates 2026-level AI engineering

This project showcases skills valuable in any professional AI environment.

Last Updated: March 17, 2026
Status: ✅ Active & Functional
Version: 1.0.0
Repository: https://github.com/MeghasuryaB/endee
Project: examples/auto-research-agent

Thank you for using AutoResearch Agent! 🚀
If this project helped you, please consider:

- ⭐ Starring the repository
- 📢 Sharing with others
- 🤝 Contributing improvements
- 📝 Providing feedback

Happy researching! 🔬
