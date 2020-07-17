""" Chess implementation in python """
import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT = (204, 255, 230)
DARK = (51, 153, 51)
MOVE = (50, 50, 50)
CAPTURE = (120, 50, 50)

square_size = 60
board_size = square_size * 8
display_height = square_size * 8
display_width = square_size * 8

first_person_locations = {
    "pawn0": (square_size * 0, square_size * 6),
    "pawn1": (square_size * 1, square_size * 6),
    "pawn2": (square_size * 2, square_size * 6),
    "pawn3": (square_size * 3, square_size * 6),
    "pawn4": (square_size * 4, square_size * 6),
    "pawn5": (square_size * 5, square_size * 6),
    "pawn6": (square_size * 6, square_size * 6),
    "pawn7": (square_size * 7, square_size * 6),
    "knight0": (square_size * 1, square_size * 7),
    "knight1": (square_size * 6, square_size * 7),
    "bishop0": (square_size * 2, square_size * 7),
    "bishop1": (square_size * 5, square_size * 7),
    "rook0": (square_size * 0, square_size * 7),
    "rook1": (square_size * 7, square_size * 7),
    "queen": (square_size * 3, square_size * 7),
    "king": (square_size * 4, square_size * 7),
}

second_person_locations = {
    "pawn0": (square_size * 0, square_size * 1),
    "pawn1": (square_size * 1, square_size * 1),
    "pawn2": (square_size * 2, square_size * 1),
    "pawn3": (square_size * 3, square_size * 1),
    "pawn4": (square_size * 4, square_size * 1),
    "pawn5": (square_size * 5, square_size * 1),
    "pawn6": (square_size * 6, square_size * 1),
    "pawn7": (square_size * 7, square_size * 1),
    "knight0": (square_size * 1, square_size * 0),
    "knight1": (square_size * 6, square_size * 0),
    "bishop0": (square_size * 2, square_size * 0),
    "bishop1": (square_size * 5, square_size * 0),
    "rook0": (square_size * 0, square_size * 0),
    "rook1": (square_size * 7, square_size * 0),
    "queen": (square_size * 3, square_size * 0),
    "king": (square_size * 4, square_size * 0),
}

display = pygame.display.set_mode((display_width, display_height))
display.fill(LIGHT)
pygame.display.set_caption("Chess")

clock = pygame.time.Clock()


class Set:
    def __init__(self, color, is_player):
        self.is_player = is_player
        self.color = color
        self.pieces = self.generate_pieces(self.color)

    def generate_pieces(self, color):
        pieces = {}
        for i in range(8):
            name = "pawn" + str(i)
            pieces[name] = Piece(color, "pawn", name, self.is_player)
        for i in range(2):
            pieces["bishop" + str(i)] = Piece(
                color, "bishop", "bishop" + str(i), self.is_player
            )
            pieces["knight" + str(i)] = Piece(
                color, "knight", "knight" + str(i), self.is_player
            )
            pieces["rook" + str(i)] = Piece(
                color, "rook", "rook" + str(i), self.is_player
            )
        pieces["queen"] = Piece(color, "queen", "queen", self.is_player)
        pieces["king"] = Piece(color, "king", "king", self.is_player)
        return pieces


class Piece:
    def __init__(self, color, piece_type, piece_name, is_player):
        self.is_player = is_player
        self.is_moved = False
        self.color = color
        self.piece_type = piece_type
        self.piece_name = piece_name
        self.image_name = "assets/" + self.color + "/" + self.piece_type
        self.image = pygame.image.load(self.image_name + ".png")
        self.location = self.start_location(self.piece_name)

    def start_location(self, piece_name):
        if self.is_player:
            return first_person_locations[piece_name]
        else:
            return second_person_locations[piece_name]

    def possible_moves(self, first_location):
        moves = []
        capture_moves = []

        # # Movement

        # Moves for white pawn
        if self.color == "white":
            if self.piece_type == "pawn":
                if not self.is_moved:
                    moves.append(
                        (first_location[0], first_location[1] - square_size * 2)
                    )

                moves.append((first_location[0], first_location[1] - square_size))

                tmp_location = (
                    first_location[0] + square_size,
                    first_location[1] - square_size,
                )
                if self.is_capture(tmp_location):
                    capture_moves.append(tmp_location)

                tmp_location = (
                    first_location[0] - square_size,
                    first_location[1] - square_size,
                )
                if self.is_capture(tmp_location):
                    capture_moves.append(tmp_location)

        # Moves for black pawn
        else:
            if self.piece_type == "pawn":
                if not self.is_moved:
                    moves.append(
                        (first_location[0], first_location[1] + square_size * 2)
                    )

                moves.append((first_location[0], first_location[1] + square_size))

                tmp_location = (
                    first_location[0] + square_size,
                    first_location[1] + square_size,
                )
                if self.is_capture(tmp_location):
                    capture_moves.append(tmp_location)

                tmp_location = (
                    first_location[0] - square_size,
                    first_location[1] + square_size,
                )
                if self.is_capture(tmp_location):
                    capture_moves.append(tmp_location)

        # Moves for rooks
        # TODO Refactor this mess
        if self.piece_type == "rook":
            temp_location = first_location
            capture = False
            while self.is_move_in_bounds(temp_location) and (not capture):
                temp_location = (
                    temp_location[0],
                    temp_location[1] - square_size,
                )
                if self.is_obstructed(temp_location):
                    break
                if not self.is_capture(temp_location):
                    moves.append(temp_location)
                else:
                    capture_moves.append(temp_location)
                    capture = True
            temp_location = first_location
            capture = False
            while self.is_move_in_bounds(temp_location) and (not capture):
                temp_location = (
                    temp_location[0],
                    temp_location[1] + square_size,
                )
                if self.is_obstructed(temp_location):
                    break
                if not self.is_capture(temp_location):
                    moves.append(temp_location)
                else:
                    capture_moves.append(temp_location)
                    capture = True
            temp_location = first_location
            capture = False
            while self.is_move_in_bounds(temp_location) and (not capture):
                temp_location = (
                    temp_location[0] + square_size,
                    temp_location[1],
                )
                if self.is_obstructed(temp_location):
                    break
                if not self.is_capture(temp_location):
                    moves.append(temp_location)
                else:
                    capture_moves.append(temp_location)
                    capture = True
            temp_location = first_location
            capture = False
            while self.is_move_in_bounds(temp_location) and (not capture):
                temp_location = (
                    temp_location[0] - square_size,
                    temp_location[1],
                )
                if self.is_obstructed(temp_location):
                    break
                if not self.is_capture(temp_location):
                    moves.append(temp_location)
                else:
                    capture_moves.append(temp_location)
                    capture = True

        # Moves for bishops
        # TODO Refactor this mess
        if self.piece_type == "bishop":
            temp_location = first_location
            capture = False
            while self.is_move_in_bounds(temp_location) and (not capture):
                temp_location = (
                    temp_location[0] - square_size,
                    temp_location[1] - square_size,
                )
                if self.is_obstructed(temp_location):
                    break
                if not self.is_capture(temp_location):
                    moves.append(temp_location)
                else:
                    capture_moves.append(temp_location)
                    capture = True
            temp_location = first_location
            capture = False
            while self.is_move_in_bounds(temp_location) and (not capture):
                temp_location = (
                    temp_location[0] + square_size,
                    temp_location[1] + square_size,
                )
                if self.is_obstructed(temp_location):
                    break
                if not self.is_capture(temp_location):
                    moves.append(temp_location)
                else:
                    capture_moves.append(temp_location)
                    capture = True
            temp_location = first_location
            capture = False
            while self.is_move_in_bounds(temp_location) and (not capture):
                temp_location = (
                    temp_location[0] + square_size,
                    temp_location[1] - square_size,
                )
                if self.is_obstructed(temp_location):
                    break
                if not self.is_capture(temp_location):
                    moves.append(temp_location)
                else:
                    capture_moves.append(temp_location)
                    capture = True
            temp_location = first_location
            capture = False
            while self.is_move_in_bounds(temp_location) and (not capture):
                temp_location = (
                    temp_location[0] - square_size,
                    temp_location[1] + square_size,
                )
                if self.is_obstructed(temp_location):
                    break
                if not self.is_capture(temp_location):
                    moves.append(temp_location)
                else:
                    capture_moves.append(temp_location)
                    capture = True

        # Eliminate illegal moves
        final_moves = []
        for move in moves:
            illegal = False
            for name, piece in white_pieces.pieces.items():
                if move == piece.location:
                    illegal = True
            if illegal:
                continue
            for name, piece in black_pieces.pieces.items():
                if move == piece.location:
                    illegal = True
            if illegal:
                continue
            if not self.is_move_in_bounds(move):
                illegal = True
            if illegal:
                continue
            final_moves.append(move)
        return final_moves, capture_moves

    def indicate_moves(self, psb_moves):
        for possible_move in psb_moves:
            square = pygame.Rect(
                possible_move[0] + square_size // 4,
                possible_move[1] + square_size // 4,
                square_size // 2,
                square_size // 2,
            )
            pygame.draw.rect(display, MOVE, square)

    def indicate_captures(self, psb_captures):
        for possible_capture in psb_captures:
            square = pygame.Rect(
                possible_capture[0], possible_capture[1], square_size, square_size,
            )
            pygame.draw.rect(display, CAPTURE, square)

    def is_capture(self, mv):
        if self.color == "black":
            for name, piece in white_pieces.pieces.items():
                if mv == piece.location:
                    return True
        else:
            for name, piece in black_pieces.pieces.items():
                if mv == piece.location:
                    return True
        return False

    def is_obstructed(self, mv):
        if self.color == "white":
            for name, piece in white_pieces.pieces.items():
                if mv == piece.location:
                    return True
        else:
            for name, piece in black_pieces.pieces.items():
                if mv == piece.location:
                    return True
        return False

    def is_move_in_bounds(self, mv):
        if mv[0] < 0 or mv[0] >= board_size or mv[1] < 0 or mv[1] >= board_size:
            return False
        return True


def draw_grid():

    for j in range(0, display_width, square_size * 2):
        for k in range(square_size, display_height, square_size * 2):
            square = pygame.Rect(j, k, square_size, square_size)
            pygame.draw.rect(display, DARK, square)

    for j in range(square_size, display_width, square_size * 2):
        for k in range(0, display_height, square_size * 2):
            square = pygame.Rect(j, k, square_size, square_size)
            pygame.draw.rect(display, DARK, square)

    for i in range(0, display_width, square_size):
        pygame.draw.line(display, BLACK, (i, 0), (i, display_height), 1)
        pygame.draw.line(display, BLACK, (0, i), (display_width, i), 1)

    return display.copy()


def check_collisions(mouse_pos, pieces):
    for name, piece in pieces.pieces.items():
        if piece.location[0] < mouse_pos[0] < piece.location[0] + square_size:
            if piece.location[1] < mouse_pos[1] < piece.location[1] + square_size:
                return piece
    return None


def snap_piece(piece):
    offset_x = piece.location[0] % square_size
    offset_y = piece.location[1] % square_size
    if offset_x > square_size // 2:
        offset_x -= square_size
    if offset_y > square_size // 2:
        offset_y -= square_size
    snapped_location = (piece.location[0] - offset_x, piece.location[1] - offset_y)
    piece.location = snapped_location


def capture_at_location(capturing_piece, location):
    if capturing_piece.color == "white":
        for name, piece in black_pieces.pieces.items():
            if piece.location == location:
                piece_to_capture = name
                black_pieces.pieces.pop(piece_to_capture)
                break
    else:
        for name, piece in white_pieces.pieces.items():
            if piece.location == location:
                piece_to_capture = name
                white_pieces.pieces.pop(piece_to_capture)
                break


board = draw_grid()
white_pieces = Set("white", True)
black_pieces = Set("black", False)

current_player = white_pieces


def change_player(player):
    if player is white_pieces:
        player = black_pieces
    else:
        player = white_pieces
    return player


is_picked_piece = False
picked_piece = None
checkmate = False

# Main game loop
while not checkmate:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # If the player isn't already holding a piece, pick up the piece
            if not is_picked_piece:
                mouse_position = pygame.mouse.get_pos()
                picked_piece = check_collisions(mouse_position, current_player)
                if picked_piece is not None:
                    pick_location = picked_piece.location
                    possible_moves_to_play, captures = picked_piece.possible_moves(
                        pick_location
                    )
                    picked_piece.indicate_moves(possible_moves_to_play)
                    is_picked_piece = True
            # Release piece
            else:
                snap_piece(picked_piece)
                if picked_piece.location in captures:
                    capture_at_location(picked_piece, picked_piece.location)
                    picked_piece.is_moved = True
                    current_player = change_player(current_player)
                elif picked_piece.location in possible_moves_to_play:
                    if pick_location != picked_piece.location:
                        picked_piece.is_moved = True
                    current_player = change_player(current_player)
                else:
                    picked_piece.location = pick_location
                picked_piece = None
                is_picked_piece = False

    # Draw board

    display.blit(board, (0, 0))

    # Get picked piece's location and draw possible moves

    if is_picked_piece and picked_piece is not None:
        mouse_pos = pygame.mouse.get_pos()
        picked_piece.location = (
            mouse_pos[0] - square_size // 2,
            mouse_pos[1] - square_size // 2,
        )
        picked_piece.indicate_moves(possible_moves_to_play)
        picked_piece.indicate_captures(captures)

    # Draw pieces

    for name, piece in white_pieces.pieces.items():
        display.blit(piece.image, piece.location)

    for name, piece in black_pieces.pieces.items():
        display.blit(piece.image, piece.location)

    if picked_piece is not None:
        display.blit(picked_piece.image, picked_piece.location)

    pygame.display.update()
    clock.tick(60)
