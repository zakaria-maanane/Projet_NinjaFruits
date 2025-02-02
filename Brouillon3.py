import pygame
import random
import sys
import time
import math

# Initialisation de Pygame
pygame.init()

def enregistrer_score(nom, score):
    with open("scores.txt", "a") as fichier:  # Mode "a" pour ajouter sans écraser
        fichier.write(f"{nom}: Score : {score}\n")

def afficher_joueurs():
    joueurs = []
    try:
        with open("scores.txt", "r") as fichier:
            joueurs = fichier.readlines()
    except FileNotFoundError:
        pass
    return joueurs

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 1300, 700
écran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Fruit Ninja")

# Charger l'image de fond
fond = pygame.image.load("montagne.png")
fond = pygame.transform.scale(fond, (LARGEUR, HAUTEUR))

# Charger et jouer la musique de fond
pygame.mixer.init()
pygame.mixer.music.load("chinese.mp3")  # Remplace par ton fichier audio
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Chargement et redimensionnement des images des fruits
image_rouge = pygame.image.load("bombe.png")
image_rouge = pygame.transform.scale(image_rouge, (90, 90))

image_vert = pygame.image.load("pomme.png")
image_vert = pygame.transform.scale(image_vert, (100, 100))

image_bleu = pygame.image.load("glace.png")
image_bleu = pygame.transform.scale(image_bleu, (60, 60))

image_jaune = pygame.image.load("banana.png")
image_jaune = pygame.transform.scale(image_jaune, (80, 80))

image_violet = pygame.transform.scale(pygame.image.load("orange.png"), (100, 100))  # Fruit sinusoïdal

# Police
defaut_police = pygame.font.Font(None, 36)

# Variables globales
horloge = pygame.time.Clock()
FPS = 60
score = 0

hauteurs_niveaux = [HAUTEUR // 6, HAUTEUR // 3, HAUTEUR // 2, HAUTEUR * 2 // 3, HAUTEUR * 5 // 6, HAUTEUR]

class Fruit:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(self.rect.width, LARGEUR - self.rect.width)
        self.rect.bottom = HAUTEUR + self.rect.height

        if self.image == image_rouge:
            self.vitesse_y = -11
            self.vitesse_x = random.uniform(-1, 3)
            self.acceleration = 0.2
            self.position_cible = hauteurs_niveaux[0]
            self.atteint_équilibre = False
        elif self.image == image_jaune:
            self.vitesse_y = -1
            self.vitesse_x = 16
            self.acceleration = 0.2
            self.position_cible = hauteurs_niveaux[0]
            self.atteint_équilibre = False
        elif self.image == image_vert:
            self.vitesse_y = -8
            self.vitesse_x = random.uniform(-2, 3)
            self.acceleration = 0.2
            self.position_cible = random.choice(hauteurs_niveaux)
            self.atteint_équilibre = False
        elif self.image == image_bleu:
            self.vitesse_y = -5
            self.vitesse_x = random.uniform(-2, 3)
            self.acceleration = 0.2
            self.position_cible = hauteurs_niveaux[0]
            self.atteint_équilibre = False
        elif self.image == image_violet:
            self.init_fruit(0, 3, 0, 0)  # Mouvement sinusoïdal
            self.angle = 0

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

            if self.rect.bottom >= HAUTEUR + self.rect.height:
                self.coupé = True

    def dessiner(self):
        if not hasattr(self, 'coupé') or not self.coupé:
            écran.blit(self.image, self.rect)

    def est_touché(self, pos):
        return self.rect.collidepoint(pos)

class Lame:
    def __init__(self):
        self.positions = []
        self.longueur_max = 10
        self.image = pygame.image.load("ninja.png")  # Remplace par le chemin de ton image
        self.rect = self.image.get_rect()

    def mettre_a_jour(self, position_souris):
        self.positions.append(position_souris)
        self.rect.center = position_souris
        if len(self.positions) > self.longueur_max:
            self.positions.pop(0)

    def dessiner(self):
        écran.blit(self.image, self.rect)
        if len(self.positions) > 1:
            pygame.draw.lines(écran, (255, 255, 255), False, self.positions, 3)

def dessiner_score():
    texte_score = defaut_police.render(f"Score : {score}", True, (255, 255, 255))
    écran.blit(texte_score, (10, 10))





score = 0
nom_joueur = ""

# Dictionnaire associant les touches aux fruits
TOUCHES_FRUITS = {
    "x": image_rouge,  # Bombe
    "v": image_vert,   # Pomme
    "b": image_bleu,   # Glaçon
    "j": image_jaune,   # Banane
    "o": image_violet
}
class JeuFruitNinja:
    def __init__(self):
        self.fruits = []
        self.lame = Lame()
        self.en_cours = True
        self.timer_ajout = 0
        self.nom_joueur = ""
        self.pause_glaçon = False
        self.temps_debut_glaçon = 0
        self.paused_fruits = False
        self.lame.mettre_a_jour(pygame.mouse.get_pos())  # Mets à jour la position de la lame avec la position de la souris


    def ajouter_fruit(self):
        global score
        if score < 10:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune, image_violet], [0, 13, 0, 0 ,1])[0]
        elif 10 <= score < 20:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune, image_violet], [0, 5, 0, 0 ,2])[0]
        elif 20 <= score < 30:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune , image_violet], [0, 2, 1, 1,2])[0]
        elif score > 30:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune , image_violet], [1, 4, 2, 2 ,2])[0]
        else:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune , image_violet], [0, 2, 3, 1, 2])[0]

        self.fruits.append(Fruit(fruit_choisi))

    def gérer_événements(self):
        for événement in pygame.event.get():
            if événement.type == pygame.QUIT:
                self.en_cours = False

    def mettre_a_jour(self):
        global score
        if self.pause_glaçon and time.time() - self.temps_debut_glaçon < 5:
            self.paused_fruits = True
        else:
            self.paused_fruits = False
            self.pause_glaçon = False

        self.lame.mettre_a_jour(pygame.mouse.get_pos())

        fruits_a_supprimer = []

        for fruit in self.fruits:
            if not self.paused_fruits:  # Si la pause est finie, on fait bouger les fruits
                fruit.bouger()

            if fruit.rect.bottom >= HAUTEUR + fruit.rect.height:
                fruits_a_supprimer.append(fruit)

            if not hasattr(fruit, 'coupé') and fruit.est_touché(pygame.mouse.get_pos()):
                fruit.coupé = True

                if fruit.image == image_rouge:
                    self.en_cours = False
                elif fruit.image == image_vert:
                    score += 1
                elif fruit.image == image_bleu:
                    score += 2
                    self.pause_glaçon = True
                    self.temps_debut_glaçon = time.time()  # Démarre la pause
                elif fruit.image == image_jaune:
                    score += 3

                fruits_a_supprimer.append(fruit)

        for fruit in fruits_a_supprimer:
            self.fruits.remove(fruit)

        self.timer_ajout += 1
        if self.timer_ajout > 30:
            self.ajouter_fruit()
            self.timer_ajout = 0

    def dessiner(self):
        # Afficher le fond à chaque mise à jour
        écran.blit(fond, (0, 0))  # Afficher l'image de fond

        self.lame.dessiner()

        for fruit in self.fruits:
            fruit.dessiner()

        dessiner_score()

        pygame.display.flip()

    def accueil(self):
        accueil_screen = Accueil(écran)  # Crée l'instance de la classe Accueil
        self.nom_joueur = accueil_screen.saisir_nom()  # Saisir le nom et le retourner

    def executer(self):
        self.accueil()  # Afficher l'écran d'accueil
        global score
        while self.en_cours:
            self.gérer_événements()
            self.mettre_a_jour()
            self.dessiner()
            horloge.tick(FPS)

        enregistrer_score(self.nom_joueur, score)

class Accueil:
    def __init__(self, écran):
        self.écran = écran
        self.nom_joueur = ""

    def afficher(self):
        # Charger l'image de fond
        écran.blit(fond, (0, 0))  # Afficher l'image de fond à l'écran d'accueil

        font = pygame.font.Font(None, 48)
        texte_accueil = font.render("Bienvenue dans Fruit Ninja !", True, (255, 255, 255))
        écran.blit(texte_accueil, (LARGEUR // 2 - texte_accueil.get_width() // 2, 100))

        joueurs = afficher_joueurs()
        y_offset = 200
        for joueur in joueurs:
            texte_joueur = font.render(joueur.strip(), True, (255, 255, 255))
            écran.blit(texte_joueur, (LARGEUR // 2 - texte_joueur.get_width() // 2, y_offset))
            y_offset += 50

        pygame.display.flip()

    def saisir_nom(self):
        global nom_joueur
        nom_joueur = ""
        active = True
        font = pygame.font.Font(None, 48)

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if nom_joueur != "":
                            return nom_joueur  # Renvoie le nom du joueur après validation
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        nom_joueur = nom_joueur[:-1]
                    else:
                        nom_joueur += event.unicode

                    # Redessiner l'écran à chaque modification
                    écran.blit(fond, (0, 0))  # Redessiner l'image de fond
                    self.afficher()  # Afficher les éléments de l'écran d'accueil

                    # Afficher le nom du joueur en train d'être saisi
                    texte_nom = font.render(f"Nom du joueur : {nom_joueur}", True, (255, 255, 255))
                    écran.blit(texte_nom, (LARGEUR // 2 - texte_nom.get_width() // 2, 400))

                    pygame.display.flip()

# Boucle principale
jeu = JeuFruitNinja()
jeu.accueil()

while jeu.en_cours:
    jeu.gérer_événements()
    jeu.mettre_a_jour()
    jeu.dessiner()

    horloge.tick(FPS)

pygame.quit()
