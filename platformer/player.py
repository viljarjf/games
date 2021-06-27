from .object import Object, Point

class Player(Object):

    def __init__(self, bottom_left_corner: Point, height: float, width: float):

        self.v_max: float = 10 # pixels per second
        self.a: float = 0.7
        self.v: float = 0
        self.mu: float = 0.3
        self.direction: int = 0
        self.is_jumping = False
        self.start_jump = False
        self.v_jump = 0
        self.v_jump_init = 10
        self.g = 1
        self.y_min = bottom_left_corner.y + height/2

        super().__init__(bottom_left_corner, height, width)

    def jump(self):
        self.start_jump = not self.start_jump and not self.is_jumping
            

    def move(self):
        if self.start_jump:
            self.start_jump = False
            self.is_jumping = True
            self.v_jump += self.v_jump_init
            self.y += self.v_jump

        self.x += self.v
        self.v += (self.a*self.direction - self.mu*self.v)*(1-self.is_jumping)
        self.v = min(self.v, self.v_max)

        if self.y > self.y_min + self.height / 2:
            self.y += self.v_jump
            self.v_jump -= self.g

        if self.y <= self.y_min + self.height / 2:
            self.is_jumping = False
            self.v_jump = 0
            self.y = self.y_min + self.height / 2

        self.update_hitbox()
    
    def set_ground(self, y: float):
        self.y_min = y
    
    
    def __str__(self):
        return f"Speed: {self.v}\nPosition: {Point(self.x, self.y)}"
    
    def tl(self):
        return self.hitbox.tl()
    def br(self):
        return self.hitbox.br()