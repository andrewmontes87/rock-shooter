# Andrew's Rock Shooter Computer Program Digital Environment Activity
# http://www.codeskulptor.org/#user16_t7CwHUetyIwf4uq.py
# TRY BOMB, ZOOM, AND SCATTER SHOT!

import simplegui
import math
import random

# global variables
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
scatter_shots = 0
scatter_shot_level = 0
once = False
started = False
special_onscreen = False
bomb_expired = False
rock_group = set([])
missile_group = set([])
explosion_group = set([])
bomb_group = set([])
scatter_shot_message = "Get 50 points to unlock Scatter Shot"


# ImageInfo Class - includes sizing, lifespan
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


# splash image by Andrew
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://static.wixstatic.com/media/de8510_e225fd7e4748591553dd5a1cb12bdca8.png_srz_400_300_75_22_0.50_1.20_0.00_png_srz")  
    
# all other art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris1_brown.png")
# extras - debris2_brown.png, debris3_brown.png, debris4_brown.png, 
#          debris1_blue.png, debris2_blue.png, debris3_blue.png,
#          debris4_blue.png, debris_blend.png

# nebula images
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png")
# extras - nebula_blue.png

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

# scatter missile image
scatter_missile_info = ImageInfo([5,5], [10, 10], 3, 20)
scatter_missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# bomb image
bomb_info = ImageInfo([10,10], [20, 20], 6, 150)
bomb_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot3.png")

# asteroid images
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
asteroid_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png")
asteroid_image3 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")
rock_images = [asteroid_image1, asteroid_image2, asteroid_image3]

# animated explosion
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")
bomb_explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
# extras - explosion_blue.png, explosion_blue2.png


# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.boost = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust or self.boost:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # update velocity
        acc = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
        elif self.boost:
            self.vel[0] += acc[0] * .2
            self.vel[1] += acc[1] * .2
        #apply friction    
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
            
    def set_boost(self, on):
        self.boost = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .06
        
    def decrement_angle_vel(self):
        self.angle_vel -= .06

    def shoot(self):
    # shoot normal missile 
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        new_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(new_missile)
     
    def shoot_bomb(self):
    # shoot bomb 
        global special_onscreen, bomb_group
        if not special_onscreen:
            forward = angle_to_vector(self.angle)
            missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
            missile_vel = [self.vel[0] + 1.5 * forward[0], self.vel[1] + 1.5 * forward[1]]
            new_bomb = Sprite(missile_pos, missile_vel, self.angle, 0, bomb_image, bomb_info, missile_sound, True)
            bomb_group.add(new_bomb)
            special_onscreen = True        
       
    def shoot_scatter(self):
    # shoot scatter shot 
        global special_onscreen, scatter_shots
        if scatter_shots > 0 and not special_onscreen:
            for i in range(8): 
                missile_ang = self.angle + i * 0.78539816339      
                forward = angle_to_vector(missile_ang)
                missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
                missile_vel = [self.vel[0] + 12 * forward[0], self.vel[1] + 12 * forward[1]]
                new_missile = Sprite(missile_pos, missile_vel, missile_ang, 0, scatter_missile_image, scatter_missile_info, missile_sound, False, True)
                missile_group.add(new_missile)
            scatter_shots -= 1
            special_onscreen = True
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius

    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None, bomb = False, scatter = False):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.bomb = bomb
        self.scatter = scatter
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            current_rock_index = ((self.age) % self.image_size[0]) // 1
            current_rock_center = [self.image_center[0] +  current_rock_index * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, current_rock_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                            self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        # update age
        self.age += 1
        # return True if expired
        if self.lifespan != None and self.age >= self.lifespan:
            return True
        else:
            return False
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
       
    def collide(self, other_object):
    # return True if collision between self and other_object 
        if (dist(self.get_position(), other_object.get_position())) < (self.get_radius() + other_object.get_radius()):
            return True
        else:
            return False
  
        
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['z']:
        my_ship.set_boost(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
    elif key == simplegui.KEY_MAP['b']:
        my_ship.shoot_bomb()
    elif key == simplegui.KEY_MAP['s']:
        my_ship.shoot_scatter()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
    elif key == simplegui.KEY_MAP['z']:
        my_ship.set_boost(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        soundtrack.play()

# draw handler        
def draw(canvas):
    global time, started, lives, score, rock_group, special_onscreen, scatter_shot_message, scatter_shots, once, scatter_shot_level
    
    # animate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(scatter_shot_message, [235, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    if scatter_shots > 0:
        canvas.draw_text(str(scatter_shots), [235, 80], 22, "White")

    # draw/update ship
    my_ship.draw(canvas)
    my_ship.update()
    
    # draw/update sprite groups
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    process_sprite_group(bomb_group, canvas)

    # adjust scatter shot ammo
    if scatter_shots < 1:
        scatter_shot_message = "Get 50 points to unlock Scatter Shot"
    if score / 50 >= scatter_shot_level:
        scatter_shot_level += 1
        once = False
    if score > 50 and once == False:
        scatter_shot_message = "Scatter Shots"
        scatter_label.set_text("S: Scatter Shot")
        scatter_shots += 20
        once = True   
    
    # adjust score
    score += group_group_collide(rock_group, missile_group)
    bomb_score = bomb_collide(rock_group, bomb_group)
    if bomb_score > 0:
        special_onscreen = False
        score += bomb_score
    
    # adjust lives
    if group_collide(rock_group, my_ship) > 0:
        lives -= 1   
    if lives <=0:
        started = False
        lives = 3
        score = 0
        scatter_shots = 0
        scatter_shot_level = 0
        scatter_shot_message = "Get 50 points to unlock Scatter Shot"
        scatter_label.set_text(scatter_shot_message)
        rock_group = set([])
        
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        ship_thrust_sound.pause()
        soundtrack.rewind()

# draw and update sprite groups helper function        
def process_sprite_group(sprite_set, canvas):
    global special_onscreen, bomb_expired
    temp = set(sprite_set)
    for sprite in sprite_set:
        sprite.draw(canvas)
        expired = sprite.update()
        if expired:
            if sprite.bomb:
                special_onscreen = False
                bomb_expired = True
            elif sprite.scatter:
                special_onscreen = False
                temp.remove(sprite)
            else:
                temp.remove(sprite)
    sprite_set.intersection_update(temp)

# collision helper functions    
def group_collide(sprite_set, other_object):
    # check if other_object has collided with any object in sprite_set
    temp = set(sprite_set)
    ship_collisions = 0
    for sprite in sprite_set:
        if sprite.collide(other_object):
            temp.remove(sprite)
            ship_collisions += 1
            explosion = Sprite(sprite.get_position(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
    sprite_set.intersection_update(temp)
    return ship_collisions

def group_group_collide(first_sprite_set, second_sprite_set):
    # check if any object in second_sprite_set has collided with any object in first_sprite set
    temp = set(first_sprite_set)
    current_collisions = 0
    total_collisions = 0
    for sprite in first_sprite_set:
        current_collisions = group_collide(second_sprite_set, sprite)
        if current_collisions > 0:
            temp.remove(sprite)
        total_collisions += current_collisions
    first_sprite_set.intersection_update(temp)
    return total_collisions

def bomb_collide(sprite_set, bomb_set):
    # check if any object in bomb_set has collided with any object in sprite_set
    global bomb_expired
    temp = set(sprite_set)
    temp2 = set(bomb_set)
    bomb_collisions = 0
    for sprite in sprite_set:
        for bomb in bomb_set:
            if bomb.collide(sprite) or bomb_expired:
                temp2.remove(bomb)
                explosion1 = Sprite((bomb.pos[0], bomb.pos[1]), [0,0], 0, 0, bomb_explosion_image, explosion_info, explosion_sound)
                explosion2 = Sprite((bomb.pos[0]+75, bomb.pos[1]), [0,0], 0, 0, bomb_explosion_image, explosion_info, explosion_sound)
                explosion3 = Sprite((bomb.pos[0]-75, bomb.pos[1]), [0,0], 0, 0, bomb_explosion_image, explosion_info, explosion_sound)
                explosion4 = Sprite((bomb.pos[0], bomb.pos[1]+75), [0,0], 0, 0, bomb_explosion_image, explosion_info, explosion_sound)
                explosion5 = Sprite((bomb.pos[0], bomb.pos[1]-75), [0,0], 0, 0, bomb_explosion_image, explosion_info, explosion_sound)
                explosion_group.add(explosion1)
                explosion_group.add(explosion2)
                explosion_group.add(explosion3)
                explosion_group.add(explosion4)
                explosion_group.add(explosion5)
                for sprite in sprite_set:
                    if dist(sprite.pos, bomb.pos) < 150:
                        temp.remove(sprite)
                        bomb_collisions += 1
        bomb_set.intersection_update(temp2)
    sprite_set.intersection_update(temp)
    bomb_expired = False
    return bomb_collisions


# timer handler that spawns a rock    
def rock_spawner():
    if started and len(rock_group) < 10:
        multiplier = (score * .1) + 1
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [(random.random() * .6 - .3) * multiplier, (random.random() * .6 - .3) * multiplier]
        rock_avel = random.random() * .2 - .1
        rock_image = random.choice(rock_images)
        new_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, rock_image, asteroid_info)
        if not new_rock.collide(my_ship):
            rock_group.add(new_rock)

            
# initialize frame
frame = simplegui.create_frame("Andrew's Rock Shooter Computer Program Digital Environment Activity", WIDTH, HEIGHT)

# initialize ship
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
frame.add_label("CONTROLS")
frame.add_label("")
frame.add_label("ARROWS: Move Ship")
frame.add_label("SPACE: Shoot")
frame.add_label("B: Bomb")                
frame.add_label("Z: Zoom")
frame.add_label("")
scatter_label = frame.add_label(scatter_shot_message)  
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

# THIS CLASS WAS LOTS OF FUN
