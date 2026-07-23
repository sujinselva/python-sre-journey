from pathlib import Path
import sys

from ai import ask_gpt


LOG_FILE = "python-errors.log"


def main() -> int:
    print("AI Failure Analyzer started")

    log_path = Path(LOG_FILE)

    if not log_path.exists():
        print(f"Error: {LOG_FILE} was not found.")
        return 1

    error_log = log_path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    if not error_log.strip():
        print(f"Error: {LOG_FILE} is empty.")
        return 1

    prompt = f"""
You are a senior Python mentor helping an experienced SRE learn Python.

Analyze the following GitHub Actions failure.

Provide these sections:

1. Root Cause
2. Failed File
3. Failed Line
4. Simple Explanation
5. Smallest Fix

Do not rewrite the entire program.

ERROR LOG:

{error_log}
"""

    try:
        answer = ask_gpt(prompt)
    except Exception as error:
        print("AI analysis failed.")
        print(f"Reason: {error}")
        return 1

    print()
    print("=" * 80)
    print("AI FAILURE ANALYSIS")
    print("=" * 80)
    print(answer)
    print("=" * 80)

    return 0


if __name__ == "__main__":
    sys.exit(main())