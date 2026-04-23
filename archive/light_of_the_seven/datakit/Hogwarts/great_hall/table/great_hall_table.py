#!/usr/bin/env python3
"""
Great Hall Table Builder
Reads a JSONL stream of Great Hall events and produces:
- outputs/discussion_table.csv
- outputs/receipt.json
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

class TableBuilder:
    def __init__(self):
        self.session: Dict[str, Any] = {}
        self.rows: List[Dict[str, Any]] = []
        self.criteria: Dict[str, Dict[str, Any]] = {}
        self.options: Dict[str, Dict[str, Any]] = {}
        self.decisions: Dict[str, Dict[str, Any]] = {}
        self.actions: Dict[str, Dict[str, Any]] = {}
        self.settings: Dict[str, Any] = {}
        self.milestones: List[Dict[str, Any]] = []

    def process_line(self, line: str):
        if not line.strip():
            return
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            print(f"Warning: Skipping invalid JSON line: {line[:50]}...", file=sys.stderr)
            return

        etype = event.get("type")
        payload = event.get("payload", {})
        ts = event.get("at", "")

        # Inject timestamp into payload for easier usage if missing
        if "at" not in payload:
            payload["at_"] = ts

        if etype == "session":
            self.session = payload
        elif etype == "row":
            self.rows.append(payload)
        elif etype == "criteria":
            cid = payload.get("id")
            if cid: self.criteria[cid] = payload
        elif etype == "option":
            oid = payload.get("id")
            if oid: self.options[oid] = payload
        elif etype == "decision":
            did = payload.get("decision_id")
            if did: self.decisions[did] = payload
        elif etype == "action":
            aid = payload.get("action_id")
            if aid: self.actions[aid] = payload
        elif etype == "setting":
            key = payload.get("key")
            if key: self.settings[key] = payload
        elif etype == "milestone":
            self.milestones.append(payload)

    def _resolve_speaker(self, speaker_id: str) -> str:
        # Look up in session participants
        participants = self.session.get("participants", [])
        for p in participants:
            if p.get("id") == speaker_id:
                return p.get("display_name", speaker_id)
        return speaker_id

    def _resolve_criteria_names(self, cids: List[str]) -> str:
        names = []
        for cid in cids:
            c = self.criteria.get(cid)
            if c:
                names.append(c.get("name", cid))
            else:
                names.append(cid)
        return "; ".join(names)

    def _resolve_option_labels(self, oids: List[str]) -> str:
        labels = []
        for oid in oids:
            o = self.options.get(oid)
            if o:
                labels.append(o.get("label", oid))
            else:
                labels.append(oid)
        return "; ".join(labels)

    def write_csv(self, outpath: Path):
        fieldnames = [
            "row_id", "at", "speaker", "kind", "content", "tone_tag",
            "criteria_touched", "options_referenced",
            "decision_ref", "action_ref"
        ]

        with open(outpath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for row in self.rows:
                # Resolve references
                speaker_id = row.get("speaker_id", "")
                speaker_name = self._resolve_speaker(speaker_id)

                c_ids = row.get("criteria_touched", [])
                o_ids = row.get("option_refs", [])

                decision_id = row.get("decision_ref")
                decision_str = ""
                if decision_id:
                    d = self.decisions.get(decision_id)
                    if d:
                        decision_str = f"{d.get('title')} ({d.get('status')})"
                    else:
                        decision_str = decision_id

                action_id = row.get("action_ref")
                action_str = ""
                if action_id:
                    a = self.actions.get(action_id)
                    if a:
                        action_str = f"{a.get('title')} (Owner: {self._resolve_speaker(a.get('owner_id'))})"
                    else:
                        action_str = action_id

                record = {
                    "row_id": row.get("row_id"),
                    "at": row.get("at_") or row.get("at") or "", # Fallback if 'at' is in payload or injected
                    "speaker": speaker_name,
                    "kind": row.get("kind"),
                    "content": row.get("content"),
                    "tone_tag": row.get("tone_tag"),
                    "criteria_touched": self._resolve_criteria_names(c_ids),
                    "options_referenced": self._resolve_option_labels(o_ids),
                    "decision_ref": decision_str,
                    "action_ref": action_str
                }
                writer.writerow(record)
        print(f"Wrote CSV to {outpath}")

    def write_receipt(self, outpath: Path):
        # Construct summary object
        receipt = {
            "session": {
                "id": self.session.get("session_id"),
                "title": self.session.get("title"),
                "participants_count": len(self.session.get("participants", [])),
            },
            "stats": {
                "rows_count": len(self.rows),
                "decisions_count": len(self.decisions),
                "actions_count": len(self.actions)
            },
            "decisions": list(self.decisions.values()),
            "actions": list(self.actions.values()),
            "outstanding_questions": [r for r in self.rows if r.get("kind") == "question"]
        }

        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(receipt, f, indent=2)
        print(f"Wrote receipt to {outpath}")

    def write_json_table(self, outpath: Path):
        table_rows: List[Dict[str, Any]] = []

        for row in self.rows:
            speaker_id = row.get("speaker_id", "")
            speaker_name = self._resolve_speaker(speaker_id)

            c_ids = row.get("criteria_touched", [])
            if not isinstance(c_ids, list):
                c_ids = []

            o_ids = row.get("option_refs", [])
            if not isinstance(o_ids, list):
                o_ids = []

            criteria_names: List[str] = []
            for cid in c_ids:
                c = self.criteria.get(cid)
                criteria_names.append(c.get("name", cid) if c else cid)

            option_labels: List[str] = []
            for oid in o_ids:
                o = self.options.get(oid)
                option_labels.append(o.get("label", oid) if o else oid)

            decision_id = row.get("decision_ref") or ""
            decision_title = ""
            decision_status = ""
            decision_bridge_used = ""
            if decision_id:
                d = self.decisions.get(decision_id)
                if d:
                    decision_title = d.get("title") or ""
                    decision_status = d.get("status") or ""
                    decision_bridge_used = d.get("bridge_used") or ""
                else:
                    decision_title = decision_id

            action_id = row.get("action_ref") or ""
            action_title = ""
            action_owner_id = ""
            action_owner = ""
            action_due_at = ""
            action_status = ""
            if action_id:
                a = self.actions.get(action_id)
                if a:
                    action_title = a.get("title") or ""
                    action_owner_id = a.get("owner_id") or ""
                    action_owner = self._resolve_speaker(action_owner_id) if action_owner_id else ""
                    action_due_at = a.get("due_at") or ""
                    action_status = a.get("status") or ""
                else:
                    action_title = action_id

            decision_ref = ""
            if decision_id:
                if decision_status:
                    decision_ref = f"{decision_title} ({decision_status})"
                else:
                    decision_ref = decision_title

            action_ref = ""
            if action_id:
                if action_title and action_owner:
                    action_ref = f"{action_title} (Owner: {action_owner})"
                else:
                    action_ref = action_title

            table_rows.append(
                {
                    "row_id": row.get("row_id"),
                    "at": row.get("at_") or row.get("at") or "",
                    "speaker_id": speaker_id,
                    "speaker": speaker_name,
                    "kind": row.get("kind"),
                    "content": row.get("content"),
                    "tone_tag": row.get("tone_tag"),
                    "criteria_ids": c_ids,
                    "criteria_names": criteria_names,
                    "criteria_touched": "; ".join(criteria_names),
                    "option_ids": o_ids,
                    "option_labels": option_labels,
                    "options_referenced": "; ".join(option_labels),
                    "decision_id": decision_id,
                    "decision_title": decision_title,
                    "decision_status": decision_status,
                    "bridge_used": decision_bridge_used,
                    "decision_ref": decision_ref,
                    "action_id": action_id,
                    "action_title": action_title,
                    "action_owner_id": action_owner_id,
                    "action_owner": action_owner,
                    "action_due_at": action_due_at,
                    "action_status": action_status,
                    "action_ref": action_ref,
                }
            )

        with open(outpath, "w", encoding="utf-8") as f:
            json.dump(table_rows, f, indent=2, ensure_ascii=False)
        print(f"Wrote JSON table to {outpath}")

def main():
    parser = argparse.ArgumentParser(description="Great Hall Table Builder")
    parser.add_argument("--input", required=True, help="Input JSONL file")
    parser.add_argument("--outdir", required=True, help="Output directory")

    args = parser.parse_args()

    input_path = Path(args.input)
    out_dir = Path(args.outdir)

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)

    builder = TableBuilder()

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            builder.process_line(line)

    builder.write_csv(out_dir / "discussion_table.csv")
    builder.write_json_table(out_dir / "discussion_table.json")
    builder.write_receipt(out_dir / "receipt.json")

if __name__ == "__main__":
    main()
