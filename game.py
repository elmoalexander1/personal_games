import gamebox
import pygame
import random
import urllib.request

game_on = False

camera = gamebox.Camera(1100, 600)


coin_velocity = 10

music = gamebox.load_sound('https://upload.wikimedia.org/wikipedia/commons/1/1f/An_8_Bit_Story.ogg')
music.play()

endgame_music = gamebox.load_sound('https://upload.wikimedia.org/wikipedia/commons/9/9d/Anthem_of_Europe_%28US_Navy_instrumental_long_version%29.ogg')

startscreen = gamebox.from_image(camera.x, camera.y, 'http://www.dailygalaxy.com/.a/6a00d8341bf7f753ef01b8d26b68df970c-pi')
startscreen.size = 1100, 600
real_background = gamebox.from_image(camera.x, camera.y, 'https://upload.wikimedia.org/wikipedia/commons/9/9b/Hs-2004-07-a-full_jpgNR.jpg')
real_background.size = 2000, 1000
game_over_background = gamebox.from_image(camera.x, camera.y, 'http://cdn.playbuzz.com/cdn/834c424a-7fc1-438e-845b-dbdc7d89ff9e/f1f22690-5563-4ca5-8f3c-e0044897a6a6.jpg')
game_over_background.size = (1100,600)

player = gamebox.from_image(75, 75, 'https://image.shutterstock.com/z/stock-vector-vector-astronaut-design-329646671.jpg')
player.size = 50, 50

coin = gamebox.from_image(500, 300, 'https://upload.wikimedia.org/wikipedia/commons/4/4c/Louis_XIV_par_Varin_C_des_M.jpg')
coin.size = 30, 30

#giving the coin an initial speed
coin.xspeed = coin_velocity
coin.yspeed= coin_velocity


enemy = gamebox.from_image(800, 450, 'https://www.nasa.gov/sites/default/files/thumbnails/image/edu_asteroid_large.jpg')


# more enemies
enemies = []
for number in range(50 , 600, 125 ):
    enemies.append(gamebox.from_image(1400, number,
                                      'https://www.nasa.gov/sites/default/files/thumbnails/image/edu_asteroid_large.jpg'))
different_moving_enemies = []
for number in range(550, 2100, 150):
    different_moving_enemies.append(gamebox.from_image(number, -200,
                                      'https://www.nasa.gov/sites/default/files/thumbnails/image/edu_asteroid_large.jpg'))
# all the walls and lists of walls
walls = [gamebox.from_color(550,600,'brown',1500,20), gamebox.from_color(0,300,'brown',20,780), gamebox.from_color(1100,300, 'brown',20,780),
         gamebox.from_color(550, 0, 'brown', 1500, 20)]
top_bottom = [gamebox.from_color(550,0,'brown',1500,20), gamebox.from_color(550,600,'brown',1500,20)]
left_right = [gamebox.from_color(0,300,'brown',20,780), gamebox.from_color(1100,300, 'brown',20,780)]
floor = gamebox.from_color(550,600,'brown',1500,20)
left_wall = gamebox.from_color(0,300,'brown',20,780)
right_wall = gamebox.from_color(1100,300, 'brown',20,780)
ceiling = gamebox.from_color(550,0,'brown',1500,20)

score = 0
def start(keys):
    global game_on
    game_on = False
    names = gamebox.from_text(camera.x,camera.y + 100, "By Elmo Alexander", "Arial", 40, "Red")
    welcome = gamebox.from_text(camera.x, camera.y , "WELCOME TO ACE THE TREASURE HUNTING ASTRONAUT", "Arial", 40, "Cyan")
    instructions = gamebox.from_text(camera.x, camera.y + 50, "Move With Arrow Keys, Collect Coins, and Avoid Asteroids!", "Arial", 40, 'Red')
    instructions_spacebar = gamebox.from_text(camera.x, camera.y + 150,"Press the Spacebar to Start!", "Arial", 40, 'Yellow')
    camera.clear("black")
    camera.draw(startscreen)
    camera.draw(welcome)
    camera.draw(names)
    camera.draw(instructions)
    camera.draw(instructions_spacebar)
    camera.display()

def end(keys):
    music.stop()
    endgame_music.play()
    endgame = gamebox.from_text(camera.x, camera.y, "Game Over ", "Arial", 70, "Red")
    score_display = gamebox.from_text(camera.x, camera.y + 200, "Your score is " + str(score) + "!", "Arial", 50,
                                      "Yellow")
    time_lasted = gamebox.from_text(camera.x, camera.y + 250,"You survived " + str(int(frame / ticks_per_second)) + " seconds", "Arial", 40,"Yellow")
    camera.clear("black")
    camera.draw(game_over_background)
    camera.draw(endgame)
    camera.draw(score_display)
    camera.draw(time_lasted)
    camera.display()

frame = 0
def tick(keys):
    global frame
    global game_on
    if game_on == True:
        for wall in walls:
            if player.touches(wall):
                player.move_to_stop_overlapping(wall)

        global score
        if player.touches(coin):
            coin.x = random.randrange(50, 1050)
            coin.y = random.randrange(50, 550)
            coin.yspeed = random.randrange(-1, 10)
            coin.xspeed = random.randrange(-1, 10)
            score += 1

        # coin moves around
        coin.move_speed()
        for wall in top_bottom:
            if coin.touches(wall):
                coin.speedy *= -1
        if coin.touches(left_wall) or coin.touches(right_wall):
                coin.speedx *= -1

        camera.clear('black')

        # characters and coins
        camera.draw(real_background)
        camera.draw(player)
        camera.draw(coin)

        camera.draw(floor)
        camera.draw(ceiling)
        camera.draw(left_wall)
        camera.draw(right_wall)

        for asteroid in enemies:
            camera.draw(asteroid)
            asteroid.size = 70, 70
            if player.touches(asteroid):
                return end(keys)
        for projectile in different_moving_enemies:
            camera.draw(projectile)
            projectile.size = 40, 40
            if player.touches(projectile):
                return end(keys)

        # move asteroid and projectiles to the side
        for asteroid in enemies:
            asteroid.x -= random.randrange(4, 15)
            if asteroid.left <= 0:
                asteroid.x = 1550
                if player.touches(asteroid):
                    return end(keys)

        for projectile in enemies:
            projectile.x -= 7
            projectile.y += 7
            projectile.rotate(5)
            if projectile.left <= 0 or projectile.bottom >= 800:
                projectile.x = random.randrange(750, 2500, 200)
                projectile.y = -200
                if player.touches(projectile):
                    return end(keys)
                # losing
        if player.touches(asteroid):
            gamebox.pause()
            return end(keys)
        if player.touches(projectile):
            gamebox.pause()
            return end(keys)
        frame += 1
        #moving the character
        if pygame.K_UP in keys:
            player.y -= 10
        if pygame.K_DOWN in keys:
            player.y += 10
        if pygame.K_RIGHT in keys:
            player.x += 10
        if pygame.K_LEFT in keys:
            player.x -= 10

        camera.display()

    if pygame.K_SPACE in keys:
        game_on = True
    if game_on == False:
        return start(keys)




ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)
