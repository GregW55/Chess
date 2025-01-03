import pygame
from config import *

pygame.init()


class Board:
    """Class to handle GUI/Drawing stuff on screen"""
    def __init__(self, chess_instance):
        self.chess = chess_instance  # Pass the chess class to be able to access variables
        self.board_white = (235, 236, 208)  # Whatever color you want, this is just the white i chose
        self.board_green = (118, 146, 85)  # Same thing for green
        self.grid_color = "black"  # Grid pattern on the screen, can make it whatever color you'd like


    @staticmethod
    def coords_to_alg(coords):
        """Function to turn coordinates into algebraic notation"""
        # ord('a') returns the ASCII value of the letter, in this case 97, this is to have starting point of the board (a) and add the coordinate to that, so +1 is b, etc
        # This allows us to manipulate the value, to determine which square we are on(basically comparing the number value of each letter to determine where youve click)
        # chr() turns the ASCII value back to its corresponding letter
        file_letter = chr(ord('a') + coords[0])  # Gets the value of the square, then converts it to its letter form
        rank_number = 8 - coords[1]  # base of 8(max board square)
        return f"{file_letter}{rank_number}"  # Returns a string like "a9"

    @staticmethod
    def alg_to_coords(algebraic):
        """Function to turn algebraic notation into coordinates"""
        file_letter = algebraic[0]  # would be "a", or "b" etc
        y = int(str(algebraic)[1:]) - 1  # This takes the second part of the string (for example "b9" this would just take "9", and convert it to an integer instead of a string
        x = ord(file_letter) - ord('a')  # Gets the ASCII value of the letter, then subtracts the baseline of "a" (a - a = 0, or 97-97 = 0, this just allows us to manipulate the data,
        # another example would be e - a = 4, or 101 - 97 = 4, how many x places we need to move over
        y = 7 - y  # the y axis can be any of 8 numbers (0-7, so 7-7 would be 0, or the first place on the board)
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

        # Draw grid lines on the board
        for i in range(9):
            pygame.draw.line(screen, self.grid_color, (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, self.grid_color, (100 * i, 0), (100 * i, 800), 2)


    def draw_pieces(self):
        for i in range(len(self.chess.white_pieces)):  # For each piece(or i(ndex)) in self.white_pieces loop through this
            index = piece_list.index(self.chess.white_pieces[i])  # the index is where in the list the value is, for example the rook's index is 0, or 7 (depending which rook) since its first and eighth in the list
            x, y = self.alg_to_coords(self.chess.white_locations[i])  # get the x,y cordinate of the pieces location using the index value. white_locations[i] searches white_locations, looking for the index, so for rook it would look for the first or eighth thing in that list

            if self.chess.white_pieces[i] == 'pawn':  # Draw the pawns with an offset otherwise they look weird, optional
                screen.blit(white_pawn, (x * 100 + 22, y * 100 + 30))
            else:
                screen.blit(white_images[index], (x * 100 + 10, y * 100 + 10))
            if self.chess.turn_step < 2:  # If its whites turn
                if self.chess.white_selection == i:  # If white has selected a piece
                    pygame.draw.rect(screen, 'red', [x * 100 + 1, y * 100 + 1, 100, 100], 2)  # Draw the border around the selected piece

        for i in range(len(self.chess.black_pieces)):  # For each piece(or i(ndex)) in self.white_pieces loop through this
            index = piece_list.index(self.chess.black_pieces[i])  # the index is where in the list the value is, for example the rook's index is 0, or 7 (depending which rook) since its first and eighth in the list
            x, y = self.alg_to_coords(self.chess.black_locations[i])

            if self.chess.black_pieces[i] == 'pawn':  # Draws the pawns with an offset, optional
                screen.blit(black_pawn, (x * 100 + 22, y * 100 + 30))
            else:
                screen.blit(black_images[index], (x * 100 + 10, y * 100 + 10))
            if self.chess.turn_step >= 2:  # blacks turn
                if self.chess.black_selection == i:
                    pygame.draw.rect(screen, 'blue', [x * 100 + 1, y * 100 + 1, 100, 100], 2)  # Draws the border around selected piece

    def draw_check(self):
        if self.chess.white_check:  # Only use the function if a player is in check
            king_location = self.chess.white_locations[self.chess.white_pieces.index('king')]  # Same logic as before, this time you are going to get the index of the king, so your getting where in that list the king is, 4 for example then checking the 4th thing in the locations list, which would be the kings location
            x, y = self.alg_to_coords(king_location)
            if self.chess.counter < 15:  # Draw the check every 15 frames, can change this to whatever you want under 30 (or change the main loop counter inside the main function aswell)
                pygame.draw.rect(screen, 'dark red', [x * 100 + 1,
                                                      y * 100 + 1, 100, 100], 10)  # draw the red border around the king to indicate your in check
        elif self.chess.black_check:  # Only use the function if a player is in check
            king_location = self.chess.black_locations[self.chess.black_pieces.index('king')]  # Same logic as before, this time you are going to get the index of the king, so your getting where in that list the king is, 4 for example then checking the 4th thing in the locations list, which would be the kings location
            x, y = self.alg_to_coords(king_location)
            if self.chess.counter < 15:
                pygame.draw.rect(screen, 'dark blue', [x * 100, y * 100, 100, 100], 10)


    def draw_valid(self, moves):
        color = 'blue' if self.chess.turn_step < 2 else 'red'
        if len(moves) > 0:  # make sure you have some valid moves
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


    @staticmethod
    def draw_stalemate():
        pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
        screen.blit(font.render(f'The game resulted in a stalemate due to lack of moves!', True, 'white'), (210, 210))


class Chess:
    def __init__(self):
        self.winner = ''
        self.counter = 0  # Used for check drawing every so often
        self.done = False
        self.run = True
        self.white_check = False  # Track if the white player is in check
        self.black_check = False  # Track if the black player is in check
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.board = Board(self)  # Used to draw the board and pieces
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.turn_step = 0  # 0- whites turn no selection, 1: piece selected, 2 and 3 same for blacks turn
        self.white_selection = 100  # Default number to determine if white has selected a piece
        self.black_selection = 100  # Default number to determine if black has selected a piece

        self.white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                             'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        self.black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                             'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        self.white_locations = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
                                'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
        self.black_locations = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
                                'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']

        self.white_options = []  # ALL possible moves
        self.black_options = []
        self.white_moves = []  # Only valid moves
        self.black_moves = []

    # Check all valid moves per piece
    def check_king(self, position, color):
        moves_list = []
        friends_list = self.white_locations if color == 'white' else self.black_locations
        enemies_list = self.black_locations if color == 'white' else self.white_locations
        file = ord(position[0])  # Use the ASCII value of a letter to do 1:1 changes
        rank = int(position[1])  # Convert the rank into an integer from a string to allow calculations
        directions = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]

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
            capture_directions = [(1, 1), (-1, 1)]  # Diagonal capture directions
        else:
            direction = -1  # Black pawns move towards lower ranks(numbers)
            start_rank = 7  # Black pawns start at rank 7
            capture_directions = [(1, -1), (-1, -1)]  # Diagonal capture directions

        # Move forward one square
        new_file = chr(file)
        new_rank = rank + direction
        new_position = f"{new_file}{new_rank}"
        piece_index = friends_list.index(position)
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
        if color == 'white':
            locations = self.white_locations
            pieces = self.white_pieces
        else:
            locations = self.black_locations
            pieces = self.black_pieces

        for i in range(len(pieces)):  # Gets each pieces location and type of piece
            position = locations[i]
            piece = pieces[i]
            if piece == 'king':
                moves = self.check_king(position, color)
                moves_list.append(moves)

            elif piece == 'rook':
                moves = self.check_rook(position, color)
                moves_list.append(moves)

            elif piece == 'knight':
                moves = self.check_knight(position, color)
                moves_list.append(moves)

            elif piece == 'bishop':
                moves = self.check_bishop(position, color)
                moves_list.append(moves)
            elif piece == 'queen':
                moves = self.check_queen(position, color)
                moves_list.append(moves)
            elif piece == 'pawn':
                moves = self.check_pawn(position, color)
                moves_list.append(moves)
        return moves_list

    def check_valid_moves(self, color):
        """Returns all valid moves that don't put or leave the king in check."""
        valid_moves = []
        valid_moves_selection = []

        if color == 'white':
            # Set temp variables to be able to revert the board back to original state
            pieces = self.white_pieces[:]
            locations = self.white_locations[:]
            enemy_locations = self.black_locations[:]
            enemy_pieces = self.black_pieces[:]
            selection = self.white_selection
        else:
            pieces = self.black_pieces[:]
            locations = self.black_locations[:]
            enemy_locations = self.white_locations[:]
            enemy_pieces = self.white_pieces[:]
            selection = self.black_selection

        for i in range(len(pieces)):  # loop through each piece to get all pieces valid moves
            piece = pieces[i]
            current_pos = locations[i]

            # Get all possible moves for this piece
            if piece == 'pawn':
                possible_moves = self.check_pawn(current_pos, color)
            elif piece == 'rook':
                possible_moves = self.check_rook(current_pos, color)
            elif piece == 'knight':
                possible_moves = self.check_knight(current_pos, color)
            elif piece == 'bishop':
                possible_moves = self.check_bishop(current_pos, color)
            elif piece == 'queen':
                possible_moves = self.check_queen(current_pos, color)
            elif piece == 'king':
                possible_moves = self.check_king(current_pos, color)
            else:
                possible_moves = []

            piece_valid_moves = []

            for move in possible_moves:
                # Store the current state of the game
                original_pos = locations[i]
                original_enemy_locations = enemy_locations[:]
                original_enemy_pieces = enemy_pieces[:]

                captured_piece = None
                captured_piece_idx = -1

                # Update the actual class variables to simulate the move
                locations[i] = move
                if color == 'white':
                    self.white_locations = locations
                    self.black_locations = enemy_locations
                    self.black_pieces = enemy_pieces
                else:
                    self.black_locations = locations
                    self.white_locations = enemy_locations
                    self.white_pieces = enemy_pieces

                if move in enemy_locations:
                    captured_piece_idx = enemy_locations.index(move)
                    captured_piece = enemy_pieces[captured_piece_idx]
                    enemy_locations.pop(captured_piece_idx)
                    enemy_pieces.pop(captured_piece_idx)

                # Check if the king is still in check
                self.white_check = False
                self.black_check = False
                self.check(color)
                king_in_check = self.white_check if color == 'white' else self.black_check

                # Revert the state of the game
                locations[i] = original_pos
                if captured_piece_idx != -1:
                    enemy_locations.insert(captured_piece_idx, move)
                    enemy_pieces.insert(captured_piece_idx, captured_piece)

                if color == 'white':
                    self.white_locations = locations
                    self.black_locations = original_enemy_locations
                    self.black_pieces = original_enemy_pieces
                else:
                    self.black_locations = locations
                    self.white_locations = original_enemy_locations
                    self.white_pieces = original_enemy_pieces

                # If the king is not in check, this move is valid
                if not king_in_check:
                    piece_valid_moves.append(move)
                    valid_moves.append(move)

            # Store valid moves for the selected piece
            if selection == i:
                valid_moves_selection = piece_valid_moves

        return valid_moves, valid_moves_selection


    def check(self, color):
        if color == 'white':  # Whites turn
            king_index = self.white_pieces.index('king')
            king_location = self.white_locations[king_index]
            black_options = self.check_options('black')
            #  Check all blacks available options to see if the white king is in any of them
            for i in range(len(black_options)):
                if black_options[i]:
                    if king_location in black_options[i]:  # If the king is in a move, white is in check
                        self.white_check = True
                        self.board.draw_check()  # Draw the check visually

        else:  # Blacks turn
            king_index = self.black_pieces.index('king')
            king_location = self.black_locations[king_index]
            white_options = self.check_options('white')
            for i in range(len(white_options)):  # Check all whites options for blacks king
                if white_options[i]:
                    if king_location in white_options[i]:  # If the king is in a move, black is in check
                        self.black_check = True
                        self.board.draw_check()  # Draw the check visually

    def is_checkmate(self, color):
        if color == 'white':
            self.white_moves, valid_moves_selection = self.check_valid_moves('white')
            if self.white_moves:  # If white has any moves, then not in checkmate
                return False
            else:
                return True
        else:
            self.black_moves, valid_moves_selection = self.check_valid_moves('black')
            if self.black_moves:
                return False
            else:
                return True


    def white_move(self, click_alg):
        # Check if whites move will put them in check
        temp_location = self.white_locations[self.white_selection]  # Store selected piece location
        temp_black_locations = self.black_locations[:]  # Store all black locations
        temp_black_pieces = self.black_pieces[:]  # Store all black pieces

        self.white_locations[self.white_selection] = click_alg  # Apply the move
        self.white_check = False  # Look for check
        if click_alg in self.black_locations:  # If new location is inside black location
            black_piece = self.black_locations.index(click_alg)  # Find the piece at this location
            self.black_locations.pop(black_piece)  # Remove the location from the list
            self.black_pieces.pop(black_piece)  # Remove the piece from the list

        self.check('white')  # See if white is in check after moving all the pieces and removing black's piece if captured
        self.black_locations = temp_black_locations  # revert black location
        self.black_pieces = temp_black_pieces  # revert black pieces

        if not self.white_check:  # If your not in check you can make the move
            self.white_locations[self.white_selection] = click_alg
            if click_alg in self.black_locations:  # everything that was temporary, becomes permanent
                black_piece = self.black_locations.index(click_alg)
                self.black_locations.pop(black_piece)
                self.black_pieces.pop(black_piece)
                # look for checkmate
                self.check('black')
                if self.black_check and self.is_checkmate('black'):
                    self.winner = 'white'

            self.turn_step = 2
            self.white_selection = 100
            self.black_selection = 100

            if not self.white_options and not self.white_check:
                self.winner = 'stalemate'
                self.done = True
        else:
            # If in check, don't allow the move
            self.board.draw_temp_check()
            self.white_locations[self.white_selection] = temp_location  # Revert the move
            self.white_selection = 100
            self.turn_step = 0

    def black_move(self, click_alg):
        # Check if whites move will put them in check
        temp_location = self.black_locations[self.black_selection]  # Store selected piece location
        temp_white_locations = self.white_locations[:]  # Store all white locations
        temp_white_pieces = self.white_pieces[:]  # Store all white pieces

        self.black_locations[self.black_selection] = click_alg  # Apply the move
        self.black_check = False  # Look for check

        if click_alg in self.white_locations:  # If new location is inside black location
            white_piece = self.white_locations.index(click_alg)  # Find the piece at this location
            self.white_locations.pop(white_piece)  # Remove the location from the list
            self.white_pieces.pop(white_piece)  # Remove the piece from the list

        self.check('black')  # See if black is in check after moving all the pieces and removing black's piece if captured
        self.white_locations = temp_white_locations  # revert black location
        self.white_pieces = temp_white_pieces  # revert black pieces

        if not self.black_check:  # If your not in check you can make the move
            self.black_locations[self.black_selection] = click_alg
            if click_alg in self.white_locations:  # everything that was temporary, becomes permanent
                white_piece = self.white_locations.index(click_alg)
                self.white_locations.pop(white_piece)
                self.white_pieces.pop(white_piece)
                # look for checkmate
                self.check('white')
                if self.white_check and self.is_checkmate('white'):
                    self.winner = 'black'

            self.turn_step = 0
            self.white_selection = 100
            self.black_selection = 100

            if not self.black_options and not self.black_check:
                self.winner = 'stalemate'
                self.done = True
        else:
            # If in check, don't allow the move
            self.board.draw_temp_check()
            self.black_locations[self.black_selection] = temp_location  # Revert the move
            self.black_selection = 100
            self.turn_step = 2


    def play_game(self):
        self.done = False
        valid_moves_selection = None

        while self.run:
            self.timer.tick(self.fps)
            # counter is used to determine when to show the check
            if self.counter < 30:
                self.counter += 1
            else:
                self.counter = 0
            # Draw the board and pieces constantly to keep everything updated
            self.board.draw_board()
            self.board.draw_pieces()
            self.board.draw_check()

            if self.turn_step < 2:  # If its whites turn check their valid moves, and if they selected a piece check the pieces valid moves
                self.white_options = self.check_options('white')
                self.white_moves, valid_moves_selection = self.check_valid_moves('white')
                if valid_moves_selection is not None:
                    self.board.draw_valid(valid_moves_selection)
            elif self.turn_step > 1:  # If its blacks turn check their valid moves, and if they selected a piece check the pieces valid moves
                self.black_options = self.check_options('black')
                self.black_moves, valid_moves_selection = self.check_valid_moves('black')
                if valid_moves_selection is not None:
                    self.board.draw_valid(valid_moves_selection)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.done:  # When you left-click, get the X,Y coordinate of where you clicked
                    x_coord = event.pos[0] // 100
                    y_coord = event.pos[1] // 100
                    click_coords = (x_coord, y_coord)  # Where you clicked in X, Y
                    click_alg = self.board.coords_to_alg(click_coords)  # turns X,Y into alg notation (a9, b2 etc)

                    # Whites turn
                    if self.turn_step < 2:
                        self.check('white')
                            # Check for check

                        # Check if click alg is in white locations if it is, they selected a piece
                        if click_alg in self.white_locations:
                            self.white_selection = self.white_locations.index(click_alg)
                            self.white_moves, valid_moves_selection = self.check_valid_moves('white')
                            # Set turn step to moving instead of selection
                            if self.turn_step == 0:
                                self.turn_step = 1
                        elif valid_moves_selection:  # If you've selected a piece and have valid moves
                            if self.turn_step == 1 and click_alg in valid_moves_selection:  # move the piece to where the user clicked using the white_move function
                                self.white_move(click_alg)

                    # Blacks turn
                    if self.turn_step > 1:
                        # Check for Check
                        self.check('black')

                        # Check if click alg is in black locations if it is, they selected a piece
                        if click_alg in self.black_locations:
                            self.black_selection = self.black_locations.index(click_alg)
                            self.white_moves, valid_moves_selection = self.check_valid_moves('white')
                            # set the turn to moving instead of selection
                            if self.turn_step == 2:
                                self.turn_step = 3
                        if valid_moves_selection:
                            if self.turn_step == 3 and click_alg in valid_moves_selection:  # If you've selected a piece in the previous step with valid moves
                                self.black_move(click_alg)  # move the piece to click_alg using black)move function

            if self.winner != '':  # if the winner is anything
                if self.winner == 'stalemate':
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
