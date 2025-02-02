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
        self.pause_glaçon = False
        self.temps_debut_glaçon = 0
        self.paused_fruits = False
        self.nom_joueur = ""
        self.vies = 1115  # Compteur de vies
        self.score = 0  # Compteur de score
        # ... tes autres attributs
        self.boost_actif = False  # Pour savoir si le boost est activé
        self.temps_debut_boost = 0  # Pour savoir quand le boost a commencé
        self.multiplieur_pommes = 1  # Par défaut, les pommes apparaissent normalement
        self.bombes_activees = True  # Par défaut, les bombes peuvent apparaître


    def ajouter_fruit(self):
    # On ajuste l'apparition des fruits en fonction du boost
      if self.boost_actif:
        # Si le boost est actif, on augmente la probabilité de faire apparaître des pommes
        fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune, image_violet], 
                                      [0, 0, 0, 0, 0])[0]  # Évite de générer des bombes
        if random.random() < 0.9:  # On met 90% de chance de faire apparaître une pomme
            fruit_choisi = image_vert  # Pomme verte
      else:
        # Comportement habituel sans boost
        if self.score < 10:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune, image_violet], [0, 13, 0, 16 ,3])[0]
        elif 10 <= self.score < 20:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune, image_violet], [0, 5, 0, 15 ,3])[0]
        elif 20 <= self.score < 30:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune , image_violet], [0, 2, 1, 31,2])[0]
        elif self.score > 30:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune , image_violet], [1, 4, 2, 32 ,2])[0]
        else:
            fruit_choisi = random.choices([image_rouge, image_vert, image_bleu, image_jaune , image_violet], [0, 2, 3, 31, 2])[0]

      self.fruits.append(Fruit(fruit_choisi))



    def gérer_événements(self):
     for événement in pygame.event.get():
        if événement.type == pygame.QUIT:
            self.en_cours = False
        elif événement.type == pygame.KEYDOWN:
            if événement.key == pygame.K_RETURN:
                if self.nom_joueur != "":
                    enregistrer_score(self.nom_joueur, self.score)
                self.en_cours = False
            elif chr(événement.key) in TOUCHES_FRUITS:
                fruit_image = TOUCHES_FRUITS[chr(événement.key)]
                for fruit in self.fruits:
                    if fruit.image == fruit_image:
                        fruit.coupé = True
                        if fruit.image == image_rouge:
                            self.en_cours = False  # Fin du jeu si la bombe est touchée
                        elif fruit.image == image_vert:
                            self.score += 1  # Incrémente le score localement
                        elif fruit.image == image_bleu:
                            self.score += 2
                            self.pause_glaçon = True
                            self.temps_debut_glaçon = time.time()  # Démarre la pause
                        elif fruit.image == image_jaune:
                            self.score += 3
                            # Active le boost pendant 5 secondes
                            self.boost_actif = True
                            self.temps_debut_boost = time.time()
                            self.multiplieur_pommes = 10  # Multiplie les pommes par 10
                            self.bombes_activees = False  # Aucune bombe pendant le boost
                    fruits_a_supprimer = [fruit for fruit in self.fruits if getattr(fruit, 'coupé', False)]
                    for fruit in fruits_a_supprimer:
                        self.fruits.remove(fruit)


    
    def mettre_a_jour(self):
        if self.boost_actif and time.time() - self.temps_debut_boost > 5:
        # Désactive le boost après 5 secondes
           self.boost_actif = False
           self.multiplieur_pommes = 1  # Reviens à la normale
           self.bombes_activees = True  # Les bombes réapparaissent

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
                # Si un fruit sort du cadre et c'est une pomme, on perd une vie
                if fruit.image == image_vert:
                    self.vies -= 1
                    if self.vies <= 0:
                        self.en_cours = False  # La partie est terminée si les vies sont épuisées
                    fruits_a_supprimer.append(fruit)

            if not hasattr(fruit, 'coupé') and fruit.est_touché(pygame.mouse.get_pos()):
                fruit.coupé = True

                if fruit.image == image_rouge:
                    self.en_cours = False
                elif fruit.image == image_vert:
                    self.score += 1  # Incrémente le score localement
                elif fruit.image == image_bleu:
                    self.score += 2
                    self.pause_glaçon = True
                    self.temps_debut_glaçon = time.time()  # Démarre la pause
                elif fruit.image == image_jaune:
                    self.score += 3

                fruits_a_supprimer.append(fruit)

        for fruit in fruits_a_supprimer:
            self.fruits.remove(fruit)

        self.timer_ajout += 1
        if self.timer_ajout > 30:
            self.ajouter_fruit()
            self.timer_ajout = 0

        if not self.en_cours:
            self.afficher_fin_de_partie()

    def dessiner(self):
        # Afficher le fond à chaque mise à jour
        écran.blit(fond, (0, 0))  # Afficher l'image de fond

        self.lame.dessiner()

        for fruit in self.fruits:
            fruit.dessiner()

        # Affichage du score pendant la partie
        font = pygame.font.Font(None, 36)
        text_score = font.render(f"Score: {self.score}", True, (255, 255, 255))
        écran.blit(text_score, (HAUTEUR // 2 - text_score.get_width() // 2, 10))

        # Afficher les vies restantes
        text_vies = font.render(f'Vies: {self.vies}', True, (255, 255, 255))
        écran.blit(text_vies, (10, 10))

        pygame.display.flip()

    def afficher_fin_de_partie(self):    # Fenêtre de fin de partie avec score et option pour recommencer
           font = pygame.font.Font(None,58)
           text_score = font.render(f"Votre score : {self.score}", True, (1, 2, 1))
           text_recommencer = font.render("Appuyez sur 'R' pour recommencer ou 'Q' pour quitter", True, (255, 255, 255))

           écran.blit(fond, (0, 0))  # Afficher le fond
           écran.blit(text_score, (HAUTEUR // 2 - text_score.get_width() // 2, HAUTEUR // 2 - 50))

    # Décaler le message vers la droite
           decaler_droite = 200  # Ajuster cette valeur pour plus ou moins de décalage
           écran.blit(text_recommencer, (HAUTEUR // 2 - text_recommencer.get_width() // 2 + decaler_droite, HAUTEUR // 2 + 50))

           pygame.display.flip()

    # Attendre une action de l'utilisateur
           attendre_reponse = True
           while attendre_reponse:
               for événement in pygame.event.get():
                   if événement.type == pygame.QUIT:
                     pygame.quit()
                     exit()
                   elif événement.type == pygame.KEYDOWN:
                       if événement.key == pygame.K_r:  # Recommencer
                           self.__init__()  # Réinitialiser le jeu
                           attendre_reponse = False
                       elif événement.key == pygame.K_q:  # Quitter
                            pygame.quit()
                            exit()
 



#======================================
class Accueil:
    def __init__(self):
        self.nom_joueur = ""  # Attribut d'instance

    def accueil(self):
        global nom_joueur
        écran.blit(fond, (0, 0))  # Afficher l'image de fond à l'écran d'accueil

        font = pygame.font.Font(None, 58)
        texte_accueil = font.render("Bienvenue dans Fruit Ninja !", True, (255, 255, 255))
        écran.blit(texte_accueil, (LARGEUR // 2 - texte_accueil.get_width() // 2, 100))

        joueurs = afficher_joueurs()
        y_offset = 500
        for joueur in joueurs:
            texte_joueur = font.render(joueur.strip(), True, (0, 0, 0))
            écran.blit(texte_joueur, (LARGEUR // 2 - texte_joueur.get_width() // 2, y_offset))
            y_offset += 50

        # Afficher "Nom du joueur" avant la saisie du nom
        texte_nom_prompt = font.render("Nom du joueur : ", True, (0, 5, 5))
        écran.blit(texte_nom_prompt, (LARGEUR // 2 - texte_nom_prompt.get_width() // 2,200))

        pygame.display.flip()

        nom_joueur = ""
        active = True

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if nom_joueur != "":
                            self.nom_joueur = nom_joueur  # Enregistrer le nom du joueur dans l'attribut de l'instance
                            enregistrer_score(self.nom_joueur, score)
                            active = False  # Arrêter la boucle sans fermer la fenêtre
                    elif event.key == pygame.K_BACKSPACE:
                        nom_joueur = nom_joueur[:-1]
                    else:
                        nom_joueur += event.unicode

                    # Redessiner l'écran à chaque modification
                    écran.blit(fond, (0, 0))  # Redessiner l'image de fond
                    texte_accueil = font.render("Bienvenue dans Fruit Ninja !", True, (255, 255, 255))
                    écran.blit(texte_accueil, (LARGEUR // 2 - texte_accueil.get_width() // 2, 100))

                    # Afficher les joueurs
                    y_offset = 400
                    for joueur in joueurs:
                        texte_joueur = font.render(joueur.strip(), True, (0, 5, 5))
                        écran.blit(texte_joueur, (LARGEUR // 2 - texte_joueur.get_width() // 2, y_offset))
                        y_offset += 50

                    # Afficher le nom du joueur en train d'être saisi
                    texte_nom = font.render(nom_joueur, True, (5, 5, 5))
                    écran.blit(texte_nom, (LARGEUR // 2 - texte_nom.get_width() // 2, 150))  # Position du texte

                    pygame.display.flip()


# Avant la boucle principale
accueil = Accueil()
accueil.accueil()  # Afficher l'écran d'accueil avant de commencer le jeu

# Après l'écran d'accueil, commencer le jeu
jeu = JeuFruitNinja()

while jeu.en_cours:
    jeu.gérer_événements()
    jeu.mettre_a_jour()
    jeu.dessiner()

    horloge.tick(FPS)

pygame.quit()
