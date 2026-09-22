import pygame
import sys

COLOR_APP_BG = (24, 24, 24)
COLOR_TASK_BAR = (32, 32, 32)
COLOR_PANEL_LEFT = (40, 40, 40)
COLOR_PROPERTIES = (45, 45, 45)
COLOR_CANVAS_BG = (53, 53, 59)
COLOR_CANVAS = (75, 75, 82)  

COLOR_WHITE = (255, 255, 255)
COLOR_TEXT_MUTED = (140, 140, 140)

def main():
    pygame.init()

    screen_w, screen_h = 1200, 600
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
    pygame.display.set_caption("Pygame Designer")
    
    font = pygame.font.SysFont("Arial", 16, bold=True)
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                

            elif event.type == pygame.VIDEORESIZE:
                screen_w, screen_h = event.w, event.h

        task_bar_h = 40
        panel_left_w = 200
        properties_w = 250 
        
        workspace_w = screen_w - panel_left_w - properties_w
        workspace_h = screen_h - task_bar_h
        
        rect_task_bar = pygame.Rect(0, 0, screen_w, task_bar_h)
        rect_panel_left = pygame.Rect(0, task_bar_h, panel_left_w, workspace_h)
        rect_properties = pygame.Rect(screen_w - properties_w, task_bar_h, properties_w, workspace_h)
        rect_workspace = pygame.Rect(panel_left_w, task_bar_h, workspace_w, workspace_h)
        
        canvas_w, canvas_h = 640, 480
        canvas_x = rect_workspace.x + (workspace_w - canvas_w) // 2
        canvas_y = rect_workspace.y + (workspace_h - canvas_h) // 2
        rect_canvas = pygame.Rect(canvas_x, canvas_y, canvas_w, canvas_h)

        screen.fill(COLOR_APP_BG)
        
        pygame.draw.rect(screen, COLOR_CANVAS_BG, rect_workspace)
        
        pygame.draw.rect(screen, COLOR_CANVAS, rect_canvas)
        pygame.draw.rect(screen, (90, 90, 98), rect_canvas, 1)
        
        pygame.draw.rect(screen, COLOR_TASK_BAR, rect_task_bar)
        pygame.draw.rect(screen, COLOR_PANEL_LEFT, rect_panel_left)
        pygame.draw.rect(screen, COLOR_PROPERTIES, rect_properties)
        
        pygame.draw.line(screen, (20, 20, 20), (0, task_bar_h), (screen_w, task_bar_h), 1)
        pygame.draw.line(screen, (30, 30, 30), (panel_left_w, task_bar_h), (panel_left_w, screen_h), 1)
        pygame.draw.line(screen, (30, 30, 30), (screen_w - properties_w, task_bar_h), (screen_w - properties_w, screen_h), 1)

        def draw_text_center(text, rect, color=COLOR_WHITE):
            surf = font.render(text, True, color)
            text_rect = surf.get_rect(center=rect.center)
            screen.blit(surf, text_rect)

        draw_text_center("TASK BAR (Menu / Save / Export)", rect_task_bar)
        draw_text_center("TOOLBOX (Buttons, Text)", rect_panel_left, COLOR_TEXT_MUTED)
        draw_text_center("PROPERTIES (ID, X, Y, W, H)", rect_properties, COLOR_TEXT_MUTED)
        
        canvas_title = font.render("GAME CANVAS (640x480)", True, COLOR_WHITE)
        screen.blit(canvas_title, (rect_canvas.x, rect_canvas.y - 25))

        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
