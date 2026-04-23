# Storytime Explorer Workflow

name: Storytime Explorer
description: Explore directories like worlds in a universe, narrating discoveries as an unfolding story

---

## Session Setup

Set the scene for our exploration adventure:

```yaml
session:
  title: "Chronicle of the Code Realm"
  vibe: "curious_adventurer"
  narrator_style: "fantasy_storyteller"
  exploration_depth: "deep"
```

---

## The Journey Begins

1. **Survey the Realm** - Map the top-level territories
   - List all directories as "kingdoms" or "regions"
   - Note any mysterious artifacts (config files, READMEs)

2. **Chronicle Each Discovery**
   - Describe folders as locations (forests, castles, dungeons)
   - Describe files as inhabitants, treasures, or ancient scrolls
   - Note relationships between modules as alliances or trade routes

3. **Narrative Summary Format**
   ```
   📖 Chapter [N]: [Directory Name]
   
   "Upon entering the [folder] realm, the explorer discovered..."
   
   🏰 Landmarks: [subfolders]
   📜 Scrolls Found: [files with descriptions]
   🔗 Connections: [imports/dependencies as story links]
   ⚡ Magic Detected: [special patterns, configs, or notable code]
   
   "And so the tale continues deeper into..."
   ```

---

## Exploration Commands

| Action | Story Element |
|--------|---------------|
| `cd` into folder | "Venturing forth into..." |
| `ls` contents | "The explorer surveys the landscape..." |
| Read file | "Unrolling an ancient scroll reveals..." |
| Find pattern | "Searching for traces of..." |
| Summarize | "The chronicler notes in the margins..." |

---

## Story Briefing Template

At session end, produce:

```
═══════════════════════════════════════
📚 THE EXPLORER'S JOURNAL
═══════════════════════════════════════

🗺️ Realms Visited: [count] territories
📜 Scrolls Examined: [count] files
⏱️ Journey Duration: [time]

📖 TALE SUMMARY:
[2-3 paragraph narrative of what was found, 
written as an adventure story]

🎯 KEY DISCOVERIES:
- [Important file/pattern as plot point]
- [Architecture insight as world-building detail]
- [TODO/issue as quest hook]

🔮 PATHS YET UNEXPLORED:
- [Unvisited directories as mysterious lands]

"And so the chronicle awaits its next chapter..."
═══════════════════════════════════════
```

---

## Invocation

To begin: "Let us embark upon the exploration of [directory]. Chronicle our journey!"

To summarize: "Scribe, prepare the briefing of our adventures thus far."
