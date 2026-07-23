import os
import sys
from pathlib import Path

from groq import Groq


LOG_FILE = Path("python-errors.log")
MODEL = "llama-3.1-8b-instant"


def analyze_failure(log_text: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior SRE and Python mentor. "
                    "Give clear, accurate, beginner-friendly explanations."
                ),
            },
            {
                "role": "user",
                "content": f"""
Analyze this GitHub Actions failure.

Explain:

1. Which file failed
2. The exact error
3. Why it happened
4. How to fix it
5. Corrected code when possible

Do not invent details.

Log:

{log_text}
""",
            },
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content


def write_summary(analysis: str) -> None:
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")

    if not summary_path:
        print(analysis)
        return

    with Path(summary_path).open("a", encoding="utf-8") as summary:
        summary.write("# Groq AI Failure Analysis\n\n")
        summary.write(analysis)
        summary.write("\n")


def main() -> int:
    if not LOG_FILE.exists():
        print("python-errors.log was not found.")
        return 0

    log_text = LOG_FILE.read_text(
        encoding="utf-8",
        errors="replace",
    )

    try:
        analysis = analyze_failure(log_text)
    except Exception as error:
        print(f"Groq analysis failed: {error}")
        return 0

    print(analysis)
    write_summary(analysis)
    return 0


if __name__ == "__main__":
    sys.exit(main())