def saisir_lettre():
    lettre = str(input("Quelle lettre voulez-vous proposer?"))
    return lettre

def chercher_lettre(lettre,mot):
    ''' la fonction chercher_lettre prend en paramètre la lettre
    choisie par l'utilisateur précédemment et le mot concerné dans le jeu
    Elle renvoie un tuple contenant les indices des occurences de la lettre
    dans le mot
    '''
    assert type(mot) == str, "le mot n'est pas une chaine de caractère"
    assert type(lettre) == str, "la lettre n'est pas un str"
    liste_indices=[] #création une liste pour pouvoir la modifier
    for indice in range(len(mot)):
        if mot[indice] == lettre:
            liste_indices.append(indice)
    return tuple(liste_indices) #renvoi du tuple

def remplacer_lettre(mot_cache, tuple_indices, lettre):
    ''' la fonction remplacer_lettre prend en paramètre un mot de type list
    composé de *, la lettre choisie précedemment, ainsi que les indices des
    occurences de cette lettre. Elle renvoie le mot, sous forme de (str/de
     liste on verra) mais en ayant remplacé les astérisques par la lettre à
     sa place dans le mot original.
    '''
    assert type(tuples_indices) == tuple, "tuples_indices n'est pas une chaine de caractères"
    assert type(mot_cache) == list, "mot_cache n'est pas une liste"
    for indice in tuple_indices:
        mot_cache[indice] = lettre
    return mot_cache


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
