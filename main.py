from Area import Area
from prop import HEIGHT, WIDTH


main_area = Area(Area.gen_area(HEIGHT, WIDTH))
mn = main_area

main_area.populate(count=5)

main_area.text_render()
main_area.run_live()
main_area.graph_render()




