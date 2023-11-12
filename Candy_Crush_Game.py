import time
import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
GRID_SIZE = 80
GRID_ROWS, GRID_COLS = 10, 10

# Colors
WHITE = (255, 255, 255)
HIGHLIGHT_COLOR = (0, 255, 0)  # Green highlight color
score=0

# Initialize the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jelly Crush Game")

# Load images
jelly_images = [
    pygame.image.load("resized//Jelly (1).png"),  # Replace with your image file paths
    pygame.image.load("resized//Jelly (2).png"),
    pygame.image.load("resized//Jelly (3).png"),
    pygame.image.load("resized//Jelly (4).png"),
    pygame.image.load("resized//Jelly (5).png"),
    pygame.image.load("resized//Jelly (6).png"),
]

background = pygame.image.load("resized//BG.png")
# Function to draw the grid
def draw_grid():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * (GRID_SIZE) +80
            y = row * (GRID_SIZE) 
            pygame.draw.rect(screen, WHITE, (x, y, GRID_SIZE, GRID_SIZE), 1)

# Function to randomly place jelly images on the grid

def place_jellies():
    jellies = []
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * GRID_SIZE +85 # to adjust the images 
            y = row * GRID_SIZE +13  # to adjust the images 
            jelly_image = random.choice(jelly_images)
            jellies.append((jelly_image, (x, y)))
    return jellies

jelly_positions = place_jellies()


#checking for match 

def increase_score():
    global score
    score += 10

def check_matches():
    # Check for matches in rows
    valid=False
    for row in range(GRID_ROWS):
        col = 0
        while col < GRID_COLS - 2:
            count = 1
            while col + count < GRID_COLS and \
                  jelly_positions[row * GRID_COLS + col][0] == jelly_positions[row * GRID_COLS + col + count][0]:
                count += 1

            if count >= 3:
                # Replace the matching jellies with random ones
                increase_score()
                valid=True
                for i in range(count):
                    jelly_positions[row * GRID_COLS + col + i] = (random.choice(jelly_images),
                                                                    jelly_positions[row * GRID_COLS + col + i][1])

            col += count

    # Check for matches in columns
    for col in range(GRID_COLS):
        row = 0
        while row < GRID_ROWS - 2:
            count = 1
            while row + count < GRID_ROWS and \
                  jelly_positions[row * GRID_COLS + col][0] == jelly_positions[(row + count) * GRID_COLS + col][0]:
                count += 1

            if count >= 3:
                # Replace the matching jellies with random ones
                increase_score()
                valid=True
                for i in range(count):
                    jelly_positions[(row + i) * GRID_COLS + col] = (random.choice(jelly_images),
                                                                    jelly_positions[(row + i) * GRID_COLS + col][1])

            row += count

    return valid

# clearing all matches before starting the Game
check_matches()
check_matches()
check_matches()
score=0

clock = pygame.time.Clock()

# for swapping 

def are_positions_adjacent(col1, row1, col2, row2):
    return abs(col1 - col2) + abs(row1 - row2) == 1
        
def swap_adjacent_jellies(col1, row1, col2, row2):
    if are_positions_adjacent(col1, row1, col2, row2):
        frames_to_swap = 20  # Adjust the number of frames for a smoother effect
        dx1 = (col2 - col1) * GRID_SIZE / frames_to_swap
        dy1 = (row2 - row1) * GRID_SIZE / frames_to_swap
        dx2 = (col1 - col2) * GRID_SIZE / frames_to_swap
        dy2 = (row1 - row2) * GRID_SIZE / frames_to_swap
        j1 = jelly_positions[row1 * GRID_COLS + col1][0]
        j2 = jelly_positions[row2 * GRID_COLS + col2][0]

        for frame in range(frames_to_swap):
            # Move jellies gradually in both directions
            jelly_positions[row1 * GRID_COLS + col1] = j1,(
                jelly_positions[row1 * GRID_COLS + col1][1][0] + dx1,
                jelly_positions[row1 * GRID_COLS + col1][1][1] + dy1,
            )
            jelly_positions[row2 * GRID_COLS + col2]= j2,(
                jelly_positions[row2 * GRID_COLS + col2][1][0] + dx2,
                jelly_positions[row2 * GRID_COLS + col2][1][1] + dy2,
            )

            # Update the display
            screen.blit(background,(0,0))
            draw_grid()
            display_score()
            display_timer(remaing_time)
            for jelly_image, (x, y) in jelly_positions:
                screen.blit(jelly_image, (x, y))
            pygame.display.flip()
            

        # Swap the jelly images in the data structure
        
        jelly_positions[row1 * GRID_COLS + col1] = (j2),(col1 * GRID_SIZE +85,row1 * GRID_SIZE +13)
        jelly_positions[row2 * GRID_COLS + col2] = (j1),(col2 * GRID_SIZE +85,row2 * GRID_SIZE +13)
    

def display_score():
    font = pygame.font.Font(None,70 )
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 300, 100))

def display_timer(timer):
    font = pygame.font.Font(None, 70)
    text=font.render("Remaining ",True,WHITE)
    timer_text = font.render(f"Time: {timer}s", True, WHITE)
    screen.blit(text, (WIDTH - 310, 250))
    screen.blit(timer_text,(WIDTH-300,350))

# Selected tile position
selected_tile = None

# Main game loop
running = True
click=0
start_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse click
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Calculate the grid position of the mouse click
            col = mouse_x // GRID_SIZE 
            row = mouse_y // GRID_SIZE

            # Set the selected tile
            
            if(col>0 and col<11): #check the mouse click in grid 
                selected_tile=(col,row)
                click+=1
            if (click==1): # to store the previous tile data
                col1,row1=selected_tile
            elif(click==2):
                col2,row2 = selected_tile

                if are_positions_adjacent(col1, row1, col2, row2):

                    swap_adjacent_jellies(col1-1, row1,col2-1,row2)
                    
                    if(check_matches()==False):
                        pygame.time.wait(100)
                        swap_adjacent_jellies(col1-1, row1,col2-1,row2)

                selected_tile=None
                click=0



    # Clear the screen
    # screen.fill((255, 192, 203))
    screen.blit(background,(0,0))
    # Draw the grid
    draw_grid()

    check_matches()
    display_score()

    elapsed_time = int(time.time() - start_time)
    remaing_time = 60-elapsed_time
    display_timer(remaing_time)
    if(remaing_time<1):
        running=False

    # Draw the jelly images
    for jelly_image, (x, y) in jelly_positions:
        screen.blit(jelly_image, (x, y))

    # Highlight the selected tile
    if selected_tile is not None:
        col, row = selected_tile
        highlight_rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, highlight_rect, 5)

    # Update the display
    pygame.display.flip()
    clock.tick(20)

# Display the final score
font = pygame.font.Font(None, 80)
game_over_text = font.render(f"Game Over! Your Score: {score}", True, WHITE)
screen.blit(background,(0,0))
screen.blit(game_over_text, (WIDTH // 2 - 350, HEIGHT // 2 - 50))
pygame.display.flip()

# Wait for a moment before quitting
pygame.time.wait(3000)

# Quit Pygame
pygame.quit()
