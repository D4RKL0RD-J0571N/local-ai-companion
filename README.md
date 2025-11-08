# Local AI Companion v0.1

A locally hosted conversational AI designed to emulate a human-like companion personality.  
Built on top of **LM Studio**, it runs entirely offline using your own hardware and GPU for model inference.

---

## 🌐 Overview

**Local AI Companion** is an experimental project that connects a lightweight Python frontend with LM Studio's local API server.  
It’s designed for offline operation, modularity, and eventual expandability into systems with persistent memory, personality adaptation, and emotional state modeling.

---

## 🧩 Features (v0.1)

- Local conversation loop (fully offline)
- LM Studio integration via HTTP API
- System prompts for defining character/personality
- Simple text-based interface using `rich`
- Configurable model, temperature, and token limits via `.env` file

---

## ⚙️ Requirements

**Running on:**
- Windows 11  
- NVIDIA GPU (RTX 3060 or better recommended)
- 32 GB RAM (minimum 16 GB)
- Python 3.11+

**Software:**
- [LM Studio](https://lmstudio.ai/) — local API server enabled on port 1234  
- Python packages:
  ```bash
  pip install requests rich python-dotenv
