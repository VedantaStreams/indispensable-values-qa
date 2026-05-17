"""
src/transcription.py
YouTube transcription using yt-dlp (audio download) + OpenAI Whisper API.

Workflow:
  1. Extract video ID from URL
  2. Download audio-only stream via yt-dlp (no video, fast)
  3. Split audio into chunks if > 24MB (Whisper limit is 25MB)
  4. Send each chunk to OpenAI Whisper for transcription
  5. Stitch chunks together and clean transcript
  6. Return structured result dict

Cost: ~$0.006 per minute of audio (Whisper pricing)
"""

import os
import re
import json
import tempfile
from pathlib import Path
from typing import Optional


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
    from urllib.parse import urlparse, parse_qs
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    return params.get("list", [None])[0]


def get_video_metadata(video_id: str) -> dict:
    """Get basic video metadata (title, channel, duration)."""
    try:
        import yt_dlp
        ydl_opts = {"quiet": True, "skip_download": True, "no_warnings": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}", download=False
            )
            return {
                "title":       info.get("title", ""),
                "channel":     info.get("channel", info.get("uploader", "")),
                "description": (info.get("description", "") or "")[:500],
                "duration":    info.get("duration", 0),
                "upload_date": info.get("upload_date", ""),
                "url":         f"https://www.youtube.com/watch?v={video_id}",
            }
    except Exception:
        return {
            "title": "", "channel": "", "description": "",
            "duration": 0, "upload_date": "",
            "url": f"https://www.youtube.com/watch?v={video_id}",
        }


def download_audio(video_url: str, output_dir: Path) -> Path:
    """
    Download audio-only from a YouTube video using yt-dlp.
    Returns path to downloaded audio file.
    """
    try:
        import yt_dlp
    except ImportError:
        raise ImportError("yt-dlp not installed. Add to requirements.txt: yt-dlp>=2024.1.1")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    video_id = extract_video_id(video_url) or "audio"
    output_template = str(output_dir / f"{video_id}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": output_template,
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    for ext in ["m4a", "webm", "mp4", "opus", "ogg", "mp3"]:
        candidate = output_dir / f"{video_id}.{ext}"
        if candidate.exists():
            return candidate

    raise FileNotFoundError(f"Audio file not found after download in {output_dir}")


def transcribe_audio_whisper(
    audio_path: Path,
    language: str = "en",
    openai_api_key: str = None,
) -> str:
    """
    Transcribe audio using OpenAI Whisper API.
    Handles files > 24MB by splitting into 10-minute chunks.
    Returns full transcript text.
    """
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError("openai package not installed.")

    try:
        import streamlit as st
        api_key = openai_api_key or st.secrets.get("OPENAI_API_KEY")
    except Exception:
        api_key = openai_api_key

    api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found.")

    client = OpenAI(api_key=api_key)
    audio_path = Path(audio_path)
    file_size_mb = audio_path.stat().st_size / (1024 * 1024)
    lang = language if language not in ("auto", "") else None

    if file_size_mb <= 24:
        with open(audio_path, "rb") as f:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language=lang,
                response_format="text",
            )
        return str(response)
    else:
        return _transcribe_in_chunks(audio_path, lang, client)


def _transcribe_in_chunks(audio_path: Path, language, client) -> str:
    """Split large audio into 10-minute chunks and transcribe each."""
    try:
        from pydub import AudioSegment
    except ImportError:
        raise ImportError("pydub not installed. Add to requirements.txt: pydub>=0.25.1")

    audio = AudioSegment.from_file(str(audio_path))
    chunk_ms = 10 * 60 * 1000  # 10 minutes
    parts = []

    with tempfile.TemporaryDirectory() as tmp:
        for i, start in enumerate(range(0, len(audio), chunk_ms)):
            chunk = audio[start: start + chunk_ms]
            chunk_path = Path(tmp) / f"chunk_{i}.mp3"
            chunk.export(str(chunk_path), format="mp3")
            with open(chunk_path, "rb") as f:
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    language=language,
                    response_format="text",
                )
            parts.append(str(response))

    return " ".join(parts)


def fetch_youtube_transcript(
    url: str,
    language: str = "en",
    openai_api_key: str = None,
) -> dict:
    """
    Full pipeline: YouTube URL → download audio → Whisper transcription.

    Returns dict with: text, video_id, url, title, channel, language,
                       is_generated, duration
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError(f"Could not extract video ID from URL: {url}")

    metadata = get_video_metadata(video_id)

    with tempfile.TemporaryDirectory() as tmp_dir:
        audio_path = download_audio(url, Path(tmp_dir))
        text = transcribe_audio_whisper(
            audio_path,
            language=language,
            openai_api_key=openai_api_key,
        )

    text = clean_transcript(text)

    return {
        "text":         text,
        "video_id":     video_id,
        "url":          url,
        "title":        metadata.get("title", ""),
        "channel":      metadata.get("channel", ""),
        "language":     language,
        "is_generated": True,
        "duration":     metadata.get("duration", 0),
    }


def clean_transcript(text: str) -> str:
    """Clean a Whisper transcript — remove fillers, fix spacing."""
    filler_patterns = [
        r"\b(um+|uh+|hmm+)\b,?\s*",
        r"\b(you know|I mean|like I said|sort of|kind of)\b,?\s*",
        r"\b(right\??|okay\??|so)\s+(?=\b(so|the|a|we|you|I|it|this|that)\b)",
    ]
    for pattern in filler_patterns:
        text = re.sub(pattern, " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\b(\w+)\s+\1\b", r"\1", text, flags=re.IGNORECASE)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(
        r"\[(Music|Applause|Laughter|Inaudible|Crosstalk)\]",
        "", text, flags=re.IGNORECASE
    )
    return text.strip()


def get_playlist_video_ids(playlist_url: str) -> list:
    """Get all video IDs and titles from a YouTube playlist."""
    try:
        import yt_dlp
    except ImportError:
        raise ImportError("yt-dlp not installed.")

    videos = []
    ydl_opts = {
        "quiet": True, "extract_flat": True,
        "skip_download": True, "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        if "entries" in info:
            for entry in info["entries"]:
                if entry:
                    vid_id = entry.get("id", "")
                    videos.append({
                        "video_id": vid_id,
                        "title":    entry.get("title", "Unknown"),
                        "url":      f"https://www.youtube.com/watch?v={vid_id}",
                    })
    return videos


def save_transcript_cache(video_id: str, data: dict, cache_dir: Path):
    """Save transcript to local JSON cache."""
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    with open(cache_dir / f"{video_id}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_transcript_cache(video_id: str, cache_dir: Path) -> Optional[dict]:
    """Load transcript from local cache if available."""
    cache_file = Path(cache_dir) / f"{video_id}.json"
    if cache_file.exists():
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return None
