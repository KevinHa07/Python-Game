import pygame

class Stage:
    """
    The stage class is used to create a stage object.
    """
    def __init__(self, stage, sprite):
        """
        Arguments:
            stage(int): The stage number.
            sprite: The image of the background.
        """
        self.stage = stage
        self.stage_pic = pygame.image.load(sprite).convert_alpha()

    def update(self, screen):
        """
        Updates the screen based on the stage.
        Arguments:
            screen: The surface of the game to display the background.
        """
        screen.blit(self.stage_pic, (0,0))