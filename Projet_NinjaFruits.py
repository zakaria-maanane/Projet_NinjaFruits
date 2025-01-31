import pygame
import random
import sys
import time

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
fond = pygame.image.load("5.png")
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
image_vert = pygame.transform.scale(image_vert, (80, 80))  

image_bleu = pygame.image.load("glacon.png")
image_bleu = pygame.transform.scale(image_bleu, (60, 60))  

image_jaune = pygame.image.load("banana.jpg")
image_jaune = pygame.transform.scale(image_jaune, (60, 60)) 

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
            self.vitesse_y = -5
            self.vitesse_x = 6
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

    def bouger(self):
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

    def mettre_à_jour(self, pos):
        self.positions.append(pos)
        if len(self.positions) > self.longueur_max:
            self.positions.pop(0)

    def dessiner(self):
        if len(self.positions) > 1:
            pygame.draw.lines(écran, (255, 255, 255), False, self.positions, 3)

def dessiner_score():
    texte_score = defaut_police.render(f"Score : {score}", True, (255, 255, 255))
    écran.blit(texte_score, (10, 10))

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

    def ajouter_fruit(self):
        global score
        if score < 10:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune], [0, 8, 0, 0])[0]
        elif 10 <= score < 20:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune], [0, 5, 0, 0])[0]
        elif 20 <= score < 30:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune], [0, 2, 1, 1])[0]
        elif score > 30:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune], [1, 4, 2, 2])[0]
        else:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune], [0, 2, 3, 1])[0]

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

        self.lame.mettre_à_jour(pygame.mouse.get_pos())

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
        # Afficher le fond d'écran d'accueil
        écran.blit(fond, (0, 0))  # Afficher l'image de fond à l'écran d'accueil

        # Écran d'accueil où le joueur entre son nom
        font = pygame.font.Font(None, 48)
        texte_accueil = font.render("Bienvenue dans Fruit Ninja !", True, (255, 255, 255))
        texte_nom = font.render("Entrez votre nom:", True, (255, 255, 255))
        
        # Afficher l'écran d'accueil
        écran.blit(texte_accueil, (LARGEUR // 3, HAUTEUR // 3))
        écran.blit(texte_nom, (LARGEUR // 3, HAUTEUR // 2))
        pygame.display.flip()

        # Entrée du nom du joueur
        nom = ""
        entrer_nom = True
        while entrer_nom:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.nom_joueur = nom
                        entrer_nom = False
                    elif event.key == pygame.K_BACKSPACE:
                        nom = nom[:-1]
                    else:
                        nom += event.unicode
            # Afficher le nom en temps réel
            écran.fill((0, 0, 0))
            écran.blit(fond, (0, 0))  # Afficher l'image de fond pendant la saisie du nom
            écran.blit(texte_accueil, (LARGEUR // 3, HAUTEUR // 3))
            écran.blit(texte_nom, (LARGEUR // 3, HAUTEUR // 2))
            nom_texte = font.render(nom, True, (255, 255, 255))
            écran.blit(nom_texte, (LARGEUR // 3, HAUTEUR // 1.5))
            pygame.display.flip()

    def executer(self):
        self.accueil()  # Afficher l'écran d'accueil
        global score
        while self.en_cours:
            self.gérer_événements()
            self.mettre_a_jour()
            self.dessiner()
            horloge.tick(FPS)

        enregistrer_score(self.nom_joueur, score)

if __name__ == "__main__":
    jeu = JeuFruitNinja()
    jeu.executer()
    pygame.quit()
    sys.exit()
