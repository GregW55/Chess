import pygame
from config import *
import time

pygame.init()


class Board:
    def __init__(self, chess_instance):
        self.chess = chess_instance
        self.board_white = (235, 236, 208)
        self.board_green = (118, 146, 85)
        self.grid_color = "black"
        self.panel_color = "black"
        self.border_color = "black"
        self.ff_button_color = "black"
        self.ff_text = "FORFEIT"
        self.ff_button = pygame.Rect(800, 800, 200, 100)
        self.status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                            'Black: Select a Piece to Move!', 'Black: Select a Destination!']

    @staticmethod
    def coords_to_alg(coords):
        file_letter = chr(ord('a') + coords[0])
        rank_number = 8 - coords[1]
        return f"{file_letter}{rank_number}"

    @staticmethod
    def alg_to_coords(algebraic):
        file_letter = algebraic[0]
        y = int(str(algebraic)[1:]) - 1
        x = ord(file_letter) - ord('a')
        y = 7 - y
        return x, y

    def draw_board(self):
        screen.fill(self.board_white)  # Fill screen
        # Loop through each row and column of the 8x8 grid
        for row in range(8):
            for col in range(8):
                square_name = self.coords_to_alg((col, row))  # Reverse y coords to fix algebraic notation
                # Calculate coordinates for each square
                x = col * 100
                y = row * 100

                # Determine color based on row and column indices
                if (row + col) % 2 == 0:
                    pygame.draw.rect(screen, self.board_white, [x, y, 100, 100])
                else:
                    pygame.draw.rect(screen, self.board_green, [x, y, 100, 100])
                square_text = font.render(square_name, True, 'black')
                screen.blit(square_text, (x + 5, y + 5))
        # Draw the bottom panel of the screen
        # pygame.draw.rect(screen, self.panel_color, [0, 800, WIDTH, 100])

        # Draw a border around the bottom panel
        pygame.draw.rect(screen, self.border_color, [0, 800, WIDTH, 100], 5)

        # Draw a border around the right panel of the screen
        pygame.draw.rect(screen, self.border_color, [800, 0, 200, HEIGHT], 5)

        # Display current game status text based on turn_step
        screen.blit(big_font.render(self.status_text[self.chess.turn_step], True, self.ff_button_color), (20, 820))

        # Draw grid lines on the board
        for i in range(9):
            pygame.draw.line(screen, self.grid_color, (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, self.grid_color, (100 * i, 0), (100 * i, 800), 2)

            # Draw the "FORFEIT" text on the forfeit button area
            screen.blit(medium_font.render(self.ff_text, True, self.ff_button_color), (810, 830))

    def draw_pieces(self):
        for i in range(len(self.chess.white_pieces)):
            index = piece_list.index(self.chess.white_pieces[i])
            x, y = self.alg_to_coords(self.chess.white_locations[i])

            if self.chess.white_pieces[i] == 'pawn':
                screen.blit(white_pawn, (x * 100 + 22, y * 100 + 30))
            else:
                screen.blit(white_images[index], (x * 100 + 10, y * 100 + 10))
            if self.chess.turn_step < 2:
                if self.chess.white_selection == i:
                    pygame.draw.rect(screen, 'red', [x * 100 + 1, y * 100 + 1, 100, 100], 2)

        for i in range(len(self.chess.black_pieces)):
            index = piece_list.index(self.chess.black_pieces[i])
            x, y = self.alg_to_coords(self.chess.black_locations[i])

            if self.chess.black_pieces[i] == 'pawn':
                screen.blit(black_pawn, (x * 100 + 22, y * 100 + 30))
            else:
                screen.blit(black_images[index], (x * 100 + 10, y * 100 + 10))
            if self.chess.turn_step >= 2:
                if self.chess.black_selection == i:
                    pygame.draw.rect(screen, 'blue', [x * 100 + 1, y * 100 + 1, 100, 100], 2)

    def draw_check(self):
        if self.chess.white_check:
            king_location = self.chess.white_locations[self.chess.white_pieces.index('king')]
            x, y = self.alg_to_coords(king_location)
            if self.chess.counter < 15:
                pygame.draw.rect(screen, 'dark red', [x * 100 + 1,
                                                      y * 100 + 1, 100, 100], 10)
        elif self.chess.black_check:
            king_location = self.chess.black_locations[self.chess.black_pieces.index('king')]
            x, y = self.alg_to_coords(king_location)
            if self.chess.counter < 15:
                pygame.draw.rect(screen, 'dark blue', [x * 100, y * 100, 100, 100], 10)

    def draw_captured(self):
        for i in range(len(self.chess.captured_pieces_white)):
            captured_piece = self.chess.captured_pieces_white[i]
            index = piece_list.index(captured_piece)
            screen.blit(small_black_images[index], (825, 5 + 50 * i))
        for i in range(len(self.chess.captured_pieces_black)):
            captured_piece = self.chess.captured_pieces_black[i]
            index = piece_list.index(captured_piece)
            screen.blit(small_white_images[index], (925, 5 + 50 * i))

    def draw_valid(self, moves):
        color = 'blue' if self.chess.turn_step < 2 else 'red'
        if len(moves) > 0:
            for i in range(len(moves)):  # Draw circles to indicate valid move options
                moves_x, moves_y = self.alg_to_coords(moves[i])
                pygame.draw.circle(screen, color, (moves_x * 100 + 50, moves_y * 100 + 50), 5)

    def draw_temp_check(self):
        if self.chess.turn_step < 2:
            king_location = self.chess.white_locations[self.chess.white_pieces.index('king')]
            if self.chess.counter < 15:
                pygame.draw.rect(screen, 'dark red', [ord(king_location[0]) * 100 + 1,
                                                      (7 - int(king_location[1])) * 100 + 1, 100, 100], 10)
        elif self.chess.turn_step >= 2:
            if self.chess.counter < 15:
                king_location = self.chess.black_locations[self.chess.black_pieces.index('king')]
                pygame.draw.rect(screen, 'dark blue', [ord(king_location[0]) * 100 + 1,
                                                       (7 - int(king_location[1])) * 100 + 1, 100, 100], 10)

    def draw_game_over(self):
        pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
        screen.blit(font.render(f'{self.chess.winner} won the game!', True, 'white'), (210, 210))
        screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

    @staticmethod
    def draw_draw3():
        pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
        screen.blit(font.render(f'The game resulted in a draw due to the Three Fold Repetition rule!', True, 'white'),
                    (210, 210))
        screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

    @staticmethod
    def draw_draw50():
        pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
        screen.blit(font.render(f'The game resulted in a draw due to the Fifty-Move rule!', True, 'white'), (210, 210))
        screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

    @staticmethod
    def draw_stalemate():
        pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
        screen.blit(font.render(f'The game resulted in a stalemate due to lack of moves!', True, 'white'), (210, 210))
        screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))


class Chess:
    def __init__(self):
        self.rooks_moved = {'white': [False, False], 'black': [False, False]}  # Track rook movement for castling
        self.kings_moved = {'white': False, 'black': False}  # Track king movement for castling
        self.all_options = None  # Track all options for AI to learn from later
        self.last_move = None  # Track last move for en passant
        self.captured_pieces_white = []  # Track captured pieces to draw on screen
        self.captured_pieces_black = []  # Track captured pieces to draw on screen
        self.winner = ''
        self.counter = 0
        self.white_move_counter = 0  # Used for the 50 rule
        self.black_move_counter = 0  # Used for the 50 rule
        self.done = False
        self.run = True
        self.white_check = False  # Track if the white player is in check
        self.black_check = False  # Track if the black player is in check
        self.history = []  # Track every move that has happened in the current game
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.board = Board(self)  # Used to draw the board and pieces
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.turn_step = 0  # 0- whites turn no selection, 1: piece selected, 2 and 3 same for blacks turn
        self.white_selection = 100  # Default number to determine if white has selected a piece
        self.black_selection = 100  # Default number to determine if black has selected a piece
        self.white_moves = []  # Track the valid moves
        self.black_moves = []  # Track the valid moves

        self.white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                             'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        self.black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                             'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        self.white_locations = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
                                'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
        self.black_locations = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
                                'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']

        self.white_options = self.check_options('white')  # All possible white moves, including fatal moves
        self.black_options = self.check_options('black')  # All possible black moves, including fatal moves

    # Check all valid moves per piece
    def check_king(self, position, color):
        moves_list = []
        friends_list = self.white_locations if color == 'white' else self.black_locations
        enemies_list = self.black_locations if color == 'white' else self.white_locations
        file = ord(position[0])  # Use the ASCII value of a letter to do 1:1 changes
        rank = int(position[1])  # Convert the rank into an integer from a string to allow calculations
        directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]

        # Include castling moves if conditions are met
        if color == 'white' and position == 'e1' and not self.kings_moved['white'] and not self.white_check:
            # Check queenside castling for white
            if 'a1' in friends_list and friends_list.index('a1') == 0 and not self.rooks_moved['white'][0]:
                if 'b1' not in friends_list and 'c1' not in friends_list and 'd1' not in friends_list:
                    if 'b1' not in enemies_list and 'c1' not in enemies_list and 'd1' not in enemies_list:
                        moves_list.append('b1')
            # Check kingside castling for white
            if 'h1' in friends_list and friends_list.index('h1') == 7 and not self.rooks_moved['white'][1]:
                if 'f1' not in friends_list and 'g1' not in friends_list:
                    if 'f1' not in enemies_list and 'g1' not in enemies_list:
                        moves_list.append('g1')

        elif color == 'black' and position == 'e8' and not self.kings_moved['black'] and not self.white_check:
            # Check queenside castling for white
            if 'a8' in friends_list and friends_list.index('a8') == 0 and not self.rooks_moved['black'][0]:
                if 'b8' not in friends_list and 'c8' not in friends_list and 'd8' not in friends_list:
                    if 'b8' not in enemies_list and 'c8' not in enemies_list and 'd8' not in enemies_list:
                        moves_list.append('b8')
            # Check kingside castling for white
            if 'h8' in friends_list and friends_list.index('h8') == 7 and not self.rooks_moved['black'][1]:
                if 'f8' not in friends_list and 'g8' not in friends_list:
                    if 'f8' not in enemies_list and 'g8' not in enemies_list:
                        moves_list.append('g8')

        # Straight forward king can only move one space at a time, avoiding all friendly pieces
        # Loops through each pattern of directions to check if the player can move that way
        for x, y in directions:
            # Convert the ASCII value back into its character form
            new_file = chr(file + x)
            new_rank = rank + y
            if 'a' <= new_file <= 'h' and 1 <= new_rank <= 8:  # Make sure it's in the bounds of the board
                new_position = f"{new_file}{new_rank}"  # Append as a string to keep the correct formatting
                if new_position not in friends_list:
                    moves_list.append(new_position)
        return moves_list

    def check_rook(self, position, color):
        #  Castling logic purely inside the check_king function
        moves_list = []
        friends_list = self.white_locations if color == 'white' else self.black_locations
        enemies_list = self.black_locations if color == 'white' else self.white_locations
        file = ord(position[0])  # Converting the current file into its ASCII value (for example 'a' = 97)
        rank = int(position[1])  # Convert the current rank into an integer for calculations
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Rook can only move 4 directions (up, down, left, right)
        # Loop through each possible direction
        for x, y in directions:
            path = True  # This checks if the rook should continue going or if its hit another piece/end of board
            chain = 1
            while path:  # Go forward one at a time to determine if each square is an eligible move
                new_file = chr(file + (chain * x))
                new_rank = rank + (chain * y)
                if 'a' <= new_file <= 'h' and 1 <= new_rank <= 8:
                    new_position = f"{new_file}{new_rank}"
                    if new_position not in friends_list:
                        moves_list.append(new_position)
                        if new_position in enemies_list:
                            path = False
                        chain += 1
                    else:
                        path = False
                else:
                    path = False
        return moves_list

    def check_bishop(self, position, color):
        moves_list = []
        friends_list = self.white_locations if color == 'white' else self.black_locations
        enemies_list = self.black_locations if color == 'white' else self.white_locations
        file = ord(position[0])
        rank = int(position[1])
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for x, y in directions:
            path = True
            chain = 1
            while path:
                new_file = chr(file + (chain * x))
                new_rank = rank + (chain * y)
                if 'a' <= new_file <= 'h' and 1 <= new_rank <= 8:
                    new_position = f"{new_file}{new_rank}"
                    if new_position not in friends_list:
                        moves_list.append(new_position)
                        if new_position in enemies_list:
                            path = False
                        chain += 1
                    else:
                        path = False
                else:
                    path = False
        return moves_list

    def check_queen(self, position, color):
        # Uses both the rook and bishops move, as it's just a combination of the two
        moves_list = self.check_bishop(position, color)
        second_list = self.check_rook(position, color)
        for i in range(len(second_list)):
            moves_list.append(second_list[i])
        return moves_list

    def check_pawn(self, position, color):
        moves_list = []
        friends_list = self.white_locations if color == 'white' else self.black_locations
        enemies_list = self.black_locations if color == 'white' else self.white_locations
        file = ord(position[0])
        rank = int(position[1])
        if color == 'white':
            direction = 1  # White pawns move towards higher ranks(numbers)
            start_rank = 2  # White pawns start at rank 2
            # promotion_rank = 7  # White pawns reach rank 8 (1 based index)
            capture_directions = [(1, 1), (-1, 1)]  # Diagonal capture directions
        else:
            direction = -1  # Black pawns move towards lower ranks(numbers)
            start_rank = 7  # Black pawns start at rank 7
            # promotion_rank = 0  # Black pawns reach rank 1
            capture_directions = [(1, -1), (-1, -1)]  # Diagonal capture directions

        # Move forward one square
        new_file = chr(file)
        new_rank = rank + direction
        new_position = f"{new_file}{new_rank}"
        if new_position not in friends_list and new_position not in enemies_list:
            moves_list.append(new_position)

        # Move forward two squares from the starting position
        if rank == start_rank:
            new_rank = rank + 2 * direction
            new_position_1 = f"{new_file}{new_rank - 1}" if color == 'white' else f"{new_file}{new_rank + 1}"
            new_position = f"{new_file}{new_rank}"
            # Check both ranks being moved on so make sure pawn doesn't go over an enemy or friendly piece
            if new_position not in friends_list and new_position not in enemies_list:
                if new_position_1 not in friends_list and new_position_1 not in enemies_list:
                    moves_list.append(new_position)

        # Capture diagonally
        for x, y in capture_directions:
            new_file = chr(file + x)
            new_rank = rank + y
            new_position = f"{new_file}{new_rank}"
            if new_position in enemies_list:
                moves_list.append(new_position)

        # En Passant Logic
        if self.last_move is not None and self.last_move[2] == 'pawn':  # Check if last move was a pawn
            file = ord(position[0]) - ord('a')
            rank = rank
            if color == 'white':
                if self.last_move[1][1] - self.last_move[0][1] == 2:  # Check if the pawn moved 2 spaces
                    if rank == (self.last_move[1][1] - 8) * -1:  # Check if the pawns are at the same rank(y)
                        # Check if the pawn is one file away(x)
                        if file - self.last_move[1][0] == 1 or file - self.last_move[1][0] == -1:
                            new_file = chr(self.last_move[1][0] + ord('a'))
                            new_rank = rank
                            new_position = f"{new_file}{new_rank}"
                            moves_list.append(new_position)
            elif color == 'black':
                if self.last_move[1][1] - self.last_move[0][1] == -2:  # Check if the pawn moved 2 spaces
                    if rank == (self.last_move[1][1] - 8) * -1:  # Check if the pawns are at the same rank(y)
                        # Check if the pawn is one file away(y)
                        if file - self.last_move[1][0] == 1 or file - self.last_move[1][0] == -1:
                            new_file = chr(self.last_move[1][0] + ord('a'))
                            new_rank = rank
                            new_position = f"{new_file}{new_rank}"
                            moves_list.append(new_position)
        return moves_list

    def check_knight(self, position, color):
        moves_list = []
        friends_list = self.white_locations if color == 'white' else self.black_locations
        file = ord(position[0])
        rank = int(position[1])

        # Knight moves: two squares in one direction and one in another
        targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        for target in targets:
            new_file = chr(file + target[0])
            new_rank = rank + target[1]
            if 'a' <= new_file <= 'h' and 1 <= new_rank <= 8:
                new_position = f"{new_file}{new_rank}"
                if new_position not in friends_list:
                    moves_list.append(new_position)
        return moves_list

    # Function to check all pieces valid options on board
    def check_options(self, color):
        moves_list = []
        all_moves = []
        if color == 'white':
            locations = self.white_locations
            pieces = self.white_pieces
        else:
            locations = self.black_locations
            pieces = self.black_pieces
        for i in range((len(pieces))):  # Gets each pieces location and type of piece
            position = locations[i]
            piece = pieces[i]
            if piece == 'king':
                moves = self.check_king(position, color)
                moves_list.append(moves)
                all_moves.append(('king', color, moves))
            elif piece == 'rook':
                moves = self.check_rook(position, color)
                moves_list.append(moves)
                all_moves.append(('rook', color, moves))
            elif piece == 'knight':
                moves = self.check_knight(position, color)
                moves_list.append(moves)
                all_moves.append(('knight', color, moves))
            elif piece == 'bishop':
                moves = self.check_bishop(position, color)
                moves_list.append(moves)
                all_moves.append(('bishop', color, moves))
            elif piece == 'queen':
                moves = self.check_queen(position, color)
                moves_list.append(moves)
                all_moves.append(('queen', color, moves))
            elif piece == 'pawn':
                moves = self.check_pawn(position, color)
                moves_list.append(moves)
                all_moves.append(('pawn', color, moves))
            self.all_options = all_moves

        return moves_list

    def check_valid_moves(self, color):
        # This function only appends moves from each list that keep the player out of check using move_puts_in_check()
        # If a move would put a player in check that move is deemed invalid and not appended to the list
        valid_moves = []
        valid_moves_selection = None
        if color == 'white':  # Whites turn
            options_list = self.white_options
            if self.white_selection != 100:
                valid_moves_selection = options_list[self.white_selection]
        else:  # Blacks turn
            options_list = self.black_options
            if self.black_selection != 100:
                valid_moves_selection = options_list[self.black_selection]
        for i in range(len(options_list)):
            for move in options_list[i]:
                if not self.move_puts_in_check('white' if color == 'white' else 'black', i, move):
                    valid_moves.append(move)

        return valid_moves, valid_moves_selection

    def check(self, color):
        if color == 'white':  # Whites turn
            king_index = self.white_pieces.index('king')
            king_location = self.white_locations[king_index]
            self.black_options = self.check_options('black')
            #  Check all blacks available options to see if the white king is in any of them
            for i in range(len(self.black_options)):
                if self.black_options[i]:
                    if king_location in self.black_options[i]:  # If the king is in a move, white is in check
                        self.white_check = True
                        self.board.draw_check()  # Draw the check visually

        else:  # Blacks turn
            king_index = self.black_pieces.index('king')
            king_location = self.black_locations[king_index]
            self.white_options = self.check_options('white')
            for i in range(len(self.white_options)):  # Check all whites options for blacks king
                if self.white_options[i]:
                    if king_location in self.white_options[i]:  # If the king is in a move, black is in check
                        self.black_check = True
                        self.board.draw_check()  # Draw the check visually

    def move_puts_in_check(self, color, piece_index, move):
        # Disallows moves that put the player in check using temporary moves to simulate possible outcomes
        temp_locations = self.white_locations[:] if color == 'white' else self.black_locations[:]
        temp_pieces = self.white_pieces[:] if color == 'white' else self.black_pieces[:]
        temp_white_check = self.white_check
        temp_black_check = self.black_check
        if piece_index < len(temp_locations):
            temp_locations[piece_index] = move
            if move in temp_locations:
                temp_pieces.pop(temp_locations.index(move))
                temp_locations.remove(move)

            self.check(color)
            in_check = self.white_check if color == 'white' else self.black_check

            self.white_check = temp_white_check
            self.black_check = temp_black_check
            return in_check

    def is_checkmate(self, color):
        if color == 'white':
            self.white_moves, valid_moves_selection = self.check_valid_moves('white')
            if self.white_moves:
                return False
            else:
                return True
        else:
            self.black_moves, valid_moves_selection = self.check_valid_moves('black')
            if self.black_moves:
                return False
            else:
                return True

    def add_to_history(self, starting_position, ending_position, piece, color):
        boardstate = self.white_locations + self.black_locations
        move = {
            'start': starting_position,
            'end': ending_position,
            'color': color,
            'piece': piece,
            'boardstate': boardstate
        }
        self.history.append(move)

    def get_history(self):
        return self.history

    def check_threefold_repetition(self):
        board_states = [tuple(move['boardstate']) for move in self.history]
        unique_states = set(board_states)

        for state in unique_states:
            if board_states.count(state) >= 3:
                return True

        return False

    def white_move(self, starting_position, click_alg):
        # Check if whites move will put them in check
        temp_location = self.white_locations[self.white_selection]
        temp_black_locations = self.black_locations[:]
        temp_black_pieces = self.black_pieces[:]
        self.white_locations[self.white_selection] = click_alg
        self.white_check = False
        if click_alg in self.black_locations:
            black_piece = self.black_locations.index(click_alg)
            self.black_locations.pop(black_piece)
            self.black_pieces.pop(black_piece)
        self.check('white')
        self.black_locations = temp_black_locations
        self.black_pieces = temp_black_pieces
        if not self.white_check:
            self.white_move_counter += 1
            # Check if the player is castling and move the rook
            if self.white_pieces[self.white_selection] == 'king':
                if click_alg == 'b1' and not self.kings_moved['white'] and not self.rooks_moved['white'][0]:
                    self.white_locations[0] = 'c1'  # Move the rook
                    self.kings_moved['white'] = True
                elif click_alg == 'g1' and not self.kings_moved['white'] and not self.rooks_moved['white'][1]:
                    self.white_locations[7] = 'f1'  # Move the rook
                    self.kings_moved['white'] = True
            #  Check if the player has moved a pawn or captured a piece for the fifty-move rule
            if self.white_pieces[self.white_selection] == 'pawn':
                self.white_move_counter = 0
                # Pawn promotion, for now only allows queen promotion
                if click_alg[1] == '8':
                    self.white_pieces[self.white_selection] = 'queen'
            if click_alg in self.black_locations:
                self.white_move_counter = 0

            if self.white_selection in [0, 4, 7]:
                if self.white_selection in [0, 7]:
                    self.rooks_moved['white'][self.white_selection // 7] = True
                else:
                    self.kings_moved['white'] = True
            # if not in check, update the pieces and options
            self.white_locations[self.white_selection] = click_alg  # Apply the move
            if click_alg in self.black_locations:
                black_piece = self.black_locations.index(click_alg)
                self.captured_pieces_white.append(self.black_pieces[black_piece])
                self.black_locations.pop(black_piece)
                self.black_pieces.pop(black_piece)
                # Check for checkmate
                self.check('black')
                if self.black_check and self.is_checkmate('black'):
                    self.winner = 'white'

            ending_position = click_alg  # Track the ending position of the move
            self.add_to_history(starting_position, ending_position, self.white_pieces[self.white_selection],
                                color='white')
            self.last_move = [self.board.alg_to_coords(starting_position), self.board.alg_to_coords(ending_position),
                              self.white_pieces[self.white_selection]]
            self.turn_step = 2
            self.white_selection = 100
            self.black_selection = 100

            if not self.white_moves and not self.white_check:
                self.winner = 'stalemate'
                self.done = True

        else:
            # If in check, disallow the move
            self.board.draw_temp_check()
            self.white_locations[self.white_selection] = temp_location  # Revert the move
            self.white_selection = 100
            self.turn_step = 0

    def black_move(self, starting_position, click_alg):
        # Check if blacks move will put them in check
        temp_location = self.black_locations[self.black_selection]
        temp_white_locations = self.white_locations[:]
        temp_white_pieces = self.white_pieces[:]
        self.black_locations[self.black_selection] = click_alg
        self.black_check = False
        if click_alg in self.white_locations:
            white_piece = self.white_locations.index(click_alg)
            self.white_locations.pop(white_piece)
            self.white_pieces.pop(white_piece)
        self.check('black')
        self.white_pieces = temp_white_pieces
        self.white_locations = temp_white_locations
        if not self.black_check:
            self.black_move_counter += 1
            # Check if the player has castled
            if self.black_pieces[self.black_selection] == 'king':
                if click_alg == 'b8' and not self.kings_moved['black'] and not self.rooks_moved['black'][0]:
                    self.black_locations[0] = 'c8'  # Move the rook
                    self.kings_moved['black'] = True
                elif click_alg == 'g8' and not self.kings_moved['black'] and not self.rooks_moved['black'][1]:
                    self.black_locations[7] = 'f8'  # Move the rook
                    self.kings_moved['black'] = True
            #  Check if the player has moved a pawn or captured a piece for the fifty-move rule
            if self.black_pieces[self.black_selection] == 'pawn':
                self.black_move_counter = 0
                # Pawn promotion, for now only allows queen promotion
                if click_alg[1] == '1':
                    self.black_pieces[self.black_selection] = 'queen'
            if click_alg in self.white_locations:
                self.black_move_counter = 0

            if self.black_selection in [0, 4, 7]:
                if self.black_selection in [0, 7]:
                    self.rooks_moved['black'][self.black_selection // 7] = True
                else:
                    self.kings_moved['white'] = True
            # if not in check, update the pieces and options
            self.black_locations[self.black_selection] = click_alg  # Apply the move
            if click_alg in self.white_locations:
                white_piece = self.white_locations.index(click_alg)
                self.captured_pieces_black.append(self.white_pieces[white_piece])
                self.white_locations.pop(white_piece)
                self.white_pieces.pop(white_piece)
                self.check('white')
                if self.white_check and self.is_checkmate('white'):
                    self.winner = 'black'
            ending_position = click_alg  # Track the ending position
            self.add_to_history(starting_position, ending_position, self.black_pieces[self.black_selection],
                                color='black')
            self.last_move = [self.board.alg_to_coords(starting_position), self.board.alg_to_coords(ending_position),
                              self.black_pieces[self.black_selection]]
            self.turn_step = 0
            self.white_selection = 100
            self.black_selection = 100

            if not self.black_options and not self.black_check:
                self.winner = 'stalemate'
                self.done = True
        else:
            # If in check, disallow the move
            self.board.draw_temp_check()
            self.black_locations[self.black_selection] = temp_location  # Revert the move
            self.black_selection = 100
            self.turn_step = 2

    def play_game(self):
        self.done = False
        starting_position = None  # Track the starting position of a move
        valid_moves_selection = None
        while self.run:
            self.timer.tick(self.fps)
            if self.counter < 30:
                self.counter += 1
            else:
                self.counter = 0
            self.board.draw_board()
            self.board.draw_pieces()
            self.board.draw_captured()
            self.board.draw_check()
            if self.check_threefold_repetition():
                self.winner = "draw 3"
                self.done = True
            if self.white_move_counter == 50 or self.black_move_counter == 50:
                self.winner = "draw 50"
                self.done = True
            if self.turn_step < 2:
                self.white_options = self.check_options('white')
                self.white_moves, valid_moves_selection = self.check_valid_moves('white')
                if valid_moves_selection is not None:
                    self.board.draw_valid(valid_moves_selection)
            elif self.turn_step > 1:
                self.black_options = self.check_options('black')
                self.black_moves, valid_moves_selection = self.check_valid_moves('black')
                if valid_moves_selection is not None:
                    self.board.draw_valid(valid_moves_selection)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.done:
                    x_coord = event.pos[0] // 100
                    y_coord = event.pos[1] // 100
                    click_coords = (x_coord, y_coord)
                    click_alg = self.board.coords_to_alg(click_coords)

                    # Whites turn
                    if self.turn_step < 2:
                        self.check('white')
                        # Check if white Forfeits
                        if click_coords == (8, 8) or click_coords == (9, 8):
                            self.winner = 'black'
                        else:
                            # Check for check

                            # Check if click alg is in white locations
                            if click_alg in self.white_locations:
                                self.white_selection = self.white_locations.index(click_alg)
                                starting_position = click_alg
                                self.white_moves, valid_moves_selection = self.check_valid_moves('white')
                                # Set turn step to moving instead of selection
                                if self.turn_step == 0:
                                    self.turn_step = 1
                            elif valid_moves_selection is not None:
                                if self.turn_step == 1 and click_alg in valid_moves_selection:
                                    self.white_move(starting_position, click_alg)

                    # Blacks turn
                    if self.turn_step > 1:
                        if click_coords == (8, 8) or click_coords == (9, 8):
                            self.winner = 'white'
                        else:
                            # Check for Check
                            self.check('black')
                            # Check if click alg is in black locations
                            if click_alg in self.black_locations:
                                self.black_selection = self.black_locations.index(click_alg)
                                starting_position = click_alg
                                self.black_moves, valid_moves_selection = self.check_valid_moves('black')
                                # set the turn to moving instead of selection
                                if self.turn_step == 2:
                                    self.turn_step = 3
                            elif valid_moves_selection is not None:
                                if self.turn_step == 3 and click_alg in valid_moves_selection:
                                    self.black_move(starting_position, click_alg)

                if event.type == pygame.KEYDOWN and self.done:
                    if event.key == pygame.K_RETURN:
                        self.turn_step = 0  # 0- whites turn no selection, 1: piece selected, 2 and 3 same for black
                        self.white_selection = 100
                        self.black_selection = 100
                        self.white_moves = []
                        self.black_moves = []
                        self.white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                                             'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                        self.black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                                             'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                        self.white_locations = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
                                                'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
                        self.black_locations = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
                                                'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
                        self.captured_pieces_white = []
                        self.captured_pieces_black = []
                        self.winner = ''
                        self.counter = 0
                        self.white_move_counter = 0
                        self.black_move_counter = 0
                        self.done = False
                        self.run = True
                        self.white_check = False
                        self.black_check = False
                        self.white_options = self.check_options('white')
                        self.black_options = self.check_options('black')
                        self.all_options = None
                        self.last_move = None
                        self.history = []

            if self.winner != '':
                if self.winner == 'draw 3':
                    self.done = True
                    self.board.draw_draw3()
                elif self.winner == 'draw 50':
                    self.done = True
                    self.board.draw_draw50()
                elif self.winner == 'stalemate':
                    self.done = True
                    self.board.draw_stalemate()
                elif self.winner == 'white' or self.winner == 'black':
                    self.done = True
                    self.board.draw_game_over()
            pygame.display.flip()


c = Chess()
while c.run:
    c.play_game()
pygame.quit()
