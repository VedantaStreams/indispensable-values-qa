"""
src/transcription.py — YouTube transcript extraction and cleaning utilities.
Handles individual video URLs and full playlists.
"""

import re
import json
import time
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse, parse_qs


def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/|/shorts/)([A-Za-z0-9_-]{11})",
        r"^([A-Za-z0-9_-]{11})$",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def extract_playlist_id(url: str) -> Optional[str]:
    """Extract YouTube playlist ID from URL."""
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    return params.get("list", [None])[0]


def get_playlist_video_ids(playlist_url: str) -> list[dict]:
    """
    Get video IDs and titles from a YouTube playlist.
    Uses yt-dlp if available, otherwise falls back to pytube.
    Returns list of {video_id, title, url} dicts.
    """
    videos = []
    try:
        import yt_dlp
        ydl_opts = {
            "quiet": True,
            "extract_flat": True,
            "skip_download": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            if "entries" in info:
                for entry in info["entries"]:
                    if entry:
                        vid_id = entry.get("id", "")
                        videos.append({
                            "video_id": vid_id,
                            "title": entry.get("title", "Unknown"),
                            "url": f"https://www.youtube.com/watch?v={vid_id}",
                        })
    except ImportError:
        try:
            from pytube import Playlist
            p = Playlist(playlist_url)
            for url in p.video_urls:
                vid_id = extract_video_id(url)
                videos.append({
                    "video_id": vid_id,
                    "title": "Unknown (install yt-dlp for titles)",
                    "url": url,
                })
        except Exception as e:
            raise RuntimeError(f"Could not fetch playlist. Install yt-dlp: {e}")

    return videos


def get_youtube_transcript(video_id: str, preferred_langs: list[str] = None) -> Optional[dict]:
    """
    Fetch transcript for a YouTube video using youtube-transcript-api.

    Returns:
        {
            "text": str,           # full concatenated transcript
            "segments": list,      # [{text, start, duration}]
            "language": str,       # detected language
            "is_generated": bool,  # auto-generated or manual
        }
        or None if no transcript available.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
    except ImportError:
        raise ImportError("Install youtube-transcript-api: pip install youtube-transcript-api")

    if preferred_langs is None:
        preferred_langs = ["en", "en-US", "en-GB"]

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try manual transcript first
        transcript = None
        is_generated = False
        try:
            transcript = transcript_list.find_manually_created_transcript(preferred_langs)
        except Exception:
            pass

        # Fall back to auto-generated
        if transcript is None:
            try:
                transcript = transcript_list.find_generated_transcript(preferred_langs)
                is_generated = True
            except Exception:
                # Try any available language
                for t in transcript_list:
                    transcript = t
                    is_generated = t.is_generated
                    break

        if transcript is None:
            return None

        segments = transcript.fetch()
        full_text = " ".join(seg["text"] for seg in segments)

        return {
            "text": full_text,
            "segments": segments,
            "language": transcript.language_code,
            "is_generated": is_generated,
        }

    except (Exception,) as e:
        if "TranscriptsDisabled" in str(type(e)):
            return None
        raise e


def format_transcript_with_timestamps(segments: list) -> str:
    """Format transcript segments with timestamps for context preservation."""
    lines = []
    for seg in segments:
        start = seg.get("start", 0)
        minutes = int(start // 60)
        seconds = int(start % 60)
        timestamp = f"[{minutes:02d}:{seconds:02d}]"
        text = seg.get("text", "").strip()
        if text:
            lines.append(f"{timestamp} {text}")
    return "\n".join(lines)


def clean_transcript(text: str) -> str:
    """
    Gently clean a transcript:
    - Remove excessive filler words
    - Fix repeated words
    - Preserve Sanskrit terms and scripture references
    - Preserve meaning and speaker's voice
    """
    # Remove common filler word sequences
    filler_patterns = [
        r"\b(um+|uh+|hmm+)\b,?\s*",
        r"\b(you know|I mean|like I said|sort of|kind of)\b,?\s*",
        r"\b(right\??|okay\??|so)\s+(?=\b(so|the|a|we|you|I|it|this|that)\b)",
    ]
    for pattern in filler_patterns:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE)

    # Fix repeated words (e.g., "the the", "and and")
    text = re.sub(r"\b(\w+)\s+\1\b", r"\1", text, flags=re.IGNORECASE)

    # Fix multiple spaces
    text = re.sub(r" {2,}", " ", text)

    # Fix newline clutter
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove artifacts from auto-captions like [Music] [Applause]
    text = re.sub(r"\[(Music|Applause|Laughter|Inaudible|Crosstalk)\]", "", text, flags=re.IGNORECASE)

    return text.strip()


def get_video_metadata(video_id: str) -> dict:
    """Get basic video metadata (title, channel, description)."""
    try:
        import yt_dlp
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}", download=False
            )
            return {
                "title": info.get("title", ""),
                "channel": info.get("channel", info.get("uploader", "")),
                "description": (info.get("description", "") or "")[:500],
                "duration": info.get("duration", 0),
                "upload_date": info.get("upload_date", ""),
                "url": f"https://www.youtube.com/watch?v={video_id}",
            }
    except Exception:
        return {
            "title": "",
            "channel": "",
            "description": "",
            "duration": 0,
            "upload_date": "",
            "url": f"https://www.youtube.com/watch?v={video_id}",
        }


def save_transcript_cache(video_id: str, transcript_data: dict, cache_dir: Path):
    """Save transcript to local cache to avoid re-fetching."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / f"{video_id}.json"
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(transcript_data, f, ensure_ascii=False, indent=2)


def load_transcript_cache(video_id: str, cache_dir: Path) -> Optional[dict]:
    """Load transcript from local cache if available."""
    cache_file = cache_dir / f"{video_id}.json"
    if cache_file.exists():
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def fetch_youtube_transcript(url: str, language: str = "en") -> dict:
    """
    Wrapper: fetch transcript from a YouTube URL.
    Extracts video ID, fetches transcript, cleans and returns result dict.
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError(f"Could not extract video ID from URL: {url}")

    preferred = [language, "en", "en-US"] if language != "en" else ["en", "en-US", "en-GB"]
    result = get_youtube_transcript(video_id, preferred_langs=preferred)

    if result is None:
        raise RuntimeError(
            f"No transcript found for this video. "
            f"The video may not have captions enabled."
        )

    metadata = get_video_metadata(video_id)
    result["video_id"]  = video_id
    result["url"]       = url
    result["title"]     = metadata.get("title", "")
    result["channel"]   = metadata.get("channel", "")
    result["text"]      = clean_transcript(result["text"])
    return result
