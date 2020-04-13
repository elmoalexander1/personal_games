import pygame
import gamebox
import random

camera = gamebox.Camera(800, 600)
player = gamebox.from_color(50, 300, 'red', 20, 20)

pillars = []
holes = []
for x in range(300, 800, 150):
    x_position = x
    y_position = 600
    color = 'green'
    width = 50
    height = random.randrange(0, 570)
    pillars.append(gamebox.from_color(
        x_position,
        y_position,
        color,
        width,
        height))
    pillars.append(gamebox.from_color(
        x_position,
        0,
        color,
        width,
        700 - (height / 2) ))


gameover = gamebox.from_text(camera.x, camera.y, 'You lose!', "Arial", 80, 'green')

def end_game(keys):
    camera.draw(gameover)
    time_lasted = gamebox.from_text(camera.x, camera.bottom-20, 'you played for ' + str(int(frame/ticks_per_second)) + ' seconds', 'Arial', 40, 'yellow')
    camera.draw(time_lasted)
    camera.display()

frame = 0
def ticks(keys):
    camera.clear('cyan')
    for hole in holes:
        camera.draw(hole)
    for pillar in pillars:
        camera.draw(pillar)
        if player.bottom > camera.bottom:
            return end_game(keys)
        if player.touches(pillar):
            return end_game(keys)
    global frame
    frame += 1


    # moving the player up
    if pygame.K_SPACE in keys:
        player.yspeed = -10

    # gravity
    player.yspeed += 1.1
    player.move_speed()

    #moving the pillars
    for pillar in pillars:
        pillar.x -= 3
        if pillar.x < camera.left:
            pillar.x = 850
    for hole in holes:
        hole.x -= 3
        if hole.x < camera.left:
            hole.x = 850
            hole.y = random.randrange(0, 570)

    camera.draw(player)
    camera.display()

ticks_per_second = 30

gamebox.timer_loop(ticks_per_second, ticks)