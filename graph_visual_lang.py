import pygame, time, random
from pygame.locals import QUIT
import threading as t


t.Thread(target=pygame.font.init).start()


class Text_Label:
    
    def __init__(self, text="Label text", font_size=20, color=(255, 255, 255, 255), bg=None):
        
        self.text = text
        self.color = color
        self.font = pygame.font.Font('freesansbold.ttf', font_size)
        self.bg = bg
        if self.bg:
            self.render = self.font.render(self.text, True, self.color, self.bg)
        else:
            self.render = self.font.render(self.text, True, self.color)
        self.rect = self.render.get_rect()
        
    def draw(self, surface, coordinates=(0, 0)):
        
        surface.blit(self.render, coordinates)
        
    def change_color(self, color):
        
        self.color = color
        if self.bg:
            self.render = self.font.render(self.text, True, self.color, self.bg)
        else:
            self.render = self.font.render(self.text, True, self.color)
            
    def get_rect(self):
        
        return self.rect


class Node_Pin:
    
    def __init__(self, type="input", label="Dummy Pin", text_color=(255, 255, 255, 255), radio_color=(255, 0, 0, 255),
                 on_mouse_radio_color=(0, 255, 0, 255), parent=None):
        
        self.type = type
        self.value = None
        self.radio_color = radio_color
        self.on_mouse_radio_color = on_mouse_radio_color
        
        self.label = Text_Label(text=label, color=text_color)
        
        self.is_connected = False
        self.connections = []
        self.is_selected = False
        
        self.radius = 13
        
        self.parent = parent
        
    def draw(self, surface, coordinates=(0, 0)):
        
        radius = self.radius
        mouse_pos = pygame.mouse.get_pos()
        if ((mouse_pos[0] > coordinates[0] - radius + self.parent.x and mouse_pos[0] < coordinates[0] + self.parent.x + radius) and (
            mouse_pos[1] > coordinates[1] - radius + self.parent.y and mouse_pos[1] < coordinates[1] + self.parent.y + radius
        )) or self.is_selected:
            pygame.draw.circle(surface, self.on_mouse_radio_color, coordinates, radius, 2)
        else:
            pygame.draw.circle(surface, self.radio_color, coordinates, radius, 2)
            
        label_coords = (coordinates[0] + radius + 5, coordinates[1] - 9)
        self.label.draw(surface, label_coords)
        
    def get_rect(self):
        
        return self.label.rect
        
    
class Node:
    
    def __init__(self, node_pins=[], header="Heading"):
        
        self.heading_label = Text_Label(text=header, color=(0, 0, 0), font_size=32, bg=(255, 128, 0))
        self.node_pins = node_pins
        for i in self.node_pins:
            i.parent = self
        self.number_of_pins = len(self.node_pins)
        
        self.surface_height = self.heading_label.get_rect().height + 20 + self.number_of_pins*(self.node_pins[0].get_rect().height + 20)
        widths = []
        in_w, out_w = [], []
        for i in self.node_pins:
            if i.type == "input":
                in_w.append(i.get_rect().width)
            elif i.type == "output":
                out_w.append(i.get_rect().width)
        try:
            in_max = max(in_w)
        except:
            in_max = 0
        try:
            out_max = max(out_w)
        except:
            out_max = 0
        widths.append(in_max + 30 + out_max)
        widths.append(self.heading_label.get_rect().width)
        self.surface_width = max(widths)
        
        self.surface = pygame.Surface((self.surface_width, self.surface_height), pygame.SRCALPHA)
        
        self.x, self.y = 0, 0
        self.is_selected = False
        
        self.dragable = False
        
        self.drawn_once = False
        
    def draw_initial(self, surface, coordinates=(0, 0)):
        if not(self.drawn_once):
            self.draw(surface, coordinates)
            self.drawn_once = True
        else:
            self.draw(surface)
        
    def draw(self, dis, coordinates=None):
        
        mouse_pos = pygame.mouse.get_pos()
        is_mouse_on = (mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.surface_width) and (
            mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.surface_height)
        if is_mouse_on and not(self.is_selected):
            self.surface.fill((0, 255, 255, 100))
        elif self.is_selected and is_mouse_on:
            self.surface.fill((0, 255, 0, 100))
        elif self.is_selected and not(is_mouse_on):
            self.surface.fill((0, 255, 0, 200))
        else:
            self.surface.fill((0, 255, 255, 200))
         
        if pygame.mouse.get_pressed()[2] and is_mouse_on and not(self.is_selected):
            self.is_selected = True
        
        if self.is_selected:
            self.x, self.y = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                self.is_selected = False
            
        self.heading_label.draw(self.surface, coordinates=(self.surface_width//2 - self.heading_label.get_rect().width//2, 0))
        
        y = self.heading_label.get_rect().height + 20
        for i in self.node_pins:
            if i.type == "input":
                i.draw(self.surface, (0 + i.radius, y))
                y += 20 + self.node_pins[self.node_pins.index(i) - 1].get_rect().height
        
        if coordinates:
            dis.blit(self.surface, coordinates)
            self.x, self.y = coordinates
        else:
            dis.blit(self.surface, (self.x, self.y))
    

words = "speed normalising_factor error_tolerance".split(" ")

main_dis = pygame.display.set_mode((800, 600))

types = []

p = [Node(node_pins=[Node_Pin(label=x) for x in words], header="Position Vector Calculator") for i in range(1)]

INITIATE_EXIT = False

background = pygame.image.load("plane.jpg")

while not(INITIATE_EXIT):
    
    for i in pygame.event.get():
        if i.type == QUIT:
            INITIATE_EXIT = True
    main_dis.blit(background, (0, 0))
    for i in p:
        i.draw_initial(main_dis, (0, p.index(i)*100))
    
    pygame.display.flip()
    time.sleep(1/60)

pygame.quit()
