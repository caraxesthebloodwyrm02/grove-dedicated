# 🔥 Phase 1: Phoenix Token MVP
## 2-Week Implementation Guide for Emotional Core

---

## 📋 Overview

**Goal**: Deliver a working, emotionally resonant tribute generator in 2 weeks  
**Scope**: 3 core modules, zero external dependencies, 3-step user flow  
**Output**: Personalized markdown token with 3 generated text pieces  
**Timeline**: Week 1 (Foundation) + Week 2 (Integration & Polish)  

---

## 🎯 What You're Building

```
PHOENIX TOKEN MVP
├── Input: User makes 3 personal choices
│   ├── Choice 1: Theme (7 options)
│   ├── Choice 2: Emotion (5 options)
│   └── Choice 3: Character + Location
│
├── Processing: Generate 3 text pieces
│   ├── Tribute (250 words, Ode/Reflection)
│   ├── Vignette (200 words, character moment)
│   └── Prompt (3 sentences, fan-fiction starter)
│
└── Output: Markdown file (Phoenix_Token_[timestamp].md)
    ├── Beautiful formatting
    ├── Shareable content
    └── Personal keepsake
```

---

## 📁 Phase 1 File Structure

```
full_datakit/
├── scripts/
│   └── appreciation_token.py              # Main entry point
│
├── core/
│   ├── narrative_foundation.py            # Themes, quotes, archetypes
│   ├── generative_core.py                 # All 3 generators
│   └── interactive_shell.py               # 3-Step flow + token assembly
│
├── data/
│   └── phoenix_templates.json             # Generator templates
│
└── PHASE_1_PHOENIX_MVP.md                 # This file
```

---

## 🔧 Week 1: Foundation

### Task 1.1: Curate Thematic Core (2 hours)

**Goal**: Define 7 universal themes with emotional weight

**Source**: Extract from `jk_rowling_appreciation.json` → `craft_elements.elements.moral_structure.core_themes`

**Themes to Curate**:
```json
{
  "themes": [
    {
      "id": "choice",
      "name": "Choice Defines Us",
      "description": "We are not defined by circumstances, but by the choices we make",
      "emotional_weight": 9,
      "key_quote": "It is our choices that show what we truly are, far more than our abilities.",
      "narrative_seed": "Harry's choice to sacrifice himself"
    },
    {
      "id": "love",
      "name": "Love as Protection",
      "description": "Love is the most powerful magic—it protects, heals, and transcends death",
      "emotional_weight": 10,
      "key_quote": "Love is the most powerful magic of all.",
      "narrative_seed": "Lily's sacrifice protecting Harry"
    },
    {
      "id": "courage",
      "name": "Courage Despite Fear",
      "description": "True courage is not the absence of fear, but acting despite it",
      "emotional_weight": 8,
      "key_quote": "It takes a great deal of bravery to stand up to our enemies, but just as much to stand up to our friends.",
      "narrative_seed": "Neville standing up at the final battle"
    },
    {
      "id": "friendship",
      "name": "Friendship Sustains",
      "description": "Friendship is the bond that heals wounds and enables heroism",
      "emotional_weight": 8,
      "key_quote": "It is our choices that show what we truly are, far more than our abilities.",
      "narrative_seed": "Harry, Ron, and Hermione's unbreakable bond"
    },
    {
      "id": "prejudice",
      "name": "Standing Against Prejudice",
      "description": "Prejudice is the enemy of truth; standing against it defines character",
      "emotional_weight": 8,
      "key_quote": "It is our choices that show what we truly are, far more than our abilities.",
      "narrative_seed": "Hermione's advocacy for house-elves"
    },
    {
      "id": "growth",
      "name": "Growing Up and Letting Go",
      "description": "Maturity means accepting loss and finding meaning in change",
      "emotional_weight": 7,
      "key_quote": "To the well-organized mind, death is but the next great adventure.",
      "narrative_seed": "Harry's journey from boy to man"
    },
    {
      "id": "belonging",
      "name": "Found Family and Belonging",
      "description": "Family is not just blood—it's the people who choose to stand with you",
      "emotional_weight": 9,
      "key_quote": "You're a wizard, Harry.",
      "narrative_seed": "The Weasleys adopting Harry"
    }
  ]
}
```

**Deliverable**: `phoenix_templates.json` (themes section)

---

### Task 1.2: Build Quote Bank (3 hours)

**Goal**: Curate 50-100 powerful quotes, tagged by theme and emotion

**Source**: Extract from `jk_rowling_appreciation.json` and Harry Potter books

**Structure**:
```json
{
  "quotes": [
    {
      "id": "quote_001",
      "text": "It is our choices that show what we truly are, far more than our abilities.",
      "character": "Dumbledore",
      "book": "Chamber of Secrets",
      "themes": ["choice", "growth"],
      "emotional_tone": "inspiring",
      "emotional_weight": 9
    },
    {
      "id": "quote_002",
      "text": "Love is the most powerful magic of all.",
      "character": "Dumbledore",
      "book": "Philosopher's Stone",
      "themes": ["love"],
      "emotional_tone": "hopeful",
      "emotional_weight": 10
    },
    {
      "id": "quote_003",
      "text": "It takes a great deal of bravery to stand up to our enemies, but just as much to stand up to our friends.",
      "character": "Dumbledore",
      "book": "Philosopher's Stone",
      "themes": ["courage", "friendship"],
      "emotional_tone": "wise",
      "emotional_weight": 8
    }
    // ... 47+ more quotes
  ]
}
```

**Deliverable**: `phoenix_templates.json` (quotes section)

---

### Task 1.3: Define Character Archetypes (2 hours)

**Goal**: Identify 7 key characters with motivations and locations

**Source**: Extract from `jk_rowling_appreciation.json` → `knowledge_blocks.key_characters`

**Structure**:
```json
{
  "archetypes": [
    {
      "id": "harry",
      "name": "Harry Potter",
      "role": "The Reluctant Hero",
      "core_motivation": "Courage, Sacrifice, Love",
      "key_trait": "Willing to die for others",
      "locations": ["Forbidden Forest", "Hogwarts", "Privet Drive", "Gringotts"],
      "vignette_seed": "Harry standing alone, ready to sacrifice"
    },
    {
      "id": "hermione",
      "name": "Hermione Granger",
      "role": "The Brilliant Heart",
      "core_motivation": "Knowledge, Justice, Loyalty",
      "key_trait": "Brilliant mind, compassionate heart",
      "locations": ["Hogwarts Library", "Room of Requirement", "Ministry", "Gringotts"],
      "vignette_seed": "Hermione discovering knowledge that changes everything"
    },
    {
      "id": "dumbledore",
      "name": "Albus Dumbledore",
      "role": "The Wise Mentor",
      "core_motivation": "Wisdom, Redemption, Greater Good",
      "key_trait": "Sees deeply, acts mysteriously",
      "locations": ["Headmaster's Office", "Pensieve", "Astronomy Tower", "Hogwarts"],
      "vignette_seed": "Dumbledore reflecting on choices and consequences"
    },
    {
      "id": "snape",
      "name": "Severus Snape",
      "role": "The Complex Redemption",
      "core_motivation": "Love, Loyalty, Redemption",
      "key_trait": "Lifetime of sacrifice for love",
      "locations": ["Potions Classroom", "Hogwarts", "Spinner's End", "Shrieking Shack"],
      "vignette_seed": "Snape's hidden love and sacrifice revealed"
    },
    {
      "id": "neville",
      "name": "Neville Longbottom",
      "role": "The Unexpected Hero",
      "core_motivation": "Courage, Growth, Belonging",
      "key_trait": "Fear transformed into heroism",
      "locations": ["Hogwarts", "Herbology Greenhouse", "Great Hall", "Room of Requirement"],
      "vignette_seed": "Neville standing up when it matters most"
    },
    {
      "id": "luna",
      "name": "Luna Lovegood",
      "role": "The Wise Outsider",
      "core_motivation": "Truth, Acceptance, Wonder",
      "key_trait": "Sees what others miss",
      "locations": ["Ravenclaw Tower", "Forbidden Forest", "Hogwarts", "Hogsmeade"],
      "vignette_seed": "Luna understanding something profound about the world"
    },
    {
      "id": "rowling",
      "name": "J.K. Rowling",
      "role": "The Creator",
      "core_motivation": "Storytelling, Hope, Healing",
      "key_trait": "Turned personal struggle into universal magic",
      "locations": ["Edinburgh Cafe", "Study", "Hogwarts (imagined)", "Reader's Heart"],
      "vignette_seed": "Rowling writing in a cafe, creating a world of hope"
    }
  ]
}
```

**Deliverable**: `phoenix_templates.json` (archetypes section)

---

### Task 1.4: Create Generator Templates (3 hours)

**Goal**: Define templates for Ode, Vignette, and Prompt generation

**Structure**:
```json
{
  "templates": {
    "ode": {
      "structure": [
        "Opening: Emotional hook tied to theme",
        "Development: 2-3 paragraphs exploring theme through Rowling's work",
        "Reflection: Personal resonance and gratitude",
        "Closing: Powerful final line"
      ],
      "emotional_tones": {
        "hopeful": "Uplifting, forward-looking, inspiring",
        "nostalgic": "Reflective, memory-focused, bittersweet",
        "grateful": "Thankful, acknowledging, warm",
        "awestruck": "Amazed, reverent, profound",
        "intimate": "Personal, vulnerable, honest"
      },
      "word_count": 250,
      "example": "See examples section below"
    },
    "vignette": {
      "structure": [
        "Setting: Establish location and mood",
        "Character: Internal thoughts and feelings",
        "Moment: A single, resonant moment",
        "Reflection: What this moment means"
      ],
      "word_count": 200,
      "example": "See examples section below"
    },
    "prompt": {
      "structure": [
        "Setup: Introduce character and themes",
        "Conflict: What needs to be explored",
        "Question: What should the user write about?"
      ],
      "word_count": "1-3 sentences",
      "example": "See examples section below"
    }
  }
}
```

**Deliverable**: `phoenix_templates.json` (templates section)

---

### Task 1.5: Implement GenerativeCore Class (4 hours)

**File**: `core/generative_core.py`

```python
import json
import random
from pathlib import Path
from typing import Dict, List, Tuple

class GenerativeCore:
    """Generate tribute, vignette, and prompt using templates and data."""
    
    def __init__(self, templates_path: str, appreciation_path: str):
        """Load templates and appreciation data."""
        self.templates = self._load_json(templates_path)
        self.appreciation_data = self._load_json(appreciation_path)
        self.themes = self.templates.get("themes", [])
        self.quotes = self.templates.get("quotes", [])
        self.archetypes = self.templates.get("archetypes", [])
    
    def _load_json(self, path: str) -> Dict:
        """Load JSON file."""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_tribute(self, theme_id: str, emotion: str) -> str:
        """
        Generate a 250-word Ode or Reflection.
        
        Args:
            theme_id: ID of chosen theme
            emotion: Emotional tone (hopeful, nostalgic, grateful, awestruck, intimate)
        
        Returns:
            250-word tribute text
        """
        # Find theme
        theme = next((t for t in self.themes if t["id"] == theme_id), None)
        if not theme:
            return "Theme not found."
        
        # Find relevant quotes
        relevant_quotes = [q for q in self.quotes if theme_id in q.get("themes", [])]
        selected_quote = random.choice(relevant_quotes) if relevant_quotes else None
        
        # Build tribute using template
        tribute = self._build_tribute_from_template(
            theme=theme,
            quote=selected_quote,
            emotion=emotion
        )
        
        return tribute
    
    def generate_vignette(self, character_id: str, location: str) -> str:
        """
        Generate a 200-word character vignette.
        
        Args:
            character_id: ID of chosen character archetype
            location: Location for the vignette
        
        Returns:
            200-word vignette text
        """
        # Find character
        character = next((a for a in self.archetypes if a["id"] == character_id), None)
        if not character:
            return "Character not found."
        
        # Build vignette using template
        vignette = self._build_vignette_from_template(
            character=character,
            location=location
        )
        
        return vignette
    
    def generate_prompt(self, theme1_id: str, theme2_id: str, character_id: str) -> str:
        """
        Generate a fan-fiction starter prompt.
        
        Args:
            theme1_id: First theme ID
            theme2_id: Second theme ID
            character_id: Character ID
        
        Returns:
            1-3 sentence prompt
        """
        theme1 = next((t for t in self.themes if t["id"] == theme1_id), None)
        theme2 = next((t for t in self.themes if t["id"] == theme2_id), None)
        character = next((a for a in self.archetypes if a["id"] == character_id), None)
        
        if not (theme1 and theme2 and character):
            return "Invalid selection."
        
        # Build prompt
        prompt = self._build_prompt_from_template(
            theme1=theme1,
            theme2=theme2,
            character=character
        )
        
        return prompt
    
    def _build_tribute_from_template(self, theme: Dict, quote: Dict, emotion: str) -> str:
        """Build tribute using template and data."""
        # This is a simplified version; actual implementation would be more sophisticated
        tribute = f"""
# {theme['name']}

{theme['description']}

"{quote['text']}" — {quote['character']}, {quote['book']}

J.K. Rowling understood that {theme['name'].lower()} is not abstract—it's lived, 
felt, and expressed through the choices of ordinary people in extraordinary circumstances.

Through her work, she taught us that {theme['description'].lower()}.

This is why her stories matter. This is why we are grateful.
        """
        return tribute.strip()
    
    def _build_vignette_from_template(self, character: Dict, location: str) -> str:
        """Build vignette using template and data."""
        vignette = f"""
# A Moment with {character['name']}

In {location}, {character['name']} paused. The weight of everything—
every choice, every sacrifice, every moment of courage—settled on their shoulders.

But there was something else too. A quiet knowing that they were not alone.
That friendship, love, and the choices they'd made meant something.

{character['name']} looked around and understood: this moment, this place, 
this feeling—this was what it meant to be alive. To matter. To belong.

And in that understanding, they found peace.
        """
        return vignette.strip()
    
    def _build_prompt_from_template(self, theme1: Dict, theme2: Dict, character: Dict) -> str:
        """Build prompt using template and data."""
        prompt = f"""
Write a short story about {character['name']} exploring the themes of 
'{theme1['name']}' and '{theme2['name']}'. What would they discover? 
How would these themes shape their journey?
        """
        return prompt.strip()
```

**Deliverable**: Working `GenerativeCore` class with 3 generator methods

---

## 🔨 Week 2: Integration & Polish

### Task 2.1: Implement InteractiveShell Class (3 hours)

**File**: `core/interactive_shell.py`

```python
from pathlib import Path
from datetime import datetime
from generative_core import GenerativeCore

class InteractiveShell:
    """3-Step Tribute Flow and Token Assembly."""
    
    def __init__(self, generative_core: GenerativeCore):
        self.core = generative_core
        self.user_choices = {}
    
    def run_tribute_flow(self) -> str:
        """Execute the 3-step flow: Anchor → Resonate → Create."""
        print("\n" + "="*60)
        print("🔥 THE PHOENIX TOKEN: A PERSONAL TRIBUTE")
        print("="*60)
        print("\nIn three steps, create your personal token of appreciation.\n")
        
        # Step 1: Anchor
        self._step_anchor()
        
        # Step 2: Resonate
        self._step_resonate()
        
        # Step 3: Create
        self._step_create()
        
        # Assemble and save token
        token_content = self._assemble_token()
        token_path = self._save_token(token_content)
        
        return token_path
    
    def _step_anchor(self):
        """Step 1: User selects theme and emotion."""
        print("STEP 1: ANCHOR - Finding Your Core")
        print("-" * 40)
        print("What theme resonates most with you?\n")
        
        themes = self.core.themes
        for i, theme in enumerate(themes, 1):
            print(f"{i}. {theme['name']}")
            print(f"   {theme['description']}\n")
        
        choice = int(input("Choose (1-7): ")) - 1
        self.user_choices['theme_id'] = themes[choice]['id']
        
        print("\nWhat emotion best describes your appreciation?\n")
        emotions = ["hopeful", "nostalgic", "grateful", "awestruck", "intimate"]
        for i, emotion in enumerate(emotions, 1):
            print(f"{i}. {emotion}")
        
        choice = int(input("Choose (1-5): ")) - 1
        self.user_choices['emotion'] = emotions[choice]
    
    def _step_resonate(self):
        """Step 2: User selects character and location."""
        print("\n\nSTEP 2: RESONATE - A Moment in the World")
        print("-" * 40)
        print("Which character speaks to you?\n")
        
        archetypes = self.core.archetypes
        for i, archetype in enumerate(archetypes, 1):
            print(f"{i}. {archetype['name']} - {archetype['role']}")
        
        choice = int(input("Choose (1-7): ")) - 1
        character = archetypes[choice]
        self.user_choices['character_id'] = character['id']
        
        print(f"\nWhere would you find {character['name']}?\n")
        for i, location in enumerate(character['locations'], 1):
            print(f"{i}. {location}")
        
        choice = int(input("Choose (1-4): ")) - 1
        self.user_choices['location'] = character['locations'][choice]
    
    def _step_create(self):
        """Step 3: Generate fan-fiction prompt."""
        print("\n\nSTEP 3: CREATE - The Final Spark")
        print("-" * 40)
        print("Your fan-fiction prompt is being generated...\n")
        
        # Select two random themes
        theme1 = self.core.themes[0]
        theme2 = self.core.themes[1]
        self.user_choices['theme1_id'] = theme1['id']
        self.user_choices['theme2_id'] = theme2['id']
    
    def _assemble_token(self) -> str:
        """Assemble the three generated pieces into a token."""
        tribute = self.core.generate_tribute(
            self.user_choices['theme_id'],
            self.user_choices['emotion']
        )
        
        vignette = self.core.generate_vignette(
            self.user_choices['character_id'],
            self.user_choices['location']
        )
        
        prompt = self.core.generate_prompt(
            self.user_choices['theme1_id'],
            self.user_choices['theme2_id'],
            self.user_choices['character_id']
        )
        
        token = f"""# The Phoenix Token: A Tribute

## I. Core Reflection
{tribute}

## II. A Resonant Moment
{vignette}

## III. The Spark of Creation
{prompt}

---

*Created on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} in gratitude.*
"""
        return token
    
    def _save_token(self, content: str) -> Path:
        """Save token to markdown file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Phoenix_Token_{timestamp}.md"
        filepath = Path.cwd() / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✨ Token saved to: {filepath}")
        return filepath
```

**Deliverable**: Working `InteractiveShell` class with 3-step flow

---

### Task 2.2: Create Main Entry Point (1 hour)

**File**: `scripts/appreciation_token.py`

```python
#!/usr/bin/env python3
"""
Phoenix Token: Personal Tribute to J.K. Rowling
A 2-week MVP for emotional appreciation generation.
"""

import sys
from pathlib import Path

# Add parent directory to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.generative_core import GenerativeCore
from core.interactive_shell import InteractiveShell

def main():
    """Main entry point."""
    # Load data
    templates_path = PROJECT_ROOT / "data" / "phoenix_templates.json"
    appreciation_path = PROJECT_ROOT / "data" / "jk_rowling_appreciation.json"
    
    # Initialize system
    core = GenerativeCore(str(templates_path), str(appreciation_path))
    shell = InteractiveShell(core)
    
    # Run tribute flow
    token_path = shell.run_tribute_flow()
    
    print(f"\n🔥 Your Phoenix Token is ready!")
    print(f"📄 Saved to: {token_path}")
    print("\nShare your token with others and celebrate the magic of storytelling.")

if __name__ == "__main__":
    main()
```

**Deliverable**: Working entry point script

---

### Task 2.3: Refine Generator Output (3 hours)

**Goal**: Improve template-based generation for emotional quality

**Actions**:
- [ ] Refine Ode templates with better prose
- [ ] Enhance Vignette templates with sensory details
- [ ] Improve Prompt templates for creativity
- [ ] Add variation to prevent repetition
- [ ] Test output quality with sample runs

**Deliverable**: High-quality generator output

---

### Task 2.4: User Testing (3 hours)

**Goal**: Test with 5 users, gather feedback

**Test Script**:
1. Run: `python scripts/appreciation_token.py`
2. Complete 3-step flow
3. Review generated token
4. Answer feedback questions:
   - Did the tribute feel emotionally resonant? (1-10)
   - Was the vignette compelling? (1-10)
   - Would you share this token? (Yes/No)
   - What could be improved?

**Deliverable**: User feedback report

---

### Task 2.5: Documentation (2 hours)

**Create**:
- `PHASE_1_README.md` - How to run and use
- `PHASE_1_EXAMPLES.md` - Sample outputs
- `PHASE_1_ARCHITECTURE.md` - Technical overview

**Deliverable**: Complete documentation

---

## 📊 Phase 1 Deliverables Checklist

### Data & Templates
- [ ] `phoenix_templates.json` with:
  - [ ] 7 themes (with descriptions, quotes, emotional weight)
  - [ ] 50-100 curated quotes (tagged by theme)
  - [ ] 7 character archetypes (with locations)
  - [ ] Generator templates (Ode, Vignette, Prompt)

### Code
- [ ] `core/generative_core.py` (GenerativeCore class)
- [ ] `core/interactive_shell.py` (InteractiveShell class)
- [ ] `scripts/appreciation_token.py` (Main entry point)

### Testing & Feedback
- [ ] 5+ user tests completed
- [ ] Feedback documented
- [ ] Output quality refined

### Documentation
- [ ] `PHASE_1_README.md`
- [ ] `PHASE_1_EXAMPLES.md`
- [ ] `PHASE_1_ARCHITECTURE.md`

---

## 🎯 Success Criteria

- ✅ MVP runs without errors
- ✅ 3-step flow is intuitive
- ✅ Generated output is emotionally resonant (9/10)
- ✅ Zero external dependencies
- ✅ User satisfaction: 8.5/10
- ✅ Code is clean and documented
- ✅ Ready for Phase 2 enhancement

---

## 🚀 Launch

**When**: End of Week 2  
**How**: `python scripts/appreciation_token.py`  
**Output**: `Phoenix_Token_[timestamp].md`  
**Time to Complete**: 5-10 minutes  

---

## 📈 Phase 2 Readiness

After Phase 1 completion, you'll be ready to add:
- Interactive visualizations
- Semantic dimension mapping
- Advanced exploration modes
- Learning modules and challenges

All without breaking Phase 1 functionality.

---

**Status**: Phase 1 Plan Complete ✅  
**Ready to Implement**: Yes ✅  
**Timeline**: 2 weeks  
**Quality Target**: 9/10 emotional resonance
