# src/app.py
from __future__ import annotations
import os
import argparse
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import json
import sys

# ✅ Use package-relative imports so `python -m src.app` works
from .tools import safe_call, fetch_readme_via_api
from .agents import repo_analyzer, tag_recommender, content_improver, reviewer
from .state import MASState

OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)


def ask_human_choice(prompt_text: str) -> str:
    """
    Ask the human to choose: yes / no / edit
    (Human-in-the-loop control point)
    """
    while True:
        choice = input(prompt_text + " (yes / no / edit) > ").strip().lower()
        if choice in ("yes", "y"):
            return "yes"
        if choice in ("no", "n"):
            return "no"
        if choice == "edit":
            return "edit"
        print("Please enter 'yes', 'no' or 'edit'.")


def get_multiline_input(prompt_header: str) -> str:
    """
    Collect multi-line human input until a blank line is entered.
    Used when the human wants to edit intermediate outputs.
    """
    print(prompt_header)
    print("(Enter your edited text. Finish by entering a blank line on its own.)")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def run_pipeline(repo_url: str, interactive: bool = True, timeout_sec: int = 10):
    load_dotenv()
    state = MASState()

    print(f"\nFetching README for: {repo_url} ...")
    try:
        # ✅ Wrapped in safe_call for retry + error handling
        readme = safe_call(
            fetch_readme_via_api,
            repo_url,
            tries=3,
            base_delay=1.0,
            timeout=timeout_sec,
        )
    except Exception as e:
        print(f"Error fetching README: {e}")
        readme = None

    if not readme:
        print("No README found or failed to fetch. Aborting.")
        return

    # -----------------------------
    # Stage 1: Repo Analyzer
    # -----------------------------
    print("\n=== Repo Analyzer ===")
    analysis = repo_analyzer(readme)
    state.set("analyzer", analysis)

    print("\nAnalyzer summary:")
    print(analysis.get("summary"))
    if analysis.get("suggestions"):
        print("\nSuggestions:")
        for s in analysis["suggestions"]:
            print(" -", s)

    if interactive:
        choice = ask_human_choice("\nProceed to Tag Recommender?")
        if choice == "no":
            print("Pipeline stopped by user.")
            return
        if choice == "edit":
            edited = get_multiline_input(
                "Edit README excerpt (this will be used by next agents):"
            )
            if edited:
                readme = edited
                state.set("readme_edited", True)
                print("Edited README saved for next steps.")
    else:
        print("Non-interactive mode: continuing...")

    # -----------------------------
    # Stage 2: Tag Recommender
    # -----------------------------
    print("\n=== Tag Recommender ===")
    tags_out = tag_recommender(readme)
    state.set("tags", tags_out)

    print("Suggested tags:", ", ".join(tags_out.get("tags", [])))

    if interactive:
        choice = ask_human_choice(
            "Proceed to Content Improver (title/intro suggestions)?"
        )
        if choice == "no":
            print("Pipeline stopped by user.")
            return
        if choice == "edit":
            edited = get_multiline_input(
                "Edit content (title/intro) to use next:"
            )
            if edited:
                readme = edited
                state.set("readme_edited_by_tags", True)
                print("Edited content saved for next steps.")

    # -----------------------------
    # Stage 3: Content Improver
    # -----------------------------
    print("\n=== Content Improver ===")
    improvements = content_improver(readme)
    state.set("improvements", improvements)

    print("Suggested Title:", improvements.get("suggested_title"))
    print("Suggested Intro (preview):", improvements.get("suggested_intro"))

    if interactive:
        choice = ask_human_choice("Proceed to final Reviewer?")
        if choice == "no":
            print("Pipeline stopped by user.")
            return
        if choice == "edit":
            edited = get_multiline_input(
                "Edit improved intro/title to use in final report:"
            )
            if edited:
                # simple behavior: override intro in the state
                improvements["suggested_intro"] = edited
                state.set("improvements", improvements)
                print("Edited intro saved.")

    # -----------------------------
    # Stage 4: Reviewer (aggregation)
    # -----------------------------
    print("\n=== Reviewer: Synthesizing final report ===")
    report_out = reviewer(state.to_dict())
    report_text = report_out.get("report", "No report produced.")

    # Save outputs with timestamped filenames
    ts = str(int(__import__("time").time()))
    rec_f = OUTPUTS_DIR / f"recommendations_{ts}.txt"
    rpt_f = OUTPUTS_DIR / f"report_{ts}.txt"

    with open(rec_f, "w", encoding="utf-8") as fh:
        fh.write("Recommendations (auto-generated)\n\n")
        fh.write(json.dumps(state.to_dict(), indent=2))

    with open(rpt_f, "w", encoding="utf-8") as fh:
        fh.write(report_text)

    print("\n--- Final Report ---\n")
    print(report_text)
    print(f"\nSaved: {rec_f}\nSaved: {rpt_f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        type=str,
        help="GitHub repo URL to analyze",
        required=True,
    )
    parser.add_argument(
        "--no-interactive",
        action="store_true",
        help="Run pipeline without human prompts",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="HTTP timeout seconds",
    )
    args = parser.parse_args()

    run_pipeline(
        args.repo,
        interactive=not args.no_interactive,
        timeout_sec=args.timeout,
    )


if __name__ == "__main__":
    main()