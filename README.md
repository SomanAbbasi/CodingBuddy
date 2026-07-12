# CodingBuddy

AI coding agent that turns a natural-language prompt into a **complete** small project (all files, not just one). It uses a free Groq model by default.

## How it works

1. **Planner** — designs the app (name, stack, features, file list)
2. **Architect** — creates one implementation step per file
3. **Coder** — generates full file contents and writes them under `generated_projects/`

The coder loop runs once per file until every planned file exists.

## Requirements

- Python 3.12+
- A free [Groq API key](https://console.groq.com/keys)

## Setup

```bash
# Clone
git clone https://github.com/SomanAbbasi/CodingBuddy.git
cd CodingBuddy

# Create a virtual environment (uv or venv)
uv sync
# or: python -m venv .venv && .venv\Scripts\activate && pip install -e .

# Configure API key
copy .env.example .env
# Edit .env and set GROQ_API_KEY=...
```

On macOS/Linux use `cp .env.example .env` instead of `copy`.

### Environment variables

| Variable       | Required | Default                     | Description                          |
|----------------|----------|-----------------------------|--------------------------------------|
| `GROQ_API_KEY` | Yes      | —                           | Key from Groq console                |
| `GROQ_MODEL`   | No       | `llama-3.3-70b-versatile`   | Any Groq chat model on your free tier |

Other free-tier options you can try: `llama-3.1-8b-instant`, `qwen/qwen3-32b`, `qwen/qwen3.6-27b`.

## Usage

From the project root:

```bash
python main.py "Create a simple todo list app in HTML, CSS, and JavaScript"
```

Verbose logs:

```bash
python main.py -v "Build a calculator with HTML, CSS, and JavaScript"
```

Generated apps are written to:

```text
generated_projects/<Project_Name>/
```

Open that folder and open `index.html` in a browser (for static web apps).

## Project layout

```text
CodingBuddy/
├── main.py                 # CLI entry point
├── graph/
│   ├── graph.py            # LangGraph pipeline (planner → architect → coder)
│   ├── state.py            # Pydantic schemas
│   ├── prompts.py          # Agent prompts
│   └── tools.py            # Safe file writer
├── generated_projects/     # Output (gitignored)
├── .env.example
├── pyproject.toml
└── README.md
```

## Error handling

- Missing `GROQ_API_KEY` fails fast with a clear message
- Planner / architect / coder failures are caught and reported without crashing mid-write
- Path traversal outside the project folder is blocked
- Empty model output is treated as an error for that file
- The pipeline stops early if planning or architecture fails

## License

MIT — use and modify freely.
