from .object import Object, Point

class Player(Object):

    def __init__(self, bottom_left_corner: Point, height: float, width: float):

        self.a: float = 0.7 
        self.v_x: float = 0
        self.mu: float = 0.2
        self.direction: int = 0
        self.is_jumping = False
        self.start_jump = False
        self.v_y = 0
        self.v_y_init = 10
        self.g = 1
        self.y_min = bottom_left_corner.y + height/2

        super().__init__(bottom_left_corner, height, width)

    def jump(self):
        self.start_jump = not self.start_jump and not self.is_jumping and (self.y - self.height/2) == self.y_min
            

    def move(self, time: float):
        time *= 60 # default is 60fps, so constants for a and mu are based on that. this fixes for other framerates
        if self.start_jump:
            self.start_jump = False
            self.is_jumping = True
            self.v_y = self.v_y_init
            self.y += self.v_y * time

        self.x += self.v_x * time
        self.v_x += (self.a*self.direction - self.mu*self.v_x)*(1-self.is_jumping) * time

        if self.y > self.y_min + self.height / 2:
            self.y += self.v_y * time
            self.v_y -= self.g * time

        if self.y <= self.y_min + self.height / 2:
            self.is_jumping = False
            self.v_y = 0
            self.y = self.y_min + self.height / 2

        self.update_hitbox()
    
    def set_ground(self, y: float):
        self.y_min = y
    
    
    def __str__(self):
        return f"Speed: \n\tx:{self.v_x : .3f} \n\ty:{self.v_y : .3f}\nPosition: \n\t{Point(self.x, self.y)}"
    

    def tl(self):
        return self.hitbox.tl()
    def br(self):
        return self.hitbox.br()