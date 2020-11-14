"""
Attributions:
This game contains icons & images made by https://www.flaticon.com/authors/freepik:

TODO: Refactor as to only load highscore from disk once pr. game cycle
"""
import pygame
from pygame import mixer
import random
import math
import json

from lib import pygame_textinput

pygame.init()
text_input = pygame_textinput.TextInput()  # Initializing empty text input

# Setting game window size
WINDOW_X, WINDOW_Y = 1200, 800
WINDOW_X_CENTER = WINDOW_X / 2

# Game properties
FPS = 60
COLLISION_DISTANCE = (
    40  # How close should the rocket be before a hit (collision) is registered.
)
fps_clock = pygame.time.Clock()
game_speed = 10
score_x, score_y = 10, 10
score_font = pygame.font.Font("freesansbold.ttf", 32)
game_over_font = pygame.font.Font("freesansbold.ttf", 64)
high_score_font = pygame.font.Font("freesansbold.ttf", 32)

# Window properties
pygame.display.set_caption("Space Invaders")  # Window Title
icon = pygame.image.load("assets/icon.png")  # Window Icon
pygame.display.set_icon(icon)
mixer.music.load("assets/level_1.mp3")
mixer.music.play(-1)

# Player properties
player_avatar = pygame.image.load("assets/spaceship.png")
player_width = (
    player_avatar.get_width()
)  # Using function once rather than every time we need width.
player_height = (
    player_avatar.get_height()
)  # Using function once rather than every time we need width.
player_x = WINDOW_X_CENTER - (
    player_width / 2
)  # Center screen pos minus half avatar size for center pos.
player_y_position = (WINDOW_Y / 6) * 5
player_y = player_y_position
player_x_move = 0
player_score = 0
player_name = ""

# Rocket properties
rocket_avatar = pygame.image.load("assets/rocket.png")
rocket_width = (
    rocket_avatar.get_width()
)  # Using function once rather than every time we need width.
rocket_height = (
    rocket_avatar.get_height()
)  # Using function once rather than every time we need height.
rocket_x, rocket_y = 0, 0
rocket_y_move = game_speed * 3
rocket_fired = False

# UFO properties
NUM_OF_UFO = 6
ufo_avatar = pygame.image.load("assets/ufo.png")
ufo_width = ufo_avatar.get_width()
ufo_height = ufo_avatar.get_height()

# Creating lists of UFO data TODO: Rethink UFO data structure (not pythonic?)
ufo_avatars = []
ufo_x_positions = []
ufo_y_positions = []
ufo_x_moves = []


def start_game():
    """Resetting and setting up game"""
    global ufo_avatars, ufo_x_positions, ufo_y_positions, ufo_x_moves, player_score
    #  Reset UFO / Player data
    ufo_avatars = []
    ufo_x_positions = []
    ufo_y_positions = []
    ufo_x_moves = []
    player_score = 0
    # Creating UFO's at "random" positions
    for j in range(NUM_OF_UFO):
        ufo_avatars.append(ufo_avatar)
        ufo_x_positions.append(
            random.randint(0, WINDOW_X - ufo_width)
        )  # Making sure not to go out of bounds
        ufo_y_positions.append(random.randint(50, 150))  # Not to low
        ufo_x_moves.append(game_speed)


def draw_player(x: float, y: float) -> None:
    """Draw player on screen"""
    screen.blit(player_avatar, (x, y))


def draw_ufo(x: float, y: float, n: int) -> None:
    """Draw ufo on screen"""
    screen.blit(ufo_avatars[n], (x, y))


def draw_rocket(x: float, y: float) -> None:
    """Draw rocket on screen"""
    global rocket_fired
    rocket_fired = True
    screen.blit(rocket_avatar, (x, y))


def collision(obj_1_x: float, obj_1_y: float, obj_2_x: float, obj_2_y: float) -> bool:
    """Calculates the distance between obj_1 and a obj_2 to determine if collision"""
    distance = math.sqrt(
        math.pow(obj_1_x - obj_2_x, 2) + math.pow(obj_1_y - obj_2_y, 2)
    )
    return True if distance <= COLLISION_DISTANCE else False


def show_score(x: int, y: int, score: int) -> None:
    """Displays current score on screen"""
    ren_score = score_font.render(f"Score: {str(score)}", True, (255, 255, 255))
    screen.blit(ren_score, (x, y))


def show_game_over() -> None:
    """Ender game over text on screen"""
    ren_game_over = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(ren_game_over, (WINDOW_X_CENTER - 200, WINDOW_Y / 2 - 150))


def load_highscores() -> list:
    """Read highscores from json on disk and return them as a dict"""
    with open("highscore.json") as file:
        return json.load(file)


def write_new_highscore(new_score: dict) -> None:
    highscores = load_highscores()
    highscores.append(new_score)

    # Sorting and slicing highscore
    sorted_and_sliced_highscores = sorted(
        highscores, key=lambda key: key["score"], reverse=True
    )[:3]

    with open("highscore.json", "w") as file:
        json.dump(sorted_and_sliced_highscores, file, indent=4)


def show_highscore() -> None:
    """Render highscore board on screen"""
    ren_highscore = high_score_font.render("Highscores:", True, (255, 255, 255))
    screen.blit(ren_highscore, (WINDOW_X_CENTER - 100, WINDOW_Y / 2 - 75))
    highscore = load_highscores()
    count = 0
    for score in highscore:
        ren_score = high_score_font.render(
            f'{score["name"]} : {score["score"]}', True, (255, 255, 255)
        )
        screen.blit(ren_score, (WINDOW_X_CENTER - 70, WINDOW_Y / 2 - 40 + count))
        count += 35


def compare_score_to_highscore_table(_player_score: int) -> bool:
    """Compare score to all highscores and return true if higher than one"""
    highscore = load_highscores()
    for score in highscore:
        if _player_score > score["score"]:
            return True
    return False


def show_first_start() -> None:
    """Display 'Press space to start' across the screen"""
    ren_game_over = game_over_font.render("PRESS SPACE TO START", True, (255, 255, 255))
    screen.blit(ren_game_over, (WINDOW_X_CENTER - 400, WINDOW_Y / 2 - 150))


# Initializing game window
screen = pygame.display.set_mode((WINDOW_X, WINDOW_Y))  # Screen size in px.
background = pygame.image.load("assets/3d-space-scene.png")

# Game states
game_is_over = False
is_first_start = True
new_highscore = False

# Setting up the gameloop.
start_game()
game_running = True
while game_running:
    screen.fill((0, 0, 0))  # Setting background color, RGB.
    screen.blit(background, (0, 0))  # Setting background image.

    # Listening for events
    events = pygame.event.get()
    for event in events:

        # Quit game on window close.
        if event.type == pygame.QUIT:
            game_running = False

        # Handle keypress'
        if event.type == pygame.KEYDOWN:
            # Left Arrow
            if event.key == pygame.K_LEFT:
                player_x_move = -game_speed * 1.5
            # Right Arrow
            if event.key == pygame.K_RIGHT:
                player_x_move = game_speed * 1.5
            # Spacebar
            if event.key == pygame.K_SPACE and not rocket_fired:
                rocket_sound = mixer.Sound("assets/rocket.wav")
                rocket_sound.play()
                # Adjusting the start position of the rocket for aesthetic reasons (center tip spaceship)
                rocket_x = player_x + 16
                rocket_y = player_y - 26
                draw_rocket(rocket_x, rocket_y)
            # Sacebar Restarts game
            if event.key == pygame.K_SPACE and game_is_over:
                game_is_over = False
                start_game()
            # Spacebar Reset first start
            if event.key == pygame.K_SPACE and is_first_start:
                is_first_start = False

        # Reset / Stop player movement on keyup.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_move = 0

    # Game states
    if game_is_over and not is_first_start and not new_highscore:
        if compare_score_to_highscore_table(
            player_score
        ):  # Check if user has a new highscore
            new_highscore = True
        show_highscore()
        show_game_over()

    if new_highscore:
        show_game_over()
        ren_new_highscore = high_score_font.render(
            "New Highscore, enter initials!", True, (255, 255, 255)
        )
        screen.blit(ren_new_highscore, (WINDOW_X_CENTER - 235, WINDOW_Y / 2 - 75))
        player_name = text_input.get_text()[:3]

        # Re-initializing text input to limit number of char to 3
        text_input = pygame_textinput.TextInput(
            initial_string=player_name,
            text_color=(255, 255, 255),
            cursor_color=(255, 255, 255),
        )

        finished = text_input.update(events)  # Returns True if use "Enter"
        screen.blit(text_input.get_surface(), (WINDOW_X_CENTER - 15, WINDOW_Y / 2 - 40))
        if finished:
            write_new_highscore(
                {"name": player_name if player_name else "ANO", "score": player_score}
            )
            player_score = (
                0  # Resetting score to prevent never ending loop of new highscore
            )
            new_highscore = False

    if is_first_start:
        show_highscore()
        show_first_start()

    # Rocket movement
    if rocket_y <= 0:  # Reset rocket when reach top of screen
        rocket_fired = False
    if rocket_fired:
        rocket_y -= rocket_y_move
        draw_rocket(rocket_x, rocket_y)  # Move Rocket

    # Player movement
    player_x += player_x_move
    if player_x <= 0:  # Block movement if edge of screen.
        player_x = 0
    elif player_x >= WINDOW_X - player_width:  # Block movement if edge of screen.
        player_x = WINDOW_X - player_width

    # UFO movement
    if not game_is_over and not is_first_start:
        for i in range(NUM_OF_UFO):  # Looping over each UFO

            # Game over if UFO reaches spaceship
            if ufo_y_positions[i] >= player_y_position - player_height:
                game_is_over = True
                break

            ufo_x_positions[i] += ufo_x_moves[i]  # Moving UFO horizontally
            if ufo_x_positions[i] <= 0:  # Drop down if reach LEFT edge.
                ufo_x_moves[i] += game_speed  # Turning UFO around (+)
                ufo_y_positions[i] += ufo_height / 2  # Drop
            elif (
                ufo_x_positions[i] >= WINDOW_X - ufo_width
            ):  # Drop down if reach RIGHT edge.
                ufo_x_moves[i] -= game_speed  # Turning UFO around (-)
                ufo_y_positions[i] += ufo_height / 2  # Drop

            # Collision control
            if collision(ufo_x_positions[i], ufo_y_positions[i], rocket_x, rocket_y):
                explosion_sound = mixer.Sound("assets/boom.wav")
                explosion_sound.play()
                rocket_x, rocket_y = (
                    0,
                    0,
                )  # Reset rocket position to prevent multiple hits.
                rocket_fired = False
                player_score += 1
                # Respawning UFO
                ufo_x_positions[i] = random.randint(0, WINDOW_X - ufo_width)
                ufo_y_positions[i] = 50
            draw_ufo(ufo_x_positions[i], ufo_y_positions[i], i)  # Move UFO

    draw_player(player_x, player_y)  # Move Player
    show_score(score_x, score_y, player_score)
    pygame.display.update()  # Update Screen
    fps_clock.tick(FPS)  # Sync Framerate
