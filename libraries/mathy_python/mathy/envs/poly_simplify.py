from typing import Any, Dict, List, Optional, Type

from numpy.random import randint, uniform

from .. import time_step
from ..core.expressions import MathExpression
from ..util import calculate_term_grouping_distances
from ..util import get_terms, has_like_terms, is_preferred_term_form
from ..env import MathyEnv, MathyEnvProblem
from ..problems import gen_simplify_multiple_terms
from ..core.rule import BaseRule
from ..rules import (
    CommutativeSwapRule,
    ConstantsSimplifyRule,
    DistributiveFactorOutRule,
)
from ..state import MathyEnvState, MathyObservation
from ..types import MathyEnvDifficulty, MathyEnvProblemArgs


class PolySimplify(MathyEnv):
    """A Mathy environment for simplifying polynomial expressions.

    NOTE: This environment only generates polynomial problems with
     addition operations. Subtraction, Multiplication and Division
     operators are excluded. This is a good area for improvement.
    """

    def get_env_namespace(self) -> str:
        return "mathy.polynomials.simplify"

    def max_moves_fn(
        self, problem: MathyEnvProblem, config: MathyEnvProblemArgs
    ) -> int:
        if config.difficulty == MathyEnvDifficulty.easy:
            multiplier = 3
        elif problem.complexity < 5:
            multiplier = 2
        elif problem.complexity < 7:
            multiplier = 3
        elif problem.complexity < 12:
            multiplier = 4
        else:
            multiplier = 3
        return problem.complexity * multiplier

    def transition_fn(
        self,
        env_state: MathyEnvState,
        expression: MathExpression,
        features: MathyObservation,
    ) -> Optional[time_step.TimeStep]:
        """If there are no like terms."""
        if not has_like_terms(expression):
            term_nodes = get_terms(expression)
            is_win = True
            for term in term_nodes:
                if not is_preferred_term_form(term):
                    is_win = False
            if is_win:
                return time_step.termination(features, self.get_win_signal(env_state))
        return None

    def problem_fn(self, params: MathyEnvProblemArgs) -> MathyEnvProblem:
        """Given a set of parameters to control term generation, produce
        a polynomial problem with (n) total terms divided among (m) groups
        of like terms. A few examples of the form: `f(n, m) = p`
        - (3, 1) = "4x + 2x + 6x"
        - (6, 4) = "4x + v^3 + y + 5z + 12v^3 + x"
        - (4, 2) = "3x^3 + 2z + 12x^3 + 7z"
        """
        if params.difficulty == MathyEnvDifficulty.easy:
            # Set number of noise terms and inject a bunch more in simple problems
            # so they don't learn stupid policies that only work with small trees.
            #
            # e.g. mashing the 3rd node to commute the tree until a DF shows up in
            #      the desired position.
            noise_terms = randint(1, 3)
            num_terms = randint(4, 6)
            scaling = uniform(0.35, 0.5)
            text, complexity = gen_simplify_multiple_terms(
                num_terms,
                inner_terms_scaling=scaling,
                powers_probability=0.2,
                noise_probability=0.5,
                shuffle_probability=0.0,
                noise_terms=noise_terms,
            )
        elif params.difficulty == MathyEnvDifficulty.normal:
            # Set number of noise terms and inject a bunch more in simple problems
            # so they don't learn stupid policies that only work with small trees.
            #
            # e.g. mashing the 3rd node to commute the tree until a DF shows up in
            #      the desired position.
            noise_terms = randint(1, 3)
            num_terms = randint(3, 7)
            scaling = uniform(0.35, 0.5)
            text, complexity = gen_simplify_multiple_terms(
                num_terms,
                inner_terms_scaling=scaling,
                powers_probability=0.4,
                noise_probability=1.0,
                shuffle_probability=0.0,
                noise_terms=noise_terms,
            )

            num_terms = randint(2, 7)
            scaling = uniform(0.35, 0.5)
            text, complexity = gen_simplify_multiple_terms(
                num_terms,
                inner_terms_scaling=scaling,
                powers_probability=0.5,
                noise_probability=0.6,
                shuffle_probability=0.1,
            )
        elif params.difficulty == MathyEnvDifficulty.hard:
            num_terms = randint(7, 10)
            scaling = uniform(0.25, 0.75)
            text, complexity = gen_simplify_multiple_terms(
                num_terms,
                shuffle_probability=0.5,
                powers_probability=0.8,
                inner_terms_scaling=scaling,
            )
        else:
            raise ValueError(f"Unknown difficulty: {params.difficulty}")
        return MathyEnvProblem(text, complexity, self.get_env_namespace())
