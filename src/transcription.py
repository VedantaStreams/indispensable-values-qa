"""
transcription.py — YouTube transcript fetching for Indispensable Values Q&A.

Downloads auto-generated or manual English transcripts from YouTube videos
and returns them as plain text suitable for ingestion.
"""

from __future__ import annotations

import re
from typing import Optional


def fetch_transcript(youtube_url: str) -> Optional[str]:
    """Fetch the English transcript for a YouTube video.

    Args:
        youtube_url: Full YouTube URL or video ID.

    Returns:
        The transcript as a single string, or None if unavailable.

    Raises:
        ValueError: If the URL cannot be parsed.
    """
    from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

    video_id = _extract_video_id(youtube_url)
    if not video_id:
        raise ValueError(f"Could not extract a video ID from: {youtube_url}")

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Prefer manually-created English transcript
        try:
            transcript = transcript_list.find_manually_created_transcript(["en"])
        except NoTranscriptFound:
            # Fall back to auto-generated English
            transcript = transcript_list.find_generated_transcript(["en"])

        entries = transcript.fetch()
        text = " ".join(entry["text"] for entry in entries)
        # Clean up HTML entities and extra whitespace
        text = re.sub(r"&#?\w+;", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    except TranscriptsDisabled:
        return None
    except NoTranscriptFound:
        return None


def _extract_video_id(url: str) -> Optional[str]:
    """Extract the 11-character YouTube video ID from a URL or return as-is if already an ID."""
    # Already a bare video ID?
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url.strip()):
        return url.strip()

    patterns = [
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([A-Za-z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None
