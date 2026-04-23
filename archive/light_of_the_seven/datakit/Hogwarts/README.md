# Hogwarts Visualization & Parseltongue CLI

## Integration Point: Story Research & Character Discovery Sessions

This toolkit supports structured work sessions for deep-dive exploration into:

- **Founder Studies** – e.g., Salazar Slytherin's origins, motivations, and legacy
- **Character Arc Discovery** – tracing emotional beats and pivotal moments
- **Story Point Mapping** – identifying narrative anchors across timelines
- **Lore Evolution Tracking** – documenting how characters/concepts evolved

### Session Workflow

1. **Select Focus** – Choose a character or theme (e.g., `salazar_slytherin.md`)
2. **Research Phase** – Read lore docs, cross-reference `hogwarts_lore.json`
3. **Discovery Logging** – Note new story points, contradictions, or insights
4. **Temporal Anchoring** – Use `TemporalPatronus` presets to model character moments
5. **Synthesis** – Update docs or create new narrative chapters

This directory contains a small, self-contained Hogwarts "lab" that
combines code, lore documents, and tests. The centerpiece is a
Parseltongue-themed CLI that models a **Temporal Patronus** and ties
into narrative chapters about Severus Snape and Salazar Slytherin.

All code uses only the Python standard library.

---

## YouTube Upload + Automation (OAuth)

This section documents a safe, production-minded approach for integrating this project with YouTube (uploading lore videos, attaching thumbnails, scheduled publishing, and basic monitoring).

This is intentionally optional and separate from the core Hogwarts lab (which stays stdlib-only). The YouTube upload path requires third-party libraries and Google Cloud credentials.

### OAuth flow (refresh tokens, token rotation)

- Use OAuth for an "installed app" (desktop) flow so you can obtain a long-lived **refresh token**.
- Most implementations persist OAuth state to a `token.json` file.
  - Expect **rotation**: the file contents can change over time (token refresh, re-consent, scope changes).
  - Handle `invalid_grant` by triggering a re-auth flow and regenerating the token file.

### Secure token storage posture

- Do not commit `client_secret.json`, `token.json`, or any exported tokens.
- Keep `client_secret.json` outside the repo (or generate it at runtime from environment variables / secret stores).
- Prefer storing tokens in:
  - OS keychain / credential manager, or
  - an encrypted secret store (Vault, 1Password CLI, Windows Credential Manager), or
  - a restricted-permissions file location (least preferred).

### Scopes (least privilege)

- For uploads and thumbnail setting, use `https://www.googleapis.com/auth/youtube.upload`.
- If you also list videos/playlists, use `https://www.googleapis.com/auth/youtube.readonly` where possible.
- Avoid broad scopes (e.g. full account scopes) unless you have a concrete need.

### Minimal Python upload example

Dependencies (install separately from this project):
- `google-api-python-client`
- `google-auth-oauthlib`
- `google-auth-httplib2`

This snippet demonstrates:
- OAuth token persistence
- **resumable** upload for large files
- separate thumbnail upload endpoint

```python
from __future__ import annotations

from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def get_creds(client_secret_path: Path, token_path: Path) -> Credentials:
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        if creds and creds.valid:
            return creds

    flow = InstalledAppFlow.from_client_secrets_file(str(client_secret_path), SCOPES)
    creds = flow.run_local_server(port=0)
    token_path.write_text(creds.to_json(), encoding="utf-8")
    return creds


def upload_video(
    youtube,
    video_path: Path,
    title: str,
    description: str,
    privacy_status: str = "unlisted",
) -> str:
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": "24",  # Entertainment (adjust as needed)
            },
            "status": {"privacyStatus": privacy_status},
        },
        media_body=MediaFileUpload(str(video_path), chunksize=-1, resumable=True),
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        # status.progress() is available when status is not None
    return response["id"]


def upload_thumbnail(youtube, video_id: str, thumbnail_path: Path) -> None:
    youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(str(thumbnail_path)),
    ).execute()


def main() -> None:
    client_secret_path = Path("client_secret.json")
    token_path = Path("token.json")

    creds = get_creds(client_secret_path, token_path)
    youtube = build("youtube", "v3", credentials=creds)

    video_id = upload_video(
        youtube,
        video_path=Path("output.mp4"),
        title="Severus Snape: Origins (Study Session)",
        description="Generated from Hogwarts lore exploration.",
        privacy_status="unlisted",
    )

    upload_thumbnail(youtube, video_id=video_id, thumbnail_path=Path("thumb.png"))
    print(f"Uploaded video: https://www.youtube.com/watch?v={video_id}")


if __name__ == "__main__":
    try:
        main()
    except HttpError as e:
        raise SystemExit(f"YouTube API error: {e}")
```

#### Run from PowerShell

```powershell
python -m pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
python .\upload_youtube.py
```

#### Run from WSL

```bash
python3 -m pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
python3 upload_youtube.py
```

### Resumable uploads + large files

- Prefer resumable uploads (`resumable=True`) for large files.
- Keep chunked upload logic restartable:
  - When possible, persist state and retry on transient failures.
- For thumbnails, use the separate endpoint:
  - `thumbnails.set` (do not try to "embed" thumbnails into the video upload).

### Error handling, rate limits, quota, and pagination

- Implement exponential backoff with jitter for transient failures:
  - Typical retry codes: `429`, `500`, `503`.
  - Many `403` responses are quota-related; treat them as non-transient unless your logs indicate otherwise.
- Track quota usage operationally:
  - Use Google Cloud Console quota dashboards.
  - Avoid unnecessary list calls; keep `maxResults` bounded.
- For list endpoints, always implement pagination via `nextPageToken`.

### Automation (Task Scheduler / cron) + CI considerations

- Prefer scheduling via:
  - Windows Task Scheduler (PowerShell wrapper), or
  - `cron` in WSL.
- Keep OAuth interactive steps out of CI:
  - CI should consume pre-provisioned secrets (token store) rather than re-consenting.
- Note: "service accounts" generally do not work for standard YouTube channel uploads; they are mainly applicable in special CMS/content-owner contexts.

### Monitoring + analytics exports

- Add basic structured logs:
  - upload start/end, file size, chosen privacy status, video id, retry counts.
- Alert on failures:
  - notify on repeated failures (email/Slack) and persist error payloads.
- Export lightweight analytics on a cadence:
  - daily for operational health (upload success/fail),
  - weekly for performance summaries (views, watch time) if you integrate YouTube Analytics API.

---

## Directory Structure

- `parseltongue_cli.py`  
  Main module containing the `TemporalPatronus` class and a tiny
  `argparse`-based CLI.

- `test_parseltongue_cli.py`  
  Unit tests for `parseltongue_cli.py` using the stdlib `unittest`
  framework.

- `HOGWARTS.md`  
  "Hogwarts Temporal Magic Logbook" – documentation for the
  `TemporalPatronus` implementation and how to use the CLI.

- `ACKNOWLEDGEMENT.md`  
  Credits and references (especially to **The Spellbook Chronicles**
  YouTube channel) that inspired the narrative framing.

- `salazar_slytherin.md`  
  Long-form, lore-focused essay on Salazar Slytherin and the legacy of
  Parseltongue.

- `SSSEVERUS SNAPE/`  
  Folder containing multi-chapter narrative summaries of Severus Snape:
  - `snape_chapter_1.md` – early life, Eileen Prince, childhood,
    Hogwarts years, Half-Blood Prince origins, the war.  
  - `snape_chapter_2.md` – double life at Hogwarts, Occlumency,
    Dumbledore's plan, the Half-Blood Prince reveal, Pensieve memories,
    and legacy; explicitly linked to `TemporalPatronus`.

- `__pycache__/`  
  Python bytecode cache directory. Safe to ignore or add to `.gitignore`
  in version control.

---

## Code Overview

### `TemporalPatronus` (in `parseltongue_cli.py`)

A fluent, builder-style class representing a **time-traveling Patronus**.

Key concepts:

- **State**
  - `caster: str` – who casts the Patronus.  
  - `memory: str` – the powering memory.  
  - `_form: Optional[str]` – Patronus form (e.g. `"Silver Doe"`,
    `"Stag"`).  
  - `_temporal_anchors: List[str]` – past/present/future anchors.

- **Main methods**
  - `cast(form: str) -> TemporalPatronus` – set form and add present
    anchor.
  - `anchor_to_past(past_event: str) -> TemporalPatronus` – add past
    anchor.
  - `anchor_to_future(future_event: str) -> TemporalPatronus` – add
    future anchor.
  - `manifest() -> str` – validate that a form was cast, then return a
    multi-line text block starting with `"✨ EXPECTO PATRONUM ✨"` and a
    list of temporal anchors.

- **Presets / factory methods**
  - `TemporalPatronus.snapes_doe()` – Snape's eternal doe, powered by
    love for Lily and anchored to:
    - Present: Snape casting the doe.  
    - Past: first meeting with Lily.  
    - Future: guiding Harry through the Forbidden Forest.
  - `TemporalPatronus.harry_later_years()` – later-years Harry (Cursed
    Child era), anchored to:
    - Past: final duel with Voldemort.  
    - Future: standing with Albus at the edge of time.

---

## CLI Usage

The CLI in `parseltongue_cli.py` uses `argparse` and exposes a single
optional positional argument: `preset`.

From this directory:

```bash
python parseltongue_cli.py           # Snape's eternal doe (default)
python parseltongue_cli.py snape     # Snape's eternal doe
python parseltongue_cli.py harry     # Harry's later-years stag
```

Behavior:

- If no preset is provided, `snape` is used by default.
- Output is the result of `TemporalPatronus.<preset>().manifest()`,
  printed to stdout.

You can also import and use the class directly in Python:

```python
from parseltongue_cli import TemporalPatronus

patronus = TemporalPatronus.snapes_doe()
print(patronus.manifest())
```

---

## Tests

Unit tests live in `test_parseltongue_cli.py` and use the built-in
`unittest` framework.

To run the tests from this directory:

```bash
python -m unittest test_parseltongue_cli
```

The tests currently verify:

- `manifest()` raises a `ValueError` if called before `cast()`.  
- Snape and Harry presets produce the expected `manifest()` contents.  
- The CLI `main()`:
  - Returns exit code `0` for `[]`, `["snape"]`, and `["harry"]`.  
  - Prints the appropriate caster and form.

---

## Documentation & Lore Mapping

- **Code-focused docs**
  - `HOGWARTS.md` explains the `TemporalPatronus` concept, its API, the
    Snape and Harry presets, and how to use the CLI.

- **Lore-focused docs**
  - `SSSEVERUS SNAPE/snape_chapter_1.md` and
    `SSSEVERUS SNAPE/snape_chapter_2.md` provide narrative, chaptered
    analyses of Severus Snape's life, explicitly referencing the
    Temporal Patronus idea in Chapter 2.
  - `salazar_slytherin.md` is a long-form piece exploring Salazar
    Slytherin, Parseltongue, and their historical and symbolic impact.

- **Acknowledgements**
  - `ACKNOWLEDGEMENT.md` documents external creative sources that
    inspired the framing of these materials.

Together, these files form a small, coherent Hogwarts micro-project:
code, tests, and lore that all point back to how light (a Patronus)
travels through time and memory.
