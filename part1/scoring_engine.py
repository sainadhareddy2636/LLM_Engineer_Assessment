from typing import List, Dict, Any
import math
import statistics


class ScoringEngine:
    def __init__(self):
        pass

    def process(self, predictions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not isinstance(predictions, list):
            raise TypeError("predictions must be a list")

        sector_map = {}

        for p in predictions:
            self._validate_input(p)
            sector = p["sector"]
            sector_map.setdefault(sector, []).append(p["raw_score"])

        sector_stats = {}
        for sector, scores in sector_map.items():
            if len(scores) == 0:
                sector_stats[sector] = (None, None)
            elif len(scores) == 1:
                sector_stats[sector] = (statistics.mean(scores), 0.0)
            else:
                sector_stats[sector] = (
                    statistics.mean(scores),
                    statistics.pstdev(scores),
                )

        outputs = []

        for p in predictions:
            sector = p["sector"]
            mean, std = sector_stats.get(sector, (None, None))

            excluded = False
            exclusion_reason = None

            if std == 0 or std is None:
                normalized = None
                excluded = True
                exclusion_reason = "division_by_zero"
            else:
                normalized = (p["raw_score"] - mean) / std

            if normalized is not None:
                if p["confidence"] < 0.3:
                    excluded = True
                    exclusion_reason = "confidence_below_threshold"
                elif abs(normalized) < 0.5:
                    excluded = True
                    exclusion_reason = "normalized_score_below_threshold"

            if excluded or normalized is None:
                final_score = None
            else:
                final_score = normalized * p["confidence"]
                final_score = max(-3.0, min(3.0, final_score))

            outputs.append({
                "ticker": p["ticker"],
                "final_score": final_score,
                "sector": sector,
                "excluded": excluded,
                "exclusion_reason": exclusion_reason
            })

        return outputs

    def _validate_input(self, p: Dict[str, Any]) -> None:
        required = ["ticker", "raw_score", "confidence", "sector"]
        for key in required:
            if key not in p:
                raise ValueError(f"Missing key: {key}")

        if not isinstance(p["ticker"], str):
            raise TypeError("ticker must be string")

        if not isinstance(p["raw_score"], (int, float)):
            raise TypeError("raw_score must be float")

        if not isinstance(p["confidence"], float):
            raise TypeError("confidence must be float")

        if not (0.0 <= p["confidence"] <= 1.0):
            raise ValueError("confidence out of bounds")

        if not isinstance(p["sector"], str):
            raise TypeError("sector must be string")
