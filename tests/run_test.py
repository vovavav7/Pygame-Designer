import pygame
import os
import PygameDesigner

pygame.init()

# Автоматично визначаємо правильний шлях до файлу test_ui.json у цій же папці
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, "test_ui.json")

ui = PygameDesigner.load(json_path)

win = ui.window_settings
screen = pygame.display.set_mode((win["width"], win["height"]))
pygame.display.set_caption(win["title"])

def my_button_action():
    print("🎉 Магія! Кнопка з JSON працює через .on_click!")

ui.get("click_me_btn").on_click = my_button_action

running = True
clock = pygame.time.Clock()

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
    #ui.handle_events(events)
    PygameDesigner.draw(ui, events, screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
