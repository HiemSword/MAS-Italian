

init python:

    def grant_xp(experience):
        
        old_level = get_level()
        
        
        if experience<0:
            experience=0
        
        
        persistent.playerxp += experience
        
        
        new_level = get_level()
        
        
        for i in range(old_level,new_level):
            
            queueEvent('unlock_prompt') 
        
        return


    def get_level():
        import math
        
        if persistent.playerxp<0:
            persistent.playerxp=0
        xp = persistent.playerxp
        
        if xp <= 390:
            approx_level = (-1.0+math.sqrt(1+(8.0/5.0)*xp))/2.0
            level = math.floor(approx_level)
        else:
            level = 12 + math.floor((xp-390.0)/60.0)
        
        return int(level)

