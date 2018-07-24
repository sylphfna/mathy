from ..tree_node import LEFT
from ..expressions import AddExpression, BinaryExpression, ConstantExpression
from ..util import isAddSubtract, isConstTerm, getTerm, termsAreLike
from .base_rule import BaseRule


class ConstantsSimplifyRule(BaseRule):
    """Given a binary operation on two constants, simplify to the resulting constant expression"""

    def getName(self):
        return "Simplify Constant Operation"

    def canApplyTo(self, node):
        # Check simple case of left/right child binary op with constants
        return (
            isinstance(node, BinaryExpression)
            and isinstance(node.left, ConstantExpression)
            and isinstance(node.right, ConstantExpression)
        )
    def applyTo(self, node):
        change = super().applyTo(node)
        change.saveParent()
        result = ConstantExpression(node.evaluate())
        return change.done(result)

