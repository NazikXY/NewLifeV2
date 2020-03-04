from  Area import *
from Enums import *
from Entities import *
from Render import *

ma = Area(Area.gen_area(WIDTH, HEIGHT))
ma.populate(2)
ma.run_live()
ma.graph_render()
