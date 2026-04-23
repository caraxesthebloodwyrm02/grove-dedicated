#!/usr/bin/env python3
"""
Git-Intelligence Module

AI-powered analysis and governance for GRID repositories.
Uses Ollama for local LLM inference with dynamic model selection.
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List


class OllamaClient:
    """Client for Ollama LLM API."""
    
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.base_url = base_url or os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.2")
    
    def generate(self, prompt: str, model: Optional[str] = None) -> str:
        """Generate text using Ollama CLI."""
        target_model = model or self.model
        try:
            result = subprocess.run(
                ["ollama", "run", target_model, prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return f"[Error] Ollama returned: {result.stderr}"
        except FileNotFoundError:
            return "[Error] Ollama not installed. Run: curl https://ollama.ai/install.sh | sh"
        except subprocess.TimeoutExpired:
            return "[Error] Ollama request timed out."
        except Exception as e:
            return f"[Error] {e}"
    
    def is_available(self) -> bool:
        """Check if Ollama is available."""
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, timeout=5)
            return result.returncode == 0
        except Exception:
            return False


class ComplexityEstimator:
    """Estimate task complexity for dynamic model selection."""
    
    # Complexity weights
    WEIGHTS = {
        "file_count": 0.3,
        "line_count": 0.3,
        "file_types": 0.2,
        "diff_size": 0.2
    }
    
    # Model tiers
    MODELS = {
        "low": "llama3.2:1b",      # 1-3: Simple tasks
        "medium": "llama3.2",      # 4-6: Standard analysis
        "high": "codellama:13b",   # 7-9: Complex reasoning
        "cloud": "gpt-4"           # 10+: Cloud fallback
    }
    
    @classmethod
    def estimate(cls, diff_output: str, staged_files: List[str]) -> int:
        """Estimate complexity score (1-10)."""
        score = 0
        
        # File count factor
        file_count = len(staged_files)
        if file_count <= 3:
            score += 1
        elif file_count <= 10:
            score += 3
        else:
            score += 5
        
        # Diff size factor
        diff_lines = len(diff_output.splitlines())
        if diff_lines <= 50:
            score += 1
        elif diff_lines <= 200:
            score += 3
        else:
            score += 5
        
        return min(score, 10)
    
    @classmethod
    def select_model(cls, complexity: int) -> str:
        """Select model based on complexity."""
        if complexity <= 3:
            return cls.MODELS["low"]
        elif complexity <= 6:
            return cls.MODELS["medium"]
        elif complexity <= 9:
            return cls.MODELS["high"]
        else:
            return cls.MODELS["cloud"]


class GitIntelligence:
    """Main intelligence class for Git operations."""
    
    def __init__(self, verbose: bool = False):
        self.client = OllamaClient()
        self.verbose = verbose
        self.root = Path.cwd()
    
    def _run_git(self, args: List[str]) -> str:
        """Run a git command and return output."""
        try:
            result = subprocess.run(
                ["git"] + args,
                capture_output=True,
                text=True,
                cwd=self.root
            )
            return result.stdout.strip()
        except Exception:
            return ""
    
    def analyze(self) -> Dict[str, Any]:
        """Analyze current branch changes with AI."""
        # Get diff
        diff = self._run_git(["diff", "--staged"])
        if not diff:
            diff = self._run_git(["diff"])
        
        if not diff:
            return {"status": "clean", "message": "No changes to analyze."}
        
        # Get staged files
        staged = self._run_git(["diff", "--cached", "--name-only"]).splitlines()
        
        # Estimate complexity
        complexity = ComplexityEstimator.estimate(diff, staged)
        model = ComplexityEstimator.select_model(complexity)
        
        if self.verbose:
            print(f"[Intelligence] Complexity: {complexity}/10, Model: {model}")
        
        # Build prompt
        prompt = f"""Analyze this git diff and provide:
1. Risk assessment (low/medium/high)
2. Summary of changes
3. Suggested actions

Diff:
{diff[:2000]}"""  # Truncate for token limits
        
        response = self.client.generate(prompt, model)
        
        return {
            "status": "analyzed",
            "complexity": complexity,
            "model": model,
            "analysis": response
        }
    
    def suggest(self) -> Dict[str, Any]:
        """Generate commit message and branch suggestions."""
        staged = self._run_git(["diff", "--cached", "--name-only"]).splitlines()
        diff = self._run_git(["diff", "--cached"])
        
        if not staged:
            return {"status": "empty", "message": "No staged changes."}
        
        complexity = ComplexityEstimator.estimate(diff, staged)
        model = ComplexityEstimator.select_model(complexity)
        
        prompt = f"""Based on these staged changes, suggest:
1. A conventional commit message (type: description)
2. A topic branch name (topic/theme-short)

Files: {', '.join(staged[:10])}
Diff summary: {len(diff.splitlines())} lines changed"""
        
        response = self.client.generate(prompt, model)
        
        return {
            "status": "suggested",
            "files": staged,
            "complexity": complexity,
            "suggestions": response
        }
    
    def organize(self, dry_run: bool = True) -> Dict[str, Any]:
        """AI-driven workspace organization suggestions."""
        # Get untracked files
        untracked = self._run_git(["ls-files", "--others", "--exclude-standard"]).splitlines()
        
        if not untracked:
            return {"status": "clean", "message": "No untracked files."}
        
        prompt = f"""Analyze these untracked files and suggest:
1. Which should be added to .gitignore
2. Which should be committed
3. Which should be archived

Files:
{chr(10).join(untracked[:30])}"""
        
        response = self.client.generate(prompt)
        
        return {
            "status": "suggestions",
            "dry_run": dry_run,
            "untracked_count": len(untracked),
            "suggestions": response
        }


def cmd_intelligence(subcommand: str, verbose: bool = False) -> None:
    """Execute intelligence subcommands."""
    intel = GitIntelligence(verbose=verbose)
    
    if not intel.client.is_available():
        print("[!] Ollama not available. Install: curl https://ollama.ai/install.sh | sh")
        return
    
    if subcommand == "analyze":
        result = intel.analyze()
        print(f"\n[Git-Intelligence] Analysis (Complexity: {result.get('complexity', 'N/A')})")
        print(result.get("analysis", result.get("message", "No output")))
    
    elif subcommand == "suggest":
        result = intel.suggest()
        print("\n[Git-Intelligence] Suggestions")
        print(result.get("suggestions", result.get("message", "No output")))
    
    elif subcommand == "organize":
        result = intel.organize()
        print("\n[Git-Intelligence] Organization Suggestions")
        print(result.get("suggestions", result.get("message", "No output")))
    
    else:
        print("Usage: git_intelligence.py [analyze|suggest|organize]")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        verbose = "--verbose" in sys.argv or "-v" in sys.argv
        subcmd = [arg for arg in sys.argv[1:] if not arg.startswith("-")][0]
        cmd_intelligence(subcmd, verbose=verbose)
    else:
        print("Usage: python git_intelligence.py [analyze|suggest|organize] [--verbose]")
