"""A model may supply similarity scores, but the domain must manage uncertainty."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    label: str
    score: float


@dataclass(frozen=True)
class BreedResult:
    candidates: tuple[Candidate, ...]
    abstained: bool
    explanation: str


def interpret_breed_scores(scores: dict[str, float], *, confidence_floor: float = 0.7) -> BreedResult:
    if not 0 < confidence_floor <= 1:
        raise ValueError("Invalid confidence floor")
    if not scores or any(not (0 <= value <= 1) for value in scores.values()):
        return BreedResult((), True, "No reliable estimate available.")
    ranking = tuple(Candidate(k, v) for k, v in sorted(scores.items(), key=lambda x: -x[1])[:3])
    abstain = ranking[0].score < confidence_floor
    return BreedResult(
        ranking,
        abstain,
        "Visual resemblance only. Photographs cannot establish genetic ancestry."
        if not abstain else
        "Low model certainty; no breed identification is offered.",
    )

# Breed categorization matrix updated
