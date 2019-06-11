from ..expressions import (
    AddExpression,
    MultiplyExpression,
    ConstantExpression,
    VariableExpression,
    PowerExpression,
)
from ..rule import BaseRule


class VariableMultiplyRule(BaseRule):
    r"""
    This restates `x^b * x^d` as `x^(b + d)` which has the effect of isolating
    the exponents attached to the variables, so they can be combined.

        1. When there are two terms with the same base being multiplied together, their
           exponents are added together. "x * x^3" = "x^4" because "x = x^1" so
           "x^1 * x^3 = x^(1 + 3) = x^4"

        TODO: 2. When there is a power raised to another power, they can be combined by
                 multiplying the exponents together. "x^(2^2) = x^4"

    The rule identifies terms with explicit and implicit powers, so the following
    transformations are all valid:

    Explicit powers: x^b * x^d = x^(b+d)

            *
           / \
          /   \          ^
         /     \    =   / \
        ^       ^      x   +
       / \     / \        / \
      x   b   x   d      b   d


    Implicit powers: x * x^d = x^(1 + d)

            *
           / \
          /   \          ^
         /     \    =   / \
        x       ^      x   +
               / \        / \
              x   d      1   d

    """

    @property
    def name(self):
        return "Variable Multiplication"

    @property
    def code(self):
        return "VM"

    def get_child_components(self, child):
        """Return a tuple of (variable, exponent) for the given child node, or
        (None, None) if the child is invalid for this rule.
        """
        # A power expression with variable/constant children is OKAY
        if isinstance(child, PowerExpression):
            if isinstance(child.left, VariableExpression) and isinstance(
                child.right, ConstantExpression
            ):
                return (child.left.identifier, child.right.value)
        # Otherwise just a variable is OKAY
        if isinstance(child, VariableExpression):
            return (child.identifier, 1)
        return (None, None)

    def can_apply_to(self, node):
        """To cleanly apply, the node must be a multiply and it must have single
        variable terms as its left and right children.
        """
        if not isinstance(node, MultiplyExpression):
            return False

        left_var, _ = self.get_child_components(node.left)
        if left_var is None:
            return False
        right_var, _ = self.get_child_components(node.right)
        if right_var is None:
            return False
        return left_var == right_var

    def apply_to(self, node):
        change = super().apply_to(node).save_parent()

        left_variable, left_exp = self.get_child_components(node.left)
        right_variable, right_exp = self.get_child_components(node.right)

        # If the variables don't match
        variable = left_variable
        if left_variable != right_variable:
            variable = left_variable + right_variable

        inside = AddExpression(
            ConstantExpression(left_exp), ConstantExpression(right_exp)
        )

        # If both powers are 1 and the variables don't match, drop them from the output
        if left_exp == 1 and right_exp == 1 and left_variable != right_variable:
            result = VariableExpression(variable)
        else:
            result = PowerExpression(VariableExpression(variable), inside)
        change.done(result)
        return change
