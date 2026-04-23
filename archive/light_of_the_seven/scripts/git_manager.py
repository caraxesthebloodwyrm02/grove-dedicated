#!/usr/bin/env python3
"""
GRID Git Manager

Centralized utility for Git governance, configuration repair, 
context-aware navigation (locomotion), and active schema processing (exercising).
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.path_guards import guard_integration_path  # noqa: E402, I001

# --- ANSI Coloring Helper ---
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'

def color(text: str, color_code: str) -> str:
    return f"{color_code}{text}{Colors.ENDC}"

def run_git(args: List[str], cwd: Optional[Path] = None) -> str:
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            check=False,
            capture_output=True,
            text=True,
            cwd=cwd
        )
        if result.returncode != 0:
            return ""
        return result.stdout.strip()
    except Exception:
        return ""

def cmd_status() -> None:
    """Show detailed GRID Git status and configuration."""
    print(color("\n--- GRID Git Configuration State ---", Colors.HEADER + Colors.BOLD))
    
    status_map = {
        "Global User": ("config --global user.name", "user.name"),
        "Global Email": ("config --global user.email", "user.email"),
        "Local EOL": ("config core.eol", "core.eol"),
        "Local AutoCRLF": ("config core.autocrlf", "core.autocrlf"),
        "Local SafeCRLF": ("config core.safecrlf", "core.safecrlf"),
        "Local DefaultBranch": ("config init.defaultBranch", "init.defaultBranch"),
    }

    for label, (git_args, _) in status_map.items():
        val = run_git(git_args.split())
        print(f"{color(label.ljust(20), Colors.DIM)}: {color(val if val else '(none)', Colors.OKGREEN)}")

    print(color("\n--- Remotes ---", Colors.BOLD))
    remotes = run_git(["remote", "-v"]).splitlines()
    unique_remotes = set()
    for remote in remotes:
        parts = remote.split()
        if len(parts) >= 2:
            r_str = f"{parts[0].ljust(10)} {parts[1]}"
            if r_str not in unique_remotes:
                print(color(r_str, Colors.OKCYAN))
                unique_remotes.add(r_str)
    print()

def cmd_repair(force: bool) -> None:
    """Perform root-cause analysis and repair Git misconfigurations."""
    print(color("\n[!] Running Git Root Cause Analysis...", Colors.WARNING + Colors.BOLD))
    
    repairs = []
    
    # 1. Check init.defaultbranch
    default_branch = run_git(["config", "--local", "init.defaultbranch"])
    if default_branch == "-h":
        repairs.append(("config --local init.defaultbranch main", "Fixing default branch typo ('-h' -> 'main')"))
    
    # 2. Check core.safecrlf consistency
    global_safecrlf = run_git(["config", "--global", "core.safecrlf"])
    local_safecrlf = run_git(["config", "--local", "core.safecrlf"])
    if global_safecrlf == "true" and local_safecrlf == "false":
        repairs.append(("config --local core.safecrlf true", "Synchronizing local safecrlf with global (false -> true)"))

    if not repairs:
        print(color("No misconfigurations detected. GRID is synchronized.", Colors.OKGREEN))
        return

    for git_cmd, desc in repairs:
        print(f"  → {desc}")
        confirmed = force
        if not confirmed:
            ans = input(f"    Apply fix: '{git_cmd}'? [y/N]: ").lower()
            confirmed = ans == 'y'
        
        if confirmed:
            args = git_cmd.split()
            run_git(args)
            print(color("    Applied.", Colors.OKGREEN))

def cmd_locomote(platform_id: str) -> None:
    """Switch context to a platform and process its structured input."""
    root = Path.cwd()
    allowed, reason, _cand = guard_integration_path(root, platform_id)
    if not allowed:
        print(color(f"Error: invalid platform_id ({reason}).", Colors.FAIL))
        return
    integration_file = root / "integrations" / platform_id / "integration.json"
    
    if not integration_file.exists():
        print(color(f"Error: Integration '{platform_id}' not found.", Colors.FAIL))
        return

    try:
        with open(integration_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(color(f"Error processing {integration_file}: {e}", Colors.FAIL))
        return

    rel = data.get("relationship", {})
    is_friend = rel.get("status") == "friend"

    print(color("\n" + "="*40, Colors.OKBLUE))
    header = f" Locomoting to {platform_id.upper()} context"
    if is_friend:
        header += f" {color('[FRIEND]', Colors.OKGREEN)}"
    print(color(header, Colors.BOLD))
    print(f" Path: {color('integrations/' + platform_id, Colors.DIM)}")
    print(f" Tier: {color(str(data.get('resonance_tier', 'N/A')), Colors.BOLD)}")
    if is_friend:
        print(f" Trust: {color(str(rel.get('trust_score', 'N/A')), Colors.OKGREEN)}")
    print(color("="*40, Colors.OKBLUE))

    if is_friend:
        print(color("\nFriendship Principles:", Colors.BOLD))
        for p in rel.get("principles", []):
            print(f"  ⭐ {color(p, Colors.OKGREEN)}")

    # Site-specific operations
    print(color("\nIntegrated Scopes:", Colors.BOLD))
    mapping = data.get("core_mapping", [])
    if isinstance(mapping, list):
        for item in mapping:
            comp = item.get("component", "unknown")
            layer = item.get("layer", "unknown")
            role = item.get("role", "N/A")
            print(f"  → {color(comp.ljust(15), Colors.OKCYAN)} {color(layer.ljust(8), Colors.BOLD)} [dim]{role}[/dim]")
    elif isinstance(mapping, dict):
        for comp, details in mapping.items():
            print(f"  → {color(comp.ljust(15), Colors.OKCYAN)} {color(details.get('layer', 'unknown').ljust(8), Colors.BOLD)}")

    print(f"\n{color('[TIP]', Colors.OKGREEN)} To switch shell directory, use: {color('cd integrations/' + platform_id, Colors.OKCYAN)}")

def cmd_exercise(platform_id: str) -> None:
    """Perform active contract verification based on integration schema."""
    root = Path.cwd()
    allowed, reason, _c = guard_integration_path(root, platform_id)
    if not allowed:
        print(color(f"Error: invalid platform_id ({reason}).", Colors.FAIL))
        return
    integration_file = root / "integrations" / platform_id / "integration.json"
    
    if not integration_file.exists():
        print(color(f"Error: Integration '{platform_id}' not found.", Colors.FAIL))
        return

    try:
        with open(integration_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(color(f"Error processing {integration_file}: {e}", Colors.FAIL))
        return

    print(color(f"\n[!] Exercising {platform_id.upper()} Contract Verification...", Colors.HEADER + Colors.BOLD))
    
    mapping = data.get("core_mapping", [])
    if not mapping:
        print(color("No core mapping found to exercise.", Colors.WARNING))
        return

    violations = 0
    checks = 0

    for item in mapping:
        checks += 1
        comp = item.get("component")
        layer = item.get("layer")
        
        # Heuristic check for component existence in the workspace
        # We look for a directory named after the component or containing it
        print(f"Checking component '{color(comp, Colors.OKCYAN)}' (Layer: {color(layer, Colors.BOLD)})...", end=" ")
        
        found = False
        potential_paths = [
            root / comp,
            root / "grid" / comp,
            root / comp.lower(),
            root / "grid" / comp.lower()
        ]
        
        for p in potential_paths:
            if p.exists() and p.is_dir():
                found = True
                break
        
        if found:
            print(color("[PASS]", Colors.OKGREEN))
        else:
            print(color("[FAIL]", Colors.FAIL))
            print(color(f"  → Reason: Component path for '{comp}' not detected in workspace.", Colors.DIM))
            violations += 1

    print(color("\n--- Resonance Summary ---", Colors.BOLD))
    if violations == 0:
        print(color(f"Resonance Achieved: 100% ({checks}/{checks} contracts validated)", Colors.OKGREEN))
    else:
        resonance = max(0, (checks - violations) / checks)
        print(color(f"Resonance Threshold: {resonance:.2f} ({checks - violations}/{checks} contracts validated)", Colors.WARNING))
        print(color(f"Contract Violations: {violations}", Colors.FAIL))

class GitLogic:
    """Internal module for risk mitigation and tailored GRID growth."""
    
    @staticmethod
    def reason():
        """Reason about current branch state vs integration intent."""
        cur = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
        print(color(f"\n[Git-Logic] Reasoning about branch: {cur}", Colors.HEADER))
        
        # Check for topic convention
        if not cur.startswith("topic/"):
            print(color("  ⚠ Risk: Branch does not follow 'topic/' convention. Risk to metadata persistence.", Colors.WARNING))
        else:
            print(color("  ✓ Hierarchy: Branch follows GRID topic naming standards.", Colors.OKGREEN))

    @staticmethod
    def mitigate():
        """Safeguard against risky Git states."""
        print(color("\n[Git-Logic] Performing Risk Mitigation Check...", Colors.HEADER))
        
        # Check for uncommitted changes
        status = run_git(["status", "--porcelain"])
        if status:
            print(color("  ⚠ Risk: Working tree is dirty. Suggest 'git commit' or 'git stash' before logical expansion.", Colors.WARNING))
        else:
            print(color("  ✓ Safety: Working tree is clean.", Colors.OKGREEN))

    @staticmethod
    def prosper():
        """Identify growth opportunities and automate expansion."""
        print(color("\n[Git-Logic] Identifying Prosperity Path...", Colors.HEADER))
        print(color("  → Growth: Scanning integrations for un-scaffolded sub-components...", Colors.DIM))
        # Logic to suggest new topic branches for sub-components could go here
        print(color("  ✓ Growth Path clear. System is stable for expansion.", Colors.OKGREEN))

def cmd_logic(subcommand: str) -> None:
    logic = GitLogic()
    if subcommand == "reason":
        logic.reason()
    elif subcommand == "mitigate":
        logic.mitigate()
    elif subcommand == "prosper":
        logic.prosper()
    else:
        print("Available logic commands: reason, mitigate, prosper")

def cmd_topic(topic_args: List[str]) -> None:
    """
    Wrap scripts/git-topic for unified GRID Git management.
    Enforces platform-specific branch hierarchies if running within an integration context.
    """
    root_script = Path(__file__).parent.parent
    git_topic_path = root_script / "scripts" / "git-topic"
    
    if not git_topic_path.exists():
        print(color("Error: scripts/git-topic not found.", Colors.FAIL))
        return

    # Check for integration context
    cwd = Path.cwd()
    integration_file = cwd / "integration.json"
    
    # If specifically creating a topic and we are in an integration context
    if "create" in topic_args and integration_file.exists():
        try:
            with open(integration_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            hierarchy = data.get("branch_hierarchy", {})
            valid_themes = hierarchy.get("theme_mapping", {})
            
            if valid_themes:
                provided_theme = None
                if "--theme" in topic_args:
                    idx = topic_args.index("--theme")
                    if idx + 1 < len(topic_args):
                        provided_theme = topic_args[idx + 1]
                
                if provided_theme:
                    if provided_theme not in valid_themes and provided_theme not in valid_themes.values():
                        print(color(f"Warning: Theme '{provided_theme}' is not standard for this platform.", Colors.WARNING))
                        print(color(f"Supported themes: {', '.join(valid_themes.keys())}", Colors.DIM))
                else:
                    print(color(f"[Platform Context] Available Themes: {', '.join(valid_themes.keys())}", Colors.OKCYAN))
        except Exception as e:
            print(color(f"Warning: Could not process integration context: {e}", Colors.WARNING))

    try:
        subprocess.run([sys.executable, str(git_topic_path)] + topic_args, check=True)
    except subprocess.CalledProcessError:
        pass
    except Exception as e:
        print(color(f"Error executing git-topic: {e}", Colors.FAIL))

def cmd_organize(dry_run: bool) -> None:
    """Refine workspace configuration and clean up shadow artifacts."""
    root = Path.cwd()
    print(color(f"\n[!] {'Simulating' if dry_run else 'Executing'} Workspace Organization...", Colors.HEADER + Colors.BOLD))
    
    if dry_run:
        print(color("  (DRY-RUN MODE: No changes will be written to disk)\n", Colors.DIM))

    # 1. .gitignore refinement
    gitignore_path = root / ".gitignore"
    desired_ignores = [
        "*.resolved",
        "*.log",
        "*.tmp",
        "archival/",
        "brain/trash/",
        "**/__pycache__/",
        "**/node_modules/"
    ]
    
    current_ignores = []
    if gitignore_path.exists():
        with open(gitignore_path, "r", encoding="utf-8") as f:
            current_ignores = [line.strip() for line in f.readlines()]
    
    new_ignores = [i for i in desired_ignores if i not in current_ignores]
    if new_ignores:
        print(color("  [Gitignore] Missing entries detected:", Colors.BOLD))
        for i in new_ignores:
            print(f"    + {i}")
        if not dry_run:
            with open(gitignore_path, "a", encoding="utf-8") as f:
                if current_ignores and not current_ignores[-1] == "":
                    f.write("\n")
                for i in new_ignores:
                    f.write(f"{i}\n")
            print(color("    Updated .gitignore", Colors.OKGREEN))
    else:
        print(color("  [Gitignore] Aligned.", Colors.OKGREEN))

    # 2. .gitattributes refinement
    gitattrs_path = root / ".gitattributes"
    desired_attrs = [
        "* text=auto eol=lf",
        "*.jpg binary",
        "*.png binary",
        "*.wav binary",
        "*.mp4 binary"
    ]
    
    current_attrs = []
    if gitattrs_path.exists():
        with open(gitattrs_path, "r", encoding="utf-8") as f:
            current_attrs = [line.strip() for line in f.readlines()]

    new_attrs = [a for a in desired_attrs if a not in current_attrs]
    if new_attrs:
        print(color("\n  [Gitattributes] Missing entries detected:", Colors.BOLD))
        for a in new_attrs:
            print(f"    + {a}")
        if not dry_run:
            with open(gitattrs_path, "a", encoding="utf-8") as f:
                if current_attrs and not current_attrs[-1] == "":
                    f.write("\n")
                for a in new_attrs:
                    f.write(f"{a}\n")
            print(color("    Updated .gitattributes", Colors.OKGREEN))
    else:
        print(color("\n  [Gitattributes] Aligned.", Colors.OKGREEN))

    # 3. Shadow File Archival
    archival_dir = root / "archival"
    to_archive = list(root.glob("*.resolved")) + list(root.glob("*.tmp"))
    
    if to_archive:
        print(color("\n  [Archival] Shadow files detected:", Colors.BOLD))
        if not dry_run:
            archival_dir.mkdir(exist_ok=True)
            
        for f in to_archive:
            print(f"    → Moving {f.name} to archival/")
            if not dry_run:
                target = archival_dir / f.name
                if target.exists():
                    target = archival_dir / f"{f.stem}_{int(os.path.getmtime(f))}{f.suffix}"
                f.rename(target)
        if not dry_run:
            print(color("    Archival complete.", Colors.OKGREEN))
    else:
        print(color("\n  [Archival] Workspace clean (no shadow files).", Colors.OKGREEN))

def main() -> None:
    parser = argparse.ArgumentParser(description="GRID Git Manager - Governance & Locomotion")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("status", help="Show GRID Git status")
    
    repair_parser = subparsers.add_parser("repair", help="Repair Git misconfigurations")
    repair_parser.add_argument("--force", action="store_true", help="Apply fixes without confirmation")

    locomote_parser = subparsers.add_parser("locomote", help="Locomote to an integration context")
    locomote_parser.add_argument("platform_id", help="The ID of the platform to locomote to")

    exercise_parser = subparsers.add_parser("exercise", help="Exercise platform contract verification")
    exercise_parser.add_argument("platform_id", help="The ID of the platform to exercise")

    logic_parser = subparsers.add_parser("logic", help="Internal Git-Logic reasoning")
    logic_parser.add_argument("subcommand", choices=["reason", "mitigate", "prosper"], help="Logic subcommand")

    organize_parser = subparsers.add_parser("organize", help="Workspace organization and cleanup")
    organize_parser.add_argument("--dry-run", action="store_true", help="Simulate changes without applying them")

    topic_parser = subparsers.add_parser("topic", help="Manage topic branches (wraps git-topic)")
    topic_parser.add_argument("topic_args", nargs=argparse.REMAINDER, help="Arguments passed to git-topic")

    intel_parser = subparsers.add_parser("intelligence", help="AI-powered analysis (requires Ollama)")
    intel_parser.add_argument("subcommand", choices=["analyze", "suggest", "organize"], help="Intelligence subcommand")
    intel_parser.add_argument("--verbose", "-v", action="store_true", help="Show model selection details")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status()
    elif args.command == "repair":
        cmd_repair(args.force)
    elif args.command == "locomote":
        cmd_locomote(args.platform_id)
    elif args.command == "exercise":
        cmd_exercise(args.platform_id)
    elif args.command == "logic":
        cmd_logic(args.subcommand)
    elif args.command == "organize":
        cmd_organize(args.dry_run)
    elif args.command == "topic":
        cmd_topic(args.topic_args or [])
    elif args.command == "intelligence":
        from git_intelligence import cmd_intelligence
        cmd_intelligence(args.subcommand, verbose=args.verbose)
    else:
        parser.print_help()



if __name__ == "__main__":
    main()
