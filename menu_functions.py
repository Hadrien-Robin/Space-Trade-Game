# Select the fonts
font = pygame.font.Font(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function to display text on the screen
def display_text(text, color, x_ratio, y_ratio):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    x_pos = window_width * x_ratio
    y_pos = window_height * y_ratio

    text_rect.center = (x_pos, y_pos)
    screen.blit(text_surface, text_rect)

 
# start screen loop
def start_screen():
    running = True
    while running:
        screen.fill(BLACK)
        display_text("Space Pilote Video Game", WHITE, 0.5, 0.1)
        display_text("New Game", WHITE, 0.5, 0.3)
        display_text("Load", WHITE, 0.5, 0.4)
        display_text("Settings", WHITE, 0.5, 0.5) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if the mouse click is within the region of Option 1
                if 0.25 * window_height < mouse_y < 0.35 * window_height:
                    launch_game()
                # Check for Option 2
                elif 0.35 * window_height < mouse_y < 0.45 * window_height:
                    load_menu()
                # Check for Option 3
                elif 0.45 * window_height < mouse_y < 0.55 * window_height:
                    settings_menu()

        pygame.display.flip()
    return

def load_menu():

    return

def settings_menu():

    return
