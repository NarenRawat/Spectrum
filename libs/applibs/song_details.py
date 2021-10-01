from os.path import basename
from io import BytesIO

from kivy.core.image import Image as CoreImage
from mutagen import File


def details(filething):
    detail = File(filething)
    detail_easy = File(filething, easy=True)

    artist = 'Unknown Artist'
    album = 'Unknown Album'
    title = None
    image_texture = None
    length = detail.info.length

    if 'title' in detail_easy:
        title = detail_easy.get('title')[0]
    else:
        title = basename(filething)[:-4]
    if 'artist' in detail_easy:
        artist = detail_easy.get('artist')[0]
    if 'album' in detail:
        album = detail_easy.get('album')[0]

    if 'APIC:' in detail:
        data = detail.get('APIC:').data
        image_texture = CoreImage(BytesIO(data), ext='png').texture

    return title, artist, album, image_texture, length
