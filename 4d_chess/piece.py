### Chess pieces

class Piece:
    """Chess piece
    
    Args:
        value (int or str): Type of chess piece. 
            0: None
            1: Pawn
            2: Tower
            3: Rook
            4: Bishop
            5: Queen
            6: King
        color (int): Color of the piece
            -1: None
            0: Black
            1: White
    """

    def __init__(self):
        self._value = None
        self._color = -1
    
    def set_empty(self):
        self._value = None
        self._color = -1

    def set_from_str(self, value: str, color = -1):

        names = [None, "Pawn", "Tower", "Rook", "Bishop", "Queen", "King"]
        
        if value.capitalize() not in names:
            raise IndexError(f"{value} is not a valid piece. Accepted values are 0 to 6")
        else:
            self._val = value

        if color not in [-1, 0, 1]:
            raise IndexError(f"{color} not a valid color. Choose 0 or 1.")
        
        self._color = color
        self._is_set = True
    
    def set_from_int(self, value: int, color = -1):

        names = [None, "Pawn", "Tower", "Rook", "Bishop", "Queen", "King"]

        if value > 6 or value < 0:
            raise IndexError(f"{value} is not a valid piece. Accepted values are 0 to 6")
        else: 
            self._val = names[value]
        
        if color not in [-1, 0, 1]:
            raise IndexError(f"{color} not a valid color. Choose 0 or 1.")
        
        self._color = color
        self._is_set = True

    def get_value(self)-> str:
        if not self._is_set:
            raise Exception("Piece not set yet")
        return self._val
    
    def get_color(self)-> str:
        if not self._is_set:
            raise Exception("Piece not set yet")
        if self._color == -1:
            return None
        elif self._color == 0:
            return "black"
        return "white"
