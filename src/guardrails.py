"""
src/guardrails.py — Input and output guardrails for the RAG chatbot.
Ensures reverence, accuracy, and scope compliance.
"""

import re
from typing import Tuple

# ── Blocked patterns ───────────────────────────────────────────────────────────
HARMFUL_PATTERNS = [
    r"\b(hate|insult|mock|ridicule|blaspheme|denigrate|abuse)\b",
    r"\b(kill|harm|destroy|hurt)\b.*\b(person|people|human)\b",
    r"\b(porn|sexual|erotic|obscene)\b",
    r"\b(drug|narcotic|intoxicant)\b.*\b(how to|recipe|make)\b",
]

OFF_TOPIC_HARD_BLOCKS = [
    r"\b(recipe|cooking|sport|cricket|football|movie|film|stock|invest)\b",
    r"\b(politics|election|vote|party|government policy)\b",
    r"\b(generate image|write code|debug|programming)\b",
]

# Terms that indicate genuine spiritual/philosophical questions (allow)
SPIRITUAL_KEYWORDS = [
    "value", "virtue", "humility", "ego", "ahimsa", "forgiveness", "karma",
    "gita", "bhagavad", "swamiji", "vedanta", "upanishad", "sanskrit",
    "chapter 13", "jnana", "knowledge", "self", "atma", "brahman",
    "moksha", "liberation", "devotion", "bhakti", "meditation", "teaching",
    "scripture", "verse", "shloka", "amanitva", "adambhitva", "kshanti",
    "arjavam", "saucha", "sthairyam", "vairagya", "asakti", "viveka",
    "discrimination", "dispassion", "non-attachment", "non-injury",
    "steadfastness", "self-control", "simplicity", "purity", "seeker",
    "sadhana", "practice", "reflection", "meaning", "explain", "what is",
    "how does", "why is", "difference between", "relate to", "understand",
    "indispensable", "qualify", "knowledge", "field", "knower",
]


def check_input_guardrails(query: str) -> Tuple[bool, str]:
    """
    Check if a user query is appropriate for the chatbot.

    Returns:
        (is_safe: bool, reason: str)
        If is_safe is False, reason contains the rejection message.
    """
    query_lower = query.lower().strip()

    # Empty query
    if not query_lower:
        return False, "Please enter a question."

    # Too short
    if len(query_lower) < 4:
        return False, "Please ask a complete question."

    # Too long (potential prompt injection)
    if len(query) > 2000:
        return False, "Question is too long. Please keep it under 2000 characters."

    # Check for harmful patterns
    for pattern in HARMFUL_PATTERNS:
        if re.search(pattern, query_lower, re.IGNORECASE):
            return False, "harmful"

    # Check for hard off-topic blocks (only if NO spiritual keyword is present)
    has_spiritual = any(kw in query_lower for kw in SPIRITUAL_KEYWORDS)
    if not has_spiritual:
        for pattern in OFF_TOPIC_HARD_BLOCKS:
            if re.search(pattern, query_lower, re.IGNORECASE):
                return False, "off_topic"

    # Prompt injection patterns
    injection_patterns = [
        r"ignore (previous|all|your) instructions",
        r"you are now",
        r"pretend (you are|to be)",
        r"act as (if|though|a)",
        r"disregard.*rules",
        r"jailbreak",
        r"system prompt",
    ]
    for pattern in injection_patterns:
        if re.search(pattern, query_lower, re.IGNORECASE):
            return False, "🙏 This question cannot be processed. Please ask a genuine question about the teachings."

    return True, ""


def check_output_guardrails(response: str, retrieved_context: str) -> Tuple[bool, str]:
    """
    Basic check on the generated response.
    Flags if response seems to fabricate sources or contain inappropriate content.

    Returns:
        (is_ok: bool, warning: str)
    """
    warnings = []

    # Check for hallucination markers (common LLM fabrication patterns)
    fabrication_patterns = [
        r"(Swamiji says|Swamiji said|Swamiji states|Swamiji wrote).*[\"''""]",
        r"page \d+",      # only flag if context has no page refs
        r"verse \d+:\d+", # only flag cross-chapter refs
    ]

    # If the context is thin but response is very long, flag it
    if len(retrieved_context) < 200 and len(response) > 800:
        warnings.append("⚠️ Note: Limited source material was found. Please verify this answer against original texts.")

    # Simple length check
    if len(response) > 4000:
        response = response[:4000] + "\n\n*[Response truncated for length.]*"

    warning_str = "\n\n".join(warnings) if warnings else ""
    return True, warning_str


def sanitize_metadata_input(value: str, max_length: int = 200) -> str:
    """Sanitize user-provided metadata strings."""
    if not value:
        return ""
    # Strip dangerous characters, truncate
    value = re.sub(r"[<>&\"']", "", value)
    return value[:max_length].strip()
