import pygame
import random
import sys
import os

# Initialisation de Pygame
pygame.init()

def enregistrer_score(score):
    with open("scores.txt", "a") as fichier:  # Mode "a" pour ajouter sans écraser
        fichier.write(f"Score : {score}\n")

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 1000, 600
écran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Fruit Ninja")

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

# Police
defaut_police = pygame.font.Font(None, 36)

# Variables globales
horloge = pygame.time.Clock()
FPS = 40
score = 0

# Chargement des images
BASE_PATH = "c:/Users/zakar/Projet_NinjaFruits/"
try:
    BOMBE_IMAGE = pygame.image.load(os.path.join(BASE_PATH, "bombev3.jpg"))
    BOMBE_IMAGE = pygame.transform.scale(BOMBE_IMAGE, (50, 50))


    BANANE_IMAGE = pygame.image.load(os.path.join(BASE_PATH, "banana.jpg"))
    BANANE_IMAGE = pygame.transform.scale(BANANE_IMAGE, (50, 50))

    FRAISE_IMAGE = pygame.image.load(os.path.join(BASE_PATH, "fraise.jpg"))
    FRAISE_IMAGE = pygame.transform.scale(FRAISE_IMAGE, (50, 50))

    PASTÈQUE_IMAGE = pygame.image.load(os.path.join(BASE_PATH, "pasteque.png"))
    PASTÈQUE_IMAGE = pygame.transform.scale(PASTÈQUE_IMAGE, (50, 50))

    POMME_IMAGE = pygame.image.load(os.path.join(BASE_PATH, "pomme.png"))
    POMME_IMAGE = pygame.transform.scale(POMME_IMAGE, (50, 50))

    KIWI_IMAGE = pygame.image.load(os.path.join(BASE_PATH, "kiwi.png"))
    KIWI_IMAGE = pygame.transform.scale(KIWI_IMAGE, (50, 50))

    ORANGE_IMAGE = pygame.image.load(os.path.join(BASE_PATH, "orange.png"))
    ORANGE_IMAGE = pygame.transform.scale(ORANGE_IMAGE, (50, 50))

except pygame.error as e:
    print(f"Erreur lors du chargement des images : {e}")
    sys.exit()

# Six hauteurs distinctes pour le point d'équilibre
hauteurs_niveaux = [
    HAUTEUR // 6, HAUTEUR // 3, HAUTEUR // 2,
    HAUTEUR * 2 // 3, HAUTEUR * 5 // 6, HAUTEUR
]

# Liste des fruits disponibles
FRUITS_IMAGES = [BANANE_IMAGE, FRAISE_IMAGE, PASTÈQUE_IMAGE, POMME_IMAGE, KIWI_IMAGE, ORANGE_IMAGE]

# Classe Fruit
class Fruit:
    def __init__(self):
        self.est_bombe = random.random() < 0.2  # 20% de bombes
        if self.est_bombe:
            self.image = BOMBE_IMAGE
            self.couleur = "bombe"
        else:
            self.image = random.choice(FRUITS_IMAGES)
            self.couleur = "fruit"

        # Attribuer des hauteurs et vitesses spécifiques
        self.rayon = 60
        self.x = random.randint(self.rayon, LARGEUR - self.rayon)
        self.y = HAUTEUR + self.rayon
        self.vitesse_y = -random.uniform(7, 20)  # Vitesse initiale
        self.vitesse_x = random.uniform(-13, 13)
        self.acceleration = 0.5
        self.position_cible = random.choice(hauteurs_niveaux)
        self.atteint_équilibre = False
        self.coupé = False

    def bouger(self):
        if not self.atteint_équilibre:
            # Phase de montée
            self.y += self.vitesse_y
            self.x += self.vitesse_x
            self.vitesse_y += 0.3  # Décélération de la montée

            if self.y <= self.position_cible:
                self.y = self.position_cible
                self.vitesse_y = 0
                self.atteint_équilibre = True  # Le fruit a atteint son sommet
        else:
            # Phase de descente
            self.vitesse_y += self.acceleration  # Gravité
            self.y += self.vitesse_y
            self.x += self.vitesse_x  # Mouvement horizontal

    def dessiner(self):
        if not self.coupé:
            écran.blit(self.image, (int(self.x - self.rayon), int(self.y - self.rayon)))

    def est_touché(self, pos):
        distance = ((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2) ** 0.5
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

# Classe ObjetsFantasies
class ObjetsFantasies:
    def __init__(self, type_objet, vitesse_y=10, hauteur=None):
        self.type_objet = type_objet
        self.image = None
        self.vitesse_y = vitesse_y  # Vitesse de mouvement

        if hauteur is None:
            self.y = HAUTEUR + 60  # Par défaut, l'objet commence en bas
        else:
            self.y = hauteur

        if self.type_objet == "bombe":
            self.image = BOMBE_IMAGE
        elif self.type_objet == "glacon":
            self.image = pygame.image.load(os.path.join(BASE_PATH, "glacon.png"))
            self.image = pygame.transform.scale(self.image, (50, 50))
        elif self.type_objet == "ananas":
            self.image = pygame.image.load(os.path.join(BASE_PATH, "ananas.png"))
            self.image = pygame.transform.scale(self.image, (50, 50))
        elif self.type_objet == "glace":
            self.image = pygame.image.load(os.path.join(BASE_PATH, "glace.png"))
            self.image = pygame.transform.scale(self.image, (50, 50))

        self.rayon = 60
        self.x = random.randint(self.rayon, LARGEUR - self.rayon)
        self.acceleration = 0.5
        self.atteint_équilibre = False
        self.coupé = False

    def bouger(self):
        if not self.atteint_équilibre:
            self.y += self.vitesse_y
            self.x += random.uniform(-13, 13)
            self.vitesse_y += 0.3

            if self.y <= HAUTEUR // 2:
                self.y = HAUTEUR // 2
                self.vitesse_y = 0
                self.atteint_équilibre = True
        else:
            self.vitesse_y += self.acceleration
            self.y += self.vitesse_y
            self.x += random.uniform(-13, 13)

    def dessiner(self):
        if not self.coupé:
            écran.blit(self.image, (int(self.x - self.rayon), int(self.y - self.rayon)))

    def est_touché(self, pos):
        distance = ((self.x - pos[0]) ** 2 + (self.y - pos[1]) ** 2) ** 0.5
        return distance <= self.rayon

# Classe JeuFruitNinja
class JeuFruitNinja:
    def __init__(self):
        self.fruits = []
        self.objets_fantasies = []
        self.lame = Lame()
        self.en_cours = True
        self.timer_ajout = 0
        self.effets_actifs = {}
        self.bombes_interdites = False  # Variable pour gérer l'interdiction des bombes

    def ajouter_objet_fantasie(self):
        # Paramètres de vitesse et hauteur personnalisables pour chaque objet fantastique
        type_objet = random.choice(["glacon", "ananas", "bombe", "glace"])
        vitesse_y = random.uniform(7, 15)  # Vitesse de 7 à 15 pour la montée
        hauteur = random.choice(hauteurs_niveaux)  # Hauteur choisie parmi les points d'équilibre
        self.objets_fantasies.append(ObjetsFantasies(type_objet, vitesse_y, hauteur))

    def gérer_événements(self):
        for événement in pygame.event.get():
            if événement.type == pygame.QUIT:
                self.en_cours = False

    def appliquer_effets(self):
        global FPS, score

        # Appliquer les effets des objets fantastiques
        if "ralentissement" in self.effets_actifs and pygame.time.get_ticks() > self.effets_actifs["ralentissement"]:
            FPS = 40  # Réinitialiser la vitesse

        if "ananas" in self.effets_actifs and pygame.time.get_ticks() > self.effets_actifs["ananas"]:
            self.objets_fantasies = [
                obj for obj in self.objets_fantasies if obj.type_objet != "bombe"
            ]

        if "glace" in self.effets_actifs and pygame.time.get_ticks() > self.effets_actifs["glace"]:
            self.bombes_interdites = False  # Réactiver les bombes après 5 secondes

    def mettre_à_jour(self):
        global score, FPS
        self.lame.mettre_à_jour(pygame.mouse.get_pos())

        for fruit in self.fruits:
            fruit.bouger()
            fruit.dessiner()

        for objet in self.objets_fantasies:
            objet.bouger()
            objet.dessiner()

        self.appliquer_effets()

        pygame.display.update()

    def ajouter_fruit(self):
        if pygame.time.get_ticks() - self.timer_ajout > 1000:
            self.timer_ajout = pygame.time.get_ticks()
            self.fruits.append(Fruit())

    def dessiner(self):
        écran.fill(NOIR)

    def démarrer(self):
        while self.en_cours:
            self.gérer_événements()
            self.ajouter_fruit()
            self.ajouter_objet_fantasie()
            self.mettre_à_jour()
            self.dessiner()
            horloge.tick(FPS)

if __name__ == "__main__":
    jeu = JeuFruitNinja()
    jeu.démarrer()
