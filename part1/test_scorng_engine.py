import pytest
from scoring_engine import ScoringEngine


def test_normal_case():
    engine = ScoringEngine()
    preds = [
        {"ticker": "A", "raw_score": 10, "confidence": 0.9, "sector": "Tech"},
        {"ticker": "B", "raw_score": 20, "confidence": 0.8, "sector": "Tech"},
    ]

    result = engine.process(preds)
    assert len(result) == 2
    assert result[0]["excluded"] is False


def test_confidence_filter():
    engine = ScoringEngine()
    preds = [
        {"ticker": "A", "raw_score": 10, "confidence": 0.2, "sector": "Tech"},
        {"ticker": "B", "raw_score": 20, "confidence": 0.8, "sector": "Tech"},
    ]

    result = engine.process(preds)
    assert result[0]["excluded"] is True
    assert result[0]["exclusion_reason"] == "confidence_below_threshold"


def test_single_item_sector():
    engine = ScoringEngine()
    preds = [
        {"ticker": "A", "raw_score": 10, "confidence": 0.9, "sector": "Energy"},
    ]

    result = engine.process(preds)
    assert result[0]["excluded"] is True
    assert result[0]["exclusion_reason"] == "division_by_zero"


def test_invalid_input():
    engine = ScoringEngine()
    with pytest.raises(TypeError):
        engine.process("not a list")
