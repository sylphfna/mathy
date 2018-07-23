import numpy
from .math.expressions import MathExpression
from .math.parser import ExpressionParser
from .math.properties.associative import AssociativeSwapRule
from .math.properties.commutative import CommutativeSwapRule
from .math.properties.distributive_factor import DistributiveFactorOutRule
from .math.properties.distributive_multiply import DistributiveMultiplyRule
import random


class MathGame:
    """
    Implement a math solving game where players have two distinct win conditions
    that require different strategies for solving. The first win-condition is for 
    the player to execute the right sequence of actions to reduce a math expression
    to its most basic representation. The second is for the other player to expand 
    the simple representations into more verbose expressions.

    Ideally a fully-trained player will be able to both simplify arbitrary mathematical
    expressions, and expand upon arbitrary parts of expressions to generate more complex
    representations that can be used to expand on concepts that a user may struggle with.
    """

    tokens = list(" abcdefghijklmnopqrstuvwxyz01234567890.!=()^*+-/")

    def __init__(self, expression_str: str):
        self.width = 16
        self.parser = ExpressionParser()
        self.expression_str = expression_str
        self.input_characters = MathGame.tokens
        self.tokens_count = len(self.input_characters)
        # use whitespace for padding
        self.padding_token = self.input_characters[0]
        self.token_index = dict(
            [(char, i) for i, char in enumerate(self.input_characters)]
        )
        self.input_data = self.encode_text(self.expression_str)
        self.available_actions = [
            CommutativeSwapRule(),
            DistributiveFactorOutRule(),
            DistributiveMultiplyRule(),
            AssociativeSwapRule(),
        ]

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        return self.input_data.copy()

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        return (self.width, self.tokens_count)

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        return len(self.available_actions)

    def getNextState(self, board, player, action):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        text = self.decode_board(board)
        expession = self.parser.parse(text)
        action = self.available_actions[action]
        print("Board is: {}".format(text))
        print("Action is: {}".format(action))
        print("Expression is: {}".format(expession))
        # Translate board (tokenIds) into text strings = [self.token_index[t] for t in board]

        # print("action taken!: {}".format(action))
        return board, -player

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        expression = self.parser.parse(self.decode_board(board))
        actions = [0] * self.getActionSize()
        for index, _ in enumerate(actions):
            action = self.available_actions[index]
            if action.canApplyTo(expression):
                actions[index] = 1
        return actions

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
               
        """
        return 0

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        return board.copy()

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        return []

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """

        return self.decode_board(board)

    def encode_text(self, text):
        """Encode the given math expression string into tokens on a game board"""
        data = numpy.zeros((self.width, self.tokens_count), dtype="float32")
        characters = list(str(text))
        for i, ch in enumerate(characters):
            data[i][self.token_index[ch]] = 1.
        return data

    def decode_board(self, board):
        """Decode the given board into an expression string"""
        token_indices = numpy.argmax(board, axis=1)
        text = [self.tokens[t] for t in token_indices]
        return "".join(text).strip()

