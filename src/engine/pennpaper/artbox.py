import pen
import paper
from nibs import Nibs
import pyglet
from multiprocessing import Process, Pipe


class ArtBox(object):
    def __init__(self, width, height):
        self._pen_comms = Pipe()
        self._paper_comms = Pipe()
        self._pen_ear, self._pen_mouth = Pipe()
        self._paper_ear, self._paper_mouth = Pipe()
        self._pen = pen.Pen()
        self._paper = paper.Paper(width=width, height=height)
        self._proc = Process(target=self._pen, args=(self._pen_comms, self._paper_comms))
        self._proc.daemon = True

    def add_resource_folder(self, folder_name):
        pyglet.resource.path.append(folder_name)
        pyglet.resource.reindex()

    def precache(self, asset_dict):
        for key in asset_dict:
            attributes = asset_dict[key]
            if len(attributes) == 1:
                self._paper._handle_command(Nibs.Cache(key, attributes[0]))
            elif len(attributes) == 2:
                self._paper._handle_command(Nibs.Cache(key, attributes[0], attributes[1]))

    def open(self):
        self._proc.start()
        self._paper.unfurl(self._pen_comms, self._paper_comms)
        self._proc.join(1)
        if self._proc.exitcode is None:
            self._proc.terminate()
