from ursina import *
from ursina import Vec3, time
from ursina.prefabs.modified_first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from physics3d import Debugger, BoxCollider
from panda3d.bullet import BulletWorld
from ursina.prefabs.ursfx import ursfx
# Ursina is the game engine, panda3d is the library for the engine, physics3d is the physics engine.

game = Ursina()
world = BulletWorld()
# Debugger(world, wireframe=True) use for debugging using a wireframe
world.setGravity(Vec3(0, -1962.6, 0)) # Sets the gravity for the work which is 200x earth gravity
Entity.default_shader = lit_with_shadows_shader # Basic light shader

editor_camera = EditorCamera(enabled=False, ignore_paused=True) # Camera for "free cam"
ground = Entity(model="plane", collider="box", scale=16384, texture="grass", texture_scale=(4, 4), position=(0, -10, 0)) # Object for ground
BoxCollider(world, ground, scale=(8192, 10, 8192)) # The physics collider of the ground

tank = FirstPersonController(model=r"L333_Tank\L333_Tank.obj", z=-100, origin_y=-.5, speed=512, collider="box",
                             texture=r"L333_Tank\material11.png", height=80, on_cooldown=False) # Creates Tank Model
tank_hitbox = Entity(model="cube", color=color.black) # Creates Entity for hitbox
tank_collider = BoxCollider(world, tank_hitbox, mass=100, scale=(250, 140, 175)) # Gives the hitbox a collider

for n in range(4):
    for x in range(6):
        for y in range(10):
            for z in range(6):
                test_cube = Entity(model="cube", texture=r"brick.jpg", color=color.red, scale=(200, 200, 200),
                               position=((x * 200) + 500, 100 + (y * 200),-3000 + (n * 1500)+(z * 200)))
                BoxCollider(world=world, entity=test_cube, mass=1, scale=(99, 99, 99))


def update():
    dt = time.dt # datetime
    world.doPhysics(dt) # Cause physics to actually go.
    tank_collider.position = tank.position + Vec3(0, 150, 0) # Makes the tank have the hit box follow it
    tank_collider.rotation = Vec3(0, 0, 0) # Makes the hitbox never turn
    if held_keys['left mouse']: # On left click shoot a bullet
        shoot()


def shoot():
    if not tank.on_cooldown:
        tank.on_cooldown = True
        ursfx([(0.0, 0, 0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.5, wave="sine",
              pitch=random.uniform(-13, -12), pitch_change=-12, speed=3.0) # Sound effect for firing
        Bullet()
        invoke(setattr, tank, 'on_cooldown', False, delay=.5) # Sets shooting cooldown to be .5 seconds

def pause_input(key):
    if key == 'tab':  # Press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        tank.visible_self = editor_camera.enabled
        tank.cursor.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = tank.position

        application.paused = editor_camera.enabled # When game paused have the free cam on


class Bullet(Entity): # For making new Bullets
    def __init__(self):
        super().__init__(model="cube", scale=(50, 50, 100), color=color.black, speed=10, collider="box") # super makes it so entity class is part of the new class
        self.position = tank.position + Vec3(0, 300, 0)
        self.rotation = tank.rotation_getter()
        self.rotation += tank.camera_pivot.rotation
        self.look_at_2d(tank.position) # Move the bullet so it shoots in front on the tank
        self.bullet_hitbox = Entity(model="cube", color=color.black) # New Bullet Hitbox
        self.bullet_collider = BoxCollider(world, self.bullet_hitbox, scale=(90, 90, 100)) # Give hitbox a collider

    def update(self): # Every frame have hitbox follow the bullet
        self.bullet_collider.position = self.position
        self.bullet_collider.rotation = self.rotation
        self.bullet_collider.position = self.position
        self.position += self.forward * time.dt * 80 # Causes the bullet to propel forward


pause_handler = Entity(ignore_paused=True, input=pause_input) # Object for pausing the world

game.run() # Like the mainloop function
