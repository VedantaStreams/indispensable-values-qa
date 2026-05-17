"""
guardrails.py — Content guardrails for reverence and accuracy.

Provides two checks:
1. is_on_topic  — ensures the question is related to the 20 Indispensable Values / BG Ch 13
2. is_reverent_response — post-generation check that the answer does not include
   fabricated quotes or off-topic content.
"""

from __future__ import annotations

import re

# Keywords that indicate a question is on-topic
_ON_TOPIC_KEYWORDS = [
    # Sanskrit value names (common variants)
    "amānitvam", "amanitvam",
    "adambhitvam", "adambhitva",
    "ahiṃsā", "ahimsa",
    "kṣāntiḥ", "ksanti", "kshanti",
    "ārjavam", "arjavam",
    "ācāryopāsanam", "acharya", "guru", "teacher",
    "śaucam", "shaucam", "purity",
    "sthairyam", "steadfastness",
    "ātmavinigrahaḥ", "self-control",
    "indriyārtheṣu", "sense objects",
    "vairāgyam", "vairagya", "dispassion",
    "anahaṅkāraḥ", "anahankara", "ego",
    "janma", "birth", "death", "duḥkha", "dukha", "suffering",
    "asaktih", "asaktī", "non-attachment",
    "anabhiṣvaṅgaḥ", "non-clinging",
    "samacitattvam", "equanimity",
    "mayi", "devotion", "bhakti",
    "viviktadeśa", "solitude",
    "tattva", "self-knowledge", "jñāna", "jnana",
    # Context keywords
    "indispensable values", "indispensable value",
    "bhagavad gita", "bhagavad gītā", "gita", "gītā",
    "chapter 13", "verses 7", "verses 8", "verses 9", "verses 10", "verses 11",
    "swamiji", "swami aparajitananda", "aparājitānanda",
    "chinmaya", "value", "values", "virtue", "virtues",
    "jñāna sādhana", "jnana sadhana", "knowledge",
    "discourse", "teaching", "story", "parable",
]

# Patterns that flag potential fabrication in a generated answer
_FABRICATION_PATTERNS = [
    re.compile(r'swamiji\s+(?:said|says|stated|explained|told)\s+(?:that\s+)?["\u201c\u2018]', re.IGNORECASE),
    re.compile(r'according to swamiji[,\s]+["\u201c\u2018]', re.IGNORECASE),
]


def is_on_topic(question: str) -> bool:
    """Return True if the question appears to relate to the 20 Indispensable Values or BG Ch 13.

    Uses a keyword heuristic — short questions with no keywords may still be
    answered if the RAG retrieval finds relevant chunks.
    """
    q_lower = question.lower()
    for kw in _ON_TOPIC_KEYWORDS:
        if kw in q_lower:
            return True
    # Short questions (< 8 words) pass the guardrail by default — let RAG decide
    if len(question.split()) < 8:
        return True
    return False


def is_reverent_response(response: str) -> bool:
    """Return True if the response passes basic fabrication checks."""
    for pattern in _FABRICATION_PATTERNS:
        if pattern.search(response):
            return False
    return True
