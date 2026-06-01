"""One-off: merge notebook v2 cells into sentiment/constants.py and sentiment/engine.py."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "Mlops_Sentimental_Anaylsis_robertoAL.ipynb"

with open(NB, encoding="utf-8") as f:
    nb = json.load(f)

def cell_src(idx: int) -> str:
    return "".join(nb["cells"][idx]["source"])

# Cell indices from notebook structure (v2)
CONSTANTS_SRC = cell_src(2) + "\n\n" + cell_src(4).split("def _check_explicit_override")[0]
PREPROCESS_AND_SENTIMENT = cell_src(4).split("EXPLICIT_OVERRIDES")[0]
# Actually cell 4 has EXPLICIT_OVERRIDES + helpers + preprocess
# Cell 2 has EMOJI, GYM, ROMAN

constants_body = cell_src(2) + "\n\n" + "EXPLICIT_OVERRIDES = [\n" + cell_src(4).split("EXPLICIT_OVERRIDES = [", 1)[1].split("]\n\n\n\ndef _check_explicit_override")[0] + "\n]\n"

engine_header = '''"""Fitness sentiment engine — Zain, Usama, Ali."""
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
model = AutoModelForSequenceClassification.from_pretrained(ROBERTA_MODEL)

'''

# Get helpers + preprocess + get_sentiment from cells 4 and 6
cell4 = cell_src(4)
helpers_start = cell4.index("def _check_explicit_override")
cell6 = cell_src(6)
analyze_fn = '''
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
'''

# constants: cell 2 + overrides from cell 4 + workout/diet/messages from 8,10,12
constants_full = (
    cell_src(2).rstrip()
    + "\n\n"
    + cell4[: cell4.index("def _check_explicit_override")].rstrip()
    + "\n\n"
    + cell_src(8).rstrip()
    + "\n\n"
    + cell_src(10).rstrip()
    + "\n\n"
    + cell_src(12).rstrip()
    + "\n\nLABELS = [\"Negative\", \"Neutral\", \"Positive\"]\n"
)

engine_full = engine_header + cell4[helpers_start:] + "\n" + cell6 + "\n" + analyze_fn

(ROOT / "sentiment").mkdir(exist_ok=True)
(ROOT / "sentiment" / "constants.py").write_text(constants_full, encoding="utf-8")
(ROOT / "sentiment" / "__init__.py").write_text(
    'from sentiment.engine import analyze_and_recommend, get_sentiment\n',
    encoding="utf-8",
)
(ROOT / "sentiment" / "engine.py").write_text(engine_full, encoding="utf-8")
print("Wrote sentiment/constants.py and sentiment/engine.py")
