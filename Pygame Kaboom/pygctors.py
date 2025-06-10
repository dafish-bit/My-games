from math import radians, sin, cos, atan2, degrees, sqrt
import pygame
width, height = 1, 1
screen = pygame.display.set_mode((width, height))
class Actor:
    def __init__(self, pos, image="images/player.png"):
        self.pos = pos
        self.original_image = pygame.image.load(image)
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=self.pos)
        self.maybe = False
        self.angle = 0
        self.center = self.rect.center

    def draw(self, srf=screen):
        srf.blit(self.image, self.pos)
    @property
    def angle(self, angle):
        return self._angle
    @angle.setter
    def angle(self, new_angle):
        self._angle = new_angle
        self.image = pygame.transform.rotate(self.original_image, self._angle)
        if self.maybe:
            self.rect = self.image.get_rect(topleft=self.pos) 
        else:
            self.rect.topleft = self.pos
        self.center = self.rect.center
    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, new_image):
        if isinstance(new_image, str):
            self._image = pygame.image.load(new_image)
        else:
            self._image = new_image
        self.rect = self._image.get_rect(topleft=self.pos)
        self.center = self.rect.center

    def collideactor(self, who):
        other_rect = who.image.get_rect(topleft=who.pos)
        return self.rect.colliderect(other_rect)
    def colliderect(self, who):
        return self.rect.colliderect(who)
    def collidelistR(self, who):
        return  self.rect.collidelist(who)
    def collidelistA(self, who):
        self.rect.topleft = self.pos
        who_rect = [actor.rect for actor in who]
        return  self.rect.collidelist(who_rect)
    def angle_to(self, target):
        if isinstance(target, Actor):
            tx, ty = target.pos
        else:
            tx, ty = target
        myx, myy = self.pos
        dx = tx - myx
        dy = myy - ty   
        return degrees(atan2(dy, dx))

    def distance_to_actor(self, target):
        if isinstance(target, Actor):
            tx, ty = target.pos
        else:
            tx, ty = target
        myx, myy = self.pos
        dx = tx - myx
        dy = ty - myy
        return sqrt(dx * dx + dy * dy)
    def distance_to_rect(self, target):
        if isinstance(target, Actor):
            target = target.image.get_rect(topleft=target.pos)
        elif isinstance(target, pygame.Rect):
            pass
        else:
            raise TypeError("target must be an Actor or a pygame.Rect")
        my_rect = self.image.get_rect(topleft=self.pos)
        return my_rect.distance_to(target)
    def collidepoint(self, point):
        this_rect = self.image.get_rect(topleft=self.pos)
        return this_rect.collidepoint(point)
    def returncenter(self):
        self.center = self.rect.center
        return self.center
    def changecenter(self, new_center):
        self.rect.center = new_center
        self.pos = self.rect.topleft
        self.center = self.rect.center    
    def returnangle(self):
        return self._angle
