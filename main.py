import pygame
import sys
import random

window_size = 800
cell_size = window_size // 3
infinity = float('inf')
vector_2d = pygame.math.Vector2
centre_of_cell = vector_2d (cell_size/2)


# Logic of the game
class TicTacToe:
    def __init__(self, game):
        self.game = game
        self.background_image = self.get_scaled_image(path = 'background.png', res = [window_size] * 2)
        self.X_imgae = self.get_scaled_image(path = 'cross.png', res = [cell_size] * 2)
        self.O_imgae = self.get_scaled_image(path = 'circle.png', res = [cell_size] * 2)
        
        self.game_array = [[infinity, infinity, infinity],
                           [infinity, infinity, infinity],
                           [infinity, infinity, infinity]]
        self.player = random.randint(0,1)
        #indices that contain lines that is used to check if you won
        self.array_used_to_check_win = [[(0,0), (0,1), (0,2)], #check horizontally
                                        [(1,0), (1,1), (1,2)],
                                        [(2,0), (2,1), (2,2)], 
                                        [(0,0), (1,0), (2,0)], #check vertically
                                        [(0,1), (1,1), (2,1)],
                                        [(0,2), (1,2), (2,2)],
                                        [(0,0), (1,1), (2,2)], #check diagonally
                                        [(0,2), (1,1), (2,0)]]
        self.winner = None
        self.game_steps = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32) 
    
    def check_winner(self):
        for indices in self.array_used_to_check_win:
          sum_of_line = sum([self.game_array[i][j] for i, j in indices])
          if sum_of_line in {0,3}:
            self.winner = 'XO'[sum_of_line == 0]
            self.winning_line = [vector_2d(indices[0][::-1]) * cell_size + centre_of_cell,
                                 vector_2d(indices[2][::-1]) * cell_size + centre_of_cell]

    def game_process(self):
        current_cell = vector_2d(pygame.mouse.get_pos()) // cell_size #allows us to get the index of the array element for the cell the mouse is on
        col, row = map(int, current_cell)
        left_click = pygame.mouse.get_pressed()[0]

        if left_click and self.game_array[row][col] == infinity and not self.winner:
            self.game_array[row][col] = self.player
            self.player = not self.player #changing the player through logical negation
            self.game_steps += 1
            self.check_winner()

    def draw_items(self):
        for y, row in enumerate(self.game_array):
            for x, item in enumerate(row):
                if item != infinity:
                    self.game.screen.blit(self.X_imgae if item else self.O_imgae, vector_2d(x,y) * cell_size)


    def draw_winning_line(self):
        if self.winner:
            pygame.draw.line(self.game.screen, 'blue', *self.winning_line, cell_size // 8)

            message = self.font.render(f'Player {self.winner} wins. Press spacebar to play again!', True, 'white', 'purple')
            self.game.screen.blit(message, (window_size // 2 - message.get_width() // 2, window_size // 4))

    def draw(self):
        self.game.screen.blit(self.background_image, (0,0))
        self.draw_items()
        self.draw_winning_line()

    @staticmethod
    def get_scaled_image(path, res):
        image = pygame.image.load(path)
        return pygame.transform.smoothscale(image,res)

    def run(self):
        self.draw()
        self.game_process()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([window_size] * 2)
        self.clock = pygame.time.Clock()
        self.tic_tac_toe = TicTacToe(self)

    def set_caption(self):
        pygame.display.set_caption("TicTacToe")

    def set_icon(self):
        icon = pygame.image.load('icon.png') 
        pygame.display.set_icon(icon) 


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.new_game()

    def new_game(self):
        self.tic_tac_toe = TicTacToe(self)


    def run(self):
        while True:
            self.set_caption()
            self.set_icon()
            self.check_events()
            self.screen.fill((255,255,255))
            self.tic_tac_toe.run()
            pygame.display.update()
            self.clock.tick(30)



if __name__ == '__main__':
    game = Game()
    
    game.run()

    