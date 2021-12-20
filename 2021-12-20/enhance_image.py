#!/home/andrew/.envs/venv38/bin/python3

import sys
import numpy as np

BIT_MAPPER = {0:".", 1:"#", ".":0, "#":1}

def get_input():
    alg_string = None   # "image enhancement algorithm string"
    img_lines = []
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        if alg_string is None:
            alg_string = line
            assert len(alg_string) == 512
        else:
            img_lines.append(line)
    return alg_string, img_lines


def int_to_3x3(i):
    i_bitstring = format(i, "#011b")[2:]
    i_bits = [int(c) for c in i_bitstring]
    i_3x3 = np.array(i_bits, dtype=bool).reshape((3,3))
    return i_3x3


def m3x3_to_int(m):
    m = m.astype(int)
    m_bitstring = "".join(str(b) for b in m.reshape(9))
    m_int = int(m_bitstring, 2)
    return m_int


def convert_img_lines_to_np(img_lines):
    """Convert into more usable forms (numpy array)"""
    img_bits = []
    for img_line in img_lines:
        img_bits.append([BIT_MAPPER[c] for c in img_line])
    img = np.array(img_bits, dtype=bool)
    return img


def convert_alg_to_dict(alg_string):
    """Convert into dictionary for easy lookup of 3x3 grid"""
    alg = {}
    for i in range(len(alg_string)):
        i_bitstring = format(i, "#011b")[2:]
        i_bits = [int(c) for c in i_bitstring]
        i_3x3 = np.array(i_bits, dtype=bool).reshape((3,3))
        # print(i_3x3.astype(int), alg_string[i])
        alg[i_3x3.tobytes()] = BIT_MAPPER[alg_string[i]]
    return alg


def enhance(img, alg, pad=0):
    # Pad the image with border of width 2
    rows, cols = img.shape
    border = 2
    if pad == 0:
        img_pad = np.zeros((rows+(border*2), cols+(border*2)), dtype=bool)
    elif pad == 1:
        img_pad = np.ones((rows+(border*2), cols+(border*2)), dtype=bool)
    else:
        assert False
    img_pad[border:(rows+border),border:(cols+border)] = img
    # Create new (enhanced) image
    img_new = np.zeros((img_pad.shape[0]-2, img_pad.shape[1]-2), dtype=bool)
    for i in range(img_new.shape[0]):
        for j in range(img_new.shape[1]):
            patch_3x3 = img_pad[i:(i+3),j:(j+3)]
            img_new[i,j] = alg[patch_3x3.tobytes()]
    return img_new

def print_img(img):
    for row in img.astype(int):
        row_str = "".join([BIT_MAPPER[i] for i in row])
        print(row_str)


def next_pad(pad, alg):
    m = np.zeros((3,3), dtype=bool)
    m[:,:] = pad
    return alg[m.tobytes()]


##########################################################################

alg_string, img_lines = get_input()
print("Alg string:", alg_string)
#print("Image lines:")
#print(img_lines)
img = convert_img_lines_to_np(img_lines)
alg = convert_alg_to_dict(alg_string)
print("Image bit matrix:")
print(img.astype(int))
print("Image shape:", img.shape)

img_new = img
iterations = 2
pad = 0
for i in range(iterations):
    img_new = enhance(img_new, alg, pad=pad)
    pad = next_pad(pad, alg)
    print("Image after %d enhancements has %d pixels lit:" % (i+1, np.sum(img_new)))
    print_img(img_new)
    print("Number of pixels lit after %d enhancements: %d" % (i+1, np.sum(img_new)))
