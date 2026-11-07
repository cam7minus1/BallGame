
import pygame

class Block:

    def __init__(self, screen, destroy_callback, x, y, size, hp=3):
        self.screen = screen
        self.max_hp = hp
        self.destroy_callback = destroy_callback
        self.hp = hp
        self.x = x
        self.y = y
        self.size = size
        self.default_color = (0, 150, 0)
        self.color = self.default_color
        self.update_color()

    def __str__(self):
        return "Block"

    def destroy(self):
        self.destroy_callback(self)

    def update_color(self):
        ratio = self.hp/self.max_hp
        self.color = (self.default_color[0] * ratio, self.self.default_color[1] * ratio, self.self.default_color[2] * ratio)

    def update(self):
        udim_tuple = (self.x, self.y_anchor, self.size_x, self.size_y)
        pygame.draw.rect(self.screen, self.color, udim_tuple)

    def ball_hit(self):
        self.hp -= 1

    def move_down(self):
        self.y -= self.size

    def get_size(self):
        return self.size, self.size

    def get_position(self):
        return self.x, self.y

class Ball:

    def __init__(self, screen, destroy_callback, x, y, speed_x, speed_y, size=5):
        self.screen = screen
        self.destroy_callback = destroy_callback
        self.x = x
        self.y = y
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = (255, 0, 0)

    def __str__(self):
        return f"Ball_{self.x}_{self.y}"

    def destroy(self):
        self.destroy_callback(self)

    def get_size(self):
        return self.size, self.size

    def get_position(self):
        return self.x, self.y

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

        udim_tuple = (self.x, self.y, self.size, self.size)
        center_tuple = (self.x, self.y)
        pygame.draw.circle(self.screen, self.color, center_tuple, self.size)

    def get_position(self):
        return self.x, self.y

    def get_size(self):
        return self.size, self.size

    def collide(self):
        pass

class Assets:

    def __init__(self, screen, screen_width, screen_height):
        self.assets = []
        self.screen = screen

        self.x_min_bound = 0
        self.x_max_bound = screen_width
        self.y_min_bound = 0
        self.y_max_bound = screen_height

        self.count = 0
        self.spawn_block_frequency = 60 * 10

    def __str__(self):
        return f"Assets {len(self.assets)}"

    def remove_asset(self, asset):
        print("removed asset")
        self.assets.remove(asset)

    def spawn_ball(self, x, y):
        self.assets.append(Ball(self.screen, self.remove_asset, x, y, 1, -1))

    def add_asset(self, asset):

        if asset is None:
            print("Attempted to add a None value to assets list!")
            return

        self.assets.append(asset)
    

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

            # In this case A represents the ball, B another asset
            delta_x, delta_y = 1, 1

            if a_y_end > b_y_start or a_y_start < b_y_end:
                delta_y = -1

            if a_x_end < b_x_start or a_x_start > b_x_end:
                delta_x = -1

            return True, delta_x, delta_y
        else:
            return False, 1, 1

    def update(self):

        # Spawn blocks if frequency
        self.count += 1
        if self.count > self.spawn_block_frequency:
            self.count = 0
            pass

        for asset in self.assets:
            # If ball check bounds and collisions
            if isinstance(asset, Ball):

                # Check boundaries X axis
                if asset.x < self.x_min_bound or asset.x > self.x_max_bound :
                    asset.speed_x *= -1

                # Bounce of y top but not the bottom to let fallen die
                if asset.y < self.y_min_bound:
                    asset.speed_y *= -1

                # Destroy the ball if out of bounds
                if asset.y > self.y_max_bound:
                    asset.destroy()

                # Check other instances for collisions
                for sel_asset in self.assets:

                    if sel_asset is asset:
                        continue

                    size_a_x, size_a_y = asset.get_size()
                    pos_a_x, pos_a_y = asset.get_position()
                    size_b_x, size_b_y = sel_asset.get_size()
                    pos_b_x, pos_b_y = sel_asset.get_position()

                    colliding, x_delta, y_delta = self.is_colliding(pos_a_x, pos_a_y, size_a_x, size_a_y, 
                                        pos_b_x, pos_b_y, size_b_x, size_b_y)

                    if colliding:
                        asset.speed_x *= x_delta
                        asset.speed_y *= y_delta

            # Call each assets update function
            try:
                asset.update()
            except AttributeError as e:
                print(f"Attempted to call the update function but it does not exist for {self.asset} {e}")

            


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

    def get_position(self):
        return self.x, self.y_anchor
    
    def get_size(self):
        return self.size_x, self.size_y


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
        self.assets = Assets(self.screen, self.window_width, self.window_height)
        self.assets.add_asset(self.paddle)
        self.assets.spawn_ball(200, 150)

        # Run the main game loop
        self._start_game()

    def _update(self):
        self.assets.update()

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

    colliding, _, _ = asset_instance.is_colliding(pos_a_x, pos_a_y, size_a_x, size_a_y, 
                                   pos_b_x, pos_b_y, size_b_x, size_b_y)
    if colliding:
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

    colliding, _, _ = asset_instance.is_colliding(pos_a_x, pos_a_y, size_a_x, size_a_y, 
                                   pos_b_x, pos_b_y, size_b_x, size_b_y,)

    if not colliding:
        print("Failed bounds test 2")
    else:
        print("Pass")
    

if __name__ == "__main__":
    Game()

    # test_bounds()