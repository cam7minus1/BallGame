
import pygame

class Blocks:

    def __init__(self):
        pass


class Ball:

    def __init__(self):
        pass


class Paddle:

    def __init__(self, screen, screen_dims, color=(0, 100, 200), y_anchor = 100 , size_tuple = (100, 25)):

        if screen is None:
            raise TypeError("Missing screen argument for paddle")

        if screen_dims is None:
            raise TypeError("Screen dimensions are missing")

        # Saved passed arguments for future reference
        self.color = color
        self.screen = screen
        self.y_anchor = y_anchor
        self.size_x = size_tuple[0]
        self.size_y = size_tuple[1]
        self.screen_size_x = screen_dims[0]
        self.screen_size_y = screen_dims[1]
        self.x = 0

    def update(self):
        print("Drawing paddle")
        # Pos x, y size x y
        udim_tuple = (self.size_x, self.y_anchor, self.size_x, self.size_y)
        pygame.draw.rect(self.screen, self.color, udim_tuple)


class Screen:

    def __init__(self, window_width=450, window_height=300, title='default_name', background_color = (200, 200, 200)):
        self.background_color = background_color
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(title)

    def get_screen(self):
        return self.screen

    def screen_fill(self):
        self.screen.fill(self.background_color)

    def update_screen(self):
        print("Updating screen")
        # Draw all the items requested to draw
        pygame.display.flip()


class Game:

    def __init__(self, fps=60):

        # Properties
        self.window_width = 450
        self.window_height = 300
        self.window_name = "Ball Game"

        # Default variables
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.fps = fps

        # initialize pygame
        pygame.init()

        # Step to start the screen class
        self.screen_instance = Screen(self.window_width, self.window_height, self.window_name)
        self.screen = self.screen_instance.get_screen()

        # Initialize the paddle class
        try:
            self.paddle = Paddle(self.screen, (self.window_width, self.window_height))
        except (TypeError, KeyError) as e:
            print(f"Failed to start game {type(e)} {e}")
            return

        # Run the main game loop
        self._start_game()

    def _update(self):
        self.paddle.update()

    def _start_game(self):

        # Game loop
        while self.is_running:
            print("Game loop")

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    if key == "a":
                        print("a")

            # Wipe the screen
            self.screen_instance.screen_fill()

            # Update all the game instances
            self._update()

            # Update the screen
            self.screen_instance.update_screen()

            # Wait to lock frames per second
            self.clock.tick(self.fps)


if __name__ == "__main__":
    Game()