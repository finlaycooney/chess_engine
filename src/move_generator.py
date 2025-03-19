from src.pieces import Pawn, Knight, Bishop, Rook, Queen, King

class Move:
    """Represents a chess move from one position to another."""
    def __init__(self, start_pos, end_pos):
        """Initialize a move.
        
        Args:
            start_pos: Starting position in chess notation (e.g., 'e2')
            end_pos: Ending position in chess notation (e.g., 'e4')
        """
        self.start_pos = start_pos
        self.end_pos = end_pos
        
    def __str__(self):
        """String representation of the move."""
        return f"{self.start_pos}->{self.end_pos}"
        
    def __repr__(self):
        """Representation of the move for debugging."""
        return f"Move('{self.start_pos}', '{self.end_pos}')"

class MoveGenerator:
    def __init__(self, board):
        self.board = board
    
    def generate_moves(self, color=None):
        """Generate all legal moves for the given color."""
        if color is None:
            color = self.board.active_color
            
        all_moves = []
        
        # Go through all squares on the board
        for rank in range(8):
            for file in range(8):
                position = self.board.get_position(file, rank)
                piece = self.board.get_piece(position)
                
                # If the square has a piece of the correct color
                if piece and piece.color == color:
                    # Add all legal moves for this piece
                    piece_moves = self.generate_piece_moves(piece)
                    all_moves.extend(piece_moves)
        
        return all_moves
    
    def generate_piece_moves(self, piece):
        """Generate all possible moves for a specific piece."""
        # Dispatch to the appropriate method based on piece type
        if isinstance(piece, Pawn):
            return self.generate_pawn_moves(piece)
        elif isinstance(piece, Knight):
            return self.generate_knight_moves(piece)
        elif isinstance(piece, Bishop):
            return self.generate_bishop_moves(piece)
        elif isinstance(piece, Rook):
            return self.generate_rook_moves(piece)
        elif isinstance(piece, Queen):
            return self.generate_queen_moves(piece)
        elif isinstance(piece, King):
            return self.generate_king_moves(piece)
        return []
        
    def generate_pawn_moves(self, pawn):
        """Generate all legal moves for a pawn."""
        moves = []
        file, rank = self.board.get_coordinates(pawn.position)
        
        # Determine direction based on color
        direction = 1 if pawn.color == 'white' else -1
        
        # Forward move
        new_rank = rank + direction
        if 0 <= new_rank < 8:
            new_pos = self.board.get_position(file, new_rank)
            if not self.board.get_piece(new_pos):  # Square is empty
                moves.append(Move(pawn.position, new_pos))
                
                # Double move from starting position
                if (pawn.color == 'white' and rank == 1) or (pawn.color == 'black' and rank == 6):
                    new_rank = rank + 2 * direction
                    if 0 <= new_rank < 8:
                        new_pos = self.board.get_position(file, new_rank)
                        if not self.board.get_piece(new_pos):  # Square is empty
                            moves.append(Move(pawn.position, new_pos))
        
        # Capture moves (diagonally)
        for file_offset in [-1, 1]:
            new_file = file + file_offset
            new_rank = rank + direction
            if 0 <= new_file < 8 and 0 <= new_rank < 8:
                new_pos = self.board.get_position(new_file, new_rank)
                target = self.board.get_piece(new_pos)
                if target and target.color != pawn.color:
                    moves.append(Move(pawn.position, new_pos))
        
        # En passant

        if len(self.board.move_history) > 0:
            last_move = self.board.move_history[-1]
            
            # Check if last move was a pawn double push
            last_piece = self.board.get_piece(last_move.end_pos)
            if (isinstance(last_piece, Pawn) and 
                abs(int(last_move.start_pos[1]) - int(last_move.end_pos[1])) == 2):
                
                last_file, last_rank = self.board.get_coordinates(last_move.end_pos)
                
                # Check if our pawn is adjacent to the double-pushed pawn
                if abs(file - last_file) == 1 and rank == last_rank:
                    # Create en passant move
                    new_pos = self.board.get_position(last_file, rank + direction)
                    en_passant_move = Move(pawn.position, new_pos)
                    en_passant_move.is_en_passant = True
                    en_passant_move.captured_pos = last_move.end_pos  # Position of the captured pawn
                    moves.append(en_passant_move)        
        
        # Add promotion logic here
        
        return moves
    
    def generate_knight_moves(self, knight):
        """Generate all legal moves for a knight."""
        moves = []
        file, rank = self.board.get_coordinates(knight.position)
        
        # All possible knight moves
        offsets = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        
        for file_offset, rank_offset in offsets:
            new_file = file + file_offset
            new_rank = rank + rank_offset
            
            # Check if the new position is on the board
            if 0 <= new_file < 8 and 0 <= new_rank < 8:
                new_pos = self.board.get_position(new_file, new_rank)
                target = self.board.get_piece(new_pos)
                
                # Can move if square is empty or contains an enemy piece
                if not target or target.color != knight.color:
                    moves.append(Move(knight.position, new_pos))
        
        return moves