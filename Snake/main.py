import pygame
import asyncio
import random

# Initialize Pygame
pygame.init()
pygame.mixer_music.load("rat-dance-music.mp3")
pygame.mixer_music.play(-1)

# Window Constants
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 25  # Size of one grid square
font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Snake")
clock = pygame.time.Clock()

# Colors
BLACK = (255, 105, 180)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 192, 203)
CHERRYBLOSSOM_PINK = (255, 183, 197)

async def main():
    running = True
    
    # Snake Body: A list of Rectangles
    # Head is at index 0
    snake = [
        pygame.Rect(100, 100, CELL_SIZE, CELL_SIZE),
        pygame.Rect(75, 100, CELL_SIZE, CELL_SIZE),
        pygame.Rect(50, 100, CELL_SIZE, CELL_SIZE)
    ]
    
    # Direction vector (x, y)
    # (1, 0) is Right, (-1, 0) is Left, etc.
    direction = (1, 0) 
    next_direction = (1, 0) # Prevents 180-degree turns in one frame
    
    food = pygame.Rect(300, 300, CELL_SIZE, CELL_SIZE)
    score = 0

    # Game Speed (lower is faster, but for snake we control ticks manually)
    # We will use a timer variable to control movement speed
    move_timer = 0
    MOVE_DELAY = 100 # Milliseconds between moves
    
    while running:
        dt = clock.tick(60) # Delta time (time since last frame)
        move_timer += dt
        
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    next_direction = (0, -1)
                if event.key == pygame.K_DOWN and direction != (0, -1):
                    next_direction = (0, 1)
                if event.key == pygame.K_LEFT and direction != (1, 0):
                    next_direction = (-1, 0)
                if event.key == pygame.K_RIGHT and direction != (-1, 0):
                    next_direction = (1, 0)

        # 2. Update Game Logic (We will add this soon)
        if move_timer > MOVE_DELAY:
            move_timer = 0
                
            # Update actual direction
            direction = next_direction

            # 1. Create New Head
            current_head = snake[0]
            new_x = current_head.x + (direction[0] * CELL_SIZE)
            new_y = current_head.y + (direction[1] * CELL_SIZE)
            
            new_head = pygame.Rect(new_x, new_y, CELL_SIZE, CELL_SIZE)

            # 2. Add New Head
            snake.insert(0, new_head)
            
            # Check collision with food
            if new_head.colliderect(food):
                score += 1
                # Don't pop the tail! This makes us grow.
                
                # Move food to random spot
                food.x = random.randint(0, (WIDTH//CELL_SIZE) - 1) * CELL_SIZE
                food.y = random.randint(0, (HEIGHT//CELL_SIZE) - 1) * CELL_SIZE
            else:
                # Only remove tail if we DIDN'T eat
                snake.pop()            
            
            # Check Wall Collision
            if (new_head.left < 0 or new_head.right > WIDTH or 
                new_head.top < 0 or new_head.bottom > HEIGHT):
                # Reset Game
                snake = [pygame.Rect(100, 100, CELL_SIZE, CELL_SIZE),
                         pygame.Rect(75, 100, CELL_SIZE, CELL_SIZE)]
                direction = (1, 0)
                next_direction = (1, 0)
                score = 0
            
            # Check Self Collision
            # Loop through body parts (skipping the new head we just created)
            for part in snake[1:]:
                if new_head.colliderect(part):
                    # Reset Game
                    snake = [pygame.Rect(100, 100, CELL_SIZE, CELL_SIZE),
                             pygame.Rect(75, 100, CELL_SIZE, CELL_SIZE)]
                    direction = (1, 0)
                    next_direction = (1, 0)
                    score = 0

        # 3. Drawing
        screen.fill(BLACK)
        score_text = font.render(f"Score:{score}", True, WHITE)
        screen.blit(score_text, (10,10))

        # Draw Food
        pygame.draw.rect(screen, RED, food)
        
        # Draw Snake
        for i, part in enumerate(snake):
            if i == 0:
                color = PINK # Head
            else:
                color = CHERRYBLOSSOM_PINK # Body
            pygame.draw.rect(screen, color, part)

        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())
