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
  ```

---

## 🚀 Getting Started

Install dependencies

```bash
pip install requests rich python-dotenv
```

Run LM Studio

- Load any compatible chat model.
- Enable the local API server (http://localhost:1234/v1/chat/completions).

Edit /data/config.env

```
API_URL=http://localhost:1234/v1/chat/completions
MODEL=your-model-name
TEMPERATURE=0.7
MAX_TOKENS=512
```

Start the companion

```bash
python main.py
```

---

## 🧠 Architecture Summary

The system is organized into three abstraction layers:

| Layer | Description |
|-------|-------------|
| Frontend | The user-facing interface (CLI or GUI). Handles I/O. |
| Conversation Core | Maintains dialogue context and message sequencing. |
| Backend Connector | Sends requests to LM Studio’s local inference API. |

This design allows future extensions like:

- Persistent personality memory (via binary or JSON)
- Context trimming or replay systems
- GUI frontends (PySide, Tkinter, or Unity integration)

---

## 🧰 Future Roadmap

| Version | Goal |
|---------|------|
| v0.1 | Core architecture, CLI chat, API integration ✅ |
| v0.1.1 | Context trimming, logging, multiple personalities |
| v0.2 | Persistent adaptive memory and emotion models |
| v0.3 | Frontend GUI or Unity plugin integration |

---

## 📄 License

This project is distributed for educational and experimental purposes.
Use and modification are encouraged under open, non-commercial conditions.
