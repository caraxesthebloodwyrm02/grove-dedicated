from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass
class RepoConcepts:
    main_classes: List[str]
    verbs: List[str]
    domain_terms: List[str]
    error_phrases: List[str]


KEY_CLASS_FRAGMENTS: List[str] = [
    "Recorder",
    "Narrator",
    "Uploader",
    "Processor",
    "Timeline",
    "Event",
    "Path",
    "Screen",
    "Video",
]

DOMAIN_SEEDS: List[str] = [
    "screen recording",
    "timelines",
    "events",
    "paths",
    "imports",
    "modules",
    "uploaders",
    "narrators",
    "ffmpeg",
    "YouTube",
]

VERB_KEYWORDS: List[str] = [
    "record",
    "process",
    "upload",
    "render",
    "capture",
    "timeline",
    "event",
    "path",
    "import",
    "module",
]

ERROR_PATTERNS: List[str] = [
    "error",
    "exception",
    "not found",
    "ModuleNotFoundError",
    "FileNotFoundError",
    "Path not found",
    "File not found",
]

CANONICAL_ERRORS: List[str] = [
    "ModuleNotFoundError",
    "File not found",
    "Path not found",
]


STORY_TEMPLATE: str = """
Black and white silent-film style short. No spoken dialogue, only Chaplin-style acting,
piano music, and intertitles. A young programmer bro in a small modern apartment is
learning to code using free tools: VS Code and Python.

{concepts_block}

0-15s - Title & Myth:
A black title card:
"They said: no need to learn coding. The machines will do it all."
Quick shots of the bro staring at an AI chat window on a laptop, then closing it and
opening VS Code instead.

15-40s - Fast setup with free tools:
The bro installs VS Code and Python (icons, progress bars). He opens VS Code, a new file,
the black menu bar clearly visible: 'File Edit Selection View Go Run Terminal Help'.
Intertitles say:
"Free editor. Free language. Just curiosity."

40-60s - First coding & debugging:
We only see the screen and his reactions. He types a tiny Python script and runs it in the
VS Code terminal. The terminal flashes errors like {debugging_error_examples}.
Visual gags: exaggerated sighs, head in hands, rolling back in the chair.

60-80s - Breakfast comedy highlight:
Exhausted, the bro shuffles to the kitchen. Another bro appears, silently mouthing
"what's up?" In the exhausted programmer's point of view, above the scene floats the
VS Code menu bar text: 'File Edit Selection View Go Run Terminal Help' like a HUD.

Intertitles connect coding errors to physical comedy, for example:
{breakfast_error_examples}

He tries to "import mil" by pouring milk from a carton labeled "mil", but nothing comes out.
He absent-mindedly tries to eat the spoon and fork instead of breakfast. He opens wrong
cupboards and doors, as intertitles flash:
"File not found."
"Path to fridge not found."
Finally, the friend gently turns him toward the real fridge; success.

80-90s - Quiet resolution:
Cut back to the laptop: the code (inspired by the IDE recorder project) finally runs.
A tiny success animation on screen, like a timeline playing smoothly or a recording icon
turning solid. Final cards:
"AI can help. But the joy is in learning the instrument."
"VS Code + Python. Free. The rest is play."
""".strip()


def collect_files(repo_path: str) -> Dict[str, List[Path]]:
    root = Path(repo_path)
    py_files = list(root.rglob("*.py"))
    doc_files = [
        p
        for p in root.rglob("*.md")
        if "IDE_RECORDER" in p.name or p.name in {"README.md", "INDEX.md"}
    ]
    return {"py": py_files, "docs": doc_files}


def extract_classes_and_functions(py_files: List[Path]) -> List[str]:
    counter: Counter[str] = Counter()
    class_pattern = re.compile(r"^\s*class\s+(\w+)", re.MULTILINE)
    func_pattern = re.compile(r"^\s*def\s+(\w+)", re.MULTILINE)

    for path in py_files:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for name in class_pattern.findall(text) + func_pattern.findall(text):
            if any(fragment in name for fragment in KEY_CLASS_FRAGMENTS):
                counter[name] += 1

    return [name for name, _ in counter.most_common(6)]


def extract_domain_terms(py_files: List[Path], doc_files: List[Path]) -> Tuple[List[str], List[str]]:
    text_blobs: List[str] = []

    for path in (*py_files, *doc_files):
        try:
            text_blobs.append(path.read_text(encoding="utf-8", errors="ignore").lower())
        except OSError:
            continue

    joined = "\n".join(text_blobs)

    verb_counts: Counter[str] = Counter()
    for verb in VERB_KEYWORDS:
        verb_counts[verb] = joined.count(verb)

    verbs = [verb for verb, count in verb_counts.most_common() if count > 0][:6]

    domain_terms: List[str] = []
    for term in DOMAIN_SEEDS:
        if term.split()[0].lower() in joined:
            domain_terms.append(term)

    return verbs, domain_terms


def extract_error_phrases(py_files: List[Path], doc_files: List[Path]) -> List[str]:
    phrases: set[str] = set()

    for path in (*py_files, *doc_files):
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue

        for line in lines:
            lower = line.lower()
            if any(pattern.lower() in lower for pattern in ERROR_PATTERNS):
                stripped = line.strip()
                if len(stripped) > 80:
                    stripped = stripped[:77] + "..."
                if stripped:
                    phrases.add(stripped)

    for canonical in CANONICAL_ERRORS:
        phrases.add(canonical)

    return sorted(phrases)[:5]


def extract_repo_concepts(repo_path: str) -> RepoConcepts:
    files = collect_files(repo_path)
    main_classes = extract_classes_and_functions(files["py"])
    verbs, domain_terms = extract_domain_terms(files["py"], files["docs"])
    error_phrases = extract_error_phrases(files["py"], files["docs"])
    return RepoConcepts(
        main_classes=main_classes,
        verbs=verbs,
        domain_terms=domain_terms,
        error_phrases=error_phrases,
    )


def render_concepts_block(concepts: RepoConcepts) -> str:
    if concepts.main_classes:
        classes = ", ".join(concepts.main_classes)
    else:
        classes = "ScreenRecorder, VideoProcessor, YouTubeUploader, AINarrator"

    if concepts.verbs:
        verbs = ", ".join(concepts.verbs)
    else:
        verbs = "record, process, upload, render"

    if concepts.domain_terms:
        domain = ", ".join(concepts.domain_terms)
    else:
        domain = (
            "screen recording, timelines, events, paths, imports, modules, "
            "uploaders, narrators"
        )

    if concepts.error_phrases:
        errors = ", ".join(concepts.error_phrases)
    else:
        errors = "'ModuleNotFoundError', 'File not found', 'Path not found'"

    return (
        "Concepts drawn from the programmer's actual IDE recorder codebase: "
        f"{domain}. Core components have names like {classes}. "
        f"Typical actions in this world are to {verbs}.\n\n"
        f"Coding errors from this project, such as {errors}, are reimagined as visual gags "
        "in the film: missed paths in the apartment, imports that fail in the kitchen, "
        "and timelines jumping like a jittery film reel."
    )


def select_error_examples(concepts: RepoConcepts) -> Tuple[str, str]:
    if concepts.error_phrases:
        errors = concepts.error_phrases
    else:
        errors = CANONICAL_ERRORS

    debugging = ", ".join(errors[:3])

    breakfast = (
        "When he opens the wrong cupboard, a title card says 'File not found.' "
        "When he stares at the wrong door instead of the fridge, a title card says "
        "'Path not found.' "
        f"His sleepy brain still sees errors like {debugging} hovering above everyday life."
    )

    return debugging, breakfast


def build_prompt_from_repo(repo_path: str) -> str:
    concepts = extract_repo_concepts(repo_path)
    concepts_block = render_concepts_block(concepts)
    debugging_errors, breakfast_errors = select_error_examples(concepts)

    return STORY_TEMPLATE.format(
        concepts_block=concepts_block,
        debugging_error_examples=debugging_errors,
        breakfast_error_examples=breakfast_errors,
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a Sora-style silent-film prompt derived from a Python repo "
            "(e.g., the IDE recorder project)."
        )
    )
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="Path to the root of the repository to analyze.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    prompt = build_prompt_from_repo(args.repo)
    print(prompt)


if __name__ == "__main__":
    main()
