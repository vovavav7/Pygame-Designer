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


class ListButton:
    """Клас окремої кнопки всередині списку."""
    def __init__(self, text, index, width, height, margin, callback, args=()):
        self.text = text
        self.index = index
        self.callback = callback  # Функція, яка викличеться при кліку
        self.args = args          # Аргументи функції
        
        # Позиція кнопки відносно внутрішнього полотна списку
        self.rect = pygame.Rect(10, index * (height + margin), width - 20, height)
        
        # Кольори кнопок
        self.color_normal = (50, 150, 250)
        self.color_hover = (30, 120, 220)
        self.color_text = (255, 255, 255)

    def draw(self, surface, rel_mouse_pos, font_list):
        # Ефект наведення миші
        color = self.color_hover if self.rect.collidepoint(rel_mouse_pos) else self.color_normal
        
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        text_surf = font_list.render(self.text, True, self.color_text)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def click(self):
        if self.callback:
            self.callback(*self.args)


class ScrollableList:
    """Клас менеджера скролованого списку (без handle_event)."""
    def __init__(self, x, y, width, height, button_height=50, button_margin=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.btn_height = button_height
        self.btn_margin = button_margin
        
        self.buttons = []
        
        # Параметри плавності та швидкого скролу
        self.scroll_y = 0.0
        self.target_scroll_y = 0.0
        self.scroll_speed = 140
        self.scroll_smoothing = 0.35
        
        # Внутрішні параметри полотна
        self.total_height = 0
        self.max_scroll = 0
        self.list_surface = None
        self.rel_mouse_pos = (-100, -100)

    def add_item(self, text, callback, args=()):
        """Додає новий елемент у список."""
        index = len(self.buttons)
        btn = ListButton(text, index, self.rect.width, self.btn_height, self.btn_margin, callback, args)
        self.buttons.append(btn)
        
        # Перераховуємо розміри полотна
        self.total_height = len(self.buttons) * (self.btn_height + self.btn_margin)
        self.max_scroll = max(0, self.total_height - self.rect.height)
        self.list_surface = pygame.Surface((self.rect.width, max(self.rect.height, self.total_height)))

    def update(self):
        """Оновлює плавну доводку скролу та координати миші."""
        # Ефект плавності LERP
        self.scroll_y += (self.target_scroll_y - self.scroll_y) * self.scroll_smoothing
        if abs(self.target_scroll_y - self.scroll_y) < 0.1:
            self.scroll_y = self.target_scroll_y
            
        # Оновлюємо відносні координати миші для кнопок (для Hover ефекту)
        mx, my = pygame.mouse.get_pos()
        rel_mx = mx - self.rect.x
        rel_my = my - self.rect.y + self.scroll_y
        self.rel_mouse_pos = (rel_mx, rel_my)

    def draw(self, dest_surface, font_list):
        """Малює список на вказану поверхню (наприклад, на screen)."""
        if not self.list_surface:
            return
            
        # 1. Очищаємо внутрішнє полотно
        self.list_surface.fill((255, 255, 255))
        
        # 2. Малюємо всі кнопки на внутрішньому полотні
        for btn in self.buttons:
            btn.draw(self.list_surface, self.rel_mouse_pos, font_list)
            
        # 3. Вирізаємо видиму частину
        visible_rect = pygame.Rect(0, int(self.scroll_y), self.rect.width, self.rect.height)
        sub_surface = self.list_surface.subsurface(visible_rect)
        
        # 4. Виводимо на екран
        dest_surface.blit(sub_surface, (self.rect.x, self.rect.y))
        
        # 5. Малюємо рамку навколо списку
        pygame.draw.rect(dest_surface, (0, 0, 0), self.rect, 2)

def start_level(level_num):
    print(f"-> Завантаження Рівня {level_num}...")

def open_settings():
    print("-> Відкрито налаштування гри!")

# 2. Створення об'єкта списку (X, Y, Ширина, Висота)
toolslist = ScrollableList(x=0, y=0, width=200, height=600)
toolslist.add_item("button", open_settings)

def main():
    pygame.init()

    screen_w, screen_h = 1200, 600
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.RESIZABLE)
    pygame.display.set_caption("Pygame Designer")
    
    font = pygame.font.SysFont("Arial", 16, bold=True)
    font_list = pygame.font.SysFont("Arial", 22)
    clock = pygame.time.Clock()
    
    camera_zoom = 1.0
    camera_offset_x = 0.0
    camera_offset_y = 0.0
    is_panning = False  
    
    test_button = {
        "text": "Тест Кнопка",
        "x": 60, "y": 60,
        "w": 160, "h": 50,
        "color": (0, 120, 215)
    }
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
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
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.VIDEORESIZE:
                screen_w, screen_h = event.w, event.h

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2 and rect_workspace.collidepoint(event.pos):
                    is_panning = True
                    
                elif event.button == 4 and rect_workspace.collidepoint(event.pos):
                    if camera_zoom < 3.0:  
                        camera_zoom += 0.1
                        
                elif event.button == 5 and rect_workspace.collidepoint(event.pos):
                    if camera_zoom > 0.3:  
                        camera_zoom -= 0.1

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    is_panning = False

            elif event.type == pygame.MOUSEMOTION:
                if is_panning:
                    camera_offset_x += event.rel[0]
                    camera_offset_y += event.rel[1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1. Скролінг коліщатком миші
                if event.button == 4:  # Вгору
                    toolslist.target_scroll_y = max(0, toolslist.target_scroll_y - toolslist.scroll_speed)
                elif event.button == 5:  # Вниз
                    toolslist.target_scroll_y = min(toolslist.max_scroll, toolslist.target_scroll_y + toolslist.scroll_speed)
                    
                # 2. Клік лівою кнопкою миші
                elif event.button == 1:
                    # Перевіряємо, чи клікнули всередині прямокутника списку
                    if toolslist.rect.collidepoint(event.pos):
                        # Перераховуємо глобальні координати миші у внутрішні для списку
                        rel_x = event.pos[0] - toolslist.rect.x
                        rel_y = event.pos[1] - toolslist.rect.y + toolslist.scroll_y
                        
                        # Шукаємо, по якій кнопці клікнули
                        for btn in toolslist.buttons:
                            if btn.rect.collidepoint((rel_x, rel_y)):
                                btn.click()
        
        toolslist.update()

        workspace_center_x = rect_workspace.x + workspace_w // 2
        workspace_center_y = rect_workspace.y + workspace_h // 2
        
        zoomed_canvas_w = int(canvas_w * camera_zoom)
        zoomed_canvas_h = int(canvas_h * camera_zoom)
        
        canvas_x = workspace_center_x - zoomed_canvas_w // 2 + int(camera_offset_x)
        canvas_y = workspace_center_y - zoomed_canvas_h // 2 + int(camera_offset_y)
        rect_canvas = pygame.Rect(canvas_x, canvas_y, zoomed_canvas_w, zoomed_canvas_h)

        screen.fill(COLOR_APP_BG)
        
        pygame.draw.rect(screen, COLOR_CANVAS_BG, rect_workspace)
        
        screen.set_clip(rect_workspace)
        
        pygame.draw.rect(screen, COLOR_CANVAS, rect_canvas)
        pygame.draw.rect(screen, (90, 90, 98), rect_canvas, 1)
        
        obj_x = rect_canvas.x + int(test_button["x"] * camera_zoom)
        obj_y = rect_canvas.y + int(test_button["y"] * camera_zoom)
        obj_w = int(test_button["w"] * camera_zoom)
        obj_h = int(test_button["h"] * camera_zoom)
        rect_obj = pygame.Rect(obj_x, obj_y, obj_w, obj_h)
        
        pygame.draw.rect(screen, test_button["color"], rect_obj, border_radius=max(1, int(4 * camera_zoom)))
        
        zoom_font_size = max(6, int(14 * camera_zoom))
        font_obj = pygame.font.SysFont("Arial", zoom_font_size, bold=True)
        txt_surf = font_obj.render(test_button["text"], True, COLOR_WHITE)
        txt_rect = txt_surf.get_rect(center=rect_obj.center)
        screen.blit(txt_surf, txt_rect)
        
        canvas_title = font.render(f"GAME CANVAS ({int(camera_zoom * 100)}%)", True, COLOR_WHITE)
        screen.blit(canvas_title, (rect_canvas.x, rect_canvas.y - 25))
        
        screen.set_clip(None)
        
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

        draw_text_center(f"TASK BAR (Zoom: {int(camera_zoom * 100)}%)", rect_task_bar)
        draw_text_center("TOOLBOX (Buttons, Text)", rect_panel_left, COLOR_TEXT_MUTED)
        draw_text_center("PROPERTIES (ID, X, Y, W, H)", rect_properties, COLOR_TEXT_MUTED)
        
        toolslist.draw(screen, font_list)

        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
