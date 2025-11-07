# 📚 Multi-Agent Publication Reviewer & Recommendation System (AAIDC – Project 2)

This project implements a multi-agent AI system that analyzes GitHub repositories and generates structured improvement suggestions for better publication quality.
It reviews README content, metadata, tags, structure, and missing documentation, then creates a final report with actionable recommendations.

✅ Built with LangGraph for agent orchestration
✅ Uses multiple specialized agents
✅ Integrates multiple tools including a GitHub reader, keyword extractor, and Google Gemini LLM

## ✅ Features

✔ Multi-agent system with clear roles
✔ Each agent communicates and contributes to shared task
✔ Orchestrated workflow using LangGraph
✔ Generates:

Improved project title

Better short description

Suggested tags and categories

Missing README sections

Final combined reviewer report

✔ Outputs saved locally for reference

## ✅ System Architecture
🧠 Agents
| Agent                      | Purpose                                             |
| -------------------------- | --------------------------------------------------- |
| **Repo Analyzer Agent**    | Reads GitHub repo, extracts README + file structure |
| **Tag Recommender Agent**  | Extracts keywords and proposes project tags         |
| **Content Improver Agent** | Suggests better title/summary and missing sections  |
| **Reviewer Agent**         | Consolidates all findings into final report         |

## 🛠 Tools
| Tool                     | Function                                     |
| ------------------------ | -------------------------------------------- |
| ✅ GitHub Content Reader  | Fetch README, repo structure                 |
| ✅ YAKE Keyword Extractor | Extracts tags/topics                         |
| ✅ Google Gemini API      | Writes summaries, improvements, final report |

## ✅ Tech Stack
| Component          | Technology    |
| ------------------ | ------------- |
| Language           | Python 3.9+   |
| Framework          | LangGraph     |
| LLM                | Google Gemini |
| Keyword Extraction | YAKE          |
| Environment        | dotenv        |
| Output             | Text reports  |

## ✅ Project Structure
![alt text](<Project Structure 2.png>)

## ✅ Setup Instructions
1️⃣ Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Add your API key

Create .env in project root:

GOOGLE_API_KEY=your_key_here

## ✅ How to Run

# Example:

# make src a package (one-time)
ni .\src\__init__.py -ItemType File -ErrorAction SilentlyContinue

# run the app as a module
python -m src.app --repo "https://github.com/sbm-11-SFDC/rt-aaidc-project2-multiagent"

## 💡 Output files generated:

outputs/recommendations.txt
outputs/report.txt

## ✅ Sample Output (What the report includes)

✔ Improved project title
✔ Better short summary
✔ Relevant tags & categories
✔ Missing README sections checklist
✔ Final reviewer-style recommendations

## ✅ Author

Suraj Mahale
AI & Salesforce Developer
GitHub: https://github.com/sbm-11-SFDC

