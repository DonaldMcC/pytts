# from https://stackoverflow.com/questions/18369188/python-add-id3-tags-to-mp3-file-that-has-%20no-tags

import mutagen.id3
import mutagen.mp3
import mutagen
from mutagen.easyid3 import EasyID3


def set_tags(filepath, artist='test artist', album='Test Album', title='Test Song'):
    print(filepath)
    M = mutagen.mp3.MP3(filepath)

    if M.tags is None:
        M.tags = mutagen.id3.ID3()  # also sets the filepath for the ID3 instance

    M.tags['TPE1'] = mutagen.id3.TPE1(encoding=1, text=[artist])
    M.tags['TALB'] = mutagen.id3.TALB(encoding=1, text=[album])
    M.tags['TIT2'] = mutagen.id3.TIT2(encoding=1, text=[title])

    M.save(v1=0, v2_version=4)

    #print(M)
    #type(M)
    #M['artist'] = artist
    #M['album'] = album
    #M['title'] = title
    #M.tags = mutagen.id3.ID3()  # also sets the filepath for the ID3 instance

    #M.tags['TIT2'] = mutagen.id3.TIT2(encoding=1, text=[title])
    #M.tags['TPE1'] = mutagen.id3.TPE1(encding=1, text=[artist])
    #M.tags['TALB'] = mutagen.id3.TALB(encding=1, text=[album])
    #M.save(filepath, v1=0, v2_version=3)  # save ID3v2.3 only without ID3v1 (default is ID3v2.4)
    return
