import pygame

class Orb:
    """
    The orb class is to make an orb object to update where an orb is on the screen.
    """

    def __init__(self, orb_type, type):
        """
        Arguments:
            orb_type(dict): Dictionary of orb pictures.
            type(int): The type of orb it is.
        """
        self.type = type
        self.orb = pygame.image.load(orb_type).convert_alpha()

    def display(self, screen, coor):
        """
        Displays the orb on screen.
        Arguments:
            screen: Takes the surface of the game and displays orb.
            coor: Coordinates on the screen.
        """
        self.coor = coor
        screen.blit(self.orb, self.coor)

    def update(self, screen):
        """
        Updates the orb on screen.
        Arguments:
            screen: Takes the surface of the game and updates orb.
        """
        mouse_pos = pygame.mouse.get_pos()
        self.centerx = mouse_pos[0] - 75/2
        self.centery = mouse_pos[1] - 75/2
        screen.blit(self.orb, (self.centerx, self.centery))

    def xy_coordinates(self, xy_coordinates):
        """
            xy_coordinates(int,int): Sets x,y coordinates
        """
        self.coordinates = xy_coordinates



