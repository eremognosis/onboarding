# info.md

## The Documentation

This system is an AI-Adaptive Onboarding Engine designed to stop the bleeding of corporate training inefficiencies by actually looking at what a person knows versus what the job requires. 

### How It Works (The Logic Flow)
1.  **Competency Extraction**: We ingest raw resumes and use a locally quantized **Mistral-7B-Instruct-v0.2** to strip out the adjectives and keep the hard skills.
2.  **The Semantic Bridge**: Since humans describe the same skill in fifty different ways, we use `thefuzz` to anchor these descriptions to the **O*NET SOC Database**.
3.  **Graph Synthesis**: The system calculates the "Skill Gap" ($Required - Current$) and maps these missing pieces into a **Directed Acyclic Graph (DAG)** via `networkx`.
4.  **Topological Sorting**: We don't just give a list; we give a roadmap. The algorithm performs a topological sort to ensure prerequisites (like Python 101) are finished before someone tries to build a neural net.

### The Solution Approach
We opted for a **Hybrid AI + Federal Taxonomy** model. Instead of letting an LLM hallucinate a career path, we use the LLM solely for data extraction and let graph theory handle the actual logic. This ensures the "optimal learning pathway" isn't just a suggestion—it’s mathematically sound.

---

## 📉 The Time Issue


* **The 48-Hour Constraint**: Developing a fully integrated, end-to-end adaptive engine in a two-day window is essentially an exercise in managed chaos. To maintain any semblance of code integrity, the project was developed in modular blocks (Extraction -> Mapping -> Pathing) to allow for localized debugging without crashing the entire stack.
* **The GPU Bottleneck**: Attempting to run a 7B parameter model pipeline repeatedly on consumer-grade hardware—or worse, a CPU-only environment—is like trying to run a marathon through waist-deep mud. Because constant end-to-end inference was computationally expensive and hardware-prohibitive, we pivoted to a **piecewise execution model**. 
* **Engineering Through Spite**: The current state of the project is a "modular masterpiece" born of necessity. We cached the outputs of the LLM layer to allow the Graph and Taxonomy engines to iterate without waiting for a local GPU to finish its tensor-crunching existential crisis. 

This isn't "fragmented code"; it's **"Asynchronous Resource Optimization"** necessitated by a lack of enterprise-grade compute and a deadline that arrived before we did. It works, it’s logical, and it’s held together by better math than the hardware probably deserves.