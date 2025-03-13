class Piece:
    """Base class for all chess pieces."""

    def __init__(self, color, position):
        """Initialize a chess piece.
        
        Args:
            color: 'white' or 'black'
            position: Chess notation position (e.g., 'e4')
        """
        self.color = color
        self.position = position
        self.has_moved = False 

    def move(self, new_position):
        """Move piece to a new position.
        
        This doesn't check if the move is valid since that's handled in your move generation file.
        
        Args:
            new_position: The new position in chess notation
            
        Returns:
            None
        """
        self.position = new_position
        self.has_moved = True

    def __str__(self):
        """String representation of the piece."""
        return f"{self.color} {self.__class__.__name__} at {self.position}"
    
    def __repr__(self):
        """Representation of the piece for debugging."""
        return f"{self.__class__.__name__}('{self.color}', '{self.position}')"

# Specific piece classes with their unique identifiers
class Pawn(Piece):
    """Pawn chess piece."""
    symbol = 'P'
    value = 1
    

class Knight(Piece):
    """Knight chess piece."""
    symbol = 'N'  # Uses 'N' to avoid confusion with King
    value = 3
    

class Bishop(Piece):
    """Bishop chess piece."""
    symbol = 'B'
    value = 3
    

class Rook(Piece):
    """Rook chess piece."""
    symbol = 'R'
    value = 5
    

class Queen(Piece):
    """Queen chess piece."""
    symbol = 'Q'
    value = 9
    

class King(Piece):
    """King chess piece."""
    symbol = 'K'
    value = 0  # The king's value is technically infinite

# Optional utility function to create pieces
def create_piece(piece_type, color, position):
    """Factory function to create a chess piece.
    
    Args:
        piece_type: String ('pawn', 'knight', etc.) or class (Pawn, Knight, etc.)
        color: 'white' or 'black'
        position: Chess notation position
        
    Returns:
        A Piece object of the appropriate subclass
    """
    if isinstance(piece_type, str):
        piece_map = {
            'pawn': Pawn,
            'knight': Knight, 
            'bishop': Bishop,
            'rook': Rook,
            'queen': Queen,
            'king': King
        }
        piece_class = piece_map.get(piece_type.lower())
        if not piece_class:
            raise ValueError(f"Unknown piece type: {piece_type}")
    else:
        piece_class = piece_type
        
    return piece_class(color, position)
