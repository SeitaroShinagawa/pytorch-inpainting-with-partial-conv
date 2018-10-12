import argparse
import numpy as np
import random
from PIL import Image
import cv2

action_list = [[0, 1], [0, -1], [1, 0], [-1, 0]]


def random_walk(canvas, ini_x, ini_y, length):
    x = ini_x
    y = ini_y
    img_size = canvas.shape[-1]
    x_list = []
    y_list = []
    for i in range(length):
        r = random.randint(0, len(action_list) - 1)
        x = np.clip(x + action_list[r][0], a_min=0, a_max=img_size - 1)
        y = np.clip(y + action_list[r][1], a_min=0, a_max=img_size - 1)
        x_list.append(x)
        y_list.append(y)
    canvas[np.array(x_list), np.array(y_list)] = 0
    return canvas

def generate_mask(imageHeight, imageWidth, maxVertex=100, maxLength=30, maxBrushWidth=10, maxAngle=2*np.pi):
    """
    imageHeight : input image height
    imageWidth  : input image width
    maxVertex   : the max number of vertex in a stroke
    maxLength   : the max length of each line
    maxBrushWidth: the max width of freeform lines
    maxAngle    : the max angle of freeform lines
    """

    mask = np.zeros((imageHeight,imageWidth)).astype("uint8")  #initialize mask canvas
    numVertex = np.random.randint(1,maxVertex+1)                #iteration for
    rand_flag = 0

    for i in range(numVertex):

        if rand_flag < 0.1: #initialize stroke
            startX = np.random.randint(imageWidth)
            startY = np.random.randint(imageHeight)
            brushWidth = np.random.randint(1,maxBrushWidth+1)

        angle = maxAngle * np.random.rand()
        if i % 2 == 0:
            angle = 2*np.pi - angle # reverse mode
        length = maxLength*np.random.rand()

        endX = startX + int(length*np.cos(angle))
        endY = startY + int(length*np.sin(angle))

        mask = Draw_line(mask,startX,startY,endX,endY,brushWidth)
        mask = Draw_circle(mask,endX,endY,int(brushWidth/2))

        startX = endX
        startY = endY
        rand_flag = np.random.rand()

    return 255 - mask #reverse black and white

def Draw_line(canvas, startX, startY, endX, endY, brushWidth, color=255):
    """
    color:
        mono: scalar, RGB: (red,green,blue)
    """
    canvas = cv2.line(canvas,(startX,startY),(endX,endY),color,thickness=brushWidth)
    return canvas

def Draw_circle(canvas, centerX, centerY, radius, color=255):
    """
    color:
        mono: scalar, RGB: (red,green,blue)
    """
    canvas = cv2.circle(canvas,(centerX,centerY),radius,color)
    return canvas


if __name__ == '__main__':
    import os

    parser = argparse.ArgumentParser()
    parser.add_argument('--image_size', type=int, default=128)
    parser.add_argument('--N', type=int, default=10000)
    parser.add_argument('--save_dir', type=str, default='masks')
    args = parser.parse_args()

    save_dir = args.save_dir+"/"+str(args.image_size)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for i in range(args.N):
        #canvas = np.ones((args.image_size, args.image_size)).astype("i")
        #ini_x = random.randint(0, args.image_size - 1)
        #ini_y = random.randint(0, args.image_size - 1)
        #mask = random_walk(canvas, ini_x, ini_y, args.image_size ** 2)
        mask = generate_mask(args.image_size, args.image_size)  
        print("save:", i, np.sum(mask))

        #img = Image.fromarray(mask * 255).convert('1')
        img = Image.fromarray(mask).convert('1')
        img.save('{:s}/{:06d}.bmp'.format(save_dir, i))




                        
                        
