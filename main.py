import pymunk
import pygame
import pymunk.pygame_util
import sys

pygame.init()

WIDTH,HEIGHT=600,600
window = pygame.display.set_mode((WIDTH,HEIGHT))

def draw(space,window,draw_options):
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()

def add_object(space,radius,mass):
    body = pymunk.Body()
    body.position=(300,300)
    shape=pymunk.Circle(body,radius)
    shape.mass=mass
    shape.color=(255,0,0,100)
    shape.elasticity=1
    shape.friction=0.4
    space.add(body,shape)
    return shape

def create_boundaries(space,width,height):
    rects = [
        [(width/2,height-10),(width,20)],
        [(width/2,10),(width,20)],
        [(10,height/2),(20,height)],
        [(width-10,height/2),(20,height)],
    ]
    for pos,size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position=pos
        shape=pymunk.Poly.create_box(body,size)
        shape.elasticity=0.4
        shape.friction=0.5
        space.add(body,shape)


def run(window,width,height):
    run = True

    space = pymunk.Space()
    space.gravity=(0, 981)

    ball = add_object(space,30,10)
    boundaries = create_boundaries(space,width,height)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    while run:
        FPS = pygame.time.Clock()
        fps=60
        dt = 1 / fps
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        draw(space,window,draw_options)
        space.step(dt)
        FPS.tick(fps)

if __name__ == "__main__":
    run(window,WIDTH,HEIGHT)


