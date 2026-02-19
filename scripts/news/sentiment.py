#!/usr/bin/env python3
"""News sentiment helpers with optional FinBERT backend."""

from __future__ import annotations

from typing import Dict, Iterable, List

POSITIVE_WORDS = {
    "beat",
    "growth",
    "profit",
    "record",
    "surge",
    "upgrade",
    "gain",
    "strong",
    "bullish",
    "outperform",
}
NEGATIVE_WORDS = {
    "miss",
    "decline",
    "loss",
    "drop",
    "cut",
    "downgrade",
    "weak",
    "bearish",
    "risk",
    "probe",
}


class SentimentAnalyzer:
    def __init__(self) -> None:
        self._pipe = None
        self._has_finbert = False
        try:
            from transformers import pipeline  # type: ignore

            self._pipe = pipeline("text-classification", model="ProsusAI/finbert")
            self._has_finbert = True
        except Exception:
            self._pipe = None

    def score(self, text: str) -> Dict[str, float | str]:
        if not text:
            return {"sentiment_score": 0.0, "sentiment_label": "neutral"}

        if self._has_finbert and self._pipe:
            try:
                pred = self._pipe(text[:512])[0]
                label = str(pred["label"]).lower()
                score = float(pred.get("score", 0.0))
                normalized = score if "positive" in label else -score if "negative" in label else 0.0
                return {"sentiment_score": round(normalized, 4), "sentiment_label": _norm_label(label)}
            except Exception:
                pass

        # Fallback keyword method
        words = [w.strip(".,:;!?()[]{}\"'").lower() for w in text.split()]
        pos = sum(1 for w in words if w in POSITIVE_WORDS)
        neg = sum(1 for w in words if w in NEGATIVE_WORDS)
        total = max(len(words), 1)
        raw = (pos - neg) / total
        if raw > 0.02:
            label = "positive"
        elif raw < -0.02:
            label = "negative"
        else:
            label = "neutral"
        return {"sentiment_score": round(raw, 4), "sentiment_label": label}


def _norm_label(label: str) -> str:
    if "positive" in label:
        return "positive"
    if "negative" in label:
        return "negative"
    return "neutral"
