import pygame
import random
import sys  

# Initialisation de Pygame
pygame.init()

def enregistrer_score(score):
    with open("scores.txt", "a") as fichier:  # Mode "a" pour ajouter sans écraser
        fichier.write(f"Score : {score}\n")

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 1300, 800
écran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Fruit Ninja")  

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)
JAUNE = (255, 255, 0)

# Police
defaut_police = pygame.font.Font(None, 36)

# Variables globales
horloge = pygame.time.Clock()
FPS = 60
score = 0

# Six hauteurs distinctes où les fruits atteignent leur équilibre
hauteurs_niveaux = [HAUTEUR // 6, HAUTEUR // 3, HAUTEUR // 2, HAUTEUR * 2 // 3, HAUTEUR * 5 // 6, HAUTEUR]  # 6 niveaux distincts
# Classe Fruit
class Fruit:
    def __init__(self, couleur):
        self.couleur = couleur

        # Chargez l'image du fruit rouge si nécessaire
        if self.couleur == ROUGE:
            self.image = pygame.image.load("bombev3.jpg")
            self.image = pygame.transform.scale(self.image, (80, 80))  # Redimensionner l'image à la taille souhaitée
            self.rayon = 40  
            self.vitesse_y = -11
            self.vitesse_x = random.uniform(-1, 3)  
            self.acceleration = 0.2  
            self.position_cible = hauteurs_niveaux[0]
            self.atteint_équilibre = False
        elif self.couleur == JAUNE:
            self.rayon = 20  
            self.vitesse_y = -5
            self.vitesse_x = 10
            self.acceleration = 0.2  
            self.position_cible = hauteurs_niveaux[0]
            self.atteint_équilibre = False
        elif self.couleur == VERT:
            self.rayon = 40  
            self.vitesse_y = -8
            self.vitesse_x = random.uniform(-2, 3)  
            self.acceleration = 0.2  
            self.position_cible = random.choice(hauteurs_niveaux)
            self.atteint_équilibre = False
        elif self.couleur == BLEU:
            self.rayon = 20  
            self.vitesse_y = -5
            self.vitesse_x = random.uniform(-2, 3)  
            self.acceleration = 0.2  
            self.position_cible = hauteurs_niveaux[0]
            self.atteint_équilibre = False

        self.x = random.randint(self.rayon, LARGEUR - self.rayon)
        self.y = HAUTEUR + self.rayon
        self.coupé = False

    def bouger(self):
        if not self.atteint_équilibre:
            # Phase de montée
            self.y += self.vitesse_y
            self.x += self.vitesse_x

            self.vitesse_y += 0.1  # Ralentissement de la montée

            if self.y <= self.position_cible:
                self.y = self.position_cible
                self.vitesse_y = 0
                self.atteint_équilibre = True  # Le fruit a atteint son sommet

        else:
            # Phase de descente
            self.vitesse_y += self.acceleration  # Applique la gravité
            self.y += self.vitesse_y
            self.x += self.vitesse_x  # Mouvement horizontal pour la descente

            # Si le fruit sort de l'écran par le bas, on le marque comme à supprimer
            if self.y >= HAUTEUR + self.rayon:
                self.coupé = True  # On marque le fruit comme coupé (disparaît)

    def dessiner(self):
        if not self.coupé:
            # Affiche l'image du fruit rouge si nécessaire
            if self.couleur == ROUGE:
                écran.blit(self.image, (self.x - self.rayon, self.y - self.rayon))  # Centrer l'image
            else:
                pygame.draw.circle(écran, self.couleur, (int(self.x), int(self.y)), self.rayon)

    def est_touché(self, pos):
        distance = ((self.x - pos[0])**2 + (self.y - pos[1])**2)**0.5
        return distance <= self.rayon

# Classe Lame
class Lame:
    def __init__(self):
        self.positions = []
        self.longueur_max = 10

    def mettre_à_jour(self, pos):
        self.positions.append(pos)
        if len(self.positions) > self.longueur_max:
            self.positions.pop(0)

    def dessiner(self):
        if len(self.positions) > 1:
            pygame.draw.lines(écran, BLANC, False, self.positions, 3)

# Le reste du code reste inchangé
