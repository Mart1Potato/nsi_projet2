from functions.py import *
liste_mots = ["python", "programmation", "ordinateur", "clavier", "algorithme",
              "variable", "fonction", "boucle", "liste", "chaine"]
 
NB_ESSAIS = 10
mot = choix_mot(liste_mots) 
mot_cache = cacher_mot(mot) 
essais_restants = NB_ESSAIS 
lettres_proposees = [] 

print("=== JEU DU PENDU ===") 
print("Le mot à deviner contient {len(mot)} lettres.") 
print() 

while essais_restants > 0 and "*" in mot_cache:
  print("Mot:","".join(mot_cache))
  print("Essais restants : {essais_restants}")
  print("Lettres déjà proposées : {','.join(lettres_proposees) if lettres_proposees else 'aucune'}")
  print()

lettre = saisir_lettre()
if lettre in lettres proposees:
  print("Vous avze déjà proposé la lettre") 
  continue

lettres_proposees.append(lettre)
indices = chercher_lettre(lettre,mot)

if len(indices)==0:
  essais_restants=1
  print("La lettre n'est pas dans le mot.")
else:
  mot_cache=remplacer_lettre(mot_cache,lettre)
  print("Bravo ! La lettre est dans le mot)

  
