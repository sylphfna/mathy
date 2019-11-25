from typing import List, Any, NamedTuple
from enum import Enum
from pydantic import BaseModel, Field


class MathyEnvDifficulty(str, Enum):
    easy: str = Field(
        default="easy",
        title="Easy Problems",
        description="The simplest form of problems that demonstrate a task",
    )
    normal: str = Field(
        default="normal",
        title="Normal Problems",
        description="Challenging problems that involve more terms",
    )
    hard: str = Field(
        default="hard",
        title="Hard Problems",
        description="Difficult problems that have intentionally large expressions",
    )


class MathyEnvProblemArgs(BaseModel):
    difficulty: MathyEnvDifficulty = MathyEnvDifficulty.easy


class MathyEnvProblem(NamedTuple):
    """Summarize an environment-specific problem that was generated with
    a tuple of (text, complexity, type) where:
     - "text" is the text content of the generated problem
     - "complexity" is an integer value that represents the number of
       terms in the problem text.
     - "type" is a dot namespaced string, e.g. "mathy.poly.simplify"
    """

    text: str
    complexity: int
    type: str
