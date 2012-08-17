import cProfile
from pennpaper import artbox

if __name__ == '__main__':
    box = artbox.ArtBox()
    box.add_resource_folder('../res')
    box.open()
    # cProfile.run('box.open()')
