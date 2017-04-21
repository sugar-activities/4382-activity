# g.py - globals
import pygame,utils,random

app='Rectangles'; ver='1.0'
ver='1.1'
# thinking smiley at start
# layout changed - buttons added
ver='1.2'
# g.ok=self.level should be g.level=self.level in main
ver='3.0'
# redraw implemented
ver='3.1'
# 2x2's -> 4's
# save.dat -> rects.dat
# Class Rect -> MyRect
ver='3.2'
# doubled the height of the slider marks
ver='4.0'
# new sugar cursor etc

def init(): # called by run()
    random.seed()
    global redraw
    global screen,w,h,font1,font2,font3,clock
    global factor,offset,imgf,message,version_display
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70,0,70))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    clock=pygame.time.Clock()
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    if pygame.font:
        t=int(180*imgf); font1=pygame.font.Font(None,t)
        t=int(90*imgf); font2=pygame.font.Font(None,t)
        t=int(45*imgf); font3=pygame.font.Font(None,t)
    message=''
    
    # this activity only
    global level,wait,magic,score,magic_show
    level=1
    wait=utils.load_image("wait.png",True)
    magic=utils.load_image("magic.png",True); magic_show=False
    score=0

def sx(f): # scale x function
    return int(f*factor+offset+.5)

def sy(f): # scale y function
    return int(f*factor+.5)



