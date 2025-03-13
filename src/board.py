from .pieces import Pawn, Knight, Bishop, Rook, Queen, King

class Board:
    def __init__(self):
        # Create an 8x8 board represented as a 2D array
        # None represents empty squares
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.move_history = []
        self.active_color = 'white'
        
    def setup_standard_game(self):
        """Set up the initial position of a chess game."""
        # Place pawns
        for file in range(8):
            self.place_piece(Pawn('white', self.get_position(file, 1)))
            self.place_piece(Pawn('black', self.get_position(file, 6)))
            
        # Place other pieces for both colors
        for color, row in [('white', 0), ('black', 7)]:
            self.place_piece(Rook(color, self.get_position(0, row)))
            self.place_piece(Knight(color, self.get_position(1, row)))
            self.place_piece(Bishop(color, self.get_position(2, row)))
            self.place_piece(Queen(color, self.get_position(3, row)))
            self.place_piece(King(color, self.get_position(4, row)))
            self.place_piece(Bishop(color, self.get_position(5, row)))
            self.place_piece(Knight(color, self.get_position(6, row)))
            self.place_piece(Rook(color, self.get_position(7, row)))
    
    def get_position(self, file, rank):
        """Convert file and rank indices to chess notation (e.g., 0,0 -> 'a1')."""
        return chr(file + 97) + str(rank + 1)
    
    def get_coordinates(self, position):
        """Convert chess notation to file and rank indices (e.g., 'a1' -> 0,0)."""
        file = ord(position[0]) - 97  # 'a' -> 0, 'b' -> 1, etc.
        rank = int(position[1]) - 1   # '1' -> 0, '2' -> 1, etc.
        return file, rank
    
    def place_piece(self, piece):
        """Place a piece on the board."""
        file, rank = self.get_coordinates(piece.position)
        self.squares[rank][file] = piece
    
    def get_piece(self, position):
        """Get the piece at a given position, or None if empty."""
        file, rank = self.get_coordinates(position)
        if 0 <= file < 8 and 0 <= rank < 8:
            return self.squares[rank][file]
        return None