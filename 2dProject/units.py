import pygame

class Unit:

    def __init__(self, hp, attack, recovery, type, sprite):
        """
        Arguments:
            hp(int): Hp of unit.
            attack(int): Attack of unit.
            type(int): The attack type of unit.
            sprite: The image or sprite of the unit.
        """
        self.hp = hp
        self.attack = attack
        self.recovery = recovery
        self.type = type
        self.sprite = pygame.image.load(sprite).convert_alpha()

    def update(self, screen, coordinates):
        """
        Displays the units on screen.
        Arguments:
            screen: The surface of the game.
            coordinates:  The coordinates of the units on screen.
        """
        screen.blit(self.sprite, coordinates)

