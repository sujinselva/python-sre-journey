import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


LOG_FILE = Path("python-errors.log")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# A current Groq-supported model.
MODEL = "llama-3.3-70b-versatile"


def analyze_failure(log_text: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not available")

    prompt = f"""
You are an experienced Python and Site Reliability Engineering mentor.

Analyze this GitHub Actions failure for a Python beginner.

Explain clearly:

1. Which Python file failed
2. The exact error
3. Why it happened
4. The steps to fix it
5. Corrected Python code, when possible

Do not invent details that are not present in the log.

GitHub Actions log:

{log_text}
"""

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 0.2,
    }

    request = urllib.request.Request(
        GROQ_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        response_data = json.loads(response.read().decode("utf-8"))

    return response_data["choices"][0]["message"]["content"]


def write_github_summary(analysis: str) -> None:
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")

    if not summary_path:
        print("GITHUB_STEP_SUMMARY is not available.")
        return

    with Path(summary_path).open("a", encoding="utf-8") as summary:
        summary.write("# AI Failure Analysis\n\n")
        summary.write(analysis)
        summary.write("\n")


def main() -> int:
    if not LOG_FILE.exists():
        print(f"{LOG_FILE} was not found.")
        return 0

    log_text = LOG_FILE.read_text(
        encoding="utf-8",
        errors="replace",
    )

    if not log_text.strip():
        print("The error log is empty.")
        return 0

    try:
        analysis = analyze_failure(log_text)
    except urllib.error.HTTPError as error:
        response_body = error.read().decode("utf-8", errors="replace")
        print(f"Groq API returned HTTP {error.code}")
        print(response_body)
        return 0
    except urllib.error.URLError as error:
        print(f"Unable to connect to Groq: {error}")
        return 0
    except Exception as error:
        print(f"AI analysis failed: {error}")
        return 0

    print("=" * 80)
    print("AI FAILURE ANALYSIS")
    print("=" * 80)
    print(analysis)

    write_github_summary(analysis)
    return 0


if __name__ == "__main__":
    sys.exit(main())
    