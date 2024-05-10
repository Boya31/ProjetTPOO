import random

class Case:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Case({self.x}, {self.y})"

    def adjacentes(self, jeu):
        adj = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    nx, ny = self.x + dx, self.y + dy
                    if 0 <= nx < jeu.taille_x and 0 <= ny < jeu.taille_y:
                        adj.append(jeu.listeDesCases[nx][ny])
        return adj

class Creature:
    def __init__(self, nom, position):
        self.nom = nom
        self.position = position

    def __str__(self):
        return f"Creature({self.nom}, {self.position})"

    def choisirCible(self, jeu):
        cases_adjacentes = self.position.adjacentes(jeu)
        cases_occupees = [case for case in cases_adjacentes if jeu.estOccupee(case)]
        if cases_occupees:
            return random.choice(cases_occupees)
        else:
            return random.choice(cases_adjacentes)

class Jeu:
    def __init__(self, taille_x, taille_y, nombre_creatures):
        self.taille_x = taille_x
        self.taille_y = taille_y
        self.listeDesCases = [[Case(i, j) for j in range(taille_y)] for i in range(taille_x)]
        self.listeDesCreatures = []
        while len(self.listeDesCreatures) < nombre_creatures:
            random_case = random.choice(random.choice(self.listeDesCases))
            if not any(creature.position == random_case for creature in self.listeDesCreatures):
                self.listeDesCreatures.append(Creature(f"Créature {len(self.listeDesCreatures) + 1}", random_case))
        self.actif = self.listeDesCreatures[0]

    def estOccupee(self, case):
        return any(creature.position == case for creature in self.listeDesCreatures)

    def deplacer(self, creature, case):
        if case in creature.position.adjacentes(self) and not self.estOccupee(case):
            creature.position = case
            print(f"{creature.nom} s'est déplacé à {case}.")
            self.actif = self.listeDesCreatures[(self.listeDesCreatures.index(creature) + 1) % len(self.listeDesCreatures)]
        elif self.estOccupee(case):
            print(f"{creature.nom} a capturé la case occupée par {self.actif.nom} et a gagné la partie!")
            self.actif = None  # Terminer le jeu
        else:
            print("Déplacement non autorisé !")

def simuler_jeu():
    jeu = Jeu(5, 5, 2)
    print("Position initiale de la créature 1:", jeu.listeDesCreatures[0].position)
    print("Position initiale de la créature 2:", jeu.listeDesCreatures[1].position)
    print("Créature active:", jeu.actif)

    while jeu.actif:
        for creature in jeu.listeDesCreatures:
            if jeu.actif:
                cible = creature.choisirCible(jeu)
                print(f"{creature.nom} choisit la cible à la position: {cible}")
                jeu.deplacer(creature, cible)
                if not jeu.actif:  # Vérifier si le jeu doit s'arrêter
                    break

simuler_jeu()
