# CrewAI + DomeKit Example

A multi-agent CrewAI crew that runs through [DomeKit](https://github.com/a-choyster/domekit), an open-source local-first AI runtime with enforced privacy boundaries. DomeKit sits between CrewAI and your local LLM as an OpenAI-compatible API, invisibly policy-checking every tool call and audit-logging all activity across every agent in the crew.

## Prerequisites

- **Python 3.11+**
- **Ollama** installed with `llama3.1:8b` pulled (`ollama pull llama3.1:8b`)
- **DomeKit** cloned and installed (see [DomeKit repo](https://github.com/a-choyster/domekit))

## Setup

### 1. Clone this repo

```bash
git clone https://github.com/a-choyster/domekit-crewai-example.git
cd domekit-crewai-example
```

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Create the sample database

```bash
python setup_data.py
```

### 4. Start DomeKit with the included manifest

In a separate terminal, from wherever you cloned DomeKit:

```bash
domekit start --manifest /path/to/domekit-crewai-example/domekit.yaml
```

DomeKit will start an OpenAI-compatible API on `localhost:8080`.

### 5. Run the crew

```bash
python crew.py
```

## What to expect

The crew has two agents:

1. **Researcher** -- queries the product database to find top products by revenue.
2. **Writer** -- takes the researcher's findings and writes a brief market summary.

DomeKit is invisible to CrewAI -- it looks like any other OpenAI-compatible endpoint. But behind the scenes, every tool call from every agent is:

- **Policy-checked** against `domekit.yaml` (only `sql_query` and `read_file` are allowed; only `data/` is readable; no network access)
- **Audit-logged** to `audit.jsonl`

This is especially powerful with CrewAI because you have multiple agents, and DomeKit controls what ALL of them can access.

## Checking the audit log

After running the crew, inspect the audit log:

```bash
cat audit.jsonl | python -m json.tool --json-lines
```

Each entry shows which agent made the call, what tool was invoked, what parameters were passed, and whether the policy allowed or denied it.

## Links

- [DomeKit](https://github.com/a-choyster/domekit) -- the open-source local-first AI runtime
