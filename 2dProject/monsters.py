import pygame

class Monsters:
    """
    The monster class is used to store the enemies in objects.
    """
    def __init__(self, hp, attack, type, turn, sprite, stage):
        """
        Arguments:
            hp(int): Hp of enemy.
            attack(int): Attack of enemy.
            type(int): The attack type of enemy.
            turn(int): The number of turns until this enemy attacks
            sprite: The image or sprite of the enemy.
            stage(int): The stage of enemy.
        """
        self.hp = hp
        self.type = type
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.attack = attack
        self.turn = turn
        self.stage = stage
        self.coordinate = (350, 110)
        self.current_hp = self.hp
        self.current_turn = 0
        self.fire_sound = pygame.mixer.Sound('fire_sound.wav')
        self.water_sound = pygame.mixer.Sound('water_sound.wav')
        self.wood_sound = pygame.mixer.Sound('wood_sound.wav')
        self.light_sound = pygame.mixer.Sound('light_sound.wav')
        self.dark_sound = pygame.mixer.Sound('dark_sound.wav')

    def update(self, screen):
        """
        Updates the enemy on screen.
        Arguments:
            screen: The surface of the game.
        """
        screen.blit(self.sprite, self.coordinate)
        font = pygame.font.SysFont('arialblack', 14)
        if self.type == 1:
            percent = self.current_hp / self.hp
            hp_length = 150 * percent
            pygame.draw.rect(screen, (255, 255, 255), (self.coordinate[0] - 40, self.coordinate[1] - 23, 150, 15), 0)
            pygame.draw.rect(screen, (196, 0, 0), (self.coordinate[0] - 40, self.coordinate[1] - 23, hp_length, 15), 0)
        elif self.type == 2:
            percent = self.current_hp / self.hp
            hp_length = 150 * percent
            pygame.draw.rect(screen, (255, 255, 255), (self.coordinate[0] - 40, self.coordinate[1] - 23, 150, 15), 0)
            pygame.draw.rect(screen, (0, 119, 255), (self.coordinate[0] - 40, self.coordinate[1] - 23, hp_length, 15), 0)
        elif self.type == 3:
            percent = self.current_hp / self.hp
            hp_length = 150 * percent
            pygame.draw.rect(screen, (255, 255, 255), (self.coordinate[0] - 40, self.coordinate[1] - 23, 150, 15), 0)
            pygame.draw.rect(screen, (0, 133, 20), (self.coordinate[0] - 40, self.coordinate[1] - 23, hp_length, 15), 0)
        elif self.type == 4:
            percent = self.current_hp / self.hp
            hp_length = 150 * percent
            pygame.draw.rect(screen, (255, 255, 255), (self.coordinate[0] - 40, self.coordinate[1] - 23, 150, 15), 0)
            pygame.draw.rect(screen, (240,250,60), (self.coordinate[0] - 40, self.coordinate[1] - 23, hp_length, 15), 0)
        elif self.type == 5:
            percent = self.current_hp / self.hp
            hp_length = 150 * percent
            pygame.draw.rect(screen, (255, 255, 255), (self.coordinate[0] - 40, self.coordinate[1] - 23, 150, 15), 0)
            pygame.draw.rect(screen, (187,0,255), (self.coordinate[0] - 40, self.coordinate[1] - 23, hp_length, 15), 0)

        text = font.render(str(int(self.current_hp)) + '/' + str(self.hp), True, (0,0,0))
        screen.blit(text, (self.coordinate[0] - 35, self.coordinate[1] - 25))
        text = font.render('TRN ' + str((self.turn - self.current_turn)) + '', True, (0,0,0))
        screen.blit(text, (self.coordinate[0] - 55, self.coordinate[1] - 5))

    def update_hp(self, attack):
        """
        Arguments:
            attack: Gets the incoming attack and updates the enemies hp. When hp = 0, enemy dies.
        """
        chan1 = pygame.mixer.Channel(1)
        chan2 = pygame.mixer.Channel(2)
        chan3 = pygame.mixer.Channel(3)
        chan4 = pygame.mixer.Channel(4)
        chan5 = pygame.mixer.Channel(5)
        x = 0
        for damage in attack:
            if x == x + 1 and self.type == 3: #fire and wood
                self.current_hp -= damage * 2
                chan1.queue(self.fire_sound)
            elif x == x + 1 and self.type == 1: #water and fire
                self.current_hp -= damage * 2
                chan2.queue(self.water_sound)
            elif x == x + 1 and self.type == 2: #wood and water
                self.current_hp -= damage * 2
                chan3.queue(self.wood_sound)
            elif x == x + 1 and self.type == 2: #fire and water
                self.current_hp -= damage / 2
                chan1.queue(self.fire_sound)
            elif x == x + 1 and self.type == 3: #water and wood
                self.current_hp -= damage / 2
                chan2.queue(self.water_sound)
            elif x == x + 1 and self.type == 1: #wood and fire
                self.current_hp -= damage / 2
                chan3.queue(self.wood_sound)
            elif x == x + 1 and self.type == 5: #light and dark
                self.current_hp -= damage * 2
                chan4.queue(self.light_sound)
            elif x == x + 1 and self.type == 4: #dark and light
                self.current_hp -= damage * 2
                chan5.queue(self.dark_sound)
            else:
                self.current_hp -= damage
                if damage != 0:
                    if x == 0:
                        chan1.queue(self.fire_sound)
                    elif x == 1:
                        chan2.queue(self.water_sound)
                    elif x == 2:
                        chan3.queue(self.wood_sound)
                    elif x == 3:
                        chan4.queue(self.light_sound)
                    elif x == 4:
                        chan5.queue(self.dark_sound)
            pygame.time.delay(10)
            if self.current_hp <= 0:
                self.current_hp = 0
            x += 1

    def attack_return(self, turn):
        """
        Returns the atack value of this enemy.
        Arguments:
            turn: If turn equals this enemy's turn timer, then it attacks.
        Returns:
            self.attack: The attack value of this enemy
        """
        self.current_turn += turn
        if self.current_turn == self.turn:
            self.current_turn = 0
            return self.attack
        return 0

