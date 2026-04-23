# Grid Intelligent File Organizer Workflow
---
name: grid-intelligent-organizer
description: Semantic-aware file organization workflow with git context understanding
version: 1.0.0
author: Grid Team
triggers:
  - manual
  - on_file_change
tags:
  - organization
  - semantic
  - git-aware
---

# Grid Intelligent File Organizer Workflow

> **Purpose**: Intelligently organize project files using semantic analysis, git history patterns, and content fingerprinting to maintain a clean, navigable codebase.

## Overview

This workflow analyzes your project structure through multiple lenses:
1. **Git Context** - Understanding work patterns and file relationships
2. **Semantic Analysis** - Categorizing files by purpose, not just extension
3. **Content Fingerprinting** - Detecting duplicates and related files
4. **Co-change Patterns** - Files that evolve together should stay together

---

## Start Phase - Context Gathering

name: grid-intelligent-organizer
description: Semantic-aware file organization workflow with git context understanding
version: 1.0.0

## Start Phase - Context Gathering

### Step 1: Git Session Context
```bash
# Get current branch and recent activity
git branch --show-current
git log --oneline -20 --all
git status --porcelain
git diff --name-status HEAD~5 HEAD 2>/dev/null || git diff --name-status --cached

# Get file change frequency (hot files)
git log --pretty=format: --name-only --since="7 days ago" | sort | uniq -c | sort -rn | head -20

# Understand work session timeline
git log --format="%ai %s" --since="24 hours ago"
```

### Step 2: Project Structure Analysis
```bash
# Map current directory structure with metadata
find . -type f -not -path '*/\.*' -printf '%T@ %s %p\n' | sort -rn | head -100

# Get file extensions distribution
find . -type f -not -path '*/\.*' | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Identify existing folder semantics
find . -type d -not -path '*/\.*' -maxdepth 3 | while read dir; do
  echo "=== $dir ==="
  ls -la "$dir" 2>/dev/null | head -5
done
```

### Step 3: File Content Fingerprinting
```python
import os
import hashlib
import json
from datetime import datetime
from pathlib import Path
import ast
import re

class SemanticFileAnalyzer:
    """Analyzes files for semantic properties beyond name matching."""

    MODALITY_MAP = {
        # Code
        '.py': {'modality': 'code', 'language': 'python', 'category': 'backend'},
        '.js': {'modality': 'code', 'language': 'javascript', 'category': 'frontend'},
        '.ts': {'modality': 'code', 'language': 'typescript', 'category': 'frontend'},
        '.java': {'modality': 'code', 'language': 'java', 'category': 'backend'},
        '.go': {'modality': 'code', 'language': 'go', 'category': 'backend'},
        '.rs': {'modality': 'code', 'language': 'rust', 'category': 'systems'},
        '.cpp': {'modality': 'code', 'language': 'cpp', 'category': 'systems'},
        '.c': {'modality': 'code', 'language': 'c', 'category': 'systems'},
        '.sh': {'modality': 'code', 'language': 'shell', 'category': 'scripts'},
        '.bash': {'modality': 'code', 'language': 'bash', 'category': 'scripts'},

        # Documentation
        '.md': {'modality': 'docs', 'format': 'markdown', 'category': 'documentation'},
        '.rst': {'modality': 'docs', 'format': 'restructured', 'category': 'documentation'},
        '.txt': {'modality': 'docs', 'format': 'plaintext', 'category': 'documentation'},
        '.pdf': {'modality': 'docs', 'format': 'pdf', 'category': 'documentation'},

        # Config
        '.yaml': {'modality': 'config', 'format': 'yaml', 'category': 'configuration'},
        '.yml': {'modality': 'config', 'format': 'yaml', 'category': 'configuration'},
        '.json': {'modality': 'config', 'format': 'json', 'category': 'configuration'},
        '.toml': {'modality': 'config', 'format': 'toml', 'category': 'configuration'},
        '.ini': {'modality': 'config', 'format': 'ini', 'category': 'configuration'},
        '.env': {'modality': 'config', 'format': 'env', 'category': 'secrets'},

        # Data
        '.csv': {'modality': 'data', 'format': 'csv', 'category': 'tabular'},
        '.parquet': {'modality': 'data', 'format': 'parquet', 'category': 'tabular'},
        '.sql': {'modality': 'data', 'format': 'sql', 'category': 'database'},
        '.db': {'modality': 'data', 'format': 'sqlite', 'category': 'database'},

        # Assets
        '.png': {'modality': 'asset', 'format': 'image', 'category': 'visual'},
        '.jpg': {'modality': 'asset', 'format': 'image', 'category': 'visual'},
        '.svg': {'modality': 'asset', 'format': 'vector', 'category': 'visual'},
        '.ico': {'modality': 'asset', 'format': 'icon', 'category': 'visual'},

        # Tests
        '_test.py': {'modality': 'test', 'language': 'python', 'category': 'testing'},
        '.test.js': {'modality': 'test', 'language': 'javascript', 'category': 'testing'},
        '.spec.ts': {'modality': 'test', 'language': 'typescript', 'category': 'testing'},
    }

    SEMANTIC_PATTERNS = {
        'model': r'(class\s+\w*Model|Schema|Entity|@dataclass|BaseModel)',
        'service': r'(class\s+\w*Service|@service|def\s+\w*_service)',
        'controller': r'(class\s+\w*Controller|@router|@app\.(get|post|put|delete))',
        'repository': r'(class\s+\w*Repository|class\s+\w*DAO|@repository)',
        'utility': r'(def\s+\w*util|class\s+\w*Utils?|helper|common)',
        'config': r'(settings|config|\.env|SECRET|API_KEY|DATABASE_URL)',
        'test': r'(def\s+test_|class\s+Test|@pytest|unittest|describe\(|it\()',
        'migration': r'(alembic|migration|upgrade|downgrade|revision)',
        'api': r'(endpoint|route|handler|request|response|REST|GraphQL)',
        'cli': r'(argparse|click|typer|sys\.argv|if\s+__name__)',
    }

    def __init__(self, root_path: str = '.'):
        self.root_path = Path(root_path)
        self.file_index = {}
        self.folder_semantics = {}

    def analyze_file(self, filepath: Path) -> dict:
        """Extract semantic properties from a file."""
        stat = filepath.stat()
        ext = filepath.suffix.lower()

        properties = {
            'path': str(filepath),
            'name': filepath.name,
            'stem': filepath.stem,
            'extension': ext,
            'size_bytes': stat.st_size,
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'modality': self.MODALITY_MAP.get(ext, {}).get('modality', 'unknown'),
            'category': self.MODALITY_MAP.get(ext, {}).get('category', 'unknown'),
            'semantic_tags': [],
            'content_hash': None,
            'imports': [],
            'exports': [],
            'dependencies': [],
        }

        # Content analysis for text files
        if self._is_text_file(filepath):
            try:
                content = filepath.read_text(encoding='utf-8', errors='ignore')
                properties['content_hash'] = hashlib.md5(content.encode()).hexdigest()[:12]
                properties['line_count'] = len(content.splitlines())
                properties['semantic_tags'] = self._extract_semantic_tags(content, ext)

                if ext == '.py':
                    properties.update(self._analyze_python(content))
                elif ext in ['.js', '.ts']:
                    properties.update(self._analyze_javascript(content))
                elif ext == '.md':
                    properties.update(self._analyze_markdown(content))

            except Exception as e:
                properties['analysis_error'] = str(e)

        return properties

    def _is_text_file(self, filepath: Path) -> bool:
        """Check if file is likely text-based."""
        text_extensions = {'.py', '.js', '.ts', '.md', '.txt', '.yaml', '.yml',
                          '.json', '.toml', '.ini', '.sh', '.bash', '.sql', '.css',
                          '.html', '.xml', '.rst', '.go', '.rs', '.java', '.c', '.cpp'}
        return filepath.suffix.lower() in text_extensions

    def _extract_semantic_tags(self, content: str, ext: str) -> list:
        """Extract semantic tags based on content patterns."""
        tags = []
        for tag, pattern in self.SEMANTIC_PATTERNS.items():
            if re.search(pattern, content, re.IGNORECASE):
                tags.append(tag)
        return tags

    def _analyze_python(self, content: str) -> dict:
        """Deep analysis of Python files."""
        result = {'imports': [], 'classes': [], 'functions': [], 'decorators': []}
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    result['imports'].extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        result['imports'].append(node.module)
                elif isinstance(node, ast.ClassDef):
                    result['classes'].append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    result['functions'].append(node.name)
        except SyntaxError:
            pass
        return result

    def _analyze_javascript(self, content: str) -> dict:
        """Analyze JavaScript/TypeScript files."""
        result = {'imports': [], 'exports': []}
        import_pattern = r"(?:import|require)\s*\(?['\"]([^'\"]+)['\"]"
        export_pattern = r"export\s+(?:default\s+)?(?:class|function|const|let|var)\s+(\w+)"

        result['imports'] = re.findall(import_pattern, content)
        result['exports'] = re.findall(export_pattern, content)
        return result

    def _analyze_markdown(self, content: str) -> dict:
        """Analyze Markdown documentation."""
        result = {'headers': [], 'links': [], 'code_blocks': []}
        result['headers'] = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        result['links'] = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        result['code_blocks'] = re.findall(r'```(\w+)?', content)
        return result

    def build_index(self) -> dict:
        """Build complete semantic index of project."""
        for filepath in self.root_path.rglob('*'):
            if filepath.is_file() and not any(p.startswith('.') for p in filepath.parts):
                self.file_index[str(filepath)] = self.analyze_file(filepath)
        return self.file_index
```

### Step 4: Git History Integration
```python
class GitHistoryAnalyzer:
    """Analyzes git history to understand file relationships and work patterns."""

    def __init__(self, repo_path: str = '.'):
        self.repo_path = Path(repo_path)

    def get_file_commit_history(self, filepath: str, limit: int = 50) -> list:
        """Get commit history for a specific file."""
        import subprocess
        try:
            result = subprocess.run(
                ['git', 'log', f'-{limit}', '--pretty=format:%H|%ai|%s', '--', filepath],
                capture_output=True, text=True, cwd=self.repo_path
            )
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('|', 2)
                    if len(parts) == 3:
                        commits.append({
                            'hash': parts[0],
                            'date': parts[1],
                            'message': parts[2]
                        })
            return commits
        except Exception:
            return []

    def get_co_changed_files(self, filepath: str, limit: int = 20) -> dict:
        """Find files that are frequently changed together with the given file."""
        import subprocess
        try:
            result = subprocess.run(
                ['git', 'log', f'-{limit}', '--pretty=format:%H', '--', filepath],
                capture_output=True, text=True, cwd=self.repo_path
            )
            commits = result.stdout.strip().split('\n')

            co_changes = {}
            for commit in commits:
                if not commit:
                    continue
                files_result = subprocess.run(
                    ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', commit],
                    capture_output=True, text=True, cwd=self.repo_path
                )
                for f in files_result.stdout.strip().split('\n'):
                    if f and f != filepath:
                        co_changes[f] = co_changes.get(f, 0) + 1

            return dict(sorted(co_changes.items(), key=lambda x: x[1], reverse=True)[:20])
        except Exception:
            return {}

    def get_file_authors(self, filepath: str) -> dict:
        """Get authors who have contributed to a file."""
        import subprocess
        try:
            result = subprocess.run(
                ['git', 'shortlog', '-sne', '--', filepath],
                capture_output=True, text=True, cwd=self.repo_path
            )
            authors = {}
            for line in result.stdout.strip().split('\n'):
                if line:
                    match = re.match(r'\s*(\d+)\s+(.+)', line)
                    if match:
                        authors[match.group(2)] = int(match.group(1))
            return authors
        except Exception:
            return {}

    def get_recent_activity_clusters(self, days: int = 7) -> dict:
        """Identify clusters of files modified together recently."""
        import subprocess
        try:
            result = subprocess.run(
                ['git', 'log', f'--since={days} days ago', '--pretty=format:%H'],
                capture_output=True, text=True, cwd=self.repo_path
            )
            commits = result.stdout.strip().split('\n')

            clusters = []
            for commit in commits:
                if not commit:
                    continue
                files_result = subprocess.run(
                    ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', commit],
                    capture_output=True, text=True, cwd=self.repo_path
                )
                files = [f for f in files_result.stdout.strip().split('\n') if f]
                if len(files) > 1:
                    clusters.append(set(files))

            return {'clusters': clusters, 'total_commits': len(commits)}
        except Exception:
            return {'clusters': [], 'total_commits': 0}

    def get_branch_context(self) -> dict:
        """Get current branch context and related information."""
        import subprocess
        try:
            branch = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True, text=True, cwd=self.repo_path
            ).stdout.strip()

            description = subprocess.run(
                ['git', 'config', f'branch.{branch}.description'],
                capture_output=True, text=True, cwd=self.repo_path
            ).stdout.strip()

            upstream = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', f'{branch}@{{upstream}}'],
                capture_output=True, text=True, cwd=self.repo_path
            ).stdout.strip()

            return {
                'current_branch': branch,
                'description': description or None,
                'upstream': upstream or None,
            }
        except Exception:
            return {'current_branch': 'unknown', 'description': None, 'upstream': None}
```


```python
class OrganizationEngine:
    """Engine for organizing files based on semantic analysis and git context."""

    def __init__(self, root_path: str = '.'):
        self.root_path = Path(root_path)
        self.analyzer = SemanticFileAnalyzer(root_path)
        self.git_analyzer = GitHistoryAnalyzer(root_path)

    def suggest_organization(self) -> dict:
        """Generate organization suggestions based on analysis."""
        file_index = self.analyzer.build_index()
        branch_context = self.git_analyzer.get_branch_context()

        suggestions = {
            'moves': [],
            'groups': [],
            'duplicates': [],
            'orphans': [],
        }

        # Group files by category
        categories = {}
        for filepath, props in file_index.items():
            cat = props.get('category', 'unknown')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(filepath)

        # Detect potential duplicates by content hash
        hashes = {}
        for filepath, props in file_index.items():
            h = props.get('content_hash')
            if h:
                if h not in hashes:
                    hashes[h] = []
                hashes[h].append(filepath)

        for h, files in hashes.items():
            if len(files) > 1:
                suggestions['duplicates'].append(files)

        # Suggest groupings based on semantic tags
        tag_groups = {}
        for filepath, props in file_index.items():
            for tag in props.get('semantic_tags', []):
                if tag not in tag_groups:
                    tag_groups[tag] = []
                tag_groups[tag].append(filepath)

        suggestions['groups'] = [
            {'tag': tag, 'files': files}
            for tag, files in tag_groups.items()
            if len(files) > 1
        ]

        return suggestions

    def execute_organization(self, plan: dict, dry_run: bool = True) -> list:
        """Execute an organization plan."""
        actions = []
        for move in plan.get('moves', []):
            src = Path(move['from'])
            dst = Path(move['to'])
            if dry_run:
                actions.append(f"[DRY RUN] Would move {src} -> {dst}")
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                src.rename(dst)
                actions.append(f"Moved {src} -> {dst}")
        return actions


def main():
    """Main entry point for the organization workflow."""
    import argparse

    parser = argparse.ArgumentParser(description='Grid Intelligent File Organizer')
    parser.add_argument('--root', default='.', help='Root path to analyze')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done')
    parser.add_argument('--output', default='organization_report.json', help='Output report file')
    args = parser.parse_args()

    engine = OrganizationEngine(args.root)

    print("Analyzing project structure...")
    suggestions = engine.suggest_organization()

    print(f"\nFound {len(suggestions['duplicates'])} potential duplicate groups")
    print(f"Found {len(suggestions['groups'])} semantic groupings")

    # Output report
    with open(args.output, 'w') as f:
        json.dump(suggestions, f, indent=2)
    print(f"\nReport written to {args.output}")


if __name__ == '__main__':
    main()
```
