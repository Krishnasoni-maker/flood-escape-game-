import pygame
import sys
from pygame.locals import *
import time

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flood Quiz Game")

# Colors
LAVENDER = (230, 230, 250)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 48)

# Timer
start_time = time.time()
max_time = 50  # Seconds per question

# Sounds
pygame.mixer.init()
click_sound = pygame.mixer.Sound("C:/Users\KRISHNA SONI/Downloads/select-sound-121244.mp3")
correct_sound = pygame.mixer.Sound("C:/Users/KRISHNA SONI/Downloads/menu-select-button-182476.mp3")
wrong_sound = pygame.mixer.Sound("C:/Users/KRISHNA SONI/Downloads/080167_female-scream-02-89290.mp3")

# Granny image
granny_image = pygame.image.load("C:/Users/KRISHNA SONI/Downloads/DALL·E 2024-12-14 19.56.12 - A 3D cartoon-style depiction of an elderly woman (granny) partially submerged in floodwater, with only her head and hands visible as she struggles and.webp")
granny_rect = granny_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Questions and answers (15 questions total)
questions = [
    {"question": "What is the main cause of floods?", "options": ["Heavy rainfall", "Earthquake", "Deforestation", "Overpopulation"], "answer": 0},
    {"question": "What should you do during a flood?", "options": ["Stay indoors", "Go to higher ground", "Swim in floodwaters", "Call a friend"], "answer": 1},
    {"question": "Which organization monitors floods?", "options": ["NASA", "UNESCO", "Meteorological Department", "WHO"], "answer": 2},
    {"question": "What is a flash flood?", "options": ["Sudden flood", "Flood caused by ice", "Flood in a desert", "Flood with no rain"], "answer": 0},
    {"question": "How can deforestation lead to floods?", "options": ["Prevents rain", "Reduces water absorption", "Drains water", "Causes droughts"], "answer": 1},
    {"question": "Which country has the most floods?", "options": ["India", "Bangladesh", "USA", "China"], "answer": 1},
    {"question": "What is the main purpose of a dam?", "options": ["Store water", "Block rivers", "Cause floods", "Prevent erosion"], "answer": 0},
    {"question": "What is floodplain zoning?", "options": ["Building houses", "Protecting lowlands", "Restricting construction", "Planting trees"], "answer": 2},
    {"question": "What should be in a flood emergency kit?", "options": ["Mobile phone", "First aid kit", "Canned food", "All of these"], "answer": 3},
    {"question": "Which of these causes urban flooding?", "options": ["Heavy rain", "Poor drainage", "Overpopulation", "All of these"], "answer": 3},
    {"question": "What is the role of sandbags in floods?", "options": ["Absorb water", "Block water", "Store water", "Purify water"], "answer": 1},
    {"question": "What is flood forecasting?", "options": ["Flood prediction", "Flood prevention", "Flood response", "Flood management"], "answer": 0},
    {"question": "Which of these increases flood risk?", "options": ["Paved surfaces", "Trees", "Dams", "Grasslands"], "answer": 0},
    {"question": "What is the color of flood alerts?", "options": ["Red", "Yellow", "Green", "Blue"], "answer": 0},
    {"question": "What is the safest place during a flood?", "options": ["Lowlands", "Highlands", "City centers", "Fields"], "answer": 1},
]

# Game variables
current_question = 0
game_over = False
won_game = False
feedback_message = ""  # To show "Right!" or "Wrong!"
feedback_timer = 0

def draw_question(question_data):
    """Draw question and options in the center square."""
    question_text = font.render(question_data["question"], True, BLACK)
    question_rect = question_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(question_text, question_rect)

    for i, option in enumerate(question_data["options"]):
        option_text = font.render(f"{i + 1}. {option}", True, BLACK)
        option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 50 + i * 60))
        pygame.draw.rect(screen, WHITE, option_rect.inflate(20, 10))
        pygame.draw.rect(screen, BLACK, option_rect.inflate(20, 10), 2)
        screen.blit(option_text, option_rect)

def draw_timer(time_left):
    """Draw timer on the top-right corner."""
    timer_text = font.render(f"Time left: {time_left}s", True, RED if time_left < 10 else BLACK)
    screen.blit(timer_text, (WIDTH - 200, 20))

def show_feedback(message, color):
    """Display feedback message."""
    feedback_text = big_font.render(message, True, color)
    screen.blit(feedback_text, (WIDTH // 2 - feedback_text.get_width() // 2, HEIGHT // 2))

def show_game_over(win):
    """Display game over screen."""
    screen.fill(LAVENDER)
    message = "Granny is safe! You won!" if win else "Granny drowned in the flood. Game Over."
    color = GREEN if win else RED
    text = big_font.render(message, True, color)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    if not win:
        screen.blit(granny_image, granny_rect)  # Show Granny drowning
    pygame.display.flip()
    pygame.time.wait(3000)

# Game loop
running = True
while running:
    screen.fill(LAVENDER)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
            if not game_over:
                for i in range(len(questions[current_question]["options"])):
                    option_y = HEIGHT // 4 + 50 + i * 60
                    if WIDTH // 2 - 100 < event.pos[0] < WIDTH // 2 + 100 and option_y - 20 < event.pos[1] < option_y + 20:
                        click_sound.play()
                        if i == questions[current_question]["answer"]:
                            correct_sound.play()
                            feedback_message = "Right!"
                            feedback_timer = time.time()
                            current_question += 1
                            start_time = time.time()
                            if current_question >= len(questions):
                                game_over = True
                                won_game = True
                        else:
                            wrong_sound.play()
                            feedback_message = "Wrong!"
                            feedback_timer = time.time()
                            game_over = True
                            won_game = False

    # Timer logic
    time_left = max_time - int(time.time() - start_time)
    if time_left <= 0 and not game_over:
        game_over = True
        won_game = False

    # Draw question and timer
    if not game_over:
        draw_question(questions[current_question])
        draw_timer(time_left)
        if feedback_message and time.time() - feedback_timer < 1.5:  # Show feedback for 1.5 seconds
            show_feedback(feedback_message, GREEN if feedback_message == "Right!" else RED)
    else:
        show_game_over(won_game)
        running = False

    pygame.display.flip() 

pygame.quit()
sys.exit()
