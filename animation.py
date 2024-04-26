import pygame

class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, animation_loop, sprite_name, size=(200, 200)):
        super().__init__()
        self.size = size
        self.name = sprite_name
        self.image = pygame.image.load(f'PygameAssets/{sprite_name}.png')
        self.image = pygame.transform.scale(self.image, size)
        self.current_image = 0 # start animation to the first image (0)
        self.images = animations.get(sprite_name)
        self.animation = False
        self.loop = animation_loop

    #Start the animation
    def start_animation(self):
        self.animation = True

    #Show the animation
    def animate(self):
        if self.animation:

            #go to the next frame
            self.current_image += 1

            if self.current_image >= len(self.images):
                #reset anime
                self.current_image = 0

                if (self.loop is False):
                    #turn off animation
                    self.animation = False

            #change the previous image to the next one
            self.image = self.images[self.current_image]
            self.image = pygame.transform.scale(self.image, self.size)

            
#Load the images to make the animation
def load_animation_images(sprite_name):
    images = []
    path = f"PygameAssets/{sprite_name}/{sprite_name}"

    for num in range(0,100):
        try:
            image_path = path + str(num) + '.png'
            images.append(pygame.image.load(image_path))
        except:
            break
    
    return images

# ship1_ -> [...ship1_1.png, ...ship1_2.png, ...]
# ship2_ -> [...ship2_1.png, ...ship2_2.png, ...]
# spaceship1_ -> [...spaceship1_1.png, ...spaceship1_2.png, ...]
# spaceship2_ -> [...spaceship2_1.png, ...spaceship2_2.png, ...]
# spaceship3_ -> [...spaceship3_1.png, ...spaceship3_2.png, ...]
# spaceship4_ -> [...spaceship4_1.png, ...spaceship4_2.png, ...]
# spaceship5_ -> [...spaceship5_1.png, ...spaceship5_2.png, ...]
# spaceship6_ -> [...spaceship6_1.png, ...spaceship6_2.png, ...]
# explosion -> [...explosion1.png, ...explosion2.png, ...]
# red_bird_ -> [...red_bird_1.png, ...red_bird_2.png, ...]
# helicopter_ -> [...helicopter_1.png, ...helicopter_2.png, ...]

animations = {
    'ship1_' : load_animation_images('ship1_'),
    'ship2_' : load_animation_images('ship2_'),
    # 'asteroid' : load_animation_images('asteroid'),
    'spaceship1_' : load_animation_images('spaceship1_'),
    'spaceship2_' : load_animation_images('spaceship2_'),
    'spaceship3_' : load_animation_images('spaceship3_'),
    'spaceship4_' : load_animation_images('spaceship4_'),
    'spaceship5_' : load_animation_images('spaceship5_'),
    'spaceship6_' : load_animation_images('spaceship6_'),
    'explosion' : load_animation_images('explosion'),
    'red_bird_' : load_animation_images('red_bird_'),
    'helicopter_' : load_animation_images('helicopter_')
}
