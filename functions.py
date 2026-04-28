def saisir_lettre():
    lettre = str(input("Quelle lettre voulez-vous proposer?"))
    return lettre

def choix_mot(list):
    '''Cette fonction choisit un mot au hasard dans une liste de mots'''
    import random
    mot = random.choice(list)
    return mot

def cacher_mot(mot):
    '''Cette fonction cache le mot choisi en remplaçant chaque lettre par un astérisque'''
    mot_cache = []
    for car in mot:
        mot_cache.append("*")
    return mot_cache
