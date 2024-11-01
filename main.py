from ursina import *
from ursina import Vec3, time
from ursina.prefabs.modified_first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from physics3d import Debugger, BoxCollider
from panda3d.bullet import BulletWorld
from ursina.prefabs.ursfx import ursfx

game = Ursina()
world = BulletWorld()
Debugger(world, wireframe=True)
world.setGravity(Vec3(0, -9.81, 0))

Entity.default_shader = lit_with_shadows_shader

editor_camera = EditorCamera(enabled=False, ignore_paused=True)
ground = Entity(model="plane", collider="box", scale=16384, texture="grass", texture_scale=(4, 4), position=(0, -10, 0))
BoxCollider(world, ground, scale=(8192, 20, 8192))


tank = FirstPersonController(model=r"L333_Tank\L333_Tank.obj", z=-10, origin_y=-.5, speed=512, collider="box",
                             texture=r"L333_Tank\material11.png", height=80, on_cooldown=False)
tank_hitbox = Entity(model="cube", color=color.black)
tank_collider = BoxCollider(world, tank_hitbox, mass=100, scale=(250, 140, 175))

for i in range(32):
    test_cube = Entity(model="cube", color=color.red, scale=(200, 200, 200), position=((i * 200), 1000, 0))
    BoxCollider(world=world, entity=test_cube, mass=100, scale=(100, 100, 100))


def update():
    dt = time.dt
    world.doPhysics(dt)
    tank_collider.position = tank.position + Vec3(0, 150, 0)
    tank_collider.rotation = Vec3(0, 0, 0)
    if held_keys['left mouse']:
        shoot()
    print((tank.rotation_x, tank.rotation_y, tank.rotation_z))


def shoot():
    if not tank.on_cooldown:
        tank.on_cooldown = True
        ursfx([(0.0, 0, 0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.5, wave="sine",
              pitch=random.uniform(-13, -12), pitch_change=-12, speed=3.0)
        Bullet()
        invoke(setattr, tank,'on_cooldown', False, delay=.6)


def pause_input(key):
    if key == 'tab':  # press tab to toggle edit/play mode
        editor_camera.enabled = not editor_camera.enabled

        tank.visible_self = editor_camera.enabled
        tank.cursor.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = tank.position

        application.paused = editor_camera.enabled


class Bullet(Entity):
    def __init__(self):
        super().__init__(model="cube", scale=(50, 25, 100), color=color.black, speed=10, collider="box")
        self.position = tank.position + Vec3(0, 300, 0)
        self.rotation = tank.rotation_getter()
        self.rotation += tank.camera_pivot.rotation
        self.look_at_2d(tank.position)
        self.bullet_hitbox = Entity(model="cube", color=color.black)
        self.bullet_collider = BoxCollider(world, self.bullet_hitbox, scale=(25,12,50))
    def update(self):
        self.bullet_collider.position = self.position
        self.bullet_collider.rotation = self.rotation
        self.bullet_collider.position = self.position
        self.position += self.forward * time.dt * 80

pause_handler = Entity(ignore_paused=True, input=pause_input)

game.run()
