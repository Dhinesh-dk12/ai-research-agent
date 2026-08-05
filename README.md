# AI Research Agent

An intelligent, end-to-end AI Research Agent built with **LangGraph**, **Claude**, **Tavily MCP**, **ChromaDB**, and **Sentence Transformers**.

The agent autonomously plans research, searches the web, extracts relevant content, summarizes documents, retrieves previous knowledge from memory, performs evidence-based reasoning, generates a professional research report, and exports the final report as a PDF.

---

## Features

- LangGraph-based workflow orchestration
- AI-powered research planning
- Tavily MCP web search integration
- Parallel webpage extraction
- AI summarization of extracted content
- URL deduplication
- Duplicate memory detection
- ChromaDB vector memory
- Semantic memory retrieval
- Evidence-based reasoning with citations
- Professional Markdown report generation
- PDF report export
- Structured logging
- Modular and scalable architecture

---

## Architecture

```
                    USER QUERY
                         │
                         ▼
                 ┌──────────────┐
                 │ Planner Node │
                 └──────────────┘
                         │
                         ▼
                ┌───────────────┐
                │ Executor Node │
                └───────────────┘
                         │
                         ▼
               ┌─────────────────┐
               │ Extraction Node │
               └─────────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │ Memory Retrieval Node  │
            └────────────────────────┘
                         │
                         ▼
              ┌────────────────────┐
              │ Reasoning Node     │
              └────────────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │ Memory Storage Node    │
            └────────────────────────┘
                         │
                         ▼
              ┌────────────────────┐
              │ Report Node        │
              └────────────────────┘
                         │
                         ▼
               ┌───────────────────┐
               │ PDF Generation    │
               └───────────────────┘
                         │
                         ▼
                    FINAL REPORT
```

---

## Project Structure

```
ai_research_agent/
│
├── graph/
│   ├── builder.py
│   ├── workflow.py
│   ├── state.py
│   └── nodes/
│
├── planner/
├── executor/
├── extractor/
├── summarizer/
├── reasoning/
├── report/
├── research/
├── memory/
├── llm/
├── utils/
│
├── reports/
├── logs/
├── main.py
├── requirements.txt
└── README.md
```

---

## Tech Stack

### AI Models

- Claude Sonnet
- Sentence Transformers (all-MiniLM-L6-v2)

### Frameworks

- LangGraph
- LiteLLM
- ChromaDB
- ReportLab

### Search

- Tavily MCP

### Vector Database

- ChromaDB

### Language

- Python 3.10+

---

## Installation

Clone the repository.

```bash
git clone https://github.com/YOUR_USERNAME/ai-research-agent.git

cd ai-research-agent
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file from `.env.example`.

```bash
cp .env.example .env
```

Then update the API keys.

---

## Running the Project

```bash
python main.py
```

---

## Workflow

1. Receive research query
2. Generate research plan
3. Execute web search
4. Extract webpages
5. Summarize content
6. Retrieve relevant memory
7. Perform evidence-based reasoning
8. Store new knowledge
9. Generate research report
10. Export PDF

---

## Example Output

The project generates:

```
reports/
    final_report.pdf
```

Example report sections include:

- Executive Summary
- Key Findings
- Technical Analysis
- Challenges
- Future Directions
- References

---

## Current Capabilities

- AI Planning
- Web Research
- Parallel Content Extraction
- Semantic Memory
- Duplicate Detection
- Evidence-based Reasoning
- Professional Report Generation
- PDF Export

---

## Roadmap

- Memory-aware extraction cache
- Hybrid Retrieval (BM25 + Vector Search)
- Reflection Agent
- Multi-Agent Collaboration
- Human-in-the-loop Review
- Streaming Progress Updates
- Deep Research Mode
- Interactive Web Interface

---

## License

This project is released under the MIT License.

---

## Acknowledgements

- LangGraph
- Tavily
- Anthropic Claude
- LiteLLM
- ChromaDB
- Sentence Transformers
- ReportLab