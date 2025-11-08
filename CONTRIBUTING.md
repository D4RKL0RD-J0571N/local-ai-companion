# Contributing

Thank you for your interest in contributing to local-ai-companion!  
This repository demonstrates a private, fully offline AI companion. Your contributions — whether code, docs, tests, or ideas — help make it better for everyone.

---

🧩 Contributing Guidelines — Overview
- Read this document to learn how to contribute, what to expect during review, and the project's coding conventions.
- Be respectful and collaborative. See the Code of Conduct section below.

---

🛠️ Getting started

1. Fork the repository
- Click the "Fork" button at the top-right of the GitHub page to create your copy.

2. Clone your fork locally
```bash
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>
```

3. Create a feature branch
```bash
git checkout -b feature/<short-description>
# Example:
git checkout -b feature/add-new-ui-panel
```

4. Install dependencies
- Add platform- and language-specific setup here (examples):
  - Unity: Unity 6.1 or higher required. Open the project in the matching Unity Editor and import packages via the Package Manager.
  - Node.js: Install Node.js 18+ and run `npm install` or `pnpm install`.
  - Python: Use a virtual environment and run `pip install -r requirements.txt`.
- If your change requires additional setup steps, document them in your PR description.

---

💬 Code style

Follow the existing style and conventions used across the repository.

General
- Keep naming consistent with current files and systems.
- Comment complex logic: concise, clear, and focused on intent.
- Avoid committing temporary, debug, or auto-generated files.
- Keep commits focused and atomic when practical.

Unity projects
- Use PascalCase for class names and camelCase for variables.
- Keep serialized fields private and use [SerializeField] where appropriate.
- Group related components logically.
- Avoid hardcoding references — prefer managers, registries, or ScriptableObjects.
- Keep Scenes and Assets organized in folders and document any required Editor tools.

Formatting & Linting
- Run project linters/formatters before committing (if configured).
- If you add or change a linter rule, include rationale in the PR.

---

🔄 Submitting changes

1. Commit with clear messages
- Use concise, descriptive commit messages that explain the "what" and "why".
```bash
git add .
git commit -m "Add: camera rotation based on mouse input"
git commit -m "Fix: actor event registration order issue"
```

2. Push your branch
```bash
git push origin feature/<short-description>
```

3. Create a Pull Request (PR)
- On GitHub, open a PR from your branch to the repository's main branch.
- Use a short summary and a more detailed description that includes:
  - What you changed
  - Why you changed it
  - How to test it (steps to reproduce, test data)
  - Any migration or setup notes

4. Wait for review
- PRs will be reviewed by maintainers and contributors.
- Address requested changes via follow-up commits on the same branch.

---

🧾 Commit message conventions (recommended)

Prefer structured prefixes for commits to make history and changelogs clearer.

| Prefix    | Meaning                                         |
|-----------|-------------------------------------------------|
| Add:      | New feature, component, or file                 |
| Fix:      | Bug fix or issue correction                     |
| Refactor: | Code improvement without feature change         |
| Remove:   | Feature or file removal                         |
| Doc:      | Documentation-only change                       |
| Style:    | Formatting, naming, or style-only changes       |

Example:
```
git commit -m "Refactor: simplify memory manager initialization"
```

---

🧰 Tests & validation

- Add unit/integration tests where appropriate.
- Run the project's test suite locally before submitting a PR.
- If your change affects builds (editor, packaging, or CI), include notes about required CI updates.

---

✅ Pull Request checklist
Before requesting review, ensure:
- [ ] Code builds and runs locally.
- [ ] Tests added or updated (when applicable).
- [ ] Linting/formatting issues resolved.
- [ ] No temporary debug code or credentials included.
- [ ] The PR description includes testing instructions and rationale.

Maintainers may request changes or additional tests during review.

---

🪧 Issues & discussions

- Search existing issues before opening a new one — it may already exist.
- Use clear titles and provide relevant details:
  - Error messages and logs
  - Steps to reproduce
  - Platform and version information
  - Screenshots or screencasts when helpful
- For feature suggestions, consider creating a Discussion or an issue labeled "enhancement".
- Use labels, milestones, and linked PRs to clarify the status of issues and proposed fixes.

---

❤️ Code of Conduct

We aim to maintain a welcoming, respectful, and inclusive community. All participants must:
- Be respectful and supportive.
- Be open to feedback and collaborative improvement.
- Avoid harassment, exclusionary language, or personal attacks.

If you encounter inappropriate behavior, contact the maintainers or open a private report via GitHub if available. We will treat reports seriously and act to resolve them.

---

📜 Licensing & attribution

- By contributing, you agree that your contributions will be licensed under the repository's license. Ensure you have rights to submit the code or content you propose.
- If you contribute third-party code or assets, include attribution and licensing details in your PR.

---

🛎️ Additional notes and contact

- If you're unsure where to start, open an issue or a Discussion asking for guidance — we can recommend small starter tasks.
- If you want help preparing a PR (tests, packaging, or build), mention it in your PR description or in a related issue.

---

Thank you for helping improve local-ai-companion! Your contributions make the project stronger, more secure, and friendlier to experiment with.
