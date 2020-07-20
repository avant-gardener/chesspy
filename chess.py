""" Chess implementation in python """
import pygame
import copy

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

UP = False
DOWN = True
LEFT = False
RIGHT = True
diagonals = [[RIGHT, UP], [RIGHT, DOWN], [LEFT, UP], [LEFT, DOWN]]
lines = [[RIGHT, None], [LEFT, None], [None, UP], [None, DOWN]]
knight_moves = [
    [[None, UP], [None, UP], [LEFT, None]],
    [[None, UP], [None, UP], [RIGHT, None]],
    [[None, DOWN], [None, DOWN], [RIGHT, None]],
    [[None, DOWN], [None, DOWN], [LEFT, None]],
    [[LEFT, None], [LEFT, None], [None, UP]],
    [[LEFT, None], [LEFT, None], [None, DOWN]],
    [[RIGHT, None], [RIGHT, None], [None, UP]],
    [[RIGHT, None], [RIGHT, None], [None, DOWN]],
]

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
                first_pawn_move = (first_location[0], first_location[1] - square_size)
                moves.append(first_pawn_move)
                if not self.is_moved and not self.is_obstructed(first_pawn_move):
                    moves.append(
                        (first_location[0], first_location[1] - square_size * 2)
                    )

                tmp_location = self.calculate_move(first_location, RIGHT, UP)
                if self.is_capture(tmp_location):
                    capture_moves.append(tmp_location)

                tmp_location = self.calculate_move(first_location, LEFT, UP)
                if self.is_capture(tmp_location):
                    capture_moves.append(tmp_location)

        # Moves for black pawn
        else:
            if self.piece_type == "pawn":
                first_pawn_move = (first_location[0], first_location[1] + square_size)
                moves.append(first_pawn_move)
                if not self.is_moved and not self.is_obstructed(first_pawn_move):
                    moves.append(
                        (first_location[0], first_location[1] + square_size * 2)
                    )

                tmp_location = self.calculate_move(first_location, RIGHT, DOWN)
                if self.is_capture(tmp_location):
                    capture_moves.append(tmp_location)

                tmp_location = self.calculate_move(first_location, LEFT, DOWN)
                if self.is_capture(tmp_location):
                    capture_moves.append(tmp_location)

        # Moves for knights
        if self.piece_type == "knight":
            for knight_move in knight_moves:
                location = first_location
                for step in knight_move:
                    location = self.calculate_move(location, step[0], step[1])
                moves, capture_moves, continue_pass = self.capture_move_or_break(
                    location, moves, capture_moves
                )

        # Moves for bishops
        elif self.piece_type == "bishop":
            moves, capture_moves = self.calculate_all_diagonals(
                first_location, moves, capture_moves
            )

        # Moves for rooks
        elif self.piece_type == "rook":
            moves, capture_moves = self.calculate_all_lines(
                first_location, moves, capture_moves
            )

        # Moves for queen
        elif self.piece_type == "queen":
            moves, capture_moves = self.calculate_all_diagonals(
                first_location, moves, capture_moves
            )
            moves, capture_moves = self.calculate_all_lines(
                first_location, moves, capture_moves
            )

        # Moves for king
        elif self.piece_type == "king":
            for diagonal in diagonals:
                temp_location = self.calculate_move(
                    first_location, diagonal[0], diagonal[1]
                )
                moves, capture_moves, continue_pass = self.capture_move_or_break(
                    temp_location, moves, capture_moves
                )
            for line in lines:
                temp_location = self.calculate_move(first_location, line[0], line[1])
                moves, capture_moves, continue_pass = self.capture_move_or_break(
                    temp_location, moves, capture_moves
                )

        # Eliminate illegal moves
        final_moves = []
        for move in moves:
            if not self.is_obstructed(move) and self.is_move_in_bounds(move):
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
        for name, piece in white_pieces.pieces.items():
            if mv == piece.location:
                return True
        for name, piece in black_pieces.pieces.items():
            if mv == piece.location:
                return True
        return False

    def will_there_be_check(self, mv):
        if self.color == "white":
            copy_pieces = copy_set(white_pieces)
            copy_pieces.pieces[self.piece_name].location = mv
            if is_there_a_check(copy_pieces, black_pieces):
                return True
        else:
            copy_pieces = copy_set(black_pieces)
            copy_pieces.pieces[self.piece_name].location = mv
            if is_there_a_check(copy_pieces, white_pieces):
                return True
        return False

    def is_move_in_bounds(self, mv):
        if mv[0] < 0 or mv[0] >= board_size or mv[1] < 0 or mv[1] >= board_size:
            return False
        return True

    def capture_move_or_break(self, mv, regular_mvs, capture_mvs):
        will_continue = True
        if not self.is_move_in_bounds(mv):
            will_continue = False
        elif self.is_capture(mv):
            capture_mvs.append(mv)
            will_continue = False
        elif not self.is_obstructed(mv):
            regular_mvs.append(mv)
        else:
            will_continue = False

        return regular_mvs, capture_mvs, will_continue

    def calculate_move(self, mv, first, second):
        if first is None:
            x = mv[0]
        elif first:
            x = mv[0] + square_size
        else:
            x = mv[0] - square_size

        if second is None:
            y = mv[1]
        elif second:
            y = mv[1] + square_size
        else:
            y = mv[1] - square_size

        return (x, y)

    def calculate_all_diagonals(self, start, mvs, captures):
        for diagonal in diagonals:
            mvs, captures = self.calc_moves_in_direction(
                start, diagonal[0], diagonal[1], mvs, captures
            )
        return mvs, captures

    def calculate_all_lines(self, start, mvs, captures):
        for line in lines:
            mvs, captures = self.calc_moves_in_direction(
                start, line[0], line[1], mvs, captures
            )
        return mvs, captures

    def calc_moves_in_direction(self, start, dir1, dir2, mvs, capture_mvs):
        temp_location = start
        continue_pass = True
        while continue_pass:
            temp_location = self.calculate_move(temp_location, dir1, dir2)
            mvs, capture_mvs, continue_pass = self.capture_move_or_break(
                temp_location, mvs, capture_mvs
            )
        return mvs, capture_mvs


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


def is_there_a_check(pieces, threatening_set):
    for name, attacking_piece in threatening_set.pieces.items():
        mvs, capture_mvs = attacking_piece.possible_moves(attacking_piece.location)
        if is_threatening_check(attacking_piece, capture_mvs, pieces):
            return True
    return False


def is_threatening_check(piece, capture_moves_of_piece, threatened_set):
    for capture_move in capture_moves_of_piece:
        if capture_move == threatened_set.pieces["king"].location:
            return True
    return False


def copy_set(piece_set):
    set_copy = Set(piece_set.color, piece_set.is_player)
    for name, piece in piece_set.pieces.items():
        set_copy.pieces[name].location = piece.location
    return set_copy


board = draw_grid()
white_pieces = Set("white", True)
black_pieces = Set("black", False)

current_player = white_pieces
other_player = black_pieces


def change_player(player, second_player):
    if player is white_pieces:
        player = black_pieces
        second_player = white_pieces
    else:
        player = white_pieces
        second_player = black_pieces
    return player, second_player


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
                if is_there_a_check(current_player, other_player):
                    picked_piece.location = pick_location
                elif picked_piece.location in captures:
                    capture_at_location(picked_piece, picked_piece.location)
                    picked_piece.is_moved = True
                    current_player, other_player = change_player(
                        current_player, other_player
                    )
                elif picked_piece.location in possible_moves_to_play:
                    if pick_location != picked_piece.location:
                        picked_piece.is_moved = True
                    current_player, other_player = change_player(
                        current_player, other_player
                    )
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
