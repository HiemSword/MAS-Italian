




init -10 python:

    def getCharacterImage(char, expression="1a"):
        
        
        
        
        
        
        
        
        
        
        
        
        return renpy.display.image.images.get((char, expression), None)



transform leftin_slow(x=640, z=0.80):
    xcenter -300 yoffset 0 yanchor 1.0 ypos 1.03 zoom z*1.00 alpha 1.00 subpixel True
    easein 1.00 xcenter x



transform ls32:
    leftin_slow(640)


transform mas_chdropin(x=640, y=405, travel_time=3.00):
    ypos -300 xcenter x
    easein travel_time ypos y

transform mas_chflip(dir):


    xzoom dir

transform mas_chflip_s(dir, travel_time=0.36):
    ease travel_time xzoom dir

transform mas_chhopflip(dir, ydist=-15, travel_time=0.36):


    easein_quad travel_time/2.0 yoffset ydist xzoom 0
    easeout_quad travel_time/2.0 yoffset 0 xzoom dir

transform mas_chmove(x, y, travel_time=1.0):


    ease travel_time xpos x ypos y



transform mas_chriseup(x=300, y=405, travel_time=1.00):
    ypos 800 xcenter x
    easein travel_time ypos y
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
