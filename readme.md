# AI-Adaptive Onboarding Engine

An intelligent, dynamically generated corporate onboarding pathway designed to eliminate "one-size-fits-all" training inefficiencies. 

This engine parses a new hire's current capabilities, cross-references them against the U.S. Department of Labor's O*NET federal taxonomy, and dynamically maps an optimized, personalized training curriculum using graph theory.

## 🧠 Core Architecture & Workflow
We bypassed standard LLM hallucinations by using a hybrid AI + Federal Taxonomy approach:
1. **Intelligent Parsing:** Utilized a locally quantized **Mistral-7B-Instruct-v0.2** model to extract pure competency data from candidate resumes, strictly avoiding corporate fluff.
2. **Semantic Grounding:** Leveraged `thefuzz` semantic matching to anchor corporate job titles to the **O*NET SOC Database**. 
3. **Adaptive Logic:** Calculated the absolute skill gap ($Required - Current$) and fed the missing nodes into a **Directed Acyclic Graph (DAG)** using `networkx`.
4. **Pedagogical Pathway:** Computed a Topological Sort to generate a prerequisite-aware, phase-by-phase learning roadmap.

## 🛠 Tech Stack
* **LLM Engine:** Mistral-7B-v0.2 Instruct (4-bit NF4 Quantization via `bitsandbytes`)
* **Data Processing:** Pandas, Regex, JSON
* **Taxonomy Engine:** FuzzyWuzzy (`thefuzz`)
* **Graph Mathematics:** NetworkX 
* **Ground Truth Dataset:** O*NET 30.1 Database (U.S. Department of Labor)
... (more coming soon)
## 🚀 Setup & Reproducibility 
-- to be updated soon