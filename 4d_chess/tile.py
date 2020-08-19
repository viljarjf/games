from piece import Piece
### Chess tile

class Tile:
    
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
        
    def get_piece(self)-> Piece:
        return self._piece
    
    def set_piece(self, value, color = -1):
        try: 
            if type(value) == str:
                self._piece.set_from_str(value, color)
            elif type(value) == int:
                self._piece.set_from_int(value, color)
            else:
                raise TypeError(f"\"value\" must be either str or int, not {type(value)}")
        except:
            raise Exception("Not a valid piece")
    
    def clear(self):
        self._piece.set_empty()

