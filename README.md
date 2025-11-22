# 📚 Multi-Agent Publication Reviewer & Recommendation System (AAIDC – Project 2)

This project implements a multi-agent AI system that analyzes GitHub repositories and produces actionable recommendations for improving technical publications.
The system evaluates README structure, tag quality, metadata completeness, clarity of explanation, and missing documentation.
It generates a concise reviewer-style report combining feedback from multiple specialized agents, creating a publish-ready improvement guide.

This project was developed as part of the Ready Tensor – Agentic AI Developer Certification (Module 2) and demonstrates multi-agent collaboration, tool augmentation, human-in-the-loop validation, and structured workflow orchestration using LangGraph.

## 🌟 Key Features

This system goes beyond a simple text analyzer by enabling cooperation between multiple agents, each responsible for a distinct aspect of the review pipeline.
Every agent contributes unique insights, and the orchestrator ensures that the sequence of analysis is deterministic, explainable, and robust.

The workflow includes:

Automated retrieval of README content from GitHub

Keyword extraction and tag recommendation

Content enhancement suggestions (title, intro, missing sections)

Final reviewer report combining all agent outputs

Human-in-the-loop checkpoints allowing the user to approve or edit intermediate results

Error handling to safely recover from malformed URLs, missing READMEs, or API failures

Clear logging and output persistence to the outputs/ directory


## 🧩 System Architecture
Agents & Their Roles
| Agent                      | Purpose                                             |
| -------------------------- | --------------------------------------------------- |
| **Repo Analyzer Agent**    | Reads GitHub repo, extracts README + file structure |
| **Tag Recommender Agent**  | Extracts keywords and proposes project tags         |
| **Content Improver Agent** | Suggests better title/summary and missing sections  |
| **Reviewer Agent**         | Consolidates all findings into final report         |

## 🛠 Tools Used
Several tools extend the intelligence of the agents:
| Tool                               | Purpose                                                              |
| ---------------------------------- | -------------------------------------------------------------------- |
| **GitHub Content Reader**          | Fetches README content using GitHub’s raw content and API patterns.  |
| **YAKE Keyword Extractor**         | Identifies salient keywords for tag generation.                      |
| **Google Gemini LLM**              | Generates improved summaries, titles, and the final reviewer report. |
| **Tenacity-based retry mechanism** | Ensures resilience against transient network failures.               |

## 🧰 Tech Stack
| Component          | Technology    |
| ------------------ | ------------- |
| Language           | Python 3.9+   |
| Framework          | LangGraph     |
| LLM                | Google Gemini |
| Keyword Extraction | YAKE          |
| Environment        | dotenv        |
| Output             | Text reports  |

## 📁 Project Structure
![alt text](<Project Structure.png>)

# ⚙️ Installation & Setup

1️⃣ Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

2️⃣ Install dependencies
python -m pip install -r requirements.txt

3️⃣ Configure environment variables
Create a .env file in the project root:
GOOGLE_API_KEY=your_google_api_key_here
.env is protected via .gitignore and will not be committed.

▶️ Running the Application One-time setup (make src a package)

ni .\src\__init__.py -ItemType File -ErrorAction SilentlyContinue

▶️ Running the system (interactive HITL)

Analyze a public GitHub repo with human-in-the-loop checkpoints:

python -m src.app --repo "https://api.github.com/repos/{owner}/{repo}/readme"

💡 Explanation:

{owner} = GitHub username or organization

{repo} = Repository name

This URL correctly points to the GitHub REST API endpoint for the README file.

Example:

python -m src.app --repo "https://github.com/sbm-11-SFDC/rt-aaidc-project2-multiagent"

Non-interactive (automated) mode:

python -m src.app --repo "https://api.github.com/repos/{owner}/{repo}/readme"--no-interactive

Example:

python -m src.app --repo "https://github.com/sbm-11-SFDC/rt-aaidc-project2-multiagent" --no-interactive

Generated Output

outputs/recommendations_<timestamp>.txt

outputs/report_<timestamp>.txt

# 🧩 Human-in-the-Loop (HITL) Interaction

At key phases, the system pauses and asks the user:

Proceed? (yes/no/edit)

Edit suggested title / intro / excerpt?

Override auto-generated suggestions?

This ensures trust, transparency, and human oversight—important principles for agentic AI systems.

# 🏗️ Architecture Overview

The system follows a clear multi-agent pipeline:

Repo Analyzer reads the GitHub repo, extracts README, project metadata, and structural signals.

Tag Recommender generates keyword-based tags using YAKE and document semantics.

Content Improver rewrites and enhances project descriptions, summaries, and titles.

Reviewer Agent evaluates the combined output and produces the final consolidated report.

Human Reviewer (HITL) optionally refines or approves the final result.

# 🛡️ Safety, Error Handling & System Resilience

The system incorporates multiple layers of defensive design:

GitHub fetch failures gracefully fallback with clear messages

Retry logic mitigates temporary API or network failures

Input sanitization protects agents from malformed README content

Shared state prevents inconsistent transitions or data loss

Missing README or empty content is safely detected early

Human approval required before finalizing key stages

These measures collectively ensure the system remains stable, interpretable, and reliable even during edge-case scenarios.

# 📊 Performance Evaluation (Summary)

A full evaluation report is available in performance_evaluation.md.
The assessment covered:

Retrieval and parsing stability across multiple repositories

Agent-to-agent coordination performance

Robustness under malformed URLs, missing READMEs, and unexpected text formats

Human-in-the-loop interaction timing and error recovery

Execution time, reliability, and failure resilience

The system achieved consistent output and demonstrated strong reliability during repeated test runs with different GitHub repositories.

# 📄 License
This project is licensed under the MIT License.

See the [LICENSE] file for details

# 👤 Author

Suraj Mahale

AI & Salesforce Developer

GitHub: https://github.com/sbm-11-SFDC

