import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 10, 20
BLOCK_SIZE = 30
PREVIEW_SIZE = 20
SCREEN_WIDTH = 300 + 150
SCREEN_HEIGHT = 600
FALL_SPEED = 500  # Milliseconds

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),    # I (Cyan)
    (255, 165, 0),    # O (Orange)
    (128, 0, 128),    # T (Purple)
    (0, 0, 255),      # J (Blue)
    (255, 0, 0),      # L (Red)
    (0, 255, 0),      # S (Green)
    (255, 0, 255)     # Z (Magenta)
]

# Tetromino shapes (4x4 grids)
SHAPES = [
    [[4, 5, 6, 7], [2, 6, 10, 14]],          # I
    [[1, 5, 6, 10], [5, 6, 10, 11]],         # Z
    [[2, 6, 5, 9], [1, 2, 6, 10]],           # S
    [[1, 5, 9, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # L
    [[1, 2, 5, 9], [5, 9, 10, 11], [1, 5, 9, 8], [0, 1, 5, 9]],   # J
    [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]],     # T
    [[1, 2, 5, 6]]                            # O
]

# Scoring system
SCORES = {0:0, 1:100, 2:300, 3:500, 4:800}

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.reset_game()

    def reset_game(self):
        self.grid = [[0] * WIDTH for _ in range(HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = random.randint(0, 6)
        self.score = 0
        self.game_over = False
        self.fall_time = 0

    def new_piece(self):
        return {
            'shape': random.randint(0, 6),
            'rotation': 0,
            'x': WIDTH // 2 - 2,
            'y': 0
        }

    def valid_position(self, piece, dx=0, dy=0):
        shape = SHAPES[piece['shape']][piece['rotation']]
        for pos in shape:
            x = piece['x'] + (pos % 4) + dx
            y = piece['y'] + (pos // 4) + dy
            if x < 0 or x >= WIDTH or y >= HEIGHT:
                return False
            if y >= 0 and self.grid[y][x]:
                return False
        return True

    def rotate(self):
        current = self.current_piece.copy()
        rotations = len(SHAPES[current['shape']])
        current['rotation'] = (current['rotation'] + 1) % rotations
        if self.valid_position(current):
            self.current_piece = current

    def lock_piece(self):
        shape = SHAPES[self.current_piece['shape']][self.current_piece['rotation']]
        color = self.current_piece['shape'] + 1
        for pos in shape:
            x = self.current_piece['x'] + (pos % 4)
            y = self.current_piece['y'] + (pos // 4)
            if y >= 0:
                self.grid[y][x] = color

        lines_cleared = self.clear_lines()
        self.score += SCORES[lines_cleared]
        self.current_piece = {
            'shape': self.next_piece,
            'rotation': 0,
            'x': WIDTH // 2 - 2,
            'y': 0
        }
        self.next_piece = random.randint(0, 6)
        if not self.valid_position(self.current_piece):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        new_grid = []
        for row in self.grid:
            if 0 not in row:
                lines_cleared += 1
            else:
                new_grid.append(row)
        for _ in range(lines_cleared):
            new_grid.insert(0, [0]*WIDTH)
        self.grid = new_grid
        return lines_cleared

    def draw_block(self, x, y, color, size=BLOCK_SIZE):
        pygame.draw.rect(self.screen, color, (x, y, size, size))
        pygame.draw.rect(self.screen, GRAY, (x, y, size, size), 1)

    def draw_next_piece(self):
        shape = SHAPES[self.next_piece][0]
        color = COLORS[self.next_piece]
        preview_x = 320
        preview_y = 150
        
        min_x = min(pos % 4 for pos in shape)
        max_x = max(pos % 4 for pos in shape)
        min_y = min(pos // 4 for pos in shape)
        max_y = max(pos // 4 for pos in shape)
        
        width = (max_x - min_x + 1) * PREVIEW_SIZE
        height = (max_y - min_y + 1) * PREVIEW_SIZE
        
        start_x = preview_x + (100 - width) // 2
        start_y = preview_y + (100 - height) // 2
        
        for pos in shape:
            x = (pos % 4 - min_x) * PREVIEW_SIZE + start_x
            y = (pos // 4 - min_y) * PREVIEW_SIZE + start_y
            self.draw_block(x, y, color, PREVIEW_SIZE)

    def draw_borders(self):
        # Main play area border
        pygame.draw.rect(self.screen, WHITE, (0, 0, 300, 600), 2)
        
        # Right panel border
        pygame.draw.line(self.screen, WHITE, (300, 0), (300, 600), 2)
        
        # Next piece preview box
        pygame.draw.rect(self.screen, WHITE, (310, 120, 130, 130), 2)
        
        # Score box
        pygame.draw.rect(self.screen, WHITE, (310, 20, 130, 80), 2)

    def draw_grid(self):
        # Draw vertical lines
        for x in range(0, WIDTH * BLOCK_SIZE, BLOCK_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT * BLOCK_SIZE))
        # Draw horizontal lines
        for y in range(0, HEIGHT * BLOCK_SIZE, BLOCK_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH * BLOCK_SIZE, y))

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw main game elements
        self.draw_grid()
        self.draw_borders()
        
        # Draw grid blocks
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.grid[y][x]:
                    self.draw_block(x * BLOCK_SIZE, y * BLOCK_SIZE, COLORS[self.grid[y][x]-1])
        
        # Draw current piece
        if not self.game_over:
            shape = SHAPES[self.current_piece['shape']][self.current_piece['rotation']]
            color = COLORS[self.current_piece['shape']]
            for pos in shape:
                x = (self.current_piece['x'] + (pos % 4)) * BLOCK_SIZE
                y = (self.current_piece['y'] + (pos // 4)) * BLOCK_SIZE
                if y >= 0:
                    self.draw_block(x, y, color)
        
        # Draw UI elements
        self.draw_next_piece()
        
        # Score text
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (320, 30))
        
        # Next piece text
        next_text = self.font.render('Next Piece:', True, WHITE)
        self.screen.blit(next_text, (320, 100))
        
        if self.game_over:
            game_over_text = self.font.render('Game Over!', True, WHITE)
            restart_text = self.font.render('R - Restart', True, WHITE)
            quit_text = self.font.render('Q - Quit', True, WHITE)
            self.screen.blit(game_over_text, (320, 200))
            self.screen.blit(restart_text, (320, 250))
            self.screen.blit(quit_text, (320, 300))
        
        pygame.display.update()

    def run(self):
        while True:
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.reset_game()
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            return
                    else:
                        if event.key == pygame.K_LEFT:
                            if self.valid_position(self.current_piece, dx=-1):
                                self.current_piece['x'] -= 1
                        elif event.key == pygame.K_RIGHT:
                            if self.valid_position(self.current_piece, dx=1):
                                self.current_piece['x'] += 1
                        elif event.key == pygame.K_DOWN:
                            if self.valid_position(self.current_piece, dy=1):
                                self.current_piece['y'] += 1
                        elif event.key == pygame.K_UP:
                            self.rotate()
                        elif event.key == pygame.K_SPACE:
                            while self.valid_position(self.current_piece, dy=1):
                                self.current_piece['y'] += 1
                            self.lock_piece()

            # Automatic falling
            if not self.game_over and self.fall_time >= FALL_SPEED:
                if self.valid_position(self.current_piece, dy=1):
                    self.current_piece['y'] += 1
                else:
                    self.lock_piece()
                self.fall_time = 0

            self.draw()

if __name__ == "__main__":
    game = Tetris()
    game.run()