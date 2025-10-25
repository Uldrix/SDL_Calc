#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes, math, os, time
from ctypes import c_int, c_uint32, c_char_p, c_void_p, POINTER, Structure, c_uint8, c_uint16

# Chargement SDL2 / SDL_ttf
def load_libs():
    sdl_candidates = ['libSDL2.so', 'libSDL2-2.0.so.0']
    ttf_candidates = ['libSDL2_ttf.so', 'libSDL2_ttf-2.0.so.0']
    sdl = None
    ttf = None
    for n in sdl_candidates:
        try:
            sdl = ctypes.CDLL(n); break
        except: pass
    for n in ttf_candidates:
        try:
            ttf = ctypes.CDLL(n); break
        except: pass
    if not sdl or not ttf:
        raise RuntimeError("SDL2/SDL_ttf introuvables")
    return sdl, ttf

sdl2, sdl2_ttf = load_libs()

# Constantes
SDL_INIT_VIDEO = 0x00000020
SDL_WINDOW_SHOWN = 0x00000004
SDL_RENDERER_ACCELERATED = 0x00000002
SDL_RENDERER_PRESENTVSYNC = 0x00000004
SDL_QUIT = 0x100
SDL_MOUSEBUTTONDOWN = 0x401
SDL_KEYDOWN = 0x300
SDL_KEYUP = 0x301
SDLK_ESCAPE = 27
SDLK_RETURN = 13
SDLK_EQUALS = 61
SDLK_BACKSPACE = 8
SDLK_DELETE = 127
SDLK_UP = 1073741906
SDLK_DOWN = 1073741905
SDLK_SPACE = 32
SDLK_6 = 54
SDLK_8 = 56
SDLK_9 = 57
SDLK_0 = 48
SDLK_F1 = 1073741882
SDLK_F2 = 1073741883
SDLK_F3 = 1073741884
SDLK_F4 = 1073741885
SDLK_F6 = 1073741887
SDLK_F7 = 1073741888
SDLK_F8 = 1073741889
SDLK_F9 = 1073741890

# Types
class SDL_Rect(Structure):
    _fields_ = [("x", c_int), ("y", c_int), ("w", c_int), ("h", c_int)]

class SDL_Color(Structure):
    _fields_ = [("r", c_uint8), ("g", c_uint8), ("b", c_uint8), ("a", c_uint8)]

class SDL_Keysym(Structure):
    _fields_ = [("scancode", c_int), ("sym", c_int), ("mod", c_uint16), ("unused", c_uint32)]

class SDL_KeyboardEvent(Structure):
    _fields_ = [("type", c_uint32), ("timestamp", c_uint32), ("windowID", c_uint32),
                ("state", c_uint8), ("repeat", c_uint8), ("padding2", c_uint8),
                ("padding3", c_uint8), ("keysym", SDL_Keysym)]

class SDL_MouseButtonEvent(Structure):
    _fields_ = [("type", c_uint32), ("timestamp", c_uint32), ("windowID", c_uint32),
                ("which", c_uint32), ("button", c_uint8), ("state", c_uint8),
                ("clicks", c_uint8), ("padding1", c_uint8), ("x", c_int), ("y", c_int)]

class SDL_Event(ctypes.Union):
    _fields_ = [("type", c_uint32), ("key", SDL_KeyboardEvent), ("button", SDL_MouseButtonEvent),
                ("padding", c_uint8 * 56)]

# Prototypes SDL
sdl2.SDL_Init.argtypes = [c_uint32]
sdl2.SDL_Init.restype = c_int
sdl2.SDL_CreateWindow.argtypes = [c_char_p, c_int, c_int, c_int, c_int, c_uint32]
sdl2.SDL_CreateWindow.restype = c_void_p
sdl2.SDL_CreateRenderer.argtypes = [c_void_p, c_int, c_uint32]
sdl2.SDL_CreateRenderer.restype = c_void_p
sdl2.SDL_SetRenderDrawColor.argtypes = [c_void_p, c_uint8, c_uint8, c_uint8, c_uint8]
sdl2.SDL_RenderClear.argtypes = [c_void_p]
sdl2.SDL_RenderPresent.argtypes = [c_void_p]
sdl2.SDL_RenderFillRect.argtypes = [c_void_p, POINTER(SDL_Rect)]
sdl2.SDL_RenderDrawRect.argtypes = [c_void_p, POINTER(SDL_Rect)]
sdl2.SDL_RenderDrawLine.argtypes = [c_void_p, c_int, c_int, c_int, c_int]
sdl2.SDL_PollEvent.argtypes = [POINTER(SDL_Event)]
sdl2.SDL_PollEvent.restype = c_int
sdl2.SDL_DestroyRenderer.argtypes = [c_void_p]
sdl2.SDL_DestroyWindow.argtypes = [c_void_p]
sdl2.SDL_Quit.argtypes = []
sdl2.SDL_Delay.argtypes = [c_uint32]
sdl2.SDL_GetWindowSize = sdl2.SDL_GetWindowSize
sdl2.SDL_GetWindowSize.argtypes = [c_void_p, POINTER(c_int), POINTER(c_int)]
sdl2.SDL_CreateTextureFromSurface.argtypes = [c_void_p, c_void_p]
sdl2.SDL_CreateTextureFromSurface.restype = c_void_p
sdl2.SDL_RenderCopy.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(SDL_Rect)]
sdl2.SDL_QueryTexture.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(c_int), POINTER(c_int)]
sdl2.SDL_DestroyTexture.argtypes = [c_void_p]
sdl2.SDL_FreeSurface.argtypes = [c_void_p]
sdl2.SDL_GetTicks = sdl2.SDL_GetTicks
sdl2.SDL_GetTicks.restype = c_uint32

# Prototypes SDL_ttf
sdl2_ttf.TTF_Init.restype = c_int
sdl2_ttf.TTF_OpenFont.argtypes = [c_char_p, c_int]
sdl2_ttf.TTF_OpenFont.restype = c_void_p
sdl2_ttf.TTF_RenderText_Solid.argtypes = [c_void_p, c_char_p, SDL_Color]
sdl2_ttf.TTF_RenderText_Solid.restype = c_void_p
sdl2_ttf.TTF_CloseFont.argtypes = [c_void_p]
sdl2_ttf.TTF_Quit.argtypes = []

# Couleurs
class Color:
    BG = (44, 62, 80)
    DISPLAY_BG = (10, 61, 10)
    DISPLAY_TEXT = (0, 255, 0)
    BTN_NUMBER = (52, 73, 94)
    BTN_OP = (243, 156, 18)
    BTN_FUNC = (52, 152, 219)
    BTN_CLEAR = (231, 76, 60)
    BTN_EQUALS = (39, 174, 96)
    BTN_GRAPH = (155, 89, 182)
    BTN_OFF = (192, 57, 43)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GRID = (220, 220, 220)

# Utilitaires police
def open_any_font(size=10):
    candidates = [
        b"./DejaVuSansMono.ttf",
        b"./LiberationMono-Regular.ttf",
        b"/usr/local/share/fonts/DejaVuSansMono.ttf",
        b"/usr/local/share/fonts/LiberationMono-Regular.ttf",
        b"/usr/share/fonts/dejavu/DejaVuSansMono.ttf",
        b"/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        b"/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        b"/system/fonts/DroidSansMono.ttf",
    ]
    for p in candidates:
        if p.startswith(b"./"):
            if not os.path.exists(p.decode()): continue
        font = sdl2_ttf.TTF_OpenFont(p, size)
        if font:
            print("Font OK:", p.decode())
            return font
    print("ERREUR: aucune police chargée. Placez DejaVuSansMono.ttf à côté du script.")
    return None

class Button:
    def __init__(self, x, y, w, h, text, color, value, font):
        self.rect = SDL_Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.value = value
        self.font = font

    def draw(self, renderer):
        # Fond du bouton
        sdl2.SDL_SetRenderDrawColor(renderer, *self.color, 255)
        sdl2.SDL_RenderFillRect(renderer, ctypes.byref(self.rect))
        
        # Bordure
        sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
        sdl2.SDL_RenderDrawRect(renderer, ctypes.byref(self.rect))
        
        # Texte
        if self.font and self.text:
            text_color = SDL_Color(255, 255, 255, 255)
            text_bytes = self.text.encode("utf-8", errors="ignore")
            surf = sdl2_ttf.TTF_RenderText_Solid(self.font, text_bytes, text_color)
            if surf:
                tex = sdl2.SDL_CreateTextureFromSurface(renderer, surf)
                if tex:
                    tw = c_int()
                    th = c_int()
                    sdl2.SDL_QueryTexture(tex, None, None, ctypes.byref(tw), ctypes.byref(th))
                    tx = self.rect.x + (self.rect.w - tw.value) // 2
                    ty = self.rect.y + (self.rect.h - th.value) // 2
                    dst = SDL_Rect(tx, ty, tw.value, th.value)
                    sdl2.SDL_RenderCopy(renderer, tex, None, ctypes.byref(dst))
                    sdl2.SDL_DestroyTexture(tex)
                sdl2.SDL_FreeSurface(surf)

class Calculator:
    def __init__(self):
        self.expression = ""
        self.history = []
        self.buttons = []
        self.show_graph = False
        self.graph_func = "x**2"
        self.scroll_offset = 0
        self.key_press_times = {}
        self.just_calculated = False
        self.last_was_error = False
        self.fullscreen_mode = False

    def build_layout_compact(self, font_btn):
        self.buttons = []
        btn_w, btn_h = 50, 30
        start_x, start_y, gap = 3, 125, 2
        
        # Layout pour colonnes 1-5 avec Bk en position (4,0) = 5ème colonne ligne 1
        layout_main = [
            # Ligne 1 - Bk est maintenant en position 5 (colonne 5)
            [('x2', Color.BTN_FUNC, 'x²'), ('xy', Color.BTN_FUNC, 'xʸ'),
             ('log', Color.BTN_FUNC, 'log'), ('ln', Color.BTN_FUNC, 'ln'),
             ('Bk', Color.BTN_CLEAR, '⌫')],
            # Ligne 2
            [('(', Color.BTN_NUMBER, '('), (')', Color.BTN_NUMBER, ')'),
             ('C', Color.BTN_CLEAR, 'C'), ('CE', Color.BTN_CLEAR, 'CE'),
             ('sq', Color.BTN_FUNC, '√')],
            # Ligne 3
            [('7', Color.BTN_NUMBER, '7'), ('8', Color.BTN_NUMBER, '8'),
             ('9', Color.BTN_NUMBER, '9'), ('/', Color.BTN_OP, '/'),
             ('Gr', Color.BTN_GRAPH, 'Gr')],
            # Ligne 4
            [('4', Color.BTN_NUMBER, '4'), ('5', Color.BTN_NUMBER, '5'),
             ('6', Color.BTN_NUMBER, '6'), ('*', Color.BTN_OP, '*'),
             ('mod', Color.BTN_FUNC, 'mod')],
            # Ligne 5
            [('1', Color.BTN_NUMBER, '1'), ('2', Color.BTN_NUMBER, '2'),
             ('3', Color.BTN_NUMBER, '3'), ('-', Color.BTN_OP, '-'),
             ('1/x', Color.BTN_FUNC, '1/x')],
            # Ligne 6
            [('0', Color.BTN_NUMBER, '0'), ('.', Color.BTN_NUMBER, '.'),
             ('=', Color.BTN_EQUALS, '='), ('+', Color.BTN_OP, '+'),
             ('!', Color.BTN_FUNC, '!')]
        ]
        
        # Création des boutons colonnes 1-5
        for r, row in enumerate(layout_main):
            for c, (label, color, val) in enumerate(row):
                x = start_x + c * (btn_w + gap)
                y = start_y + r * (btn_h + gap)
                self.buttons.append(Button(x, y, btn_w, btn_h, label, color, val, font_btn))
        
        # Colonne 6 avec bouton OFF en haut (ligne 0, donc au niveau de la ligne 1 des autres colonnes)
        col6_layout = [
            ('OFF', Color.BTN_OFF, 'OFF'),    # Ligne 0 (même niveau que ligne 1 des autres)
            ('sin', Color.BTN_FUNC, 'sin'),    # Ligne 1 (décalé vers le bas)
            ('cos', Color.BTN_FUNC, 'cos'),    # Ligne 2
            ('tan', Color.BTN_FUNC, 'tan'),    # Ligne 3
            ('pi', Color.BTN_FUNC, 'π'),       # Ligne 4
            ('e', Color.BTN_FUNC, 'e'),        # Ligne 5
            ('', Color.BG, '')                 # Ligne 6 (vide)
        ]
        
        col6_x = start_x + 5 * (btn_w + gap)
        for r, (label, color, val) in enumerate(col6_layout):
            if label:  # Ne pas créer le bouton vide
                y = start_y + r * (btn_h + gap)
                self.buttons.append(Button(col6_x, y, btn_w, btn_h, label, color, val, font_btn))

    def draw_display(self, renderer, font_display, width, height):
        # Zone d'affichage adaptatif selon le mode
        if self.fullscreen_mode:
            # Mode plein écran : toute la fenêtre avec petites marges
            display_rect = SDL_Rect(3, 3, width - 6, height - 6)
            max_visible_lines = (height - 12) // 18  # Calcul dynamique du nombre de lignes
        else:
            # Mode normal : zone d'affichage agrandie
            display_rect = SDL_Rect(3, 3, 314, 115)
            max_visible_lines = 6

        sdl2.SDL_SetRenderDrawColor(renderer, *Color.DISPLAY_BG, 255)
        sdl2.SDL_RenderFillRect(renderer, ctypes.byref(display_rect))
        sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
        sdl2.SDL_RenderDrawRect(renderer, ctypes.byref(display_rect))

        if not font_display:
            return
        
        text_color = SDL_Color(0, 255, 0, 255)
        line_height = 18
        max_chars = 40 if not self.fullscreen_mode else 60
        
        all_lines = []
        for line in self.history:
            line = (line[:max_chars] + "...") if len(line) > max_chars else line
            all_lines.append(line)
        if self.expression:
            expr = (self.expression[:max_chars] + "...") if len(self.expression) > max_chars else self.expression
            all_lines.append(expr)
        
        total_lines = len(all_lines)
        max_scroll = max(0, total_lines - max_visible_lines)
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
        
        start_idx = self.scroll_offset
        end_idx = min(start_idx + max_visible_lines, total_lines)
        visible_lines = all_lines[start_idx:end_idx]
        
        y_offset = display_rect.y + 4
        for line in visible_lines:
            surf = sdl2_ttf.TTF_RenderText_Solid(font_display, line.encode('utf-8'), text_color)
            if surf:
                tex = sdl2.SDL_CreateTextureFromSurface(renderer, surf)
                if tex:
                    tw = c_int()
                    th = c_int()
                    sdl2.SDL_QueryTexture(tex, None, None, ctypes.byref(tw), ctypes.byref(th))
                    dst = SDL_Rect(display_rect.x + 6, y_offset, tw.value, th.value)
                    sdl2.SDL_RenderCopy(renderer, tex, None, ctypes.byref(dst))
                    sdl2.SDL_DestroyTexture(tex)
                    y_offset += line_height
                sdl2.SDL_FreeSurface(surf)

    def scroll_up(self):
        self.scroll_offset = max(0, self.scroll_offset - 1)
    
    def scroll_down(self):
        self.scroll_offset += 1

    def adjust_scroll_to_show_input(self):
        """Ajuste le scroll pour afficher la ligne de saisie active"""
        max_visible_lines = 6 if not self.fullscreen_mode else 15
        total_lines = len(self.history) + (1 if self.expression else 0)
        
        # Positionner le scroll pour voir la dernière ligne (saisie active)
        if total_lines > max_visible_lines:
            self.scroll_offset = total_lines - max_visible_lines
        else:
            self.scroll_offset = 0

    def handle_button(self, value):
        # Gestion du bouton OFF
        if value == 'OFF':
            import sys
            sys.exit(0)
            
        # Si dernière opération était une erreur et qu'on tape un chiffre, nouveau calcul
        if self.last_was_error and value.isdigit():
            self.expression = value
            self.last_was_error = False
            return
            
        if value == '=':
            self.calculate()
        elif value == 'C':
            self.expression = ""
            self.history = []
            self.scroll_offset = 0
            self.just_calculated = False
            self.last_was_error = False
        elif value == 'CE':
            self.expression = ""
            self.just_calculated = False
            self.last_was_error = False
        elif value == '⌫' or value == 'Bk':
            self.expression = self.expression[:-1]
            self.just_calculated = False
            self.last_was_error = False
        elif value == 'Gr' or value == 'Graph':
            self.show_graph = not self.show_graph
        elif value in ['+', '-', '*', '/', '%']:
            self.expression += value
            self.just_calculated = False
            self.last_was_error = False
        elif value == 'π' or value == 'pi':
            if self.just_calculated:
                self.expression = str(math.pi)
            else:
                self.expression += str(math.pi)
            self.just_calculated = False
            self.last_was_error = False
        elif value == 'e':
            if self.just_calculated:
                self.expression = str(math.e)
            else:
                self.expression += str(math.e)
            self.just_calculated = False
            self.last_was_error = False
        elif value == '√' or value == 'sq':
            self.expression += 'sqrt('
            self.just_calculated = False
            self.last_was_error = False
        elif value == 'x²' or value == 'x2':
            self.expression += '**2'
            self.just_calculated = False
            self.last_was_error = False
        elif value == 'xʸ' or value == 'xy':
            self.expression += '**'
            self.just_calculated = False
            self.last_was_error = False
        elif value == 'log':
            self.expression += 'log10('
            self.just_calculated = False
            self.last_was_error = False
        elif value == 'ln':
            self.expression += 'log('
            self.just_calculated = False
            self.last_was_error = False
        elif value in ['sin', 'cos', 'tan']:
            self.expression += value + '('
            self.just_calculated = False
            self.last_was_error = False
        elif value == '1/x':
            self.expression += '**(-1)'
            self.just_calculated = False
            self.last_was_error = False
        elif value == '!':
            self.expression += '!'
            self.just_calculated = False
            self.last_was_error = False
        elif value == 'mod':
            self.expression += '%'
            self.just_calculated = False
            self.last_was_error = False
        else:
            self.expression += value
            self.just_calculated = False
            self.last_was_error = False

    def calculate(self):
        if not self.expression:
            return
        try:
            expr = self.expression
            import re
            for m in re.findall(r'(\d+)!', expr):
                expr = expr.replace(f'{m}!', str(math.factorial(int(m))), 1)
            expr = expr.replace('sqrt', 'math.sqrt')
            expr = expr.replace('sin', 'math.sin')
            expr = expr.replace('cos', 'math.cos')
            expr = expr.replace('tan', 'math.tan')
            expr = expr.replace('log10', 'math.log10')
            expr = expr.replace('log', 'math.log')
            result = eval(expr)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            else:
                result = round(result, 10)
            self.history.append(self.expression)
            self.history.append(f"= {result}")
            self.expression = str(result)
            max_visible_lines = 6 if not self.fullscreen_mode else 15
            self.scroll_offset = max(0, len(self.history) + 1 - max_visible_lines)
            self.just_calculated = True
            self.last_was_error = False
        except:
            self.history.append(self.expression)
            self.history.append("= Error")
            self.expression = ""
            max_visible_lines = 6 if not self.fullscreen_mode else 15
            self.scroll_offset = max(0, len(self.history) + 1 - max_visible_lines)
            self.just_calculated = False
            self.last_was_error = True

    def toggle_fullscreen(self):
        self.fullscreen_mode = not self.fullscreen_mode
        # Ajuster le scroll pour afficher la zone de saisie active
        if not self.fullscreen_mode:
            self.adjust_scroll_to_show_input()

def main():
    if sdl2.SDL_Init(SDL_INIT_VIDEO) < 0:
        print("SDL_Init erreur"); return
    if sdl2_ttf.TTF_Init() < 0:
        print("TTF_Init erreur"); return

    window = sdl2.SDL_CreateWindow(b"Calc", 0, 0, 320, 320, SDL_WINDOW_SHOWN)
    if not window:
        print("Window erreur"); return
    renderer = sdl2.SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC)
    if not renderer:
        print("Renderer erreur"); return

    w = c_int()
    h = c_int()
    sdl2.SDL_GetWindowSize(window, ctypes.byref(w), ctypes.byref(h))
    width, height = w.value, h.value
    
    # Police display: 14px, Police boutons: 10px
    font_display = open_any_font(14)
    font_btn = open_any_font(10)

    calc = Calculator()
    calc.build_layout_compact(font_btn)

    running = True
    event = SDL_Event()

    while running:
        while sdl2.SDL_PollEvent(ctypes.byref(event)):
            if event.type == SDL_QUIT:
                running = False
            elif event.type == SDL_MOUSEBUTTONDOWN:
                if not calc.fullscreen_mode:  # Boutons seulement en mode normal
                    x, y = event.button.x, event.button.y
                    for btn in calc.buttons:
                        if (btn.rect.x <= x <= btn.rect.x + btn.rect.w and
                            btn.rect.y <= y <= btn.rect.y + btn.rect.h):
                            calc.handle_button(btn.value)
                            break
            elif event.type == SDL_KEYDOWN:
                if event.key.repeat:
                    continue
                    
                key = event.key.keysym.sym
                calc.key_press_times[key] = sdl2.SDL_GetTicks()
                
                if key == SDLK_ESCAPE:
                    running = False
                elif key == SDLK_SPACE:
                    calc.toggle_fullscreen()
                elif key == SDLK_RETURN:
                    calc.calculate()
                elif key == SDLK_BACKSPACE:
                    calc.expression = calc.expression[:-1]
                    calc.just_calculated = False
                    calc.last_was_error = False
                elif key == SDLK_DELETE:
                    calc.expression = ""
                    calc.history = []
                    calc.scroll_offset = 0
                    calc.just_calculated = False
                    calc.last_was_error = False
                elif key == SDLK_UP:
                    calc.scroll_up()
                elif key == SDLK_DOWN:
                    calc.scroll_down()
                elif key in [43, 45, 42, 47, 46]:
                    calc.expression += chr(key)
                    calc.just_calculated = False
                    calc.last_was_error = False
                elif key in [49, 50, 51, 52, 53, 55]:
                    if calc.just_calculated or calc.last_was_error:
                        calc.expression = chr(key)
                        calc.just_calculated = False
                        calc.last_was_error = False
                    else:
                        calc.expression += chr(key)
                    
            elif event.type == SDL_KEYUP:
                key = event.key.keysym.sym
                
                if key in calc.key_press_times:
                    press_duration = sdl2.SDL_GetTicks() - calc.key_press_times[key]
                    long_press = press_duration > 500
                    
                    if key == SDLK_0:
                        if long_press:
                            calc.expression += ')'
                        else:
                            if calc.just_calculated or calc.last_was_error:
                                calc.expression = '0'
                                calc.just_calculated = False
                                calc.last_was_error = False
                            else:
                                calc.expression += '0'
                    elif key == SDLK_6:
                        if long_press:
                            calc.expression += '^'
                        else:
                            if calc.just_calculated or calc.last_was_error:
                                calc.expression = '6'
                                calc.just_calculated = False
                                calc.last_was_error = False
                            else:
                                calc.expression += '6'
                    elif key == SDLK_8:
                        if long_press:
                            calc.expression += '*'
                            calc.just_calculated = False
                            calc.last_was_error = False
                        else:
                            if calc.just_calculated or calc.last_was_error:
                                calc.expression = '8'
                                calc.just_calculated = False
                                calc.last_was_error = False
                            else:
                                calc.expression += '8'
                    elif key == SDLK_9:
                        if long_press:
                            calc.expression += '('
                        else:
                            if calc.just_calculated or calc.last_was_error:
                                calc.expression = '9'
                                calc.just_calculated = False
                                calc.last_was_error = False
                            else:
                                calc.expression += '9'
                    elif key == SDLK_EQUALS:
                        if long_press:
                            calc.expression += '+'
                            calc.just_calculated = False
                            calc.last_was_error = False
                        else:
                            calc.calculate()
                    # Nouvelles touches F1-F4 (appui court) et F6-F9 (appui long)
                    elif key == SDLK_F1:
                        if long_press:
                            calc.expression += 'sqrt('
                        else:
                            calc.expression += 'sin('
                        calc.just_calculated = False
                        calc.last_was_error = False
                    elif key == SDLK_F2:
                        if long_press:
                            calc.expression += '**2'
                        else:
                            calc.expression += 'cos('
                        calc.just_calculated = False
                        calc.last_was_error = False
                    elif key == SDLK_F3:
                        if long_press:
                            calc.expression += 'log10('
                        else:
                            calc.expression += 'tan('
                        calc.just_calculated = False
                        calc.last_was_error = False
                    elif key == SDLK_F4:
                        if long_press:
                            calc.expression += 'log('
                        else:
                            if calc.just_calculated or calc.last_was_error:
                                calc.expression = str(math.pi)
                            else:
                                calc.expression += str(math.pi)
                        calc.just_calculated = False
                        calc.last_was_error = False
                    elif key == SDLK_F6:
                        calc.expression += 'sqrt('
                        calc.just_calculated = False
                        calc.last_was_error = False
                    elif key == SDLK_F7:
                        calc.expression += '**2'
                        calc.just_calculated = False
                        calc.last_was_error = False
                    elif key == SDLK_F8:
                        calc.expression += 'log10('
                        calc.just_calculated = False
                        calc.last_was_error = False
                    elif key == SDLK_F9:
                        calc.expression += 'log('
                        calc.just_calculated = False
                        calc.last_was_error = False
                    
                    del calc.key_press_times[key]

        sdl2.SDL_SetRenderDrawColor(renderer, *Color.BG, 255)
        sdl2.SDL_RenderClear(renderer)

        calc.draw_display(renderer, font_display, width, height)
        
        # Dessiner les boutons seulement en mode normal
        if not calc.fullscreen_mode:
            for btn in calc.buttons:
                btn.draw(renderer)

        sdl2.SDL_RenderPresent(renderer)
        sdl2.SDL_Delay(16)

    if font_display:
        sdl2_ttf.TTF_CloseFont(font_display)
    if font_btn:
        sdl2_ttf.TTF_CloseFont(font_btn)
    sdl2_ttf.TTF_Quit()
    sdl2.SDL_DestroyRenderer(renderer)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()

if __name__ == "__main__":
    main()
