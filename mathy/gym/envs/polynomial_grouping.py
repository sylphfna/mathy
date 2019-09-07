from gym.envs.registration import register

from ...envs.polynomial_grouping import MathyPolynomialGroupingEnv
from ...types import MathyEnvDifficulty, MathyEnvProblemArgs
from ..mathy_gym_env import MathyGymEnv

#
# Group like terms
#


class GymPolynomialGrouping(MathyGymEnv):
    def __init__(self, difficulty: MathyEnvDifficulty, **kwargs):
        super(GymPolynomialGrouping, self).__init__(
            env_class=MathyPolynomialGroupingEnv,
            env_problem_args=MathyEnvProblemArgs(difficulty=difficulty),
            **kwargs
        )


class PolynomialGroupingEasy(GymPolynomialGrouping):
    def __init__(self, **kwargs):
        super(PolynomialGroupingEasy, self).__init__(
            difficulty=MathyEnvDifficulty.easy, **kwargs
        )


class PolynomialGroupingNormal(GymPolynomialGrouping):
    def __init__(self, **kwargs):
        super(PolynomialGroupingNormal, self).__init__(
            difficulty=MathyEnvDifficulty.normal, **kwargs
        )


class PolynomialGroupingHard(GymPolynomialGrouping):
    def __init__(self, **kwargs):
        super(PolynomialGroupingHard, self).__init__(
            difficulty=MathyEnvDifficulty.hard, **kwargs
        )


register(
    id="mathy-poly-grouping-easy-v0",
    entry_point="mathy.gym.envs:PolynomialGroupingEasy",
)
register(
    id="mathy-poly-grouping-normal-v0",
    entry_point="mathy.gym.envs:PolynomialGroupingNormal",
)
register(
    id="mathy-poly-grouping-hard-v0",
    entry_point="mathy.gym.envs:PolynomialGroupingHard",
)