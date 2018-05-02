from eventloop.base import EventLoop, DataLoader
from eventloop.routines import Logger

loop = EventLoop()
loop.add_tod_list("data/s17_pa4_sublist.txt")

loop.add_routine(DataLoader(input_dir="outputs/s17_pa4_sublist/", output_key="cut"))
loop.add_routine(Logger(input_key="cut"))

loop.run(0, 2)
