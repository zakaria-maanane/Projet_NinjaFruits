import pygame
import random
import sys  

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
LARGEUR, HAUTEUR = 800, 600
écran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Fruit Ninja") # 

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
VERT = (0, 255, 0)
BLEU = (0, 0, 255)

# Police
defaut_police = pygame.font.Font(None, 36)

# Variables globales
horloge = pygame.time.Clock()
FPS = 60
score = 0

# Classe Fruit
class Fruit:
    def __init__(self):
        self.rayon = random.randint(20, 40)
        self.x = random.randint(self.rayon, LARGEUR - self.rayon) #self sert a 
        self.y = HAUTEUR + self.rayon
        self.couleur = random.choice([ROUGE, VERT, BLEU])
        self.vitesse = random.uniform(3, 6)
        self.coupé = False

    def bouger(self):
        self.y -= self.vitesse

    def dessiner(self):
        if not self.coupé:
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

# Classe principale du jeu
class JeuFruitNinja:
    def __init__(self):
        self.fruits = []
        self.lame = Lame()
        self.en_cours = True
        self.timer_ajout = 0

    def ajouter_fruit(self):
        self.fruits.append(Fruit())

    def gérer_événements(self):
        for événement in pygame.event.get():
            if événement.type == pygame.QUIT:
                self.en_cours = False

    def mettre_à_jour(self): 
        global score
        self.lame.mettre_à_jour(pygame.mouse.get_pos())

        for fruit in self.fruits:
            fruit.bouger()
            if fruit.y < -fruit.rayon:
                self.fruits.remove(fruit)

            if not fruit.coupé and fruit.est_touché(pygame.mouse.get_pos()):
                                                 # Vérifie si le fruit n'est pas encore coupé (not fruit.coupé) 
                                                 # et si le curseur est en contact avec le fruit (fruit.est_touché()).
                fruit.coupé = True
                score += 1
                self.fruits.remove(fruit)

        self.timer_ajout += 1
        if self.timer_ajout > 30:  # Ajouter un fruit toutes les 30 frames
            self.ajouter_fruit()
            self.timer_ajout = 0

    def dessiner(self):
        écran.fill(NOIR)
        self.lame.dessiner()

        for fruit in self.fruits:
            fruit.dessiner()

        texte_score = defaut_police.render(f"Score : {score}", True, BLANC)
        écran.blit(texte_score, (10, 10))

        pygame.display.flip()

    def exécuter(self):
        while self.en_cours:
            self.gérer_événements()
            self.mettre_à_jour()
            self.dessiner()
            horloge.tick(FPS)

# Lancer le jeu
if __name__ == "__main__":
    jeu = JeuFruitNinja()
    jeu.exécuter()
    pygame.quit()
    sys.exit()