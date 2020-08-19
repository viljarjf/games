### Chess pieces

class Piece:

    names = [None, "Pawn", "Tower", "Rook", "Bishop", "Queen", "King"]

    def __init__(self, value, color = -1: ):
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
        if type(value) == str:
            if value.capitalize() not in names:
                raise IndexError(f"{value} is not a valid piece. Accepted values are 0 to 6")
            else:
                self._val = value
        elif type(value) == int:
            if value > 6 or value < 0:
                raise IndexError(f"{value} is not a valid piece. Accepted values are 0 to 6")
            else: 
                self._val = names[value]
        else:
            raise TypeError(f"\"value\" must be str or int, not {type(value)}.")

        if color not in [-1, 0, 1]:
            raise IndexError(f"{color} not a valid color. Choose 0 or 1.")
        
        self._color = color
    

    def get_value(self)-> str:
        return self._val
    
    def get_color(self)-> str:
        if self._color == -1:
            return None
        elif self._color == 0:
            return "black"
        return "white"
