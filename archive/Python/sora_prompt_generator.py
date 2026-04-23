"""
sora_prompt_generator.py - Cost-optimized Sora prompt generation from repository.

Extracts programming concepts from the IDE Recorder codebase and generates a
Chaplin-inspired silent-film prompt for Sora 2, with cost optimization strategies.

Architecture:
  1. RepoAnalyzer    - Scans repo for class names, errors, concepts
  2. ConceptMapper   - Maps programming terms to physical comedy metaphors
  3. StoryTemplate   - Modular story structure with injection points
  4. PromptOptimizer - Reduces token count while maintaining clarity
  5. SoraClient      - Handles API calls with budget tracking
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class TokenBudgetLevel(Enum):
    """Cost optimization levels for API budget."""

    ULTRA_LOW = 1500  # ~$0.15 - minimal prompt
    LOW = 2500        # ~$0.25 - lean but complete
    MEDIUM = 3500     # ~$0.35 - balanced
    STANDARD = 5000   # ~$0.50 - full quality


@dataclass
class RepositoryConcepts:
    """Extracted concepts from codebase."""

    classes: "list[str]" = field(default_factory=list)
    key_methods: "list[str]" = field(default_factory=list)
    error_patterns: "list[str]" = field(default_factory=list)
    file_names: "list[str]" = field(default_factory=list)
    docstring_themes: "list[str]" = field(default_factory=list)
    core_metaphors: "list[str]" = field(default_factory=list)

    @property
    def summary(self) -> str:
        """Generate concise summary of concepts."""
        concepts_str = ", ".join(self.core_metaphors[:3])
        errors_str = ", ".join(self.error_patterns[:2])
        return f"Core: {concepts_str}. Errors: {errors_str}."


@dataclass
class MetaphorMapping:
    """Maps programming concept to visual comedy gag."""

    concept: str
    technical_term: str
    physical_gag: str
    timing_seconds: float
    visual_card: Optional[str] = None

    def to_prompt_fragment(self) -> str:
        """Convert to prompt snippet."""
        return f"'{self.technical_term}' visual metaphor: {self.physical_gag}"


class RepoAnalyzer:
    """Extracts programming concepts from repository."""

    def __init__(self, repo_path: Path):
        """Initialize analyzer.

        Args:
            repo_path: Root path to repository.
        """
        self.repo_path = Path(repo_path)
        self.concepts = RepositoryConcepts()

    def analyze(self) -> RepositoryConcepts:
        """Scan repository and extract concepts.

        Returns:
            RepositoryConcepts instance.
        """
        logger.info("Analyzing repository: %s", self.repo_path)

        # Scan Python files
        self._extract_classes()
        self._extract_methods()
        self._extract_errors()
        self._extract_file_names()
        self._extract_themes()
        self._infer_metaphors()

        logger.info("Extracted %d classes, %d error patterns",
                   len(self.concepts.classes), len(self.concepts.error_patterns))

        return self.concepts

    def _extract_classes(self) -> None:
        """Extract class names from Python files."""
        class_pattern = re.compile(r"^class\s+(\w+)\s*[:\(]", re.MULTILINE)

        for py_file in self.repo_path.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")
                matches = class_pattern.findall(content)
                self.concepts.classes.extend(matches)
            except (IOError, UnicodeDecodeError):
                pass

        # Deduplicate and keep top 6
        self.concepts.classes = list(dict.fromkeys(self.concepts.classes))[:6]

    def _extract_methods(self) -> None:
        """Extract common method names."""
        method_pattern = re.compile(r"def\s+(\w+)\s*\(", re.MULTILINE)
        method_count: dict[str, int] = {}

        for py_file in self.repo_path.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")
                matches = method_pattern.findall(content)
                for m in matches:
                    method_count[m] = method_count.get(m, 0) + 1
            except (IOError, UnicodeDecodeError):
                pass

        # Get top recurring methods
        sorted_methods = sorted(method_count.items(), key=lambda x: x[1], reverse=True)
        self.concepts.key_methods = [m[0] for m in sorted_methods[:4]]

    def _extract_errors(self) -> None:
        """Extract common error patterns from comments and code."""
        error_patterns = [
            "ModuleNotFoundError",
            "ImportError",
            "FileNotFoundError",
            "PathNotFound",
            "AttributeError",
            "TypeError",
            "ValueError",
        ]

        for py_file in self.repo_path.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")
                for pattern in error_patterns:
                    if pattern in content:
                        self.concepts.error_patterns.append(pattern)
            except (IOError, UnicodeDecodeError):
                pass

        self.concepts.error_patterns = list(dict.fromkeys(self.concepts.error_patterns))[:3]

    def _extract_file_names(self) -> None:
        """Extract significant file names."""
        significant_files = [
            "config", "events", "recorder", "timeline", "narrator",
            "video_processor", "uploader", "cli"
        ]

        for py_file in self.repo_path.rglob("*.py"):
            stem = py_file.stem
            if any(sig in stem for sig in significant_files):
                self.concepts.file_names.append(stem)

        self.concepts.file_names = list(dict.fromkeys(self.concepts.file_names))[:5]

    def _extract_themes(self) -> None:
        """Extract themes from docstrings."""
        docstring_pattern = re.compile(r'"""(.*?)"""', re.DOTALL)
        theme_keywords = {
            "record": "recording",
            "track": "tracking",
            "generate": "generation",
            "process": "processing",
            "upload": "uploading",
            "narration": "narration",
            "stream": "streaming",
            "cache": "caching",
        }

        found_themes: set[str] = set()

        for py_file in self.repo_path.rglob("*.py"):
            try:
                content = py_file.read_text(encoding="utf-8")
                for match in docstring_pattern.finditer(content):
                    docstring = match.group(1).lower()
                    for keyword, theme in theme_keywords.items():
                        if keyword in docstring:
                            found_themes.add(theme)
            except (IOError, UnicodeDecodeError):
                pass

        self.concepts.docstring_themes = list(found_themes)[:4]

    def _infer_metaphors(self) -> None:
        """Infer core metaphors from extracted data."""
        # Build metaphor list from concepts
        metaphor_keywords = {
            "record": "recording tape that plays backward",
            "track": "following a trail of breadcrumbs",
            "timeline": "film strip fragments in wrong order",
            "event": "things happening too fast to catch",
            "path": "getting lost in apartment hallways",
            "upload": "uploading thoughts into a cloud",
            "narrator": "inner voice narrating everything",
            "import": "importing physical objects",
        }

        for concept in (self.concepts.classes + self.concepts.file_names):
            concept_lower = concept.lower()
            for keyword, metaphor in metaphor_keywords.items():
                if keyword in concept_lower:
                    self.concepts.core_metaphors.append(metaphor)

        self.concepts.core_metaphors = list(dict.fromkeys(self.concepts.core_metaphors))[:4]


class ConceptMapper:
    """Maps programming concepts to visual comedy metaphors."""

    CONCEPT_TO_GAG_MAP = {
        "ModuleNotFoundError": MetaphorMapping(
            concept="missing_module",
            technical_term="ModuleNotFoundError",
            physical_gag="searching through apartment for a module that doesn't exist, "
                        "opening cupboards, finding nothing",
            timing_seconds=4.5,
            visual_card="MODULE NOT FOUND"
        ),
        "FileNotFoundError": MetaphorMapping(
            concept="missing_file",
            technical_term="FileNotFoundError",
            physical_gag="frantically looking for a file on desk covered in papers, "
                        "papers flying everywhere",
            timing_seconds=3.0,
            visual_card="FILE NOT FOUND"
        ),
        "PathNotFound": MetaphorMapping(
            concept="lost_path",
            technical_term="Path not found",
            physical_gag="walking down hallway, opening many wrong doors, "
                        "path-not-found sign appears, friend points correct direction",
            timing_seconds=5.0,
            visual_card="PATH TO FRIDGE NOT FOUND"
        ),
        "import_mil": MetaphorMapping(
            concept="import_milk",
            technical_term="import mil",
            physical_gag="tries to pour milk from carton labeled 'mil', nothing comes out, "
                        "squeezes and shakes it in desperation",
            timing_seconds=4.0,
            visual_card="import mil"
        ),
        "ImportError": MetaphorMapping(
            concept="import_error",
            technical_term="ImportError",
            physical_gag="trying to import things into hands that are already full, "
                        "dropping everything",
            timing_seconds=3.5,
            visual_card="IMPORT ERROR"
        ),
        "record": MetaphorMapping(
            concept="recording",
            technical_term="ScreenRecorder",
            physical_gag="coffee cup that refills in reverse, playing film strip backward",
            timing_seconds=2.5,
            visual_card=None
        ),
        "timeline": MetaphorMapping(
            concept="timeline",
            technical_term="TimelineManager",
            physical_gag="shuffling through film strips in wrong order, trying to organize them",
            timing_seconds=3.0,
            visual_card="TIMELINE INVALID"
        ),
    }

    @staticmethod
    def get_metaphor(concept: str) -> Optional[MetaphorMapping]:
        """Get metaphor for concept.

        Args:
            concept: Programming concept.

        Returns:
            MetaphorMapping or None.
        """
        return ConceptMapper.CONCEPT_TO_GAG_MAP.get(concept)

    @classmethod
    def map_concepts_to_gags(
        cls,
        concepts: "RepositoryConcepts",
        max_gags: int = 3
    ) -> "list[MetaphorMapping]":
        """Map extracted concepts to visual gags.

        Args:
            concepts: Extracted repository concepts.
            max_gags: Maximum number of gags to include.

        Returns:
            List of metaphor mappings.
        """
        gags: "list[MetaphorMapping]" = []

        # Always include key errors as 70% breakfast segment
        error_gag_keys = ["PathNotFound", "import_mil", "ImportError"]
        for key in error_gag_keys:
            if key in cls.CONCEPT_TO_GAG_MAP:
                gags.append(cls.CONCEPT_TO_GAG_MAP[key])
                if len(gags) >= max_gags:
                    break

        return gags


class StoryTemplate:
    """Modular story structure with injection points."""

    # Template uses {variable} syntax for injection
    TEMPLATE = """\
Black and white silent-film style short (90 seconds). Inspired by Charlie Chaplin.

**SCENE 1: Title & Myth (0–15s)**
Opening intertitle card:
"{myth_quote}"

Visuals: Young programmer bro staring at laptop screen, AI chat window visible, 
closes it dismissively. Only the {first_error} error message briefly visible.

---

**SCENE 2: Fast Setup (15–40s)**
Intertitle: "Free editor. Free language. Just curiosity."

Montage of icons and installation screens:
- VS Code logo appears and magnifies
- Python snake icon downloads, spins
- File system folders open and close
- Menu bar visualization: "File Edit Selection View Go Run Terminal Help" 

Quick piano music builds. Bro sits down at desk, opens laptop. Blank editor.

---

**SCENE 3: First Coding & Debugging (40–60s)**
Screen shows tiny Python script being typed. Terminal flashes errors in rapid succession:
- "{first_error}"
- "{second_error}"
- "{third_error}"

Intertitle cards appear between shots:
- "Module not found."
- "Path not found."
- "Try again."

Bro sighs deeply, head in hands, dramatic rubbing of temples. 
Repeats typing. Still errors. Throws hands up.

---

**SCENE 4: BREAKFAST COMEDY / 70% HIGHLIGHT (60–80s)**
[This is where {breakfast_gag} happens]

Bro stumbles away from desk, shuffles to kitchen exhausted. 

Another bro enters silently, tilts head quizzically. 
Intertitle: "What's up?"

**In the exhausted programmer's POV**: floating above everything, 
the VS Code menu bar appears, overlaid on reality:
"File Edit Selection View Go Run Terminal Help"

**Comedy sequence (no dialogue, only visuals + title cards):**

1. Intertitle: "import mil"
   Bro tries to pour milk from a carton labeled "mil". Nothing comes out. 
   Squeezes harder. Still nothing. Shakes violently.

2. Intertitle: "{path_not_found_card}"
   Bro opens wrong cupboards repeatedly: wrong doors, wrong shelves.
   Friend shakes head in background.

3. Intertitle: "FILE NOT FOUND" 
   Bro looks at fork and spoon, tries to eat them instead of picking up actual food.

4. Friend gently guides bro to the *real* fridge. Opens it. 
   Sudden sunlight glow. Milk bottle clearly labeled. Success.

Both stand in kitchen. Bro blinks. Nods slowly. Recovery.

---

**SCENE 5: Quiet Resolution (80–90s)**
Cut back to VS Code. 
The script now runs. Small success animation on screen—a green checkmark pulses.

Final intertitle card:
"AI can help. But the joy is in learning the instrument."

Final card:
"{closing_tagline}"

Screen fades to black. Piano music resolves. 
Title appears: "VS Code + Python. Free. The rest is play."

---

**VISUAL STYLE & TONE:**
- Black and white throughout
- Silent (no dialogue whatsoever)
- Piano-only soundtrack, reminiscent of 1920s Chaplin films
- Exaggerated physical comedy, slapstick without cruelty
- Endearing protagonist—bro is likeable, just overwhelmed
- Technical errors become physical obstacles
- Lighting: high contrast, dramatic shadows
- Props: modern laptop + VS Code UI superimposed, vintage apartment furniture
- Pacing: rapid during debug montage, slow and tender in kitchen scene
"""

    @staticmethod
    def render(
        myth_quote: str,
        first_error: str,
        second_error: str,
        third_error: str,
        breakfast_gag: str,
        path_not_found_card: str,
        closing_tagline: str,
    ) -> str:
        """Render story template with injected values.

        Args:
            myth_quote: Opening myth about AI.
            first_error: First error message.
            second_error: Second error message.
            third_error: Third error message.
            breakfast_gag: Description of breakfast comedy.
            path_not_found_card: Card text for path not found.
            closing_tagline: Final tagline.

        Returns:
            Rendered story.
        """
        return StoryTemplate.TEMPLATE.format(
            myth_quote=myth_quote,
            first_error=first_error,
            second_error=second_error,
            third_error=third_error,
            breakfast_gag=breakfast_gag,
            path_not_found_card=path_not_found_card,
            closing_tagline=closing_tagline,
        )


class PromptOptimizer:
    """Reduces token count while maintaining prompt clarity."""

    # Aggressive compression dictionary
    COMPRESSION_RULES = {
        "Black and white silent-film style short": "B&W silent film",
        "Charlie Chaplin": "Chaplin-esque",
        "intertitle card": "card",
        "VS Code menu bar": "menu bar",
        "programmer bro": "bro",
        "visual metaphor": "metaphor",
        "repeatedly": "repeat",
        "desperately": "desperate",
        "dramatically": "dramatic",
    }

    @staticmethod
    def compress_prompt(prompt: str, target_budget: TokenBudgetLevel) -> str:
        """Compress prompt to fit token budget.

        Args:
            prompt: Full prompt text.
            target_budget: Target token budget level.

        Returns:
            Compressed prompt.
        """
        logger.info("Compressing prompt to %d tokens", target_budget.value)

        # Apply compression rules iteratively
        for verbose, concise in PromptOptimizer.COMPRESSION_RULES.items():
            prompt = prompt.replace(verbose, concise)

        # Remove excessive detail comments
        prompt = re.sub(r"---\n+", "\n", prompt)

        # Remove redundant section headers if too long
        if len(prompt) > target_budget.value * 4:  # ~4 chars per token
            prompt = re.sub(r"\*\*SCENE \d+:.*?\n", "SCENE: ", prompt)

        # Truncate descriptions if still over budget
        estimated_tokens = len(prompt) // 4
        if estimated_tokens > target_budget.value:
            # Keep key visual and story elements, cut descriptive text
            lines = prompt.split("\n")
            kept_lines = [l for l in lines if any(
                keyword in l.lower()
                for keyword in ["metaphor", "intertitle", "visuals:", "bro", "kitchen"]
            )]
            prompt = "\n".join(kept_lines)

        return prompt

    @staticmethod
    def estimate_tokens(prompt: str) -> int:
        """Estimate token count (rough: 1 token ≈ 4 chars).

        Args:
            prompt: Prompt text.

        Returns:
            Estimated token count.
        """
        return len(prompt) // 4


class SoraPromptGenerator:
    """Orchestrates full pipeline: repo analysis → prompt generation."""

    def __init__(
        self,
        repo_path: Path,
        budget: TokenBudgetLevel = TokenBudgetLevel.LOW,
    ):
        """Initialize generator.

        Args:
            repo_path: Path to repository.
            budget: Token budget level.
        """
        self.repo_path = Path(repo_path)
        self.budget = budget
        self.concepts: Optional[RepositoryConcepts] = None
        self.gags: list[MetaphorMapping] = []

    def generate(self) -> str:
        """Generate optimized Sora prompt from repository.

        Returns:
            Ready-to-use Sora prompt string.
        """
        logger.info("Starting prompt generation pipeline")

        # Step 1: Analyze repository
        analyzer = RepoAnalyzer(self.repo_path)
        self.concepts = analyzer.analyze()

        logger.info("Concepts: %s", self.concepts.summary)

        # Step 2: Map to comedy gags
        self.gags = ConceptMapper.map_concepts_to_gags(self.concepts, max_gags=3)
        logger.info("Mapped %d gags from concepts", len(self.gags))

        # Step 3: Render story template with injected values
        story = self._render_story()

        # Step 4: Optimize for token budget
        optimized = PromptOptimizer.compress_prompt(story, self.budget)

        # Step 5: Add final Sora-specific directives
        final_prompt = self._add_sora_directives(optimized)

        estimated = PromptOptimizer.estimate_tokens(final_prompt)
        logger.info("Generated prompt: %d estimated tokens (budget: %d)",
                   estimated, self.budget.value)

        return final_prompt

    def _render_story(self) -> str:
        """Render story template with extracted concepts."""
        errors = self.concepts.error_patterns if self.concepts.error_patterns else [
            "ModuleNotFoundError", "FileNotFoundError", "ImportError"
        ]

        gag_descriptions = [g.physical_gag for g in self.gags]
        breakfast_gag = gag_descriptions[0] if gag_descriptions else "mysterious kitchen adventure"

        return StoryTemplate.render(
            myth_quote="They said: no need to learn coding. The machines will do it all.",
            first_error=errors[0] if len(errors) > 0 else "ModuleNotFoundError",
            second_error=errors[1] if len(errors) > 1 else "FileNotFoundError",
            third_error=errors[2] if len(errors) > 2 else "ImportError",
            breakfast_gag=breakfast_gag,
            path_not_found_card="PATH TO FRIDGE NOT FOUND",
            closing_tagline="Learning to code is play. Start with VS Code + Python. Free.",
        )

    def _add_sora_directives(self, prompt: str) -> str:
        """Add Sora 2 specific generation directives.

        Args:
            prompt: Base prompt.

        Returns:
            Prompt with Sora directives.
        """
        sora_header = """\
[SORA 2 GENERATION SETTINGS]
Duration: 90 seconds
Aspect Ratio: 16:9
Style: Black and white, high-contrast silent film (1920s Chaplin era)
Music: Piano soundtrack only, vintage
Resolution: 1080p minimum

[KEY VISUAL CONSTRAINTS]
- NO dialogue or voiceover (completely silent except piano)
- Typography: Use period-appropriate intertitle cards
- Lighting: High contrast, dramatic shadows
- Setting: Modern small apartment mixed with vintage furniture aesthetic
- Props: Laptop with VS Code UI elements superimposed on reality
- Color: Strictly black and white, no color grading

[PERFORMANCE NOTES]
- Main actor: Likeable, endearing male protagonist (20s-30s)
- Supporting: Second male character (friend) who provides silent guidance
- Physical comedy style: Slapstick with heart (Chaplin-inspired)
- Pacing: Rapid during technical sequences, slow and tender in kitchen
- Emotional arc: Frustration → exhaustion → gentle humor → triumph

[TONE]
Funny around 70% mark (breakfast kitchen sequence). Affectionate toward both 
coding and the beginner's journey. Inviting, not mocking.
"""

        return sora_header + "\n" + prompt


def build_prompt_from_repo(
    repo_path: str | Path,
    budget: TokenBudgetLevel = TokenBudgetLevel.LOW,
) -> str:
    """Generate Sora prompt from repository (main entry point).

    Args:
        repo_path: Path to repository.
        budget: Token budget level (for cost optimization).

    Returns:
        Ready-to-use Sora 2 prompt.
    """
    generator = SoraPromptGenerator(Path(repo_path), budget=budget)
    return generator.generate()


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    repo_path = Path("e:/projects/python/hello")

    print("=" * 70)
    print("SORA PROMPT GENERATOR - IDE RECORDER REPO")
    print("=" * 70)

    prompt = build_prompt_from_repo(repo_path, budget=TokenBudgetLevel.LOW)

    print("\n" + "=" * 70)
    print("GENERATED PROMPT")
    print("=" * 70)
    print(prompt)

    tokens = PromptOptimizer.estimate_tokens(prompt)
    print(f"\nEstimated tokens: {tokens} / {TokenBudgetLevel.LOW.value}")
    print(f"Budget remaining: {TokenBudgetLevel.LOW.value - tokens} tokens")
