import pygame
import random
import sys

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

# Chargement et redimensionnement des images des fruits
image_rouge = pygame.image.load("bombe.png")
image_rouge = pygame.transform.scale(image_rouge, (90, 90))  

image_vert = pygame.image.load("pomme.png")
image_vert = pygame.transform.scale(image_vert, (80, 80))  

image_bleu = pygame.image.load("glacon.png")
image_bleu = pygame.transform.scale(image_bleu, (60, 60))  

image_jaune = pygame.image.load("fraise.png")
image_jaune = pygame.transform.scale(image_jaune, (60, 60)) 

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
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()  # Récupérer les dimensions de l'image
        self.rect.centerx = random.randint(self.rect.width, LARGEUR - self.rect.width)
        self.rect.bottom = HAUTEUR + self.rect.height

        # Définir les vitesses et autres propriétés en fonction de l'image choisie
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
            # Phase de montée
            self.rect.y += self.vitesse_y
            self.rect.x += self.vitesse_x
            self.vitesse_y += 0.1

            if self.rect.top <= self.position_cible:
                self.rect.top = self.position_cible
                self.vitesse_y = 0
                self.atteint_équilibre = True
        else:
            # Phase de descente
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
            pygame.draw.lines(écran, (255, 255, 255), False, self.positions, 3)
# Votre code principal

# Fonction de mise à jour de l'affichage du score
def dessiner_score():
    texte_score = defaut_police.render(f"Score : {score}", True, (255, 255, 255))
    écran.blit(texte_score, (10, 10))  # Dessine le score en haut à gauche de l'écran



class JeuFruitNinja:
    def __init__(self):
        self.fruits = []
        self.lame = Lame()
        self.en_cours = True
        self.timer_ajout = 0
        self.nom_joueur = ""

    def accueil(self):
        nom = ""
        actif = True
        while actif:
            for événement in pygame.event.get():
                if événement.type == pygame.QUIT:
                    self.en_cours = False  # Ferme le jeu si la fenêtre est fermée
                    actif = False
                    break
                if événement.type == pygame.KEYDOWN:
                    if événement.key == pygame.K_BACKSPACE:
                        nom = nom[:-1]
                    elif événement.key == pygame.K_RETURN:
                        self.nom_joueur = nom
                        actif = False
                    else:
                        nom += événement.unicode

            # Afficher l'écran d'accueil et les scores
            écran.fill((0, 0, 0))
            titre = defaut_police.render("Fruit Ninja", True, (255, 255, 255))
            écran.blit(titre, (LARGEUR // 2 - titre.get_width() // 2, 100))

            joueur_text = defaut_police.render("Entrez votre nom:", True, (255, 255, 255))
            écran.blit(joueur_text, (LARGEUR // 2 - joueur_text.get_width() // 2, 200))

            nom_text = defaut_police.render(nom, True, (255, 255, 255))
            écran.blit(nom_text, (LARGEUR // 2 - nom_text.get_width() // 2, 300))

            # Afficher les scores des joueurs enregistrés
            joueurs = afficher_joueurs()
            y_offset = 400
            for joueur in joueurs:
                score_text = defaut_police.render(joueur, True, (255, 255, 255))
                écran.blit(score_text, (LARGEUR // 2 - score_text.get_width() // 2, y_offset))
                y_offset += 40

            pygame.display.flip()
            horloge.tick(FPS)

    def ajouter_fruit(self):
        # Logique pour ajouter un fruit en fonction du score
        if score < 10:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune], [0, 5, 0, 0])[0]
        elif 10 <= score < 20:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune], [2, 3, 0, 0])[0]
        elif 20 <= score < 30:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune], [4, 1, 2, 0])[0]
        else:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune], [5, 2, 3, 1])[0]

        self.fruits.append(Fruit(fruit_choisi))

    def gérer_événements(self):
        for événement in pygame.event.get():
            if événement.type == pygame.QUIT:
                self.en_cours = False  # Ferme le jeu si la fenêtre est fermée

    def mettre_à_jour(self):
        global score
        self.lame.mettre_à_jour(pygame.mouse.get_pos())

        fruits_a_supprimer = []

        for fruit in self.fruits:
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
        écran.fill((0, 0, 0))  # Effacer l'écran à chaque itération
        self.lame.dessiner()

        for fruit in self.fruits:
            fruit.dessiner()

        dessiner_score()  # Afficher le score

        pygame.display.flip()

    def exécuter(self):
        self.accueil()  # Appel à la page d'accueil avant de commencer le jeu
        global score
        while self.en_cours:
            self.gérer_événements()
            self.mettre_à_jour()
            self.dessiner()
            horloge.tick(FPS)

        enregistrer_score(self.nom_joueur, score)

# Lancer le jeu
if __name__ == "__main__":
    jeu = JeuFruitNinja()
    jeu.exécuter()
    pygame.quit()
    sys.exit()
