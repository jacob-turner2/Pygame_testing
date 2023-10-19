import pygame

# Initialize Pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((800, 600))

# Set a title for the window
pygame.display.set_caption('PyRPG with All Features')

# Initialize game state
game_state = 'title_screen'

# Initialize inventory and flag for showing inventory
inventory = ['Sword', 'Potion', 'Shield']
show_inventory = False

# Initialize character position
x, y = 400, 300

# Initialize object positions
chair_pos = (100, 300)
fridge_pos = (400, 100)
sink_pos = (500, 100)

# Initialize room
current_room = 'main'

# Initialize interaction text
interaction_text = ""

# Initialize timer
time_left = 60
timer_paused = False
pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1-second timer

# Function to reset game state
def reset_game_state():
    global x, y, current_room, interaction_text, time_left
    x, y = 400, 300
    current_room = 'main'
    interaction_text = ""
    time_left = 60

# Main event loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            if game_state == 'gameplay':
                time_left -= 1
                if time_left <= 0:
                    game_state = 'out_of_time'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_state == 'title_screen':
                if 300 < mouse_pos[0] < 500 and 300 < mouse_pos[1] < 350:
                    game_state = 'gameplay'
                elif 300 < mouse_pos[0] < 500 and 400 < mouse_pos[1] < 450:
                    running = False
            elif game_state == 'in_game_menu':
                if 300 < mouse_pos[0] < 500 and 300 < mouse_pos[1] < 350:
                    game_state = 'gameplay'
                    timer_paused = False
                elif 300 < mouse_pos[0] < 500 and 400 < mouse_pos[1] < 450:
                    game_state = 'title_screen'
                    reset_game_state()
            elif game_state == 'out_of_time':
                if 300 < mouse_pos[0] < 500 and 300 < mouse_pos[1] < 350:
                    game_state = 'gameplay'
                    reset_game_state()
                elif 300 < mouse_pos[0] < 500 and 400 < mouse_pos[1] < 450:
                    game_state = 'title_screen'
                
        elif event.type == pygame.KEYDOWN:
            if game_state == 'gameplay':
                if event.key == pygame.K_ESCAPE:
                    game_state = 'in_game_menu'
                    timer_paused = True
                elif event.key == pygame.K_i:
                    show_inventory = not show_inventory  # Toggle inventory display
                elif event.key == pygame.K_e:
                    # Check for door interactions based on the current room
                    if current_room == 'main':
                        if abs(x - 400) < 30 and abs(y - 10) < 30:
                            current_room = 'top_room'
                            x, y = 400, 580
                        # Check for object interactions in the main room
                        elif abs(x - chair_pos[0]) < 30 and abs(y - chair_pos[1]) < 30:
                            interaction_text = "This is a chair."
                        elif abs(x - fridge_pos[0]) < 30 and abs(y - fridge_pos[1]) < 30:
                            interaction_text = "This is a fridge."
                        elif abs(x - sink_pos[0]) < 30 and abs(y - sink_pos[1]) < 30:
                            interaction_text = "This is a sink."
                    elif current_room == 'top_room':
                        if abs(x - 400) < 30 and abs(y - 580) < 30:
                            current_room = 'main'
                            x, y = 400, 30
            elif game_state == 'in_game_menu':
                if event.key == pygame.K_ESCAPE:
                    game_state = 'gameplay'
                    timer_paused = False

    # Check key states for smooth movement
    keys = pygame.key.get_pressed()
    if game_state == 'gameplay':
        if keys[pygame.K_LEFT] and x > 20:
            x -= 0.5
        if keys[pygame.K_RIGHT] and x < 780:
            x += 0.5
        if keys[pygame.K_UP] and y > 20:
            y -= 0.5
        if keys[pygame.K_DOWN] and y < 580:
            y += 0.5

        # Clear interaction text if character is not near any object in the main room
        if current_room == 'main':
            if not (abs(x - chair_pos[0]) < 30 and abs(y - chair_pos[1]) < 30) and \
               not (abs(x - fridge_pos[0]) < 30 and abs(y - fridge_pos[1]) < 30) and \
               not (abs(x - sink_pos[0]) < 30 and abs(y - sink_pos[1]) < 30):
                interaction_text = ""

    # Clear screen
    screen.fill((0, 0, 0))

    if game_state == 'title_screen':
        font = pygame.font.Font(None, 74)
        title_surface = font.render('PyRPG', True, (255, 255, 255))
        screen.blit(title_surface, (350, 100))

        pygame.draw.rect(screen, (0, 255, 0), (300, 300, 200, 50))
        pygame.draw.rect(screen, (255, 0, 0), (300, 400, 200, 50))

        font = pygame.font.Font(None, 36)
        start_surface = font.render('Start Game', True, (0, 0, 0))
        screen.blit(start_surface, (340, 310))

        exit_surface = font.render('Exit', True, (0, 0, 0))
        screen.blit(exit_surface, (390, 410))

    elif game_state == 'gameplay':
        # Draw character
        pygame.draw.circle(screen, (0, 0, 255), (int(x), int(y)), 20)
        
        font = pygame.font.Font(None, 36)
        timer_surface = font.render(f'Time Left: {time_left}', True, (255, 255, 255))
        screen.blit(timer_surface, (650, 10))
        
        # Draw doors and objects based on the current room
        if current_room == 'main':
            pygame.draw.rect(screen, (139, 69, 19), (390, 0, 20, 20))  # Top door
            pygame.draw.rect(screen, (139, 69, 19), (*chair_pos, 20, 20))  # Chair
            pygame.draw.rect(screen, (192, 192, 192), (*fridge_pos, 20, 20))  # Fridge
            pygame.draw.rect(screen, (211, 211, 211), (*sink_pos, 20, 20))  # Sink
        elif current_room == 'top_room':
            pygame.draw.rect(screen, (139, 69, 19), (390, 580, 20, 20))  # Bottom door leading back to main

        # Draw interaction text
        if interaction_text:
            font = pygame.font.Font(None, 36)
            text_surface = font.render(interaction_text, True, (255, 255, 255))
            screen.blit(text_surface, (10, 560))

    elif game_state == 'in_game_menu':
        pygame.draw.rect(screen, (0, 255, 0), (300, 300, 200, 50))
        pygame.draw.rect(screen, (255, 0, 0), (300, 400, 200, 50))

        font = pygame.font.Font(None, 36)
        resume_surface = font.render('Resume', True, (0, 0, 0))
        screen.blit(resume_surface, (360, 310))

        back_surface = font.render('Back to Title', True, (0, 0, 0))
        screen.blit(back_surface, (320, 410))
        
    elif game_state == 'out_of_time':
        font = pygame.font.Font(None, 74)
        out_of_time_surface = font.render('Out of Time', True, (255, 0, 0))
        screen.blit(out_of_time_surface, (300, 100))

        pygame.draw.rect(screen, (0, 255, 0), (300, 300, 200, 50))
        pygame.draw.rect(screen, (255, 0, 0), (300, 400, 200, 50))

        font = pygame.font.Font(None, 36)
        try_again_surface = font.render('Try Again', True, (0, 0, 0))
        screen.blit(try_again_surface, (340, 310))

        return_to_menu_surface = font.render('Return to Menu', True, (0, 0, 0))
        screen.blit(return_to_menu_surface, (320, 410))

    pygame.display.update()

# Quit Pygame
pygame.quit()

# from game_state import initialize_game, reset_game_state
# from events import handle_events
# from render import render_screen
# import pygame

# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
#     pygame.display.set_caption('PyRPG with All Features')
    
#     game_state = initialize_game()
    
#     running = True
#     while running:
#         running = handle_events(game_state)
#         render_screen(screen, game_state)
        
#     pygame.quit()

# if __name__ == "__main__":
#     main()