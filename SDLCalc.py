#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ctypes, math, os, time, re
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
SDLK_h = 104
SDLK_c = 99
SDLK_i = 105
SDLK_q = 113
SDLK_w = 119
SDLK_e = 101
SDLK_r = 114
SDLK_t = 116
SDLK_6 = 54
SDLK_8 = 56
SDLK_9 = 57
SDLK_0 = 48
SDLK_F1 = 1073741882
SDLK_F2 = 1073741883
SDLK_F3 = 1073741884
SDLK_F4 = 1073741885
SDLK_F5 = 1073741886
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
    HINT_TEXT = (255, 255, 0)
    INFO_BG = (200, 200, 200)
    INFO_TEXT = (0, 0, 0)
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
    def __init__(self, x, y, w, h, text, color, value, font, hint=""):
        self.rect = SDL_Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.value = value
        self.font = font
        self.hint = hint

    def draw(self, renderer, show_hints=True, hint_font=None):
        # Fond du bouton
        sdl2.SDL_SetRenderDrawColor(renderer, *self.color, 255)
        sdl2.SDL_RenderFillRect(renderer, ctypes.byref(self.rect))
        
        # Bordure
        sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
        sdl2.SDL_RenderDrawRect(renderer, ctypes.byref(self.rect))
        
        # Texte principal
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
        
        # Overlay d'aide (hint) en haut à droite
        if show_hints and self.hint and hint_font:
            hint_color = SDL_Color(*Color.HINT_TEXT, 255)
            hint_bytes = self.hint.encode("utf-8", errors="ignore")
            surf = sdl2_ttf.TTF_RenderText_Solid(hint_font, hint_bytes, hint_color)
            if surf:
                tex = sdl2.SDL_CreateTextureFromSurface(renderer, surf)
                if tex:
                    tw = c_int()
                    th = c_int()
                    sdl2.SDL_QueryTexture(tex, None, None, ctypes.byref(tw), ctypes.byref(th))
                    tx = self.rect.x + self.rect.w - tw.value - 2
                    ty = self.rect.y + 2
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
        self.show_hints = True
        self.show_info = False

    def build_layout_compact(self, font_btn):
        self.buttons = []
        btn_w, btn_h = 50, 30
        start_x, start_y, gap = 3, 125, 2
        
        # Mapping des hints (touches clavier)
        hints = {
            'OFF': 'Esc',
            'CE': 'Del',
            'sin': 'F1',
            'cos': 'F2',
            'tan': 'F3',
            'pi': 'F4',
            'e': 'F5',
            'x2': 'F6',
            'xy': 'F7',
            'log': 'F8',
            'ln': 'F9',
            '*': '8',
            '+': '=',
            '(': '9',
            ')': '0',
            'sq': 'Q',
            'Gr': 'W',
            'mod': 'E',
            '1/x': 'R',
            '!': 'T'
        }
        
        # Layout pour colonnes 1-5
        layout_main = [
            # Ligne 1
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
                hint = hints.get(label, "")
                self.buttons.append(Button(x, y, btn_w, btn_h, label, color, val, font_btn, hint))
        
        # Colonne 6
        col6_layout = [
            ('OFF', Color.BTN_OFF, 'OFF'),
            ('sin', Color.BTN_FUNC, 'sin'),
            ('cos', Color.BTN_FUNC, 'cos'),
            ('tan', Color.BTN_FUNC, 'tan'),
            ('pi', Color.BTN_FUNC, 'π'),
            ('e', Color.BTN_FUNC, 'e'),
            ('', Color.BG, '')
        ]
        
        col6_x = start_x + 5 * (btn_w + gap)
        for r, (label, color, val) in enumerate(col6_layout):
            if label:
                y = start_y + r * (btn_h + gap)
                hint = hints.get(label, "")
                self.buttons.append(Button(col6_x, y, btn_w, btn_h, label, color, val, font_btn, hint))

    def undo_step(self):
        """Retire la dernière étape de l'expression"""
        if not self.expression:
            return
        
        # Pattern pour identifier les différents types d'étapes
        patterns = [
            r'(sin|cos|tan|sqrt|log10|log)\($',  # Fonctions
            r'\d+\.?\d*$',  # Nombres (avec ou sans décimale)
            r'[+\-*/%^]$',  # Opérateurs
            r'\*\*\d*$',  # Puissance
            r'\)$',  # Parenthèse fermante
            r'\($',  # Parenthèse ouvrante
            r'!$',  # Factorielle
            r'\d+\.\d+e[+-]?\d+$',  # Notation scientifique (pi, e)
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.expression)
            if match:
                self.expression = self.expression[:match.start()]
                self.just_calculated = False
                self.last_was_error = False
                return
        
        # Si aucun pattern ne correspond, retire le dernier caractère
        if self.expression:
            self.expression = self.expression[:-1]
            self.just_calculated = False
            self.last_was_error = False

    def draw_display(self, renderer, font_display, width, height):
        if self.fullscreen_mode:
            display_rect = SDL_Rect(3, 3, width - 6, height - 6)
            max_visible_lines = (height - 12) // 18
        else:
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

    def draw_info_overlay(self, renderer, font_info, width, height):
        """Dessine l'overlay d'information"""
        if not self.show_info or not font_info:
            return
        
        # Rectangle centré
        info_w, info_h = 250, 100
        info_x = (width - info_w) // 2
        info_y = (height - info_h) // 2
        
        info_rect = SDL_Rect(info_x, info_y, info_w, info_h)
        
        # Fond gris clair
        sdl2.SDL_SetRenderDrawColor(renderer, *Color.INFO_BG, 255)
        sdl2.SDL_RenderFillRect(renderer, ctypes.byref(info_rect))
        
        # Bordure noire
        sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
        sdl2.SDL_RenderDrawRect(renderer, ctypes.byref(info_rect))
        
        # Textes
        text_color = SDL_Color(*Color.INFO_TEXT, 255)
        lines = [
            "Designed by Uldrix",
            "For experimentations only",
            "Not allowed for commercial use"
        ]
        
        y_offset = info_y + 15
        for line in lines:
            surf = sdl2_ttf.TTF_RenderText_Solid(font_info, line.encode('utf-8'), text_color)
            if surf:
                tex = sdl2.SDL_CreateTextureFromSurface(renderer, surf)
                if tex:
                    tw = c_int()
                    th = c_int()
                    sdl2.SDL_QueryTexture(tex, None, None, ctypes.byref(tw), ctypes.byref(th))
                    tx = info_x + (info_w - tw.value) // 2
                    dst = SDL_Rect(tx, y_offset, tw.value, th.value)
                    sdl2.SDL_RenderCopy(renderer, tex, None, ctypes.byref(dst))
                    sdl2.SDL_DestroyTexture(tex)
                    y_offset += 25
                sdl2.SDL_FreeSurface(surf)

    def scroll_up(self):
        self.scroll_offset = max(0, self.scroll_offset - 1)
    
    def scroll_down(self):
        self.scroll_offset += 1

    def adjust_scroll_to_show_input(self):
        max_visible_lines = 6 if not self.fullscreen_mode else 15
        total_lines = len(self.history) + (1 if self.expression else 0)
        
        if total_lines > max_visible_lines:
            self.scroll_offset = total_lines - max_visible_lines
        else:
            self.scroll_offset = 0

    def toggle_hints(self):
        self.show_hints = not self.show_hints

    def toggle_info(self):
        self.show_info = not self.show_info

    def handle_button(self, value):
        if value == 'OFF':
            import sys
            sys.exit(0)
            
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
            # Remplacer ^ par **
            expr = expr.replace('^', '**')
            # Factorielles
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
    
    font_display = open_any_font(14)
    font_btn = open_any_font(10)
    font_hint = open_any_font(8)
    font_info = open_any_font(12)

    calc = Calculator()
    calc.build_layout_compact(font_btn)

    running = True
    event = SDL_Event()

    while running:
        while sdl2.SDL_PollEvent(ctypes.byref(event)):
            if event.type == SDL_QUIT:
                running = False
            elif event.type == SDL_MOUSEBUTTONDOWN:
                if not calc.fullscreen_mode:
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
                elif key == SDLK_h:
                    calc.toggle_hints()
                elif key == SDLK_i:
                    calc.toggle_info()
                elif key == SDLK_c:
                    calc.undo_step()
                elif key == SDLK_q:
                    calc.expression += 'sqrt('
                    calc.just_calculated = False
                    calc.last_was_error = False
                elif key == SDLK_w:
                    calc.show_graph = not calc.show_graph
                elif key == SDLK_e:
                    calc.expression += '%'
                    calc.just_calculated = False
                    calc.last_was_error = False
                elif key == SDLK_r:
                    calc.expression += '**(-1)'
                    calc.just_calculated = False
                    calc.last_was_error = False
                elif key == SDLK_t:
                    calc.expression += '!'
                    calc.just_calculated = False
                    calc.last_was_error = False
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
                    elif key == SDLK_F5:
                        if calc.just_calculated or calc.last_was_error:
                            calc.expression = str(math.e)
                        else:
                            calc.expression += str(math.e)
                        calc.just_calculated = False
                        calc.last_was_error = False
                    elif key == SDLK_F6:
                        calc.expression += '**2'
                        calc.just_calculated = False
                        calc.last_was_error = False
                    elif key == SDLK_F7:
                        calc.expression += '**'
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
        
        if not calc.fullscreen_mode:
            for btn in calc.buttons:
                btn.draw(renderer, calc.show_hints, font_hint)
        
        # Dessiner l'overlay d'info par-dessus tout
        calc.draw_info_overlay(renderer, font_info, width, height)

        sdl2.SDL_RenderPresent(renderer)
        sdl2.SDL_Delay(16)

    if font_display:
        sdl2_ttf.TTF_CloseFont(font_display)
    if font_btn:
        sdl2_ttf.TTF_CloseFont(font_btn)
    if font_hint:
        sdl2_ttf.TTF_CloseFont(font_hint)
    if font_info:
        sdl2_ttf.TTF_CloseFont(font_info)
    sdl2_ttf.TTF_Quit()
    sdl2.SDL_DestroyRenderer(renderer)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()

if __name__ == "__main__":
    main()
