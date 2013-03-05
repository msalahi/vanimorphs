from images2gif import writeGif
import numpy
from math import floor, ceil
from PIL import Image

def next_move(current, last, im):

    h,w = im.shape
    y,x = current
    neighbors = []

    order = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
    for i,j in order:
        if 0 <= y + i < h and 0 <= x + j < w and im[y+i,x+j]==0:
            neighbors.append((y+i, x+j))

    index = (neighbors.index(last) + 1) % len(neighbors) if last else 0
    return neighbors[index]

def outline(im):

    mid_x = im.shape[1]/2
    mid_y = im.shape[0]/2

    #Outlines foreground
    im[im<255] = 0 

    #rows, cols contain the 'y' and 'x' locations of black pixels respectively
    rows,cols = numpy.where(im==0)
   
    #Start drawing outline at first black pixel
    start_x, start_y = cols[0], rows[0]
    y,x = next_move((start_y, start_x), None, im)

    outline = [(start_y, start_x),(y,x)]

    while outline[0] != outline[-1]:
        outline.append( next_move(outline[-1], outline[-2], im))

    normalized = []
    for y,x in outline:
        normalized.append((y - mid_y, x - mid_x))
    return normalized

def draw_outline(outline, shape):
    
    
    im = numpy.ones(shape, dtype=numpy.uint8)
    im[im >= 0] = 255
    for y,x in outline:
        im[y+shape[0]/2, x+shape[1]/2] = 0
    return im

def interpolate_outline(shape, num_samples):

    resized_shape = []
    for t in range(num_samples):
        target = (len(shape) - 1) * t * 1.0/ num_samples
        a = int(floor(target))
        b = int(ceil(target))

        if a==b:
            resized_shape.append(shape[int(a)])
        else:
            y_a, x_a = shape[int(a)]
            y_b, x_b = shape[int(b)]

            x = abs(b-target) * x_b + abs(a-target) * x_a
            y = abs(b-target) * y_b + abs(a-target) * y_a

            x = int(round(x))
            y = int(round(y))
            resized_shape.append((y,x))

    return resized_shape
        
def transition(file_name):

    num_steps = 100
    van = Image.open('static/van.png').convert("L")
    morpher = Image.open(file_name).convert("L")

    ratio = morpher.size[1]*1.0/van.size[1]
    size = (int(van.size[0] * ratio) , int(van.size[1] * ratio))
    van.thumbnail(size)

    van = numpy.array(van)
    morpher = numpy.array(morpher)

    h = max(van.shape[0],morpher.shape[0])
    w = max(van.shape[1],morpher.shape[1])

    size = (h,w)

    van_shape = outline(van)
    morpher_shape = outline(morpher)

    num_samples = max(len(van_shape), len(morpher_shape))
    van_shape = interpolate_outline(van_shape, num_samples)
    morpher_shape = interpolate_outline(morpher_shape, num_samples)

    seq = []
    for t in range(num_steps):

        target = t * 1.0/ num_steps
        shape = []

        for i in range(num_samples):
            y_a, x_a = morpher_shape[i]
            y_b, x_b = van_shape[i]

            x = (1-target) * x_a + target * x_b
            y = (1-target) * y_a + target * y_b

            x = int(round(x))
            y = int(round(y))
            shape.append((y,x))

        seq.append(Image.fromarray(draw_outline(shape, size)))

    writeGif('lololol.gif', seq, duration=.1, dither=0)

transition('static/murad.png')
