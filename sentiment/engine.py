"""Fitness sentiment engine — Zain, Usama, Ali."""
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

from sentiment.constants import (
    DIET_PLANS,
    EMOJI_MAP,
    EXPLICIT_OVERRIDES,
    GYM_SLANG,
    LABELS,
    MESSAGES,
    ROMAN_URDU,
    WORKOUT_PLANS,
)

ROBERTA_MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(ROBERTA_MODEL)
model = AutoModelForSequenceClassification.from_pretrained(
    ROBERTA_MODEL,
    use_safetensors=True,
)

def _check_explicit_override(text: str):
    """
    Scan raw text for explicit sentiment phrases.
    Returns forced label string if matched, else None.
    """
    for pattern, label in EXPLICIT_OVERRIDES:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return label
    return None



def _replace_emojis(text: str) -> str:
    """Swap each emoji for its sentiment-descriptive phrase."""
    for emoji, phrase in EMOJI_MAP.items():
        text = text.replace(emoji, phrase)
    return text


def _expand_slang(text: str, slang_dict: dict) -> str:
    """
    Replace every slang key in the text with its expansion.
    Sorted longest-first so multi-word phrases match before
    shorter overlapping sub-strings.
    """
    for key, expansion in sorted(slang_dict.items(),
                                  key=lambda x: len(x[0]), reverse=True):
        # Word-boundary aware replacement (case-insensitive)
        pattern = r'(?<!\w)' + re.escape(key) + r'(?!\w)'
        text = re.sub(pattern, f' {expansion} ', text, flags=re.IGNORECASE)
    return text


def _clean_hashtags(text: str) -> str:
    """#BeastMode → beast mode  (split camel-case, drop the #)."""
    def split_hashtag(match):
        tag = match.group(1)
        # Insert space before every uppercase run following a lowercase letter
        spaced = re.sub(r'([a-z])([A-Z])', r'\1 \2', tag)
        return ' ' + spaced.lower() + ' '
    return re.sub(r'#(\w+)', split_hashtag, text)


def _normalize_repeated_chars(text: str) -> str:
    """sooooore → soore  (collapse any char repeated >2 times to 2)."""
    return re.sub(r'(.)\1{2,}', r'\1\1', text)


def _handle_mentions_and_urls(text: str) -> str:
    """RoBERTa training convention: @handle → @user, URLs → http."""
    tokens = text.split()
    cleaned = []
    for token in tokens:
        if token.startswith('@') and len(token) > 1:
            cleaned.append('@user')
        elif token.startswith('http') or token.startswith('www.'):
            cleaned.append('http')
        else:
            cleaned.append(token)
    return ' '.join(cleaned)


def preprocess(text: str) -> str:
    """
    Full pre-processing pipeline for fitness / gym text.

    Order matters:
      1  Emoji → descriptive phrase   (before lowercasing so Unicode matches)
      2  Lowercase
      3  Hashtag splitting            (#BeastMode → beast mode)
      4  Roman Urdu expansion
      5  Gym / fitness slang expansion
      6  Repeated-character collapse  (sooore → soore)
      7  @mention / URL normalisation (RoBERTa convention)
      8  Whitespace cleanup
    """
    text = _replace_emojis(text)             # Step 1
    text = text.lower()                      # Step 2
    text = _clean_hashtags(text)             # Step 3
    text = _expand_slang(text, ROMAN_URDU)   # Step 4
    text = _expand_slang(text, GYM_SLANG)    # Step 5
    text = _normalize_repeated_chars(text)   # Step 6
    text = _handle_mentions_and_urls(text)   # Step 7
    text = re.sub(r'\s+', ' ', text).strip() # Step 8
    return text

def get_sentiment(text: str) -> dict:
    """
    Run RoBERTa sentiment analysis on fitness/gym text.

    Returns
    -------
    {
        "original_text"   : str,
        "processed_text"  : str,
        "scores"          : {"Negative": float, "Neutral": float, "Positive": float},
        "dominant"        : "Negative" | "Neutral" | "Positive",
        "confidence_pct"  : float          # 0-100
    }
    """
    processed = preprocess(text)

    # ── Step A: check explicit override BEFORE the model ─────
    forced_label = _check_explicit_override(text)

    # ── Step B: run RoBERTa ───────────────────────────────────
    encoded = tokenizer(
        processed,
        return_tensors='pt',
        truncation=True,
        max_length=512
    )
    output = model(**encoded)

    raw_scores  = output.logits[0].detach().numpy()
    soft_scores = softmax(raw_scores)

    score_dict = {label: round(float(soft_scores[i]) * 100, 2)
                  for i, label in enumerate(LABELS)}

    # ── Step C: apply override if triggered ──────────────────
    if forced_label:
        dominant         = forced_label
        override_applied = True
        # Raw model scores are still stored accurately below
    else:
        dominant         = max(score_dict, key=score_dict.get)
        override_applied = False

    return {
        "original_text"   : text,
        "processed_text"  : processed,
        "scores"          : score_dict,   # raw model scores always preserved
        "dominant"        : dominant,
        "confidence_pct"  : score_dict[dominant],
        "override_applied": override_applied,   # True = explicit phrase won
    }


def analyze_and_recommend(text: str) -> dict:
    """End-to-end: raw text -> sentiment -> fitness plan."""
    sentiment = get_sentiment(text)
    dominant = sentiment["dominant"]
    return {
        "sentiment": sentiment,
        "workout_plan": WORKOUT_PLANS[dominant],
        "diet_plan": DIET_PLANS[dominant],
        "message": MESSAGES[dominant],
    }
