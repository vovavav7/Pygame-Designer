import pygame
import json

class UIElement:
    def __init__(self, item):
        self.id = item["id_name"]
        self.type = item["type"]
        self.rect = pygame.Rect(item["x"], item["y"], item["w"], item["h"])
        self.bg_color = item.get("bg_color")
        self.offset = item.get("offset", [0, 0])
        self.on_click = None  # Користувач призначить сюди функцію

        # Створюємо шрифт та Surface для тексту
        font_name = item.get("font_name", "Arial")
        font_size = item.get("font_size", 24)
        font = pygame.font.SysFont(font_name, font_size)
        
        text_str = item.get("text", "")
        text_color = item.get("text_color", [0, 0, 0, 255])
        
        # Ванільний pygame.Surface з відрендереним текстом
        self.surface = font.render(text_str, True, text_color[:3])

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.on_click:
            self.on_click()

class UIData:
    def __init__(self):
        self.elements = {}
        self.window_settings = {"title": "Game", "width": 800, "height": 600}

    def get(self, id_name):
        return self.elements.get(id_name)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for el in self.elements.values():
                    if el.type == "button":
                        el.check_click(event.pos)

def load(filepath):
    ui_data = UIData()
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    if "window" in data:
        ui_data.window_settings = data["window"]
        
    for item in data["elements"]:
        el = UIElement(item)
        ui_data.elements[el.id] = el
        
    return ui_data

def draw(ui_data, events, screen):
    ui_data.handle_events(events)

    for el in ui_data.elements.values():
        if el.bg_color:
            pygame.draw.rect(screen, el.bg_color, el.rect)

        button_center_x = el.rect.x + el.rect.w / 2
        button_center_y = el.rect.y + el.rect.h / 2

        text_rect = el.surface.get_rect(
            center=(
                button_center_x + el.offset[0],
                button_center_y + el.offset[1]
            )
        )

        screen.blit(el.surface, text_rect)