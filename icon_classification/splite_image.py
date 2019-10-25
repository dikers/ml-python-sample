from PIL import Image
import os


"""
ffmpeg -ss 00:00 -i sc.ts -f image2  -s 1024x768 -r 0.2 -t 10:20 %3d.jpg

"""

def get_file_list(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                input_file_name = os.path.join(root, file)
                L.append(input_file_name)
    return L



def splite_vedio(file_dir):
    """

    :param file_dir:
    :return:
    """
    L = get_file_list(file_dir)
    out_dir = file_dir + 'cut/'
    for input_file_name in L:
        out_file_name = '{}{}.JPG'.format(out_dir, input_file_name.split('/')[-1].split('.')[0], )
        img = Image.open(input_file_name)
        print(input_file_name)
        print('out file: ', out_file_name)
        cropped = img.crop((60, 40, 200, 180))  # (left, upper, right, lower)
        cropped.save(out_file_name)
        print('{} done------'.format(file_dir))


def splite_image():
    """

    :return:
    """
    img = Image.open("/Users/mac/tmp/test_split_image/demo/002.jpg")
    cropped = img.crop((60, 40, 200, 180))  # (left, upper, right, lower)
    cropped.save("/Users/mac/tmp/test_split_image/demo/cut/002.JPG")


# splite_vedio('/Users/mac/tmp/test_split_image/demo7/')
# splite_vedio('/Users/mac/tmp/test_split_image/demo4/')
splite_vedio('/Users/mac/tmp/test_split_image/demo5/')
# splite_vedio('/Users/mac/tmp/test_split_image/demo6/')
splite_vedio('/Users/mac/tmp/test_split_image/demo7/')

