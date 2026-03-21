# AdaptIQ 🚀

An intelligent, dynamically generated corporate onboarding pathway designed to eliminate "one-size-fits-all" training inefficiencies. 

Behind the corporate buzzwords, this is a hybrid AI pipeline that rips apart a candidate's resume, hallucinates as little as mathematically possible, maps the remnants to federal databases using string-matching witchcraft, and spits out a mathematically proven learning roadmap. 

## 🧠 Core Architecture & Workflow (The Sausage Factory)

We bypassed standard LLM API costs and data privacy lawsuits by running this locally. Here is how the magic actually happens:

1. **Intelligent Parsing (The Bouncer):** We use a locally quantized **Mistral-7B-Instruct-v0.2** model to strip corporate fluff from resumes and extract pure competency data.
2. **Semantic Grounding (The Fuzz):** Resumes have terrible spelling. We use `thefuzz` to semantically anchor whatever the candidate wrote to the absolute ground truth: the **O*NET SOC Database** (U.S. Department of Labor).
3. **Adaptive Logic (The Gap):** We calculate the absolute skill gap ($Required - Current$). 
4. **Pedagogical Pathway (The Math):** The missing skills are fed into a **Directed Acyclic Graph (DAG)** using `networkx`. We run a Topological Sort to generate a prerequisite-aware training roadmap. 
    * *Note: If a circular dependency is detected, the system deliberately throws a `NetworkXUnfeasible` error.*

---

## 💻 Installation & Setup

Choose your poison: Bare metal or Docker container. 

### Method A: Bare Metal (For the Brave)
1. Clone the repository and pray to the dependency gods.
2. Create a virtual environment: `python -m venv venv && source venv/bin/activate` (or `venv\Scripts\activate` on Windows).
3. Install the dependencies: `pip install -r requirements.txt`.
4. Run the pipeline: `python -m AI.buildgraph`

### Method B: Docker (For the "Works on my Machine" crowd)
You can containerize this, but you *must* pass your GPU through to the container, or your CPU will literally melt trying to multiply tensors.

```bash
# Build the image
docker build -t onboarding-engine .

# Run the container (NVIDIA Container Toolkit REQUIRED)
docker run --gpus all -v $(pwd)/Data:/app/Data -it onboarding-engine
```

---

## ⚠️ The Elephant in the Room: GPU & Docker Bottlenecks

Let’s not sugar-coat it. Running a 7B parameter LLM locally inside a Docker container is a logistical nightmare if you don't know what you are bottlenecking. Here is why the system might crawl and how to fix it:

### 1. The VRAM Hunger Games (Quantization Overhead)
We are using 4-bit NF4 Quantization via `bitsandbytes`. 
* **The Good:** It shrinks Mistral-7B from ~15GB of VRAM down to a manageable ~6GB, allowing it to run on consumer-grade GPUs.
* **The Bad:** There is no free lunch. The GPU has to dequantize the weights back to 16-bit float *on the fly* during matrix multiplication. This makes inference slightly slower than native unquantized models because you are bottlenecked by **compute**, not just memory bandwidth.

### 2. The Docker GPU Passthrough Trap
If you forget the `--gpus all` flag in Docker, or if your NVIDIA Container Toolkit isn't configured correctly, Docker will silently default to CPU execution. 
* **The Symptom:** Your fans sound like a Boeing 747, RAM usage spikes to 100%, and you generate 0.2 tokens per second. 
* **The Fix:** Ensure your host machine has CUDA drivers and `nvidia-docker2` installed. 

### 3. I/O and PCIe Bottlenecks (The Docker Tax)
Docker adds an abstraction layer over your file system. 
* Loading the multi-gigabyte `.safetensors` model weights from a mounted Docker volume into system RAM, and then transferring them over the PCIe bus to the GPU VRAM, can take significantly longer inside a container if volume I/O isn't optimized. 
* **Pro-tip:** Don't mount the model weights directory as a standard bind mount if you can avoid it; bake the model into the image if storage permits, or ensure you are using a Gen4 NVMe SSD to minimize the initialization bottleneck.

---
**Tech Stack:** `Mistral-7B-v0.2` | `bitsandbytes` | `Pandas` | `thefuzz` | `NetworkX` | `Spite`