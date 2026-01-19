# Seminar Report Generator 📝🤖

An LLM-powered Seminar Report Generator built using **LangGraph**, **RAG**, and **Streamlit**.  
The system automatically generates structured academic seminar reports from user input and reference documents.

---

## 🚀 Features

- 🧠 **LangGraph-based workflow** for controlled multi-step generation
- 📚 **Retrieval-Augmented Generation (RAG)** using vector embeddings
- ✍️ Section-wise academic report generation
- 🔁 Iterative refinement using graph-based execution
- 🎛️ Streamlit UI for interactive usage

---

## 🏗️ Project Architecture

  SEMINAR_REPORT_GENERATOR
  ├── config/ # Application settings & configuration
  │ └── settings.py
  ├── notebooks/ # Experiments and testing
  │ └── sample_test.ipynb
  ├── src/ # Core application logic
  │ ├── graph_builder.py # LangGraph workflow construction
  │ ├── nodes.py # Individual graph nodes (LLM calls)
  │ ├── models.py # LLM & embedding model setup
  │ ├── prompts.py # Prompt templates
  │ └── rag_setup.py # Vector store & retrieval logic
  ├── streamlit_app/ # UI layer
  │ └── app.py
  ├── requirements.txt
  ├── pyproject.toml
  └── README.md

---

## ⚙️ Tech Stack

- **Python 3.11**
- **LangGraph**
- **LangChain**
- **OpenAI API**
- **Vector Database (RAG)**
- **Streamlit**

---

## 🔑 Environment Setup

Create a `.env` file based on the example:

```bash
cp .env.example .env
```

Add your keys:

TAVILY_API_KEY=your_api_key_here

## 📦 Installation

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

```bash
streamlit run streamlit_app/app.py
```

## 🧠 How It Works

- User provides seminar topic and context

- Relevant documents are retrieved via RAG

- LangGraph executes section-wise report generation

- Final structured seminar report is synthesized

- Output is displayed via Streamlit UI, can download .md file

## 📌 Notes

- Designed with modularity and extensibility in mind

- Configuration handled via settings.py (environment-driven)

- Suitable for academic, research, and demo use cases
