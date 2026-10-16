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
- Source credibility scoring (official and academic sources weighted above blogs and forums)
- Memory relevance filtering (unrelated past research is not mixed into new reports)
- Date-aware research planning
- Automatic stealth-browser fallback for pages that block plain downloads
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
├── pyproject.toml
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

### Web Extraction

- Scrapling (HTTP fetcher with a stealth-browser fallback)

### Vector Database

- ChromaDB

### Language

- Python 3.10+

---

## Installation

### Prerequisites

- Python 3.10+
- Node.js (the Tavily MCP search server is started with `npx`)
- An Anthropic API key and a Tavily API key

Clone the repository.

```bash
git clone https://github.com/Dhinesh-dk12/ai-research-agent.git

cd ai-research-agent
```

### Option 1: uv (recommended)

Install [uv](https://docs.astral.sh/uv/), then:

```bash
uv venv
uv sync
uv run scrapling install
```

`uv sync` installs everything listed in `pyproject.toml`. `scrapling install` is a one-time download of the browser used by the stealth fallback.

### Option 2: pip

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

Install dependencies and the browser used by the stealth fallback.

```bash
pip install -r requirements.txt
scrapling install
```

---

## Environment Variables

Create a `.env` file from `.env.example`.

Linux / macOS

```bash
cp .env.example .env
```

Windows

```bash
copy .env.example .env
```

Then update the API keys.

---

## Running the Project

```bash
python main.py
```

With uv you can also run `uv run python main.py` without activating the environment.

---

## Workflow

1. Receive research query
2. Generate research plan
3. Execute web search
4. Extract webpages (stealth-browser fallback for blocked pages)
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
    final_report.md
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
- Source Credibility Scoring
- Memory Relevance Filtering
- Stealth-browser Fallback for Blocked Pages
- Professional Report Generation
- PDF Export

---

## Changelog / Fixes

**Stability**
- Fixed a startup bug (syntax error + a broken Windows async setting) that stopped the agent from running at all
- Fixed the planner crashing on research plans with more than 5 tasks
- Fixed a harmless but alarming shutdown error message on Windows

**Report quality**
- Rewrote PDF export — tables, bold/italic text, links, and lists now render correctly, and it no longer crashes on special characters
- Added source credibility scoring, so official and academic sources are weighted above low-quality ones
- Resolved proxy-wrapped source links to point at the original article

**Research quality**
- Fixed memory retrieval so unrelated past research no longer leaks into new reports
- Fixed source selection so every research task gets covered, not just the first few
- Research planning is now date-aware, so search queries use the current year instead of stale dates
- Pages that block plain downloads (bot-check stubs) are now retried with a stealth browser, so more sources are actually read

**Project cleanup**
- Reduced project dependencies from 216 packages to 13 actually used ones
- Added `uv` support (`pyproject.toml`); `requirements.txt` still works for pip users and now includes the extra Scrapling needs for fetching
- Cleaned up unused/dead code (moved to a backup folder, nothing deleted)

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