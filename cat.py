import pyglet
from pyglet.window import key
from pyglet import font
from enum import Enum
import sys
import os

window = pyglet.window.Window()
keys = key.KeyStateHandler()
window.push_handlers(keys)

if getattr(sys, 'frozen', False):
    # Running in a bundled executable: assets are extracted to sys._MEIPASS.
    # See https://pyinstaller.org/en/stable/runtime-information.html#run-time-information
    base_path = sys._MEIPASS
else:
    # Running in a normal environment.
    base_path = os.path.abspath(".")

# Construct the full path to the assets folder.
assets_path = os.path.join(base_path, 'assets')

# Set the resource path for pyglet.
pyglet.resource.path = [assets_path]

# pyglet.resource.path = ['assets']
pyglet.resource.reindex()

font_file = os.path.join(assets_path, 'sourgummy.ttf')
font.add_file(font_file)
sour_gummy = font.load('Sour Gummy')

#event_logger = pyglet.window.event.WindowEventLogger()
#window.push_handlers(event_logger)

label = pyglet.text.Label(
  'a game about a cat',
  color = (180, 180, 180),
  font_name = 'Sour Gummy',
  font_size = 30,
  x = window.width // 2,
  y = window.height // 2 + 120,
  anchor_x = 'center',
  anchor_y = 'center'
)

label2 = pyglet.text.Label(
  'more of a bare-bones tech demo really (first attempt at python / pyglet)',
  color = (180, 180, 180),
  font_name = 'Verdana',
  font_size = 8,
  x = window.width // 2,
  y = window.height // 2 + 90,
  anchor_x = 'center',
  anchor_y = 'center'
)

label3 = pyglet.text.Label(
  'WASD to walk, L-SHIFT to run',
  color = (180, 180, 180),
  font_name = 'Sour Gummy',
  font_size = 16,
  x = window.width // 2,
  y = window.height // 2 - 100,
  anchor_x = 'center',
  anchor_y = 'center'
)

class CatState(Enum):
  IDLE = 0
  WALK = 1
  SIT = 2
  RUN = 3

class CatDirection(Enum):
  SOUTH = 0
  WEST = 1
  NORTH = 2
  EAST = 3


class Cat:
  def __init__(self, x, y):
    self.direction = CatDirection.SOUTH
    self.state = CatState.IDLE
    self.last_direction = None
    self.last_state = None
    self.x = window.width//2 - 48
    self.y = window.height//2 - 64
    self.sprite = pyglet.sprite.Sprite(self.cat_sit_south_animation, x=self.x, y=self.y)
    self.sprite.push_handlers(self)

  cat_walk_speed = 1
  cat_run_speed = 3

  cat_sprite_sheet = pyglet.resource.image('catx3.png')
  cat_image_grid = pyglet.image.ImageGrid(cat_sprite_sheet, rows=17, columns=32)

  cat_sit_south_frames = [cat_image_grid[480], cat_image_grid[481], cat_image_grid[482], cat_image_grid[483], cat_image_grid[448], cat_image_grid[449], cat_image_grid[450]]
  cat_sit_west_frames = [cat_image_grid[352], cat_image_grid[353], cat_image_grid[354], cat_image_grid[355], cat_image_grid[320], cat_image_grid[321], cat_image_grid[322]]
  cat_sit_north_frames = [cat_image_grid[224], cat_image_grid[225], cat_image_grid[226], cat_image_grid[227], cat_image_grid[192], cat_image_grid[193], cat_image_grid[194]]
  cat_sit_east_frames = [cat_image_grid[96], cat_image_grid[97], cat_image_grid[98], cat_image_grid[99], cat_image_grid[64], cat_image_grid[65], cat_image_grid[66]]

  cat_idle_south_frames = [cat_image_grid[486], cat_image_grid[487], cat_image_grid[452], cat_image_grid[487], cat_image_grid[486], cat_image_grid[485], cat_image_grid[484], cat_image_grid[485]]
  cat_idle_west_frames = [cat_image_grid[358], cat_image_grid[359], cat_image_grid[324], cat_image_grid[359], cat_image_grid[358], cat_image_grid[357], cat_image_grid[356], cat_image_grid[357]]
  cat_idle_north_frames = [cat_image_grid[230], cat_image_grid[231], cat_image_grid[196], cat_image_grid[231], cat_image_grid[230], cat_image_grid[229], cat_image_grid[228], cat_image_grid[229]]
  cat_idle_east_frames = [cat_image_grid[102], cat_image_grid[103], cat_image_grid[68], cat_image_grid[103], cat_image_grid[102], cat_image_grid[101], cat_image_grid[100], cat_image_grid[101]]

  cat_walk_south_frames = cat_image_grid[492:496]
  cat_walk_west_frames = cat_image_grid[364:368]
  cat_walk_north_frames = cat_image_grid[236:240]
  cat_walk_east_frames = cat_image_grid[108:112]

  cat_run_south_frames = [cat_image_grid[496], cat_image_grid[497], cat_image_grid[498], cat_image_grid[499], cat_image_grid[464]]
  cat_run_west_frames = [cat_image_grid[368], cat_image_grid[369], cat_image_grid[370], cat_image_grid[371], cat_image_grid[336]]
  cat_run_north_frames = [cat_image_grid[240], cat_image_grid[241], cat_image_grid[242], cat_image_grid[243], cat_image_grid[208]]
  cat_run_east_frames = [cat_image_grid[112], cat_image_grid[113], cat_image_grid[114], cat_image_grid[115], cat_image_grid[80]]

  cat_sit_south_animation = pyglet.image.Animation.from_image_sequence(cat_sit_south_frames, duration=0.1, loop=False)
  cat_sit_west_animation = pyglet.image.Animation.from_image_sequence(cat_sit_west_frames, duration=0.1, loop=False)
  cat_sit_north_animation = pyglet.image.Animation.from_image_sequence(cat_sit_north_frames, duration=0.1, loop=False)
  cat_sit_east_animation = pyglet.image.Animation.from_image_sequence(cat_sit_east_frames, duration=0.1, loop=False)

  cat_idle_south_animation = pyglet.image.Animation.from_image_sequence(cat_idle_south_frames, duration=1.5)
  cat_idle_west_animation = pyglet.image.Animation.from_image_sequence(cat_idle_west_frames, duration=1.5)
  cat_idle_north_animation = pyglet.image.Animation.from_image_sequence(cat_idle_north_frames, duration=1.5)
  cat_idle_east_animation = pyglet.image.Animation.from_image_sequence(cat_idle_east_frames, duration=1.5)

  cat_walk_south_animation = pyglet.image.Animation.from_image_sequence(cat_walk_south_frames, duration=0.25)
  cat_walk_west_animation = pyglet.image.Animation.from_image_sequence(cat_walk_west_frames, duration=0.25)
  cat_walk_north_animation = pyglet.image.Animation.from_image_sequence(cat_walk_north_frames, duration=0.25)
  cat_walk_east_animation = pyglet.image.Animation.from_image_sequence(cat_walk_east_frames, duration=0.25)

  cat_run_south_animation = pyglet.image.Animation.from_image_sequence(cat_run_south_frames, duration=0.1)
  cat_run_west_animation = pyglet.image.Animation.from_image_sequence(cat_run_west_frames, duration=0.1)
  cat_run_north_animation = pyglet.image.Animation.from_image_sequence(cat_run_north_frames, duration=0.1)
  cat_run_east_animation = pyglet.image.Animation.from_image_sequence(cat_run_east_frames, duration=0.1)


  def on_animation_end(self):
    if self.state == CatState.SIT:
      self.state = CatState.IDLE

cat = Cat(x = window.width//2 - 48, y = window.height//2)

@window.event
def on_draw():
  window.clear()
  label.draw()
  label2.draw()
  label3.draw()

  global cat
  x_change = 0
  y_change = 0

  if keys[key.A]:
    cat.direction = CatDirection.WEST
    if cat.x > 0:
      x_change -= cat.cat_walk_speed
  elif keys[key.D]:
    cat.direction = CatDirection.EAST
    if cat.x < window.width - 96:
      x_change += cat.cat_walk_speed
  elif keys[key.W]:
    cat.direction = CatDirection.NORTH
    if cat.y < window.height - 96:
      y_change += cat.cat_walk_speed
  elif keys[key.S]:
    cat.direction = CatDirection.SOUTH
    if cat.y > 0:
      y_change -= cat.cat_walk_speed

  if keys[key.A] or keys[key.D] or keys[key.W] or keys[key.S]:
    if keys[key.LSHIFT]:
      cat.state = CatState.RUN
      cat.x += x_change * cat.cat_run_speed
      cat.sprite.x += x_change * cat.cat_run_speed
      cat.y += y_change * cat.cat_run_speed
      cat.sprite.y += y_change * cat.cat_run_speed
    else:
      cat.state = CatState.WALK
      cat.x += x_change
      cat.sprite.x += x_change
      cat.y += y_change
      cat.sprite.y += y_change
  elif cat.state != CatState.SIT and cat.state != CatState.IDLE and not keys[key.A] and not keys[key.D] and not keys[key.W] and not keys[key.S]:
    cat.state = CatState.SIT

  if cat.state != cat.last_state or cat.direction != cat.last_direction:
      if cat.state == CatState.WALK:
          if cat.direction == CatDirection.WEST:
              cat.sprite.image = cat.cat_walk_west_animation
          elif cat.direction == CatDirection.EAST:
              cat.sprite.image = cat.cat_walk_east_animation
          elif cat.direction == CatDirection.NORTH:
              cat.sprite.image = cat.cat_walk_north_animation
          elif cat.direction == CatDirection.SOUTH:
              cat.sprite.image = cat.cat_walk_south_animation
      elif cat.state == CatState.SIT:
          if cat.direction == CatDirection.WEST:
              cat.sprite.image = cat.cat_sit_west_animation
          elif cat.direction == CatDirection.EAST:
              cat.sprite.image = cat.cat_sit_east_animation
          elif cat.direction == CatDirection.NORTH:
              cat.sprite.image = cat.cat_sit_north_animation
          elif cat.direction == CatDirection.SOUTH:
              cat.sprite.image = cat.cat_sit_south_animation
      elif cat.state == CatState.IDLE:
          if cat.direction == CatDirection.WEST:
              cat.sprite.image = cat.cat_idle_west_animation
          elif cat.direction == CatDirection.EAST:
              cat.sprite.image = cat.cat_idle_east_animation
          elif cat.direction == CatDirection.NORTH:
              cat.sprite.image = cat.cat_idle_north_animation
          elif cat.direction == CatDirection.SOUTH:
              cat.sprite.image = cat.cat_idle_south_animation
      elif cat.state == CatState.RUN:
          if cat.direction == CatDirection.WEST:
              cat.sprite.image = cat.cat_run_west_animation
          elif cat.direction == CatDirection.EAST:
              cat.sprite.image = cat.cat_run_east_animation
          elif cat.direction == CatDirection.NORTH:
              cat.sprite.image = cat.cat_run_north_animation
          elif cat.direction == CatDirection.SOUTH:
              cat.sprite.image = cat.cat_run_south_animation


  cat.last_state = cat.state
  cat.last_direction = cat.direction

  cat.sprite.draw()

pyglet.app.run()
