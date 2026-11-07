
import pygame

class Blocks:

    def __init__(self):
        pass

class Ball:

    def __init__(self, x, y, speed_x, speed_y, size=5):
        self.x = x
        self.y = y
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y

    def get_size(self):
        return self.size, self.size

    def get_position(self):
        return self.x, self.y

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

class Assets:

    def __init__(self):
        self.assets = []

    def spawn_ball(self, x, y):
        pass

    def is_colliding(self, a_pos_x, a_pos_y, a_size_x, a_size_y, 
                        b_pos_x, b_pos_y, b_size_x, b_size_y, ):

        # Define x
        a_x_start = a_pos_x
        a_x_end = a_pos_x + a_size_x - 1
        a_y_start = a_pos_y
        a_y_end = a_pos_y + a_size_y - 1

        # Define Y
        b_x_start = b_pos_x
        b_x_end = b_pos_x + b_size_x - 1
        b_y_start = b_pos_y
        b_y_end = b_pos_y + b_size_y - 1

        # Check for collisions in the bounds
        if b_x_start <= a_x_end and b_x_end >= a_x_start \
            and b_y_start <= a_y_end and b_y_end >= a_y_start:

            return True
        else:
            return False

    def update(self):
        pass


class Paddle:

    def __init__(self, screen, screen_dims, color=(0, 100, 200) , size_tuple=(100, 25)):

        if screen is None:
            raise TypeError("Missing screen argument for paddle")

        if screen_dims is None:
            raise TypeError("Screen dimensions are missing")

        # Saved passed arguments for future reference
        self.color = color
        self.screen = screen
        self.y_anchor = screen_dims[1] - size_tuple[1] - 5
        self.size_x = size_tuple[0]
        self.size_y = size_tuple[1]
        self.screen_size_x = screen_dims[0]
        self.screen_size_y = screen_dims[1]
        self.move_speed = 5
        self.x = (self.screen_size_x)/2 - (self.size_x/2)
        self.min_pos = 0
        self.max_pos = self.screen_size_x - self.size_x
        self.border_padding = 5

    def move_left(self):

        # Check miniumum bound
        if self.x - self.move_speed < self.min_pos + self.border_padding:
            return

        self.x -= self.move_speed

    def move_right(self):

        # Check miniumum bound
        if self.x + self.move_speed > self.max_pos - self.border_padding:
            return

        self.x += self.move_speed

    def update(self):
        # Pos x, y size x y
        udim_tuple = (self.x, self.y_anchor, self.size_x, self.size_y)
        pygame.draw.rect(self.screen, self.color, udim_tuple)


class Screen:

    def __init__(self, window_width=450, window_height=300, title='default_name', background_color = (0, 0, 0)):
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

        # Initiate the Assets class which holds balls and

        # Run the main game loop
        self._start_game()

    def _update(self):
        self.paddle.update()

    def _start_game(self):

        key_a_down = False
        key_d_down = False

        # Game loop
        while self.is_running:

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    if key == "a":
                        key_a_down = True
                    if key == "d":
                        key_d_down = True
                if event.type == pygame.KEYUP:
                    key = pygame.key.name(event.key)
                    if key == "a":
                        key_a_down = False
                    if key == "d":
                        key_d_down = False

            if key_a_down:
                self.paddle.move_left()

            if key_d_down:
                self.paddle.move_right()

            # Wipe the screen
            self.screen_instance.screen_fill()

            # Update all the game instances
            self._update()

            # Update the screen
            self.screen_instance.update_screen()

            # Wait to lock frames per second
            self.clock.tick(self.fps)

def test_bounds():
    # Test case one
    # pos X, posY, 0, 0, size
    a = Ball(1, 5, 0, 0, 3)
    # pos X, posY, 0, 0, size
    b = Ball(4, 4, 0, 0, 3)

    asset_instance = Assets()

    size_a_x, size_a_y = a.get_size()
    pos_a_x, pos_a_y = a.get_position()
    size_b_x, size_b_y = b.get_size()
    pos_b_x, pos_b_y = b.get_position()
    
    if asset_instance.is_colliding(pos_a_x, pos_a_y, size_a_x, size_a_y, 
                                   pos_b_x, pos_b_y, size_b_x, size_b_y) == True:
        print("Failed bounds test 1")
    else:
        print("Pass")

    # Test Case Two
    # pos X, posY, 0, 0, size
    a = Ball(1, 5, 0, 0, 3)
    # pos X, posY, 0, 0, size
    b = Ball(3, 7, 0, 0, 3)

    size_a_x, size_a_y = a.get_size()
    pos_a_x, pos_a_y = a.get_position()

    size_b_x, size_b_y = b.get_size()
    pos_b_x, pos_b_y = b.get_position()

    if asset_instance.is_colliding(pos_a_x, pos_a_y, size_a_x, size_a_y, 
                                   pos_b_x, pos_b_y, size_b_x, size_b_y,) == False:
        print("Failed bounds test 2")
    else:
        print("Pass")
    

if __name__ == "__main__":
    Game()

    # test_bounds()