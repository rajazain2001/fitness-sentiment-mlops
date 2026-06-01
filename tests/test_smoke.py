"""Quick smoke tests for sentiment labels (run after pip install -r requirements.txt)."""
import pytest

from sentiment.engine import analyze_and_recommend, get_sentiment


@pytest.mark.parametrize(
    "text,expected",
    [
        ("beast mode activated hit a new PR today", "Positive"),
        ("no motivation at all demotivated hoon", "Negative"),
        ("feeling neutral today just gonna stick to the plan", "Neutral"),
        ("thak gaya yaar gym nahi jaon ga aaj", "Negative"),
    ],
)
def test_dominant_sentiment(text: str, expected: str):
    result = get_sentiment(text)
    assert result["dominant"] == expected


def test_analyze_returns_plans():
    out = analyze_and_recommend("great workout feeling strong")
    assert "sentiment" in out
    assert "workout_plan" in out
    assert "diet_plan" in out
    assert "message" in out
    assert out["workout_plan"]["mode"]
