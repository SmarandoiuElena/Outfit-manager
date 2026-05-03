import pygame

pygame.mixer.init()

def start_music(filepath):
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    
def stop_music():
    pygame.mixer.music.stop()
    
def pause_music():
    pygame.mixer.music.pause()
    
def resume_music():
    pygame.mixer.music.unpause()
    
def set_volume(value):
    pygame.mixer.music.set_volume(float(value))