<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">IntelSwarm</h3>

  <p align="center">
    A hierarchical multi-agent swarm that generates recruiter-style competitive intelligence briefings from a single company name.
  </p>
</div>

## Demo
<img width="1920" height="1112" alt="demo_intelswarm" src="https://github.com/user-attachments/assets/25f66953-cbc5-425a-a835-bc7a676dd59c" />

IntelSwarm is a full-stack competitive intelligence tool that uses a hierarchical multi-agent swarm built with Strands Agents and Ollama to generate recruiter-style company briefing documents from a single company name. Five specialist agents run in parallel across product, hiring, funding, news, and culture (each reviewed for quality and rerun if needed) before being synthesized into a structered markdown report with a TL;DR and strategic recommendations.

Inference runs fully locally via Ollama. No API key required.

### Built With

* [![Python][Python.org]][Python-url]
* [![FastAPI][FastAPI.tiangolo.com]][FastAPI-url]
* [![Ollama][Ollama]][Ollama-url]
* [![React][React.js]][React-url]
* [![Vite][Vite.dev]][Vite-url]


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Python 3.9 or later
* Node.js 18 or later
* [Ollama](https://ollama.com) installed and running locally

### Installation

1. Install Ollama
   ```sh
   curl -fsSL https://ollama.com/install.sh | sh
   ```
2. Pull the local model
   ```sh
   ollama pull llama3.1:8b
   ```
3. Clone the repo
   ```sh
   git clone https://github.com/your_username/intelswarm.git
   cd intelswarm
   ```
4. Install Python dependencies
   ```sh
   pip install -r requirements.txt
   ```
5. Install frontend dependencies
   ```sh
   cd frontend
   npm install
   ```
6. Configure environment variables
   ```sh
   cp .env.example .env
   ```
   ```env
   OLLAMA_HOST=http://localhost:11434
   OLLAMA_MODEL=llama3.1:8b
   MIN_QUALITY_SCORE=6
   MAX_RERUNS=2
   REPORTS_DIR=./reports
   ```

> Ollama runs locally at `http://localhost:11434` by default. Inference can run fully offline once the model is pulled.


<!-- USAGE -->
## Usage

### CLI

```sh
python main.py --company "Stripe"
```

The CLI shows a live Rich status table and prints the final report when the swarm completes.

### Full Stack App

Start the backend:
```sh
uvicorn backend.server:app --reload --port 8000
```

Start the frontend:
```sh
cd frontend
npm run dev
```

Then open `http://localhost:5173`.


<!-- HOW IT WORKS -->
## How It Works

IntelSwarm runs in four orchestration phases:

| Phase | Description |
|-------|-------------|
| **1. Parallel Delegation** | The orchestrator launches five specialist agents concurrently with `asyncio.gather()` and streams live status updates for each |
| **2. Quality Review** | Each agent outputs a parseable `QUALITY_SCORE` and sections below the configured threshold are rerun with targeted guidance up to the maximum rerun limit |
| **3. Synthesis** | The orchestrator combines the strongest outputs into a final briefing with a TL;DR and strategic recommendations |
| **4. Save Report** | The finished markdown briefing is stored in `reports/{company}_{timestamp}.md` and returned to both the CLI and web client |

### Architecture

```text
User Input
    │
    ▼
Orchestrator Agent
 ┌──┬──┬──┬──┐
 ▼  ▼  ▼  ▼  ▼
Product · Hiring · Funding · News · Culture
         (parallel)
    │
    ▼
Quality review + rerun if score < 6
    │
    ▼
Orchestrator synthesis
    │
    ▼
Final Briefing Report
```

### Frontend Views

* **Input view**: company search, CTA, and recent reports
* **Research view**: live specialist agent progress with quality badges
* **Report view**; markdown rendering, section navigation, copy, download, and reset


<!-- API ENDPOINTS -->
## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/research` | Start a new research job for `{ "company": "Stripe" }`, returns a `job_id` |
| `GET` | `/research/{job_id}/stream` | Stream live progress as SSE until the report is complete |
| `GET` | `/reports` | List previously generated markdown reports |
| `GET` | `/reports/{filename}` | Return the raw markdown for a saved report |


<!-- PROJECT STRUCTURE -->
## Project Structure

```text
IntelSwarm/
├── main.py
├── orchestrator.py
├── config.py
├── agents/
│   ├── __init__.py
│   ├── product_agent.py
│   ├── hiring_agent.py
│   ├── funding_agent.py
│   ├── news_agent.py
│   └── culture_agent.py
├── tools/
│   ├── __init__.py
│   └── search.py
├── backend/
│   └── server.py
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── index.css
│       ├── api/
│       │   └── client.js
│       └── components/
│           ├── CompanyInput.jsx
│           ├── AgentProgress.jsx
│           ├── ReportViewer.jsx
│           └── SectionCard.jsx
├── reports/
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/your_username/intelswarm.svg?style=for-the-badge
[contributors-url]: https://github.com/your_username/intelswarm/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/your_username/intelswarm.svg?style=for-the-badge
[forks-url]: https://github.com/your_username/intelswarm/network/members
[stars-shield]: https://img.shields.io/github/stars/your_username/intelswarm.svg?style=for-the-badge
[stars-url]: https://github.com/your_username/intelswarm/stargazers
[issues-shield]: https://img.shields.io/github/issues/your_username/intelswarm.svg?style=for-the-badge
[issues-url]: https://github.com/your_username/intelswarm/issues
[license-shield]: https://img.shields.io/github/license/your_username/intelswarm.svg?style=for-the-badge
[license-url]: https://github.com/your_username/intelswarm/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/your_username
[product-screenshot]: images/screenshot.png
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org
[FastAPI.tiangolo.com]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com
[Ollama]: https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logoColor=white
[Ollama-url]: https://ollama.com
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vite.dev]: https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white
[Vite-url]: https://vitejs.dev
