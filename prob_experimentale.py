import pygame

windowSurface = pygame.display.set_mode((1000, 750), pygame.DOUBLEBUF)

s = pygame.Surface((1000,750), pygame.SRCALPHA)   # per-pixel alpha
s.fill((255,255,255,128))                         # notice the alpha value in the color
windowSurface.blit(s, (0,0))
while pygame.event != pygame.QUIT:
    pass