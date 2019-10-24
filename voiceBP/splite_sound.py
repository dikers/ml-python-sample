from pydub import AudioSegment
import time
"""
pydub需要依赖 libav或者ffmpeg
安装pydub:  pip install pydub

"""


SOUND_INTERVAL = 1000 * 30


def splite_mp3(input_file, out_path):
    mp3 = AudioSegment.from_mp3(input_file)
    mp3_length = int(len(mp3) / SOUND_INTERVAL)
    print('输入文件: {} , 分成{}段  开始切割'.format(input_file, mp3_length))

    for index in range(mp3_length-1):
        out_file = '{}{}.mp3'.format(out_path, index)
        mp3[index * SOUND_INTERVAL: (index+1) * SOUND_INTERVAL].export(out_file, format="mp3")
        print(' {} {} success '.format(index, out_file))


start = time.time()
splite_mp3('/Users/mac/tmp/sound_set/sound_a.mp3', '/Users/mac/tmp/sound_set/out1/')
splite_mp3('/Users/mac/tmp/sound_set/sound_b.mp3', '/Users/mac/tmp/sound_set/out2/')
splite_mp3('/Users/mac/tmp/sound_set/sound_c.mp3', '/Users/mac/tmp/sound_set/out3/')
end = time.time()

print('切割完成 use time {}'.format((end - start)))


print('--------end-------')