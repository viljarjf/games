from chess.assets.piece import Piece

import copy
### Chess tile

class Tile:
    """Class for tiles on a chess board

    Args:
        value (str OR int, optional): value of the piece to put on the tile. Defaults to None.
        color (int, optional): Color of the piece. 0 for black, 1 for white. Defaults to -1.

    Raises:
        TypeError: wrong type for piece value
        Exception: Something wrong happened :(
    """
    
    def __init__(self, value = None, color = -1):
        try: 
            self._piece = Piece()
            if value is None: 
                self._piece.set_empty()

            elif type(value) == str:
                self._piece.set_from_str(value, color)

            elif type(value) == int:
                self._piece.set_from_int(value, color)
                
            else:
                raise TypeError(f"\"value\" must be either str, int or Nonetype, not {type(value)}")
        except:
            raise Exception("Not a valid piece")

        self._id = None
        
    def get_piece(self)-> Piece:
        """
        Returns:
            Piece: Copy of the piece in the tile
        """
        return copy.copy(self._piece)
    
    def set_piece(self, piece: Piece):
        """Set the piece of a tile

        Args:
            piece (Piece): pre-initialised Piece class
        """
        self._piece = copy.copy(piece)
    
    def clear(self):
        """Clear the tile, by calling Piece.set_empty()
        """
        self._piece.set_empty()
    
    def __str__(self):
        return str(self._piece)
