### Chess pieces

legal_names = ["Pawn", "Knight", "Rook", "Bishop", "Queen", "King", "Superqueen"]


class Piece:
    """Chess piece
    
    Args:
        value (int or str): Type of chess piece. 
            0: None
            1: Pawn
            2: Knight
            3: Rook
            4: Bishop
            5: Queen
            6: King
            69: Superqueen

        color (int): Color of the piece
            -1: None
            0: Black
            1: White
    """

    def __init__(self):
        self._val = None
        self._color = -1
    
    def set_empty(self):
        """Set a piece to be empty
        """
        self._val = None
        self._color = -1

    def set_from_str(self, value: str, color: int):
        """Set a piece from a string. Accepts capitilasation

        Args:
            value (str): Chess piece name, for example "Queen" or "rook"
            color (int): Piece color, 1 for white and 0 for black

        Raises:
            IndexError: If the piece is invalid, either from invalid value or color
        """

        names = [None] + legal_names
        value = value.capitalize()

        if value not in names:
            raise IndexError(f"{value} is not a valid piece. Accepted values are 0 to 6")
        else:
            self._val = value

        if color not in [0, 1]:
            raise IndexError(f"{color} not a valid color. Choose 0 or 1.")
        
        self._color = color
    
    def set_from_int(self, value: int, color: int):
        """Set a piece from a int. See the class doc for int/value pairs

        Args:
            value (int): Chess piece value. See the class doc for more information
            color (int): Piece color, 1 for white and 0 for black

        Raises:
            IndexError: If the piece is invalid, either from invalid value or color
        """
        names = [None] + legal_names

        if value > 6 or value < 0:
            if value == 69:
                self._val = "Superqueen"
            else:
                raise IndexError(f"{value} is not a valid piece. Accepted values are 0 to 6")
        else: 
            self._val = names[value]
        
        if color not in [0, 1]:
            raise IndexError(f"{color} not a valid color. Choose 0 or 1.")
        
        self._color = color

    def get_value(self)-> str:
        """
        Returns:
            str: String name of the piece
        """
        return self._val
    
    def get_color(self)-> str:
        """
        Returns:
            str: uncapitalised string of the piece's color
        """
        if self._color == -1:
            return None
        elif self._color == 0:
            return "black"
        return "white"
