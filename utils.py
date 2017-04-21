# utils.py
import g,pygame,os,random,copy

#constants
RED,BLUE,GREEN,BLACK,WHITE=(255,0,0),(0,0,255),(0,255,0),(0,0,0),(255,255,255)
CYAN,ORANGE,CREAM=(0,255,255),(255,165,0),(255,255,192)

def save():
    dir=''
    dir=os.environ.get('SUGAR_ACTIVITY_ROOT')
    if dir==None: dir=''
    fname=os.path.join(dir,'data','rects.dat')
    f=open(fname, 'w')
    f.write(str(g.level)+'\n')
    f.close
    
def load():
    dir=''
    dir=os.environ.get('SUGAR_ACTIVITY_ROOT')
    if dir==None: dir=''
    fname=os.path.join(dir,'data','rects.dat')
    try:
        f=open(fname, 'r')
    except:
        return None #****
    try:
        g.level=int(f.readline())
    except:
        pass
    f.close

def version_display():
    g.message=g.app+' V '+g.ver
    g.message+='  '+str(g.screen.get_width())+' x '+str(g.screen.get_height())+' '+str(g.h)
    message(g.screen,g.font3,g.message)
    
# loads an image (eg pic.png) from the data subdirectory
# converts it for optimum display
# resizes it using the image scaling factor, g.imgf
#   so it is the right size for the current screen resolution
#   all images are designed for 1200x900
def load_image(file1,alpha=False,subdir=''): # eg subdir='glow'
    data='data'
    if subdir!='': data=os.path.join('data',subdir)
    fname=os.path.join(data,file1)
    try:
        img=pygame.image.load(fname)
    except:
        print "Peter says: Can't find "+fname; exit()
    if alpha:
        img=img.convert_alpha()
    else:
        img=img.convert()
    if abs(g.imgf-1.0)>.1: # only scale if factor <> 1
        w=img.get_width(); h=img.get_height()
        try: # allow for less than 24 bit images
            img=pygame.transform.smoothscale(img,(int(g.imgf*w),int(g.imgf*h)))
        except:
            img=pygame.transform.scale(img,(int(g.imgf*w),int(g.imgf*h)))
    return img
        
# eg new_list=copy_list(old_list)
def copy_list(l):
    new_list=[];new_list.extend(l)
    return new_list

def shuffle(lst):        
    l1=lst; lt=[]
    for i in range(len(lst)):
        ln=len(l1); r=random.randint(0,ln-1);
        lt.append(lst[r]); l1.remove(lst[r])
    return lt

def centre_blit(screen,img,(cx,cy),angle=0): # rotation is clockwise
    img1=img
    if angle!=0: img1=pygame.transform.rotate(img,-angle)
    rect=img1.get_rect()
    screen.blit(img1,(cx-rect.width/2,cy-rect.height/2))
    
# m is the message
# d is the # of pixels in the border around the text
# (cx,cy) = co-ords centre - (0,0) means use screen centre
def message(screen,font,m,(cx,cy)=(0,0),d=20):
    if m!='':
        if pygame.font:
            text=font.render(m,True,(255,255,255))
            shadow=font.render(m,True,(0,0,0))
            rect=text.get_rect();
            if cx==0: cx=screen.get_width()/2
            if cy==0: cy=screen.get_height()/2
            rect.centerx=cx;rect.centery=cy
            bgd=pygame.Surface((rect.width+2*d,rect.height+2*d))
            bgd.fill((0,255,255))
            bgd.set_alpha(128)
            screen.blit(bgd,(rect.left-d,rect.top-d))
            screen.blit(shadow,(rect.x+2,rect.y+2,rect.width,rect.height))
            screen.blit(text,rect)

# eg click_img=ImgClickClass(img,(x,y)) (x,y)=top left
#   if click_img.mouse_on():
#   click_img.draw(gscreen)
class ImgClickClass: # for clickable images
    def __init__(self,img,(x1,y1),centre=False):
        w=img.get_width();h=img.get_height();x=x1;y=y1
        if centre: x=x-w/2; y=y-h/2; self.cx=x1; self.cy=y1
        self.rect=pygame.Rect(x,y,w,h)
        self.x=x; self.y=y; self.img=img

    def mouse_on(self):
        mx,my=pygame.mouse.get_pos()
        return self.rect.collidepoint(mx,my)

    def draw(self,screen):
        screen.blit(self.img,(self.x,self.y))
        
    
def mouse_in(x1,y1,x2,y2):
    mx,my=pygame.mouse.get_pos()
    if x1>mx: return False
    if x2<mx: return False
    if y1>my: return False
    if y2<my: return False
    return True

def display_number(n,(cx,cy),font,colour=CREAM,bgd=None):
    if pygame.font:
        if bgd==None:
            text=font.render(str(n),True,colour)
        else:
            text=font.render(str(n),True,colour,bgd)
        centre_blit(g.screen,text,(cx,cy))

def text_blit1(screen,s,font,(x,y),(r,g,b)):
    text=font.render(s,True,(r,g,b))
    rect=text.get_rect(); rect.x=x; rect.y=y
    screen.blit(text,rect)


    
              


       
        
        
