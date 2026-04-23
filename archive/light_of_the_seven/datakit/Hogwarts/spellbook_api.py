"""Spellbook Chronicles Data API Integration (YouTube Data API v3).

This module provides a small, stable client for retrieving authoritative metadata
from the YouTube channel "The Spellbook Chronicles" to support the Hogwarts
visualization corpus.

Auth modes:
- MOCK mode: offline, deterministic responses (no network).
- LIVE mode: OAuth 2.0 (installed app flow) using a Google Cloud OAuth client
  secret JSON file.

Why OAuth (vs API key)?
- Some environments/projects prefer OAuth for quota/account attribution and
  future expansion to endpoints requiring user auth.
- If you only need public channel/video metadata, an API key is also viable,
  but this file standardizes on OAuth for LIVE mode for consistency.

Prerequisites (LIVE mode):
- Install dependencies:
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
- Use an OAuth **Desktop app** client secret JSON (downloaded from Google Cloud Console).
  IMPORTANT: Web app OAuth clients often cause `redirect_uri_mismatch` with local flows.
  This file defaults to DEFAULT_CLIENT_SECRET_FILE; change it or pass `--client-secret-file`.

Security:
- Do NOT commit refreshed tokens to source control. If you add token persistence,
  ensure token files are in .gitignore.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass

# Optional (only required for LIVE OAuth mode). Imported lazily in code to keep
# MOCK mode usable even if deps aren't installed.
try:
    from google.auth.transport.requests import Request as GoogleAuthRequest
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except Exception:  # pragma: no cover
    GoogleAuthRequest = None  # type: ignore[assignment]
    InstalledAppFlow = None  # type: ignore[assignment]
    build = None  # type: ignore[assignment]

logger = logging.getLogger("SpellbookAPI")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"

DEFAULT_CHANNEL_ID = "UCHa1nCaL35Gng9Oq3gmJxrg"
DEFAULT_CLIENT_SECRET_FILE = "client_secret_77445086716-3lfslc7iq76dtsh41cvm82tb0e056rhk.apps.googleusercontent.com.json"


class SpellbookClient:
    """Client for interacting with the YouTube Data API v3 using OAuth 2.0."""

    def __init__(
        self,
        channel_id: str,
        *,
        client_secret_file: str | Path = DEFAULT_CLIENT_SECRET_FILE,
        scopes: list[str] | None = None,
        credentials: Any = None,
    ):
        self.channel_id = channel_id
        self.client_secret_file = Path(client_secret_file)
        self.scopes = scopes or [YOUTUBE_READONLY_SCOPE]
        self.credentials = credentials

        self._validate_config()

    def _validate_config(self) -> None:
        if not self.channel_id:
            raise ValueError("channel_id is required.")
        if not self.channel_id.startswith("UC"):
            logger.warning(
                "Channel ID %r does not start with 'UC'. This may be incorrect.",
                self.channel_id,
            )

    def _ensure_oauth_deps(self) -> None:
        if InstalledAppFlow is None or build is None:
            raise RuntimeError(
                "OAuth dependencies not available. Install: "
                "google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client"
            )

    def _load_credentials_interactive(self) -> Any:
        """Run the installed-app OAuth flow (opens browser)."""
        self._ensure_oauth_deps()

        if not self.client_secret_file.exists():
            raise FileNotFoundError(
                "OAuth client secret JSON not found.\n"
                f"- Looked for: {self.client_secret_file}\n"
                "- Fix: rename your newly created Desktop app JSON to "
                f"'{DEFAULT_CLIENT_SECRET_FILE}' OR pass `--client-secret-file <path>`.\n"
                "- Note: use a Desktop app OAuth client to avoid redirect_uri_mismatch."
            )

        if InstalledAppFlow is None:
            raise RuntimeError(
                "OAuth dependencies not available. Install: "
                "google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client"
            )
        flow = InstalledAppFlow.from_client_secrets_file(
            str(self.client_secret_file),
            scopes=self.scopes,
        )
        # Port=0 lets the OS select an available port.
        creds = flow.run_local_server(port=0)
        return creds

    def _get_service(self):
        """Build and return the YouTube API service client."""
        self._ensure_oauth_deps()

        assert InstalledAppFlow is not None
        assert build is not None

        if self.credentials is None:
            self.credentials = self._load_credentials_interactive()

        # Refresh token if possible/needed
        if getattr(self.credentials, "expired", False) and getattr(
            self.credentials, "refresh_token", None
        ):
            if GoogleAuthRequest is None:
                raise RuntimeError(
                    "google-auth transport Request unavailable; cannot refresh token."
                )
            self.credentials.refresh(GoogleAuthRequest())

        return build("youtube", "v3", credentials=self.credentials)

    def verify_integration(self) -> bool:
        """Verify that the channel exists and is accessible."""
        try:
            service = self._get_service()
            resp = (
                service.channels()
                .list(
                    part="snippet",
                    id=self.channel_id,
                    hl="en",
                    fields="items(id,snippet(title,description))",
                )
                .execute()
            )
            items = resp.get("items", [])
            if not items:
                logger.error("Verification failed: no channel items returned.")
                return False

            title = items[0].get("snippet", {}).get("title", "<unknown>")
            logger.info("Verified channel: %s (%s)", title, self.channel_id)
            return True
        except Exception as e:
            # HttpError is a subclass of Exception; keep generic handler stable.
            logger.error("Verification error: %s", e)
            return False

    def get_latest_videos(self, max_results: int = 5) -> list[dict[str, Any]]:
        """Fetch latest videos from the channel via `search.list`."""
        if max_results <= 0:
            return []

        try:
            service = self._get_service()
            resp = (
                service.search()
                .list(
                    part="snippet",
                    channelId=self.channel_id,
                    maxResults=max_results,
                    order="date",
                    type="video",
                    hl="en",
                    fields="items(id(videoId),snippet(title,publishedAt,description))",
                )
                .execute()
            )
            return resp.get("items", [])
        except Exception as e:
            logger.error("Error fetching latest videos: %s", e)
            return []


class MockSpellbookClient(SpellbookClient):
    """Mock client for offline verification of the contract logic.

    This intentionally does NOT require OAuth dependencies.
    """

    def __init__(self, channel_id: str = DEFAULT_CHANNEL_ID):
        super().__init__(
            channel_id, client_secret_file=DEFAULT_CLIENT_SECRET_FILE, credentials=None
        )

    def verify_integration(self) -> bool:
        logger.info("MOCK VERIFICATION: Channel ID accepted: %s", self.channel_id)
        return True

    def get_latest_videos(self, max_results: int = 5) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = [
            {
                "id": {"videoId": "mock_vid_1"},
                "snippet": {
                    "title": "Mock Video 1: The History of Hogwarts",
                    "publishedAt": "2023-01-01T12:00:00Z",
                    "description": "Mock data for offline verification.",
                },
            },
            {
                "id": {"videoId": "mock_vid_2"},
                "snippet": {
                    "title": "Mock Video 2: Parseltongue 101",
                    "publishedAt": "2023-01-02T12:00:00Z",
                    "description": "Mock data for offline verification.",
                },
            },
            {
                "id": {"videoId": "mock_vid_3"},
                "snippet": {
                    "title": "Mock Video 3: The Founders' Legacy",
                    "publishedAt": "2023-01-03T12:00:00Z",
                    "description": "Mock data for offline verification.",
                },
            },
        ]
        return items[: max(0, max_results)]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Spellbook Chronicles Data API Client")
    parser.add_argument(
        "--mock", action="store_true", help="Run in Mock Mode (Offline Verification)"
    )
    parser.add_argument(
        "--channel-id",
        default=DEFAULT_CHANNEL_ID,
        help="YouTube Channel ID (starts with UC...)",
    )
    parser.add_argument(
        "--client-secret-file",
        default=DEFAULT_CLIENT_SECRET_FILE,
        help="Path to OAuth client_secret JSON file",
    )
    parser.add_argument(
        "--max-results", type=int, default=3, help="Number of videos to fetch"
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()

    if args.mock:
        print("Entering MOCK MODE...")
        client: SpellbookClient = MockSpellbookClient(args.channel_id)
    else:
        print("Connecting to LIVE API with OAuth 2.0...")
        client = SpellbookClient(
            args.channel_id,
            client_secret_file=args.client_secret_file,
        )

    if not client.verify_integration():
        print("Verification Failed: Channel mismatch or API/auth error.")
        return 2

    mode = "MOCK" if args.mock else "LIVE"
    print(f"Integration Verified ({mode} MODE): Channel confirmed.")

    videos = client.get_latest_videos(args.max_results)
    print(f"Latest {len(videos)} videos:")
    for v in videos:
        snippet = v.get("snippet", {})
        title = snippet.get("title", "<no title>")
        published = snippet.get("publishedAt", "<no date>")
        print(f"- {title} ({published})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
