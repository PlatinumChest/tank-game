from PIL.ImageOps import scale
from ursina import *
from ursina import Vec3, time
from ursina.prefabs.modified_first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from physics3d import Debugger, BoxCollider, MeshCollider
from physics3d.character_controller import CharacterController
from panda3d.bullet import BulletWorld

game = Ursina()
world = BulletWorld()
Debugger(world, wireframe=True)
world.setGravity(Vec3(0, -98.1, 1))
fire_cooldown = False

Entity.default_shader = lit_with_shadows_shader

editor_camera = EditorCamera(enabled=False, ignore_paused=True)
ground = Entity(model="plane", collider="box", scale=16384, texture="grass", texture_scale=(4, 4), position=(0, -10, 0))
BoxCollider(world, ground, scale=(16384,50,16384))

tank = FirstPersonController(model=r"L333\L333_Tank.obj", z=-10, origin_y=-.5, speed=512, collider="box",
                             texture=r"L333\L333_Tank v1\image.png", height=80)
tank_hitbox = Entity(model="cube", color=color.black)
tank_collider = BoxCollider(world, tank_hitbox, mass=100, scale=(200,100,200))

test_cube = Entity(model="cube", color=color.red, scale=(200,200,200), position=(0, 1000, 0))
BoxCollider(world=world,entity=test_cube,mass=100,scale=(100,100,100))

def update():
    dt = time.dt
    world.doPhysics(dt)
    tank_collider.position = tank.position + Vec3(0, 150, 0)
    tank_collider.rotation = Vec3(0,0,0)
    if held_keys['left mouse']:
        shoot()

def shoot():
    if not fire_cooldown:
        bullet = Entity(model="cube", scale=(100,50,100), color=color.black)
        bullet.position = tank.position + Vec3(0,400,0)
        bullet.rotation = tank.rotation
        bullet.position += bullet.forward

def pause_input(key):
    if key == 'tab':    # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        tank.visible_self = editor_camera.enabled
        tank.cursor.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = tank.position

        application.paused = editor_camera.enabled

pause_handler = Entity(ignore_paused=True, input=pause_input)

game.run()