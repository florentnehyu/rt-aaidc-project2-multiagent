# src/agents.py
from typing import Dict, List, Tuple
import re
from collections import Counter

STOPWORDS = {
    "the", "and", "to", "of", "a", "in", "is", "for", "this", "that", "on", "with",
    "by", "as", "it", "an", "be", "are", "or", "from", "your", "we", "our", "you"
}


def repo_analyzer(readme_text: str) -> Dict:
    """
    Analyze README: presence of common sections, length, quick suggestions.
    Returns a dict with keys: summary, sections, suggestions
    """
    text = (readme_text or "").strip()
    tokens = len(text.split())
    sections = {
        "title": bool(re.search(r"^#\s+", text, re.MULTILINE)),
        "installation": bool(re.search(r"(?i)installation", text)),
        "usage": bool(re.search(r"(?i)usage", text)),
        "contributing": bool(re.search(r"(?i)contributing", text)),
        "license": bool(re.search(r"(?i)license", text)),
        "examples": bool(re.search(r"(?i)example", text)),
    }

    suggestions = []
    if not sections["title"]:
        suggestions.append("Add a short, descriptive title at the top (H1).")
    if not sections["installation"]:
        suggestions.append("Add an Installation section with 3 steps (venv, install, .env).")
    if not sections["usage"]:
        suggestions.append("Add Usage examples and example CLI commands.")
    if tokens < 100:
        suggestions.append(
            "Consider expanding the README with a short project description (100+ words)."
        )

    summary = (
        f"README length: {tokens} words. "
        f"Sections found: {', '.join(k for k, v in sections.items() if v)}."
    )
    return {
        "summary": summary,
        "sections": sections,
        "suggestions": suggestions,
        "readme_excerpt": text[:1000],
    }


def _simple_keywords(text: str, k: int = 6) -> List[Tuple[str, int]]:
    text = re.sub(r"[^\w\s]", " ", (text or "").lower())
    tokens = [t for t in text.split() if t not in STOPWORDS and len(t) > 2]
    counts = Counter(tokens)
    return counts.most_common(k)


def tag_recommender(readme_text: str) -> Dict:
    """
    Suggest project tags (simple frequency-based keywords).
    """
    kw = _simple_keywords(readme_text, k=8)
    tags = [w.replace(" ", "-") for w, _ in kw]
    return {"tags": tags, "keywords": kw}


def content_improver(readme_text: str) -> Dict:
    """
    Provide a few suggested rewrites for title/intro.
    Keep this simple: pick first heading and suggest a polished version.
    """
    text = (readme_text or "").strip()
    title_match = re.search(r"^#\s*(.+)$", text, re.MULTILINE)
    first_para = ""

    if title_match:
        title = title_match.group(1).strip()
    else:
        title = "Project Title"

    # find first paragraph after title
    after = text[title_match.end():] if title_match else text
    paras = re.split(r"\n\s*\n", after.strip())
    if paras:
        first_para = paras[0].strip()

    # simple polish: shorten long sentences (very naive)
    suggestion_title = f"{title} — A concise RAG & multi-agent assistant"
    suggestion_intro = (
        (first_para[:320] + ("…" if len(first_para) > 320 else ""))
        or "This repository implements a multi-agent assistant that reviews GitHub repositories and recommends improvements."
    )

    return {
        "suggested_title": suggestion_title,
        "suggested_intro": suggestion_intro,
    }


def reviewer(state: Dict) -> Dict:
    """
    Synthesize outputs from agents into a final actionable report (string).
    state: expected keys: analyzer, tags, improvements
    """
    analyzer = state.get("analyzer", {})
    tags = state.get("tags", {}).get("tags", [])
    improvements = state.get("improvements", {})

    lines = []
    lines.append("Final Report — Multi-Agent Publication Reviewer\n")
    lines.append(analyzer.get("summary", "No analysis available."))

    if analyzer.get("suggestions"):
        lines.append("\nTop Suggestions:")
        for s in analyzer["suggestions"]:
            lines.append(f" - {s}")

    if tags:
        lines.append("\nSuggested tags: " + ", ".join(tags))

    if improvements:
        lines.append("\nContent improvement suggestions:")
        lines.append(f" * Title: {improvements.get('suggested_title')}")
        lines.append(f" * Intro (preview): {improvements.get('suggested_intro')}")

    report = "\n".join(lines)
    return {"report": report}