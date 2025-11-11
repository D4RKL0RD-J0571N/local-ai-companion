# 🧑‍💻 Local AI Companion — Fully Offline Conversational AI Framework

**A solo-developed, modular Python project demonstrating a fully offline, customizable AI companion with contextual dialogue, persistent memory, and voice interaction capabilities—built for experimentation, learning, and creative R&D.**

---

## 🎯 Overview

_Local AI Companion_ is a Python-first toolkit for building private, self-contained AI assistants—without any cloud dependency or external API requirement. Designed as a testbed for my interests in natural language processing, agent memory systems, and ethical AI, this project demonstrates modular architecture, extensibility, and user privacy.

Developed solo as both an engineering challenge and a learning experience, it’s ideal for:
- **Developers** interested in customizable AI chatbots
- **Researchers** focusing on privacy-first, offline LLM experimentation
- **Hobbyists** exploring AI dialogue and personal assistant tech

---

## 🧠 Architecture Overview

```
LocalAICompanion/
├── core/
│   ├── DialogueEngine.py    # Manages context-aware conversations
│   ├── MemoryModule.py      # Implements persistent, queryable memory
│   └── PluginManager.py     # Simple plugin/modular system
├── voice/
│   ├── SpeechRecognition.py # (Optional) Handles offline speech input
│   ├── TTSModule.py         # (Optional) Offline text-to-speech
├── models/
│   └── LocalLLMWrapper.py   # Interfaces local LLMs (e.g., llama.cpp, GPT4All)
├── utils/
│   ├── Config.py            # Centralized config/settings handler
│   └── Helpers.py           # Miscellaneous utility functions
└── app.py                   # Entry point CL/UI for launching the companion
```

---

## ⚙️ Core Features

- **🛡️ 100% Offline**: No data leaves your device. Absolutely no external API calls.
- **🧠 Contextual Dialogue System**: Maintains multi-turn, context-aware conversations using local language models.
- **🌿 Modular Memory**: Supports short- and long-term memory with file-based or database persistence.
- **🔌 Extensible Plugins**: Simple plugin architecture for adding new skills or modules (e.g., reminders, media control, web search).
- **🎤 (Optional) Voice Interface**: Integrates local speech-to-text and text-to-speech libraries for full voice interaction.
- **💡 Configurable Personality**: Easily customize companion’s responses, tone, and behavior at runtime.
- **🛠️ Developer-Friendly**: Designed for hacking—straightforward architecture, clear interfaces, and ample docstrings.

---

## 🚦 Example Usage Flow

1. **User launches the app** (`python app.py`), chooses terminal or voice mode.
2. **Input is captured** (text or speech) and routed through the dialogue engine.
3. **Context + memory**: Current input is merged with conversational history and relevant memory snippets.
4. **Local LLM processes** the prompt, with customized personality/system-prompt.
5. **Companion responds** (in text/voice), optionally logging the new interaction to memory.

---

## 🧩 Portfolio Value & Learning Highlights

- **System Modularity**: Isolated dialogue, memory, and voice—rapidly swap or test new modules with minimal friction.
- **Privacy by Design**: Inspired by ethical AI—demonstrates processing all data offline, exposing no personal details.
- **Python Engineering**: Applies object-oriented best practices, config-driven design, and plugin interfaces.
- **Hands-on LLM Experimentation**: Explores local large language model wrappers, prompt engineering, and context management.
- **Human-AI UX**: Focuses on SQ (suitably “human”-sounding) dialogue, proactive memory, and useful agent behaviors.

---

## 🔗 Key Tech & Tools

- **Python 3.10+**
- Local LLMs (e.g., [llama.cpp](https://github.com/ggerganov/llama.cpp), [GPT4All](https://github.com/nomic-ai/gpt4all))
- Optional: `SpeechRecognition`, `TTS` libs (e.g., `vosk`, `pyttsx3`)
- Data: Local file system or lightweight SQLite for memory persistence

---

## 🧾 Example Code: Contextual Dialogue Step

```python
# DialogueEngine.py - main dialogue loop
user_input = capture_input()
context = memory.retrieve_context(user_input)
response = local_llm.generate_response(context, user_input)
print("AI Companion:", response)
memory.store_interaction(user_input, response)
```

---

## 🗒️ Lessons Learned

- **Designing for privacy** changes architecture and tradeoffs meaningfully.
- **Modular Python design** makes prototyping and feature-adding fast.
- RLHF (reinforcement learning from human feedback) is tough solo but simulating feedback via rules can teach a lot.
- Voice interfaces require graceful error handling for every module.
- Experimenting locally offers unique freedom compared to cloud-based AI design.

---

## ✨ Future Roadmap

- Full voice UI (audio input and TTS output) with noise-robust handling
- Advanced memory/semantic recall (embedding search)
- Plug-in framework for generic “skills” (calendar, music, home automation, etc)
- Portable desktop app using `PyQt` or similar, for easier deployment
- Integrate unit/integration tests
- Write detailed user/developer documentation

---

## 👤 Author

**Jostin Lopez (J0571N)**  
Indie Python Developer · AI Experimenter · Passionate about ethical, private-by-default technology

“Pushing boundaries with what’s possible—locally.”

---

## 📜 License

MIT License. This project may be freely studied, adapted, or built upon for non-commercial and educational use.

---

> *This repository is a personal portfolio project, intended as a technical showcase and learning resource.*
