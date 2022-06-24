from chess.assets.board import Board
from chess.assets.mover import Mover

class NDChess:
    """
    Abstract class for chess.

    Methods:
        move_piece: move a piece on the board and update the turn.
    """

    def __init__(self, dimension: int, board_size: int, init_random: bool = False):
        # initialize the board
        self.board_size = board_size
        self.dimension = dimension

        self._board = Board(dimension = self.dimension, board_size = self.board_size)
        
        if init_random:
            self._board.init_random()

        # set up some stuff to enable moving
        self._turn = False
        self._moves = Mover(self.dimension, self.board_size)
    
    def get_legal_moves(self, pos: int) -> list[tuple]:
        current_piece = self._board.get_tile(pos).get_piece()
        legal_moves = []
        if current_piece.get_value() != "Pawn":
            for moves in self._moves.get_moves(current_piece, pos):
                for move in moves:
                    piece = self._board.get_tile(move).get_piece()
                    # stop in direction if same color piece
                    if piece.get_color() == current_piece.get_color():
                        break
                    legal_moves.append(move)
                    # stop in direction if hitting enemy
                    if piece.get_value() is not None:
                        break
            return legal_moves

        # pawns are stupid
        # forward:
        forward_dirs = self.dimension // 2
        moves = self._moves.get_moves(current_piece, pos)
        for forward_moves in moves[:forward_dirs]:
            for move in forward_moves:
                piece = self._board.get_tile(move).get_piece()
                # only allowed if empty
                if piece.get_value() is None:
                    legal_moves.append(move)
                else:
                    break
        # sides:
        for move in moves[forward_dirs:]:
            # skip if empty
            if not move:
                continue
            # we know there is only one move in each sub-list
            move = move[0]
            piece = self._board.get_tile(move).get_piece()
            # only allowed if enemy
            c = piece.get_color()
            if c is not None and c != current_piece.get_color():
                legal_moves.append(move)
        return legal_moves

    def move_piece(self, init_pos, dest_pos)-> bool:
        """
        Move a piece from `init_pos` to `dest_pos`, if the move is allowed
        Updates the turn (`self._turn`)

        Args:
            init_pos (tuple):   nD coordinates for the piece. 
            dest_pos (tuple):   nD coordinates for the destination. 
        
        Returns:
            bool, success state of the move
        """
        piece = self._board.get_tile(init_pos).get_piece()
        dest_piece = self._board.get_tile(dest_pos).get_piece()
        if piece.get_value() is not None:
            legal_moves = self.get_legal_moves(init_pos)
            # check if the move is legal
            if dest_pos in legal_moves:
                # attempt the move
                if self._board.move(self._previous_pos, dest_pos):
                    # Then, check if the move resulted in a check against the player
                    c = piece.get_color()
                    for pos in self._board.get_iterator():
                        p = self._board.get_tile(pos).get_piece()
                        if p.get_value() == "King":
                            if p.get_color() == c:
                                if self.is_check(pos):
                                    # the move was illegal. reset 
                                    self._board.move(dest_pos, self._previous_pos)
                                    self._board.set_tile(dest_pos, dest_piece)
                                    return False
                    self._turn = not self._turn
                    return True
        return False 
    
    def is_check(self, pos)-> bool:
        """return wether a position is in check or not
        returns false if tile is empty

        Args:
            pos (tuple):    nD coordinates for the piece. 

        Returns:
            bool: Wether the position is in check.
        """
        ### Setup
        p = self._board.get_tile(pos).get_piece()
        if p.get_color() is None:
            return False
        c = p.get_color()
        moves = list()
        for pos_it in self._board.get_iterator():
            new_p = self._board.get_tile(pos_it).get_piece()
            # if the piece is on the opposing team..
            if new_p.get_color() is not None and new_p.get_color() != c:
                # .. add their available moves to the list
                [moves.append(i) for i in self.get_legal_moves(pos_it)]

        # remove duplicates
        moves = list(set(moves))

        return pos in moves
