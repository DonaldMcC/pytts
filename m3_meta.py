# from https://stackoverflow.com/questions/18369188/python-add-id3-tags-to-mp3-file-that-has-%20no-tags
# seems method at bottom of above works - package has been updated since original - windows doesnt show
# anything but it works on doppler which is where I want it so sort of OK

import mutagen.id3
import mutagen.mp3
import mutagen
from mutagen.mp4 import MP4


def set_tags(filetype, filepath, artist='test artist', album='Test Album', title='Test Song'):
    if filetype == 'mp3':
        set_tags_mp3(filepath, artist=artist, album=album, title=title)
    elif filetype == 'mp4' or filetype == 'm4a':
        set_tags_mp4(filepath, artist=artist, album=album, title=title)
    else:
        print(f"I can't set tags for this filetype: {filetype}")


def set_tags_mp3(filepath, artist, album, title):
    print(filepath)
    m = mutagen.mp3.MP3(filepath)

    if m.tags is None:
        m.tags = mutagen.id3.ID3()  # also sets the filepath for the ID3 instance
    m.tags['TPE1'] = mutagen.id3.TPE1(encoding=1, text=[artist])
    m.tags['TALB'] = mutagen.id3.TALB(encoding=1, text=[album])
    m.tags['TIT2'] = mutagen.id3.TIT2(encoding=1, text=[title])
    m.save(v1=0, v2_version=4)
    return


def set_tags_mp4(filepath, artist, album, title):
    m = mutagen.mp4.MP4(filepath)
    m['©nam'] = title
    m['©ART'] = artist
    m['©alb'] = album
    m.pprint()
    m.save()
    return
