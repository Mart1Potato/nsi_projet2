from matplotlib.pylab import indices

from functions import *
liste_mots = ["python", "programmation", "ordinateur", "clavier", "algorithme",
              "variable", "fonction", "boucle", "liste", "chaine"]

NB_ESSAIS = 10
mot = choix_mot(liste_mots) 
mot_cache = cacher_mot(mot) 
essais_restants = NB_ESSAIS 
lettres_proposees = [] 
long_mot = len(mot)

print("=== JEU DU PENDU ===") 
print(f"Le mot à deviner contient {long_mot} lettres.") 
print() 

while essais_restants > 0 and "*" in mot_cache:
  print("Mot:","".join(mot_cache))
  print(f"Essais restants : {essais_restants}")
  print(f"Lettres déjà proposées : {','.join(lettres_proposees) if lettres_proposees else 'aucune'}")
  print()

  lettre = saisir_lettre()
  if lettre in lettres_proposees:
    print("Vous avez déjà proposé la lettre") 
    continue
  lettres_proposees.append(lettre)
  indices = chercher_lettre(lettre,mot)
  print(type(indices))

  if len(indices)==0:
    essais_restants -= 1
    print("La lettre n'est pas dans le mot.")
  else:
    mot_cache= remplacer_lettre(mot_cache, indices, lettre)
    print("Bravo ! La lettre est dans le mot")
