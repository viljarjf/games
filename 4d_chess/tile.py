from piece import Piece
### Chess tile

class Tile:
    
    def __init__(self, value = None, color = -1):
        try: 
            self._piece = Piece(value, color)
        except:
            raise Exception("Not a valid piece")
        
    def get_piece(self)-> Piece:
        return self._piece
    
    def set_piece(self, value, color = -1):
        try: 
            self._piece = Piece(value, color)
        except:
            raise Exception("Not a valid piece")
    
    def clear(self):
        self._piece = Piece(None)

