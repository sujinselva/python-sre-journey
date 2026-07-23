# Python SRE Journey

This repository is used to practice Python with a simple CI/CD workflow.

Whenever code is pushed to GitHub, GitHub Actions automatically runs all Python files inside the `Day01` directory.

If any Python file fails, the workflow captures the error and sends it to Groq AI. Groq then explains:

- Which file failed
- What the exact error is
- Why the error happened
- How to fix it
- A corrected code example

This gives the repository an automated AI-based troubleshooting process.

---

## Repository Structure

```text
python-sre-journey/
├── .github/
│   └── workflows/
│       └── python.yml
├── Day01/
│   ├── variables.py
│   ├── lists.py
│   └── loops.py
├── scripts/
│   └── analyze_failure.py
├── Projects/
├── Challenges/
├── Notes/
├── push.sh
└── README.md

Folder Purpose
Day01/ contains Python learning programs.
scripts/ contains supporting automation scripts.
.github/workflows/ contains the GitHub Actions workflow.
Projects/ will contain larger Python projects.
Challenges/ will contain coding challenges.
Notes/ will contain Python and SRE study notes.
push.sh provides a single command to commit and push local changes.
README.md documents the project.