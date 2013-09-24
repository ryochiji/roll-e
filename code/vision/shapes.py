from SimpleCV import Image, Color, DrawingLayer
import time

global M
M = [ 0 for i in range(0,512) ]
# Horizontal line
M[7] = 1 
M[56] = 1 
M[64+128+256] = 1 

# Vertical line
M[1+8+64] = 2 
M[2+16+128] = 2 
M[292] = 2 

# Top left to bottom right
M[1+16+256] = 3 
M[2+32] = 3 
M[8+128] = 3 

# Top right to bottom left
M[4+16+64] = 4 
M[2+8] = 4 
M[32+128] = 4 

def get_bitmap(img, x_offset, y_offset):
    out = 0
    for y in range(0,3):
        for x in range(0,3):
            p = img.getPixel(x+x_offset, y+y_offset)
            if not p: continue
            if not p[0]>250.0: continue
            out |=  1 << ( (y*3) + x )
    return out

def draw_bitmap(dl, bm, x, y):
    pattern = M[bm]
    if pattern==1:
        dl.line((x, y+1), (x+2, y+1), color=Color.RED, antialias=False)
    elif pattern==2:
        dl.line((x+1, y), (x+1, y+2), color=Color.RED, antialias=False)
    elif pattern==3:
        dl.line((x,y), (x+2, y+2), color=Color.RED, antialias=False)
    elif pattern==4:
        dl.line((x+2,y), (x, y+2), color=Color.RED, antialias=False)

img = Image('/home/pi/outline.png')
dl = DrawingLayer((img.width,img.height))
img.addDrawingLayer(dl)

print "Starting %s" % (time.time())
for y in range(0, img.height-3, 3):
    for x in range(0, img.width-3, 3):
        bm = get_bitmap(img, x, y)
        draw_bitmap(dl, bm, x, y)
print "Finished %s" % (time.time())
img.save('outline2.png')
