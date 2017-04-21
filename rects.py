# rects.py
import g,pygame,random,utils

RC=((4,6),(5,7),(6,9),(7,10),(8,12),(9,13),(10,15),(11,16),(12,18),(13,19))
COLOURS=((255,0,0),(0,255,0),(50,50,255),(255,255,0),(0,255,255),(255,0,255))

class Sq:
    def __init__(self,r,c,x,y):
        self.r=r; self.c=c; self.x=x; self.y=y
        self.colour=6 # colour=0..5 6=none - final colour
        self.colour_player=6 # colour=0..5 6=none - current colour
        self.n=0 # rectangle #
        self.area=0
        self.checked=False # used bt correct() method

class MyRect:
    def __init__(self,r1,c1,r2,c2):
        self.r1=r1; self.c1=c1; self.r2=r2; self.c2=c2 

class Rects:
    def __init__(self):
        self.nr=0 # of rows
        self.nc=0 # of cols
        self.ss=0 # square side in pixels
        self.sqs=[]
        self.rects=[]
        self.nos=[] # list of sq's with the area displayed
        self.last_sq=None
        self.area=0 # area when encountered in count()

    def setup(self,level): # 1..10
        ind=level-1; self.nr,self.nc=RC[ind]; self.total=self.nr*self.nc
        ss=17.0/self.nr; self.ss=g.sy(ss); self.sss=self.ss+g.sy(.05)
        w=self.nc*ss; x0=27-w
        self.x0=g.sx(x0); self.y0=g.sy(1.2)
        self.sqs=[] # new set for each round cos nr,nc can change
        y=self.y0
        for r in range(1,self.nr+1):
            x=self.x0
            for c in range(1,self.nc+1):
                sq=Sq(r,c,x,y)
                self.sqs.append(sq)
                sq.colour=6 #none
                sq.colour_player=6 #none
                x+=self.ss
            y+=self.ss
        success=False
        while not success:
            success=self.fill_in()
            if success:
                self.do_nos()
                self.fours()
                success=self.colour_in()
        self.last_sq=None

    def reset(self):
        for sq in self.sqs: sq.colour_player=6
        
    def sq(self,r,c):
        ind=(r-1)*self.nc+c-1
        return self.sqs[ind]
                
    def draw(self):
        x=self.x0; y=self.y0; w=self.nc*self.ss; h=self.nr*self.ss
        pygame.draw.rect(g.screen,(150,0,0),(x,y,w,h))
        self.draw_sqs()
        self.draw_nos()
        self.draw_last()
        self.draw_grid()
        #for sq in self.sqs:###
            #utils.display_number(sq.n,(sq.x+10,sq.y+12),g.font3,(0,0,0)) ###

    def draw_grid(self):
        # horizontals
        s=self.ss
        ln=self.nc*s; x=self.x0; y=self.y0
        for i in range(self.nr+1):
            pygame.draw.line(g.screen,(196,196,196),(x,y),(x+ln,y))
            pygame.draw.line(g.screen,(196,196,196),(x,y+1),(x+ln,y+1)); y+=s
        # verticals
        ln=self.nr*s; x=self.x0; y=self.y0
        for i in range(self.nc+1):
            pygame.draw.line(g.screen,(196,196,196),(x,y),(x,y+ln))
            pygame.draw.line(g.screen,(196,196,196),(x+1,y),(x+1,y+ln)); x+=s

    def draw_sqs(self):
        s=self.sss
        for sq in self.sqs:
            if sq.colour_player<6:
                x=sq.x; y=sq.y
                colour=COLOURS[sq.colour_player]
                pygame.draw.rect(g.screen,colour,(x,y,s,s))
        
    def draw_last(self):
        sq=self.last_sq; s=self.sss; w=g.sy(.3)
        if sq<>None:
            x=sq.x; y=sq.y
            pygame.draw.rect(g.screen,utils.WHITE,(x,y,s,s),w)

    def draw_nos(self):
        s=self.sss; s2=self.ss/2
        font=g.font1
        if g.level>1: font=g.font2
        if g.level>4: font=g.font3
        for sq in self.nos:
            x=sq.x; y=sq.y
            colour=COLOURS[sq.colour]
            pygame.draw.rect(g.screen,colour,(x,y,s,s))
            cx=x+s2; cy=y+s2
            utils.display_number(sq.area,(cx,cy),font,(0,0,0))

    def fill_in(self):
        count=0; rect_n=0
        for sq in self.sqs: sq.n=0
        self.rects=[]
        for ii in range(100):
            if count==self.total: return True
            if (self.total-count)==1: return False
            if self.single(): return False
            # find empty square:
            r=random.randint(1,self.nr); c=random.randint(1,self.nc)
            for i in range(self.total):
                if self.sq(r,c).n==0: break
                c+=1
                if c>self.nc:
                    r+=1; c=1
                    if r>self.nr:r=1
            found=False
            # set w,h limits
            while not found:
                found=True
                w=random.randint(1,self.nc); h=random.randint(1,self.nr)
                if (w==1 and h==1): found=False
                if w*h>(self.total-count+1): found=False
                if w*h>self.total/4: found=False
            # do rect from (r,c) to a max of (w,h)
            rect_n+=1; k=0 # k counts squares filled in
            r0=r; c0=c; col_count=0
            while col_count<w and c<=self.nc:
                if self.sq(r,c).n>0: break
                k+=1; self.sq(r,c).n=rect_n; col_count+=1; c+=1
            # have filled in a horizontal from (r0,c0) to (r0,c-1)
            row_count=1; c2=c-1
            # try more rows
            while row_count<h and r<self.nr:
                ok=True; c=c0; r+=1
                for i in range(col_count):
                    if self.sq(r,c).n>0: ok=False; break
                    c+=1
                if ok:
                    c=c0
                    for i in range(col_count):
                        self.sq(r,c).n=rect_n; c+=1
                    row_count+=1; k+=col_count
                else:
                    break
            # if only 1 square, restore it
            if k==1:
                rect_n-=1; self.sq(r0,c0).n=0
            else:
                count+=k
                r2=r0+row_count-1; rect=MyRect(r0,c0,r2,c2)
                self.rects.append(rect)
        return False

    def single(self):
        for r in range(1,self.nr):
            for c in range(1,self.nc):
                if self.sq(r,c).n==0:
                    if self.neighbours(r,c)==4: return True
        return False

    def sq2area(self,sq0):
        n=sq0.n
        for sq in self.sqs:
            if sq.n==n:
                if sq.area>0: return sq.area
        return 0 # shouldn't happen

    def four(self,r,c):
        found=[]
        for dr in range(2):
            for dc in range(2):
                sq=self.sq(r+dr,c+dc)
                if self.sq2area(sq)>2: return False
                n=sq.n
                if n not in found:
                    found.append(n)
                    if len(found)>2: return False
        rnd=random.randint(1,4); k=1
        for dr in range(2):
            for dc in range(2):
                sq=self.sq(r+dr,c+dc)
                if sq in self.nos: self.nos.remove(sq)
                sq.n=n; sq.area=0
                if k==rnd: sq.area=4; self.nos.append(sq)
                k+=1
        #print r,c ###
        return True

    def fours(self):
        for r in range(1,self.nr):
            for c in range(1,self.nc):
                if self.four(r,c):
                    rect=MyRect(r,c,r,c+1)
                    if rect in self.rects: self.rects.remove(rect)
                    rect=MyRect(r+1,c,r+1,c+1)
                    if rect in self.rects: self.rects.remove(rect)
                    rect=MyRect(r,c,r+1,c)
                    if rect in self.rects: self.rects.remove(rect)
                    rect=MyRect(r,c+1,r+1,c+1)
                    if rect in self.rects: self.rects.remove(rect)
                    rect=MyRect(r,c,r+1,c+1); self.rects.append(rect)
        #print '========='###
        
    def neighbours(self,r,c): # treats border as neighbour
        k=0
        if r==1: k+=1
        elif self.sq(r-1,c).n>0: k+=1
        if r==self.nr: k+=1
        elif self.sq(r+1,c).n>0: k+=1
        if c==1: k+=1
        elif self.sq(r,c-1).n>0: k+=1
        if c==self.nc: k+=1
        elif self.sq(r,c+1).n>0: k+=1
        return k

    def colour_in(self):
        for rect in self.rects:
            colour=self.free_colour(rect)
            if colour==None: return False
            for r in range(rect.r1,rect.r2+1):
                for c in range(rect.c1,rect.c2+1):
                    self.sq(r,c).colour=colour
        return True

    def free_colour(self,rect): # find a random colour not used by any of rect's neighbours
        used_colours=[]
        r1=rect.r1; c1=rect.c1; r2=rect.r2; c2=rect.c2
        if r1>1:
            r=r1-1
            for c in range(c1,c2+1):
                colour=self.sq(r,c).colour
                if colour<6 and colour not in used_colours:
                    used_colours.append(colour)
        if r2<self.nr:
            r=r2+1
            for c in range(c1,c2+1):
                colour=self.sq(r,c).colour
                if colour<6 and colour not in used_colours:
                    used_colours.append(colour)
        if c1>1:
            c=c1-1
            for r in range(r1,r2+1):
                colour=self.sq(r,c).colour
                if colour<6 and colour not in used_colours:
                    used_colours.append(colour)
        if c2<self.nc:
            c=c2+1
            for r in range(r1,r2+1):
                colour=self.sq(r,c).colour
                if colour<6 and colour not in used_colours:
                    used_colours.append(colour)
        free_colours=[]
        for colour in range(6):
            if colour not in used_colours: free_colours.append(colour)
        if len(free_colours)==0: return None
        ind=random.randint(0,len(free_colours)-1)
        return free_colours[ind]
        
    def do_nos(self):
        self.nos=[]
        for rect in self.rects:
            r1=rect.r1; c1=rect.c1; r2=rect.r2; c2=rect.c2
            area=(r2-r1+1)*(c2-c1+1)
            r=random.randint(r1,r2); c=random.randint(c1,c2)
            sq=self.sq(r,c); sq.area=area; self.nos.append(sq)
            
    def play(self,sq1,sq2):
        # check rectangle with corners sq1,sq2 for area squares:
        r1=sq1.r; c1=sq1.c; r2=sq2.r; c2=sq2.c
        if r1>r2: t=r1; r1=r2; r2=t
        if c1>c2: t=c1; c1=c2; c2=t
        sqs=[]
        for r in range(r1,r2+1):
            for c in range(c1,c2+1):
                sq=self.sq(r,c)
                if sq in self.nos: sqs.append(sq)
        if len(sqs)==0:
            colour=6
        elif len(sqs)==1:
            colour=sqs[0].colour
        else:
            return False # no colouring cos more than one area square
        # ok to colour in or blank
        for r in range(r1,r2+1):
            for c in range(c1,c2+1):
                self.sq(r,c).colour_player=colour
        return True

    def which(self):
        s=self.ss
        for sq in self.sqs:
            x=sq.x; y=sq.y
            if utils.mouse_in(x,y,x+s,y+s):
                return sq
        return None
        
    def click(self):
        sq=self.which()
        if sq==None: return False
        if self.last_sq==None:
            self.last_sq=sq
        else:
            if self.last_sq==sq:
                self.last_sq=None
            else:
                if self.play(self.last_sq,sq):
                    self.last_sq=None
                else:
                    self.last_sq=sq
        return True

    def correct(self):
        for sq in self.sqs: sq.checked=False
        for sq in self.sqs:
            colour=sq.colour_player
            if colour==6: return False
            if not sq.checked:
                self.area=0
                count=self.count(sq.r,sq.c,colour)
                #print sq.n,count,self.area###
                if count<>self.area: return False
        return True

    def count(self,r,c,colour):
        sq=self.sq(r,c)
        if sq.checked: return 0
        if sq.colour_player<>colour: return 0
        sq.checked=True
        if sq in self.nos:
            if self.area>0:
                self.area=1000 # already encountered an area square - give a silly value
            else:
                self.area=sq.area # remember area
        n=1
        if r>1: n+=self.count(r-1,c,colour)
        if r<self.nr: n+=self.count(r+1,c,colour)
        if c>1: n+=self.count(r,c-1,colour)
        if c<self.nc: n+=self.count(r,c+1,colour)
        return n

        
        
                
                
            



