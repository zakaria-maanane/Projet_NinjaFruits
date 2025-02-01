import pygame
import random
import sys
import time
import math

# Initialisation de Pygame
pygame.init()

def enregistrer_score(nom, score):
    with open("scores.txt", "a") as fichier:
        fichier.write(f"{nom}: Score : {score}\n")

def afficher_joueurs():
    try:
        with open("scores.txt", "r") as fichier:
            return fichier.readlines()
    except FileNotFoundError:
        return []

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 1300, 700
écran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Fruit Ninja")

# Charger l'image de fond
fond = pygame.image.load("5.png")
fond = pygame.transform.scale(fond, (LARGEUR, HAUTEUR))

# Charger et jouer la musique de fond
pygame.mixer.init()
pygame.mixer.music.load("chinese.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Chargement et redimensionnement des images des fruits
image_rouge = pygame.transform.scale(pygame.image.load("bombe.png"), (90, 90))  
image_vert = pygame.transform.scale(pygame.image.load("pomme.png"), (80, 80))  
image_bleu = pygame.transform.scale(pygame.image.load("glacon.png"), (60, 60))  
image_jaune = pygame.transform.scale(pygame.image.load("banana.jpg"), (60, 60)) 
image_violet = pygame.transform.scale(pygame.image.load("glace.png"), (70, 70))  # Fruit sinusoïdal
image_or = pygame.transform.scale(pygame.image.load("orange.png"), (75, 75))  # Fruit plume

# Police
defaut_police = pygame.font.Font(None, 36)

# Variables globales
horloge = pygame.time.Clock()
FPS = 60
score = 0
hauteurs_niveaux = [HAUTEUR // 6, HAUTEUR // 3, HAUTEUR // 2, HAUTEUR * 2 // 3, HAUTEUR * 5 // 6, HAUTEUR]

temps_depart = time.time()

class Fruit:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.coupé = False
        self.timer = 0
        
        if self.image == image_rouge:
            self.init_fruit(-11, random.uniform(-1, 3), 0.2, hauteurs_niveaux[0])
        elif self.image == image_jaune:
            self.init_fruit(-5, 6, 0.2, hauteurs_niveaux[0])
        elif self.image == image_vert:
            self.init_fruit(-8, random.uniform(-2, 3), 0.2, random.choice(hauteurs_niveaux))
        elif self.image == image_bleu:
            self.init_fruit(-5, random.uniform(-2, 3), 0.2, hauteurs_niveaux[0])
        elif self.image == image_violet:
            self.init_fruit(0, 3, 0, 0)  # Mouvement sinusoïdal
            self.angle = 0
        elif self.image == image_or:
            self.init_fruit(-4, random.uniform(-1, 1), 0.1, HAUTEUR)  # Mouvement plume
            self.direction = 1

    def init_fruit(self, vy, vx, acc, pos):
        self.vitesse_y = vy
        self.vitesse_x = vx
        self.acceleration = acc
        self.position_cible = pos
        self.atteint_équilibre = False
        self.rect.centerx = random.randint(self.rect.width, LARGEUR - self.rect.width)
        self.rect.bottom = HAUTEUR + self.rect.height
    
    def bouger(self):
        if self.image == image_violet:
            self.rect.x += 5 * math.sin(self.angle)
            self.rect.y -= 3
            self.angle += 0.1
        elif self.image == image_or:
            self.rect.y += self.vitesse_y
            self.rect.x += self.vitesse_x * self.direction
            self.direction *= -1 if random.random() < 0.1 else 1
        else:
            if not self.atteint_équilibre:
                self.rect.y += self.vitesse_y
                self.rect.x += self.vitesse_x
                self.vitesse_y += 0.1
                if self.rect.top <= self.position_cible:
                    self.rect.top = self.position_cible
                    self.vitesse_y = 0
                    self.atteint_équilibre = True
            else:
                self.vitesse_y += self.acceleration
                self.rect.y += self.vitesse_y
                self.rect.x += self.vitesse_x

    def dessiner(self):
        if not self.coupé:
            écran.blit(self.image, self.rect)

    def est_touché(self, pos):
        return self.rect.collidepoint(pos)

class JeuFruitNinja:
    def __init__(self):
        self.fruits = []
        self.en_cours = True
        self.timer_ajout = 0

    def ajouter_fruit(self):
        fruit_choisi = random.choices(
            [image_rouge, image_vert, image_bleu, image_jaune, image_violet, image_or],
            [1, 5, 2, 2, 2, 2]  # Répartition des chances d'apparition
        )[0]
        self.fruits.append(Fruit(fruit_choisi))

    def mettre_a_jour(self):
        self.fruits = [fruit for fruit in self.fruits if not fruit.coupé]
        for fruit in self.fruits:
            fruit.bouger()
            if fruit.est_touché(pygame.mouse.get_pos()):
                fruit.coupé = True
        if self.timer_ajout > 30:
            self.ajouter_fruit()
            self.timer_ajout = 0
        self.timer_ajout += 1

    def dessiner(self):
        écran.blit(fond, (0, 0))
        for fruit in self.fruits:
            fruit.dessiner()
        pygame.display.flip()

    def executer(self):
        while self.en_cours:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.en_cours = False
            self.mettre_a_jour()
            self.dessiner()
            horloge.tick(FPS)

if __name__ == "__main__":
    jeu = JeuFruitNinja()
    jeu.executer()
    pygame.quit()
    sys.exit()
