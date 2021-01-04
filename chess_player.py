class ChessPlayer():


    def __init__(self, color, AI = False):
        self.color = color
        self.is_AI = AI
        self.pieces = []
        self.check = False
        self.check_mate = False
        self.selection = None

    def is_own_piece(self, piece):
        if piece in self.pieces:
            return True
        else:
            return False

