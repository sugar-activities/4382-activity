#!/usr/bin/python
# Rectangles.py
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,utils,pygame,gtk,sys,rects,buttons,slider

class Rectangles:
    
    def __init__(self):
        self.level=1
        self.journal=True # set to False if we come in via main()

    def display(self,wait=False):
        g.screen.fill((0,0,100))
        if wait:
            utils.centre_blit(g.screen,g.wait,(g.sx(16),g.sy(10)))
        else:
            self.rects.draw()
        buttons.draw()
        self.slider.draw()
        if g.magic_show:
            utils.centre_blit(g.screen,g.magic,(g.sx(27.8),g.sy(3.2)))
        if g.score>0:
            x=g.sx(29.5); y=g.sy(8)
            utils.display_number(g.score,(x,y),g.font2,utils.CREAM)
       
    def button(self,bu):
        if bu=='cyan': self.new1()
        if bu=='black': g.magic_show=False; self.rects.reset()

    def new1(self):
        g.magic_show=False
        self.display(True)
        pygame.display.flip()
        self.rects.setup(g.level)
        buttons.on("black")

    def run(self):
        g.init()
        self.rects=rects.Rects()
        if not self.journal:
            utils.load()
        else:
            g.level=self.level
        self.slider=slider.Slider(g.sx(16),g.sy(20.5),10,utils.GREEN)
        self.new1()
        bx=g.sx(29.5); by=g.sy(12)
        buttons.Button("cyan",(bx,by),True)
        by=g.sy(16)
        buttons.Button("black",(bx,by),True)
        if self.journal: # Sugar only
            a,b,c,d=pygame.cursors.load_xbm('my_cursor.xbm','my_cursor_mask.xbm')
            pygame.mouse.set_cursor(a,b,c,d)
        going=True
        while going:
            # Pump GTK messages.
            while gtk.events_pending():
                gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.redraw=True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==2: # centre button
                        if not self.journal:
                            g.version_display=not g.version_display; break
                    bu=buttons.check()
                    if bu<>'': self.button(bu); break
                    if self.slider.mouse(): self.new1(); break
                    if self.rects.click():
                        if not g.magic_show:
                            if self.rects.correct():
                                g.score+=g.level; g.magic_show=True
                                buttons.off("black")
            if not going: break
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                pygame.display.flip()
                g.redraw=False
            tf=False
            if pygame.mouse.get_focused(): tf=True
            pygame.mouse.set_visible(tf)
            g.clock.tick(40)
            # be ready for xo quit at any time
            self.level=g.level

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((800, 600))
    game=Rectangles()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
