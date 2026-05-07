# Documentation complète — Jeu du Pendu (Tkinter)

> Ce document explique **intégralement** le code du projet : chaque fichier, chaque variable, chaque fonction, chaque widget et chaque concept utilisé.

---

## Table des matières

1. [Vue d'ensemble du projet](#1-vue-densemble-du-projet)
2. [functions.py — Les fonctions de base](#2-functionspy--les-fonctions-de-base)
3. [main.py — Structure générale](#3-mainpy--structure-générale)
4. [Les imports](#4-les-imports)
5. [Les constantes globales](#5-les-constantes-globales)
6. [ETAPES_DESSIN — Le cœur du dessin](#6-etapes_dessin--le-cœur-du-dessin)
7. [La classe PenduApp](#7-la-classe-penduapp)
8. [__init__ — Le constructeur](#8-__init__--le-constructeur)
9. [_build_ui — Construction de l'interface](#9-_build_ui--construction-de-linterface)
10. [_dessiner_etape — Le dessin progressif](#10-_dessiner_etape--le-dessin-progressif)
11. [_nouvelle_partie — Initialisation du jeu](#11-_nouvelle_partie--initialisation-du-jeu)
12. [_proposer — Traitement d'une lettre](#12-_proposer--traitement-dune-lettre)
13. [_actualiser_affichage — Mise à jour visuelle](#13-_actualiser_affichage--mise-à-jour-visuelle)
14. [_verifier_fin — Fin de partie](#14-_verifier_fin--fin-de-partie)
15. [Lancement du programme](#15-lancement-du-programme)
16. [Tableau récapitulatif de toutes les variables](#16-tableau-récapitulatif-de-toutes-les-variables)
17. [Tableau récapitulatif de toutes les méthodes](#17-tableau-récapitulatif-de-toutes-les-méthodes)
18. [Schéma de l'interface](#18-schéma-de-linterface)
19. [Déroulement d'une partie pas à pas](#19-déroulement-dune-partie-pas-à-pas)

---

## 1. Vue d'ensemble du projet

Le projet est composé de deux fichiers Python :

| Fichier | Rôle |
|---|---|
| `functions.py` | Contient les fonctions "métier" du jeu (choisir un mot, le cacher, chercher une lettre, la révéler) |
| `main.py` | Contient l'interface graphique Tkinter et la logique qui relie tout |

Le principe de séparation est important : `functions.py` ne sait rien de Tkinter, et `main.py` appelle les fonctions de `functions.py` pour effectuer les opérations sur les mots.

---

## 2. functions.py — Les fonctions de base

### `choix_mot(list)`

```python
def choix_mot(list):
    import random
    mot = random.choice(list)
    return mot
```

**Paramètre :** `list` — une liste de chaînes de caractères (les mots du jeu).  
**Retourne :** un mot choisi **aléatoirement** dans la liste grâce à `random.choice()`.  
**Utilisée dans :** `_nouvelle_partie()` de `main.py`.

---

### `cacher_mot(mot)`

```python
def cacher_mot(mot):
    mot_cache = []
    for car in mot:
        mot_cache.append("*")
    return mot_cache
```

**Paramètre :** `mot` — la chaîne de caractères à cacher.  
**Retourne :** une **liste** de `*`, une étoile par lettre du mot.  
**Exemple :** `cacher_mot("python")` → `['*', '*', '*', '*', '*', '*']`  
**Pourquoi une liste et pas une chaîne ?** Parce qu'une liste est **modifiable** (on peut changer un élément à un indice précis), contrairement à une chaîne Python qui est immuable.

---

### `chercher_lettre(lettre, mot)`

```python
def chercher_lettre(lettre, mot):
    assert type(mot) == str
    assert type(lettre) == str
    liste_indices = []
    for indice in range(len(mot)):
        if mot[indice] == lettre:
            liste_indices.append(indice)
    return tuple(liste_indices)
```

**Paramètres :**
- `lettre` — la lettre proposée par le joueur (str)
- `mot` — le mot à deviner (str)

**Retourne :** un **tuple** contenant les indices (positions) où la lettre apparaît dans le mot.  
**Exemple :** `chercher_lettre("o", "boucle")` → `(1,)` (la lettre "o" est en position 1).  
**Exemple :** `chercher_lettre("z", "python")` → `()` (tuple vide = lettre absente).  
Les `assert` vérifient que les types sont corrects et lèvent une erreur si ce n'est pas le cas.

---

### `remplacer_lettre(mot_cache, tuple_indices, lettre)`

```python
def remplacer_lettre(mot_cache, tuple_indices, lettre):
    assert type(tuple_indices) == tuple
    assert type(mot_cache) == list
    for indice in tuple_indices:
        mot_cache[indice] = lettre
    return mot_cache
```

**Paramètres :**
- `mot_cache` — la liste de `*` en cours de révélation
- `tuple_indices` — les positions où placer la lettre
- `lettre` — la lettre à insérer

**Retourne :** la liste `mot_cache` **modifiée** avec la lettre révélée à ses positions.  
**Exemple :** `remplacer_lettre(['*','*','*'], (0, 2), 'p')` → `['p', '*', 'p']`

---

## 3. main.py — Structure générale

Le fichier `main.py` est organisé en **trois grandes parties** :

```
main.py
├── Imports
├── Constantes globales (couleurs, config, dessin)
└── Classe PenduApp (hérite de tk.Tk)
    ├── __init__          → initialise la fenêtre
    ├── _build_ui         → construit tous les widgets
    ├── _dessiner_etape   → dessine une étape du bonhomme
    ├── _nouvelle_partie  → remet le jeu à zéro
    ├── _proposer         → traite la lettre saisie
    ├── _actualiser_affichage → met à jour l'écran
    └── _verifier_fin     → détecte victoire ou défaite
```

---

## 4. Les imports

```python
import tkinter as tk
from tkinter import font as tkfont
from functions import choix_mot, cacher_mot, chercher_lettre, remplacer_lettre
```

| Import | Explication |
|---|---|
| `import tkinter as tk` | Importe toute la bibliothèque graphique Tkinter sous l'alias `tk`. On écrit `tk.Label`, `tk.Button`, etc. |
| `from tkinter import font as tkfont` | Importe le sous-module `font` de Tkinter pour créer des polices personnalisées (taille, graisse...) |
| `from functions import ...` | Importe uniquement les 4 fonctions nécessaires depuis `functions.py`. On n'importe pas `saisir_lettre` car la saisie se fait via l'interface graphique. |

---

## 5. Les constantes globales

Les constantes sont des variables écrites en **MAJUSCULES** par convention Python. Elles ne changent jamais pendant l'exécution.

### Configuration du jeu

```python
LISTE_MOTS = ["python", "programmation", "ordinateur", ...]
NB_ESSAIS  = 10
```

| Variable | Type | Valeur | Rôle |
|---|---|---|---|
| `LISTE_MOTS` | `list` | 10 mots | Réservoir de mots dans lequel `choix_mot()` pioche |
| `NB_ESSAIS` | `int` | `10` | Nombre d'essais autorisés, **égal au nombre d'étapes du dessin** (4 potence + 6 bonhomme) |

`NB_ESSAIS = 10` n'est pas un choix arbitraire : il correspond **exactement** au nombre d'éléments dans `ETAPES_DESSIN`. Ainsi, quand tous les essais sont épuisés, le dessin est complet.

### Palette de couleurs

Toutes les couleurs sont des codes **hexadécimaux** (format `#RRGGBB`).

```python
BG       = "#0f0f1a"
SURFACE  = "#1a1a2e"
BORDER   = "#2a2a4a"
ACCENT   = "#e94560"
ACCENT2  = "#0f3460"
TEXT     = "#eaeaea"
TEXT_DIM = "#6c6c8a"
SUCCESS  = "#4ecca3"
WARNING  = "#f5a623"
```

| Constante | Couleur | Utilisée pour |
|---|---|---|
| `BG` | Noir bleuté | Fond de toute la fenêtre |
| `SURFACE` | Bleu nuit | Fond du canvas, du cadre essais, du champ de saisie |
| `BORDER` | Bleu-gris | Bordure du cadre essais et du canvas |
| `ACCENT` | Rouge/rose | Titre, bouton Valider, messages d'erreur, bonhomme |
| `ACCENT2` | Bleu foncé | Bouton Nouvelle Partie |
| `TEXT` | Blanc cassé | Mot caché, texte du bouton Nouvelle Partie |
| `TEXT_DIM` | Gris violet | Sous-titre, lettres proposées, potence |
| `SUCCESS` | Vert menthe | Messages de bonne lettre, message de victoire |
| `WARNING` | Orange | Compteur d'essais, messages d'avertissement |

---

## 6. ETAPES_DESSIN — Le cœur du dessin

```python
ETAPES_DESSIN = [
    ("socle",   lambda c: c.create_line(20, 190, 140, 190, fill="#6c6c8a", width=4)),
    ("poteau",  lambda c: c.create_line(60, 190, 60,  20,  fill="#6c6c8a", width=4)),
    ("poutre",  lambda c: c.create_line(60, 20,  150, 20,  fill="#6c6c8a", width=4)),
    ("corde",   lambda c: c.create_line(150, 20, 150, 50,  fill="#6c6c8a", width=3)),
    ("tête",    lambda c: c.create_oval(130, 50, 170, 90,  outline="#e94560", width=3)),
    ("corps",   lambda c: c.create_line(150, 90, 150, 145, fill="#e94560", width=3)),
    ("bras_g",  lambda c: c.create_line(150,105, 120, 130, fill="#e94560", width=3)),
    ("bras_d",  lambda c: c.create_line(150,105, 180, 130, fill="#e94560", width=3)),
    ("jambe_g", lambda c: c.create_line(150,145, 125, 175, fill="#e94560", width=3)),
    ("jambe_d", lambda c: c.create_line(150,145, 175, 175, fill="#e94560", width=3)),
]
```

C'est une **liste de tuples**. Chaque tuple contient :
1. Un **nom** (str) — identifiant lisible pour savoir ce que l'étape dessine
2. Une **fonction lambda** — la fonction de dessin à exécuter

### Pourquoi des lambdas ?

Une **lambda** est une fonction anonyme écrite sur une seule ligne. Ici, chaque lambda attend un paramètre `c` (le canvas) et appelle une méthode de dessin dessus.

```python
lambda c: c.create_line(...)
```

On utilise des lambdas pour **ne pas exécuter le dessin immédiatement** lors de la définition de la liste. Les fonctions sont stockées et appelées plus tard une par une, à chaque erreur du joueur.

### Les méthodes de dessin du Canvas

| Méthode | Paramètres | Résultat |
|---|---|---|
| `c.create_line(x1, y1, x2, y2, fill, width)` | Coordonnées des deux extrémités, couleur, épaisseur | Trace un segment de droite |
| `c.create_oval(x1, y1, x2, y2, outline, width)` | Coordonnées du rectangle englobant, couleur du contour, épaisseur | Trace un cercle (ou une ellipse) |

Le système de coordonnées du canvas : `(0, 0)` est le **coin supérieur gauche**. `x` va vers la droite, `y` va vers le bas. Le canvas fait 220×200 pixels.

### Les 10 étapes en détail

| Index | Nom | Type | Coordonnées | Partie du dessin |
|---|---|---|---|---|
| 0 | socle | ligne | (20,190)→(140,190) | Base horizontale de la potence |
| 1 | poteau | ligne | (60,190)→(60,20) | Poteau vertical |
| 2 | poutre | ligne | (60,20)→(150,20) | Bras horizontal |
| 3 | corde | ligne | (150,20)→(150,50) | Corde qui pend |
| 4 | tête | ovale | rect(130,50,170,90) | Tête du bonhomme |
| 5 | corps | ligne | (150,90)→(150,145) | Tronc |
| 6 | bras_g | ligne | (150,105)→(120,130) | Bras gauche |
| 7 | bras_d | ligne | (150,105)→(180,130) | Bras droit |
| 8 | jambe_g | ligne | (150,145)→(125,175) | Jambe gauche |
| 9 | jambe_d | ligne | (150,145)→(175,175) | Jambe droite |

---

## 7. La classe PenduApp

```python
class PenduApp(tk.Tk):
```

`PenduApp` **hérite** de `tk.Tk`. Cela signifie que `PenduApp` **est** la fenêtre principale de l'application. On n'a pas besoin de créer une fenêtre séparément : instancier `PenduApp()` crée directement la fenêtre et y ajoute tous les widgets.

L'héritage (`tk.Tk`) donne accès à toutes les méthodes de la fenêtre : `title()`, `configure()`, `resizable()`, `mainloop()`, etc.

---

## 8. `__init__` — Le constructeur

```python
def __init__(self):
    super().__init__()
    self.title("Le Pendu")
    self.resizable(False, False)
    self.configure(bg=BG)

    self.f_title  = tkfont.Font(family="Courier", size=20, weight="bold")
    self.f_word   = tkfont.Font(family="Courier", size=26, weight="bold")
    self.f_label  = tkfont.Font(family="Courier", size=10)
    self.f_btn    = tkfont.Font(family="Courier", size=10, weight="bold")
    self.f_small  = tkfont.Font(family="Courier", size=9)
    self.f_essais = tkfont.Font(family="Courier", size=13, weight="bold")

    self._build_ui()
    self._nouvelle_partie()
```

`__init__` est appelé automatiquement à la création de l'objet (`app = PenduApp()`).

### `super().__init__()`
Appelle le constructeur de `tk.Tk` pour initialiser correctement la fenêtre parente avant d'y ajouter nos éléments.

### Méthodes de configuration de la fenêtre

| Appel | Effet |
|---|---|
| `self.title("Le Pendu")` | Texte affiché dans la barre de titre du système d'exploitation |
| `self.resizable(False, False)` | Interdit le redimensionnement (largeur=False, hauteur=False) |
| `self.configure(bg=BG)` | Applique la couleur de fond à la fenêtre entière |

### Les polices (`tkfont.Font`)

Chaque police est un objet `tkfont.Font` stocké dans un attribut `self.f_*`.

| Attribut | Taille | Graisse | Utilisée pour |
|---|---|---|---|
| `self.f_title` | 20 | bold | Titre "◈ LE PENDU ◈" |
| `self.f_word` | 26 | bold | Mot caché et champ de saisie |
| `self.f_label` | 10 | normal | Messages d'état |
| `self.f_btn` | 10 | bold | Texte des boutons |
| `self.f_small` | 9 | normal | Sous-titre, lettres proposées, barre d'essais |
| `self.f_essais` | 13 | bold | Compteur "X / 10" dans le cadre |

---

## 9. `_build_ui` — Construction de l'interface

Cette méthode crée **tous les widgets** (éléments graphiques) et les organise en deux colonnes. Elle est appelée une seule fois dans `__init__`.

### Structure en deux colonnes

```
root_frame (tk.Frame)
├── col_gauche (tk.Frame) — colonne 0
│   ├── cadre_essais (tk.Frame avec bordure)
│   │   ├── Label "ESSAIS RESTANTS"
│   │   ├── Label ← var_essais_nb  ("10 / 10")
│   │   └── Label ← var_barre      ("██████████")
│   ├── Label "◈ LE PENDU ◈"
│   ├── Label "devinez le mot..."
│   ├── Label ← var_mot            ("p  *  *  h  o  n")
│   ├── Label ← var_msg
│   ├── frame_saisie (tk.Frame)
│   │   ├── Entry  ← self.entry
│   │   └── Button "VALIDER"
│   └── Label ← var_lettres
└── col_droite (tk.Frame) — colonne 1
    ├── Canvas ← self.canvas
    └── Button "↺ NOUVELLE PARTIE"
```

### Les widgets Tkinter utilisés

| Widget | Rôle |
|---|---|
| `tk.Frame` | Conteneur invisible qui regroupe d'autres widgets. Permet d'organiser la mise en page. |
| `tk.Label` | Affiche du texte (statique ou lié à une `StringVar`) |
| `tk.Entry` | Champ de saisie texte où l'utilisateur tape la lettre |
| `tk.Button` | Bouton cliquable qui déclenche une fonction (`command=`) |
| `tk.Canvas` | Surface de dessin sur laquelle on trace des formes géométriques |

### Les gestionnaires de mise en page

Deux gestionnaires sont utilisés :

**`pack()`** — place les widgets les uns après les autres (verticalement par défaut).  
Paramètres importants :
- `pady=(haut, bas)` — espace vertical autour du widget
- `padx=(gauche, droite)` — espace horizontal
- `anchor="w"` — aligne à gauche ("w" = west), `"center"` = centré
- `side="left"` — place côte à côte horizontalement
- `ipady` — espace interne vertical (agrandit le widget)

**`grid()`** — place les widgets dans une grille (lignes/colonnes).  
Paramètres importants :
- `row=0, column=0` — position dans la grille
- `sticky="nsew"` — le widget s'étire pour remplir sa cellule (north, south, east, west)

Les deux ne peuvent pas être mélangés dans le même conteneur. Ici, `pack()` est utilisé dans les colonnes, et `grid()` pour placer les deux colonnes l'une à côté de l'autre.

### Les `StringVar`

Une `StringVar` est une **variable observable** de Tkinter. Quand sa valeur change (via `.set()`), tous les `Label` qui y sont liés (`textvariable=`) se mettent à jour **automatiquement**, sans avoir à modifier le widget manuellement.

| StringVar | Label associé | Contenu |
|---|---|---|
| `self.var_essais_nb` | Cadre essais | `"10 / 10"` |
| `self.var_barre` | Cadre essais | `"██████████"` |
| `self.var_mot` | Colonne gauche | `"p  *  *  h  o  n"` |
| `self.var_msg` | Colonne gauche | Messages d'état |
| `self.var_lettres` | Colonne gauche | `"Proposées : A  B  C"` |

### Le cadre "Essais restants"

```python
cadre_essais = tk.Frame(col_gauche, bg=SURFACE,
                        highlightbackground=BORDER,
                        highlightthickness=1)
```

`highlightbackground` + `highlightthickness=1` simulent une **bordure colorée** autour du Frame (Tkinter n'a pas d'option `border` directe sur les frames).

### L'Entry et le binding clavier

```python
self.entry = tk.Entry(frame_saisie, width=3, ...)
self.entry.bind("<Return>", lambda e: self._proposer())
```

`.bind("<Return>", ...)` attache un **écouteur d'événement** : quand l'utilisateur appuie sur la touche Entrée dans le champ, la fonction `_proposer()` est appelée. La lambda reçoit un objet événement `e` (qu'on n'utilise pas ici).

### Le bouton et la commande

```python
tk.Button(..., command=self._proposer)
```

`command=` reçoit une **référence à une fonction** (sans les parenthèses). Tkinter appellera cette fonction automatiquement au clic. On ne met pas `self._proposer()` (avec parenthèses) car cela l'appellerait immédiatement lors de la création.

---

## 10. `_dessiner_etape` — Le dessin progressif

```python
def _dessiner_etape(self, numero_etape):
    if 0 <= numero_etape < len(ETAPES_DESSIN):
        _nom, fn = ETAPES_DESSIN[numero_etape]
        fn(self.canvas)
```

### Paramètre
- `numero_etape` (int) — index de 0 à 9, indique quelle étape dessiner

### Fonctionnement
1. On vérifie que l'index est valide (entre 0 et 9 inclus)
2. On **décompacte** le tuple de `ETAPES_DESSIN[numero_etape]` : `_nom` reçoit le nom (inutilisé, d'où le `_`), `fn` reçoit la lambda
3. On **appelle** la lambda en lui passant `self.canvas` : `fn(self.canvas)` → exécute `canvas.create_line(...)` ou `canvas.create_oval(...)`

Chaque appel **ajoute** un élément sur le canvas sans effacer ce qui existe déjà. C'est ainsi que le dessin se construit progressivement.

---

## 11. `_nouvelle_partie` — Initialisation du jeu

```python
def _nouvelle_partie(self):
    self.mot              = choix_mot(LISTE_MOTS)
    self.mot_cache        = cacher_mot(self.mot)
    self.essais_restants  = NB_ESSAIS
    self.lettres_proposees = []
    self.partie_finie     = False

    self.canvas.delete("all")
    self._actualiser_affichage()
    self.var_msg.set("")
    self.entry.configure(state="normal")
    self.entry.delete(0, "end")
    self.entry.focus()
```

### Variables d'instance initialisées

| Attribut | Type | Valeur initiale | Rôle |
|---|---|---|---|
| `self.mot` | `str` | mot aléatoire | Le mot à deviner |
| `self.mot_cache` | `list` | `['*', '*', ...]` | Le mot en cours de révélation |
| `self.essais_restants` | `int` | `10` | Nombre d'essais restants |
| `self.lettres_proposees` | `list` | `[]` | Historique des lettres déjà tentées |
| `self.partie_finie` | `bool` | `False` | Vrai quand la partie est terminée (victoire ou défaite) |

### `self.canvas.delete("all")`
Efface **tout** ce qui a été dessiné sur le canvas. Le mot-clé `"all"` est une balise spéciale Tkinter qui cible tous les éléments du canvas.

### `self.entry.configure(state="normal")`
Réactive le champ de saisie (qui avait été désactivé en fin de partie).

### `self.entry.delete(0, "end")`
Vide le contenu du champ de saisie. `0` = premier caractère, `"end"` = jusqu'à la fin.

### `self.entry.focus()`
Place le curseur dans le champ de saisie automatiquement, pour que l'utilisateur puisse taper directement sans cliquer.

---

## 12. `_proposer` — Traitement d'une lettre

```python
def _proposer(self):
    if self.partie_finie:
        return

    lettre = self.entry.get().strip().lower()
    self.entry.delete(0, "end")

    if len(lettre) != 1 or not lettre.isalpha():
        ...
        return

    if lettre in self.lettres_proposees:
        ...
        return

    self.lettres_proposees.append(lettre)
    indices = chercher_lettre(lettre, self.mot)

    if len(indices) == 0:
        self.essais_restants -= 1
        numero_etape = NB_ESSAIS - self.essais_restants - 1
        self._dessiner_etape(numero_etape)
        ...
    else:
        self.mot_cache = remplacer_lettre(self.mot_cache, indices, lettre)
        ...

    self._actualiser_affichage()
    self._verifier_fin()
```

### Récupération de la saisie

```python
lettre = self.entry.get().strip().lower()
```

| Méthode | Effet |
|---|---|
| `.get()` | Lit le contenu du champ `Entry` et retourne une chaîne |
| `.strip()` | Supprime les espaces au début et à la fin |
| `.lower()` | Convertit en minuscules pour uniformiser (le mot est en minuscules) |

### Validations

**Validation 1 :** la saisie doit être exactement une lettre alphabétique.
```python
if len(lettre) != 1 or not lettre.isalpha():
```
- `len(lettre) != 1` : rejette les chaînes vides ou de plusieurs caractères
- `not lettre.isalpha()` : rejette les chiffres et caractères spéciaux

**Validation 2 :** la lettre ne doit pas déjà avoir été proposée.
```python
if lettre in self.lettres_proposees:
```
L'opérateur `in` vérifie si l'élément est présent dans la liste.

### Calcul du numéro d'étape

```python
numero_etape = NB_ESSAIS - self.essais_restants - 1
```

**Exemple :** si on vient de perdre le 1er essai :
- `self.essais_restants` passe de 10 à 9
- `numero_etape = 10 - 9 - 1 = 0` → on dessine l'étape 0 (le socle)

**Exemple :** si on vient de perdre le 5e essai :
- `self.essais_restants = 5`
- `numero_etape = 10 - 5 - 1 = 4` → on dessine l'étape 4 (la tête)

---

## 13. `_actualiser_affichage` — Mise à jour visuelle

```python
def _actualiser_affichage(self):
    self.var_mot.set("  ".join(self.mot_cache))

    self.var_essais_nb.set(f"{self.essais_restants} / {NB_ESSAIS}")

    barres = "█" * self.essais_restants + "░" * (NB_ESSAIS - self.essais_restants)
    self.var_barre.set(barres)

    if self.lettres_proposees:
        self.var_lettres.set("Proposées : " + "  ".join(self.lettres_proposees).upper())
    else:
        self.var_lettres.set("Aucune lettre proposée")
```

### `"  ".join(self.mot_cache)`

`join()` est une méthode de `str` qui assemble les éléments d'une liste en une seule chaîne, séparés par la chaîne sur laquelle on l'appelle.

**Exemple :** `"  ".join(['p', '*', '*', 'h', 'o', 'n'])` → `"p  *  *  h  o  n"`

Les deux espaces entre chaque caractère améliorent la lisibilité du mot.

### La barre de vie

```python
barres = "█" * self.essais_restants + "░" * (NB_ESSAIS - self.essais_restants)
```

En Python, `"█" * n` répète le caractère `n` fois.

**Exemple :** avec 7 essais restants sur 10 :
- `"█" * 7` → `"███████"`
- `"░" * 3` → `"░░░"`
- Résultat : `"███████░░░"`

### `.upper()`

Convertit toutes les lettres en majuscules pour un meilleur affichage dans la liste des lettres proposées.

---

## 14. `_verifier_fin` — Fin de partie

```python
def _verifier_fin(self):
    if "*" not in self.mot_cache:
        # Victoire
        self.partie_finie = True
        self.entry.configure(state="disabled")

    elif self.essais_restants == 0:
        # Défaite
        self.partie_finie = True
        self.entry.configure(state="disabled")
        self.var_mot.set("  ".join(list(self.mot)))
```

### Condition de victoire

```python
if "*" not in self.mot_cache:
```

S'il ne reste aucun `*` dans la liste `mot_cache`, c'est que toutes les lettres ont été trouvées.

### Condition de défaite

```python
elif self.essais_restants == 0:
```

Plus aucun essai restant = le dessin est entièrement complété = défaite.

### `self.entry.configure(state="disabled")`

Désactive le champ de saisie visuellement et fonctionnellement. L'utilisateur ne peut plus taper de lettre.

### `"  ".join(list(self.mot))`

En cas de défaite, on révèle le mot complet. `list(self.mot)` convertit la chaîne `"python"` en liste `['p','y','t','h','o','n']`, puis `join` les assemble avec des espaces.

### `self.partie_finie = True`

Ce drapeau booléen est vérifié en début de `_proposer()` : si `True`, la fonction sort immédiatement sans rien faire. Cela empêche l'utilisateur de continuer à jouer après la fin de la partie.

---

## 15. Lancement du programme

```python
if __name__ == "__main__":
    app = PenduApp()
    app.mainloop()
```

### `if __name__ == "__main__"`

Ce bloc ne s'exécute **que** si on lance directement ce fichier (`python main.py`). Si `main.py` était importé par un autre fichier, ce bloc serait ignoré. C'est une bonne pratique Python.

### `app = PenduApp()`

Crée une instance de la classe `PenduApp`, ce qui déclenche `__init__` et donc :
1. Crée la fenêtre
2. Construit tous les widgets
3. Lance une première partie

### `app.mainloop()`

Lance la **boucle d'événements** de Tkinter. Le programme entre dans cette boucle infinie qui :
- Attend les actions de l'utilisateur (clics, frappes clavier)
- Appelle les fonctions correspondantes
- Met à jour l'affichage

La boucle se termine uniquement quand l'utilisateur ferme la fenêtre.

---

## 16. Tableau récapitulatif de toutes les variables

### Variables globales (constantes)

| Nom | Type | Valeur | Rôle |
|---|---|---|---|
| `LISTE_MOTS` | `list[str]` | 10 mots | Réservoir de mots |
| `NB_ESSAIS` | `int` | `10` | Nombre d'essais = nombre d'étapes du dessin |
| `BG` | `str` | `"#0f0f1a"` | Couleur de fond principale |
| `SURFACE` | `str` | `"#1a1a2e"` | Couleur des surfaces secondaires |
| `BORDER` | `str` | `"#2a2a4a"` | Couleur des bordures |
| `ACCENT` | `str` | `"#e94560"` | Couleur d'accent principale |
| `ACCENT2` | `str` | `"#0f3460"` | Couleur d'accent secondaire |
| `TEXT` | `str` | `"#eaeaea"` | Couleur du texte principal |
| `TEXT_DIM` | `str` | `"#6c6c8a"` | Couleur du texte secondaire |
| `SUCCESS` | `str` | `"#4ecca3"` | Couleur des succès |
| `WARNING` | `str` | `"#f5a623"` | Couleur des avertissements |
| `ETAPES_DESSIN` | `list[tuple]` | 10 tuples | Étapes du dessin (nom + lambda) |

### Attributs d'instance de `PenduApp`

#### Polices
| Attribut | Taille | Graisse | Usage |
|---|---|---|---|
| `self.f_title` | 20 | bold | Titre |
| `self.f_word` | 26 | bold | Mot caché, Entry |
| `self.f_label` | 10 | normal | Messages |
| `self.f_btn` | 10 | bold | Boutons |
| `self.f_small` | 9 | normal | Textes secondaires |
| `self.f_essais` | 13 | bold | Compteur d'essais |

#### Widgets
| Attribut | Type Tkinter | Usage |
|---|---|---|
| `self.canvas` | `tk.Canvas` | Surface de dessin du pendu |
| `self.entry` | `tk.Entry` | Champ de saisie de la lettre |
| `self.lbl_msg` | `tk.Label` | Label du message d'état (gardé pour changer sa couleur) |

#### StringVar (variables d'affichage)
| Attribut | Contenu affiché |
|---|---|
| `self.var_mot` | Le mot caché (`"p  *  *  h  o  n"`) |
| `self.var_msg` | Message d'état (`"✓ Bravo !"`) |
| `self.var_lettres` | Lettres proposées (`"Proposées : A  B  C"`) |
| `self.var_essais_nb` | Compteur (`"7 / 10"`) |
| `self.var_barre` | Barre visuelle (`"███████░░░"`) |

#### Variables de jeu
| Attribut | Type | Rôle |
|---|---|---|
| `self.mot` | `str` | Le mot à deviner |
| `self.mot_cache` | `list[str]` | Le mot avec les `*` et lettres révélées |
| `self.essais_restants` | `int` | Essais restants (de 10 à 0) |
| `self.lettres_proposees` | `list[str]` | Historique des lettres tentées |
| `self.partie_finie` | `bool` | Vrai si la partie est terminée |

#### Variables locales dans `_build_ui`
| Variable | Type | Rôle |
|---|---|---|
| `root_frame` | `tk.Frame` | Conteneur principal des deux colonnes |
| `col_gauche` | `tk.Frame` | Conteneur de la colonne gauche |
| `col_droite` | `tk.Frame` | Conteneur de la colonne droite |
| `cadre_essais` | `tk.Frame` | Cadre bordé des essais restants |
| `frame_saisie` | `tk.Frame` | Conteneur du champ + bouton valider |

#### Variables locales dans `_proposer`
| Variable | Type | Rôle |
|---|---|---|
| `lettre` | `str` | La lettre lue, nettoyée et mise en minuscules |
| `indices` | `tuple` | Positions de la lettre dans le mot (retour de `chercher_lettre`) |
| `numero_etape` | `int` | Index de l'étape à dessiner (de 0 à 9) |

#### Variables locales dans `_actualiser_affichage`
| Variable | Type | Rôle |
|---|---|---|
| `barres` | `str` | La barre visuelle `"███████░░░"` |

#### Variables locales dans `_dessiner_etape`
| Variable | Type | Rôle |
|---|---|---|
| `numero_etape` | `int` | Index reçu en paramètre |
| `_nom` | `str` | Nom de l'étape (non utilisé, préfixe `_` par convention) |
| `fn` | `function` | La lambda à appeler pour dessiner |

---

## 17. Tableau récapitulatif de toutes les méthodes

| Méthode | Appelée par | Rôle |
|---|---|---|
| `__init__` | Python (création de l'objet) | Initialise la fenêtre, les polices, appelle `_build_ui` et `_nouvelle_partie` |
| `_build_ui` | `__init__` | Crée tous les widgets et la mise en page |
| `_dessiner_etape(n)` | `_proposer` | Dessine la n-ième étape sur le canvas |
| `_nouvelle_partie` | `__init__`, bouton | Réinitialise le jeu et l'interface |
| `_proposer` | bouton Valider, touche Entrée | Lit la lettre, la valide, met à jour le jeu |
| `_actualiser_affichage` | `_nouvelle_partie`, `_proposer` | Met à jour toutes les StringVar |
| `_verifier_fin` | `_proposer` | Vérifie et gère la fin de partie |

---

## 18. Schéma de l'interface

```
┌─────────────────────────────────────────────────────────────┐
│                        FENÊTRE PRINCIPALE                   │
│  ┌──────────────────────────────┐  ┌─────────────────────┐  │
│  │       COLONNE GAUCHE         │  │   COLONNE DROITE    │  │
│  │  ┌────────────────────────┐  │  │  ┌───────────────┐  │  │
│  │  │  ESSAIS RESTANTS       │  │  │  │               │  │  │
│  │  │  10 / 10               │  │  │  │    CANVAS     │  │  │
│  │  │  ██████████            │  │  │  │  (dessin du   │  │  │
│  │  └────────────────────────┘  │  │  │    pendu)     │  │  │
│  │                              │  │  │               │  │  │
│  │      ◈ LE PENDU ◈            │  │  └───────────────┘  │  │
│  │  devinez le mot lettre...    │  │                     │  │
│  │                              │  │  ↺ NOUVELLE PARTIE  │  │
│  │   p  *  *  h  o  n          │  │                     │  │
│  │                              │  └─────────────────────┘  │
│  │   ✓ Bravo, 'p' est là !     │                           │
│  │                              │                           │
│  │  [ p ]  [ VALIDER ]          │                           │
│  │                              │                           │
│  │  Proposées : A  P  O         │                           │
│  └──────────────────────────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 19. Déroulement d'une partie pas à pas

Voici ce qui se passe exactement dans le code à chaque moment :

**1. Lancement (`python main.py`)**
- `PenduApp()` → `__init__()` → `_build_ui()` + `_nouvelle_partie()`
- `choix_mot()` choisit par exemple `"python"`
- `cacher_mot()` produit `['*','*','*','*','*','*']`
- `_actualiser_affichage()` affiche `"* * * * * *"` et `"10 / 10"`

**2. Le joueur tape "p" et appuie sur Entrée**
- `_proposer()` lit `"p"`, valide la saisie
- `chercher_lettre("p", "python")` → `(0,)` (la lettre est en position 0)
- `len(indices) != 0` → bonne lettre
- `remplacer_lettre(['*','*','*','*','*','*'], (0,), 'p')` → `['p','*','*','*','*','*']`
- `_actualiser_affichage()` affiche `"p  *  *  *  *  *"`
- `_verifier_fin()` → il reste des `*`, pas de fin

**3. Le joueur tape "z" (lettre absente)**
- `chercher_lettre("z", "python")` → `()` (tuple vide)
- `len(indices) == 0` → mauvaise lettre
- `self.essais_restants` passe à `9`
- `numero_etape = 10 - 9 - 1 = 0` → `_dessiner_etape(0)` → dessine le **socle**
- La barre affiche `"█████████░"`

**4. Après 10 mauvaises lettres (défaite)**
- `self.essais_restants == 0`
- Le dessin est complet (10 étapes dessinées)
- `_verifier_fin()` détecte la défaite
- Le mot complet est révélé, la saisie est désactivée

**5. Le joueur clique "Nouvelle Partie"**
- `_nouvelle_partie()` efface le canvas, choisit un nouveau mot, remet les compteurs à zéro

---

## 20. `self` — Ce que c'est et pourquoi c'est indispensable

C'est probablement le concept le plus déroutant quand on débute avec les classes Python. Voici une explication complète.

### Le problème que `self` résout

Imaginons une classe sans `self` :

```python
class Compteur:
    def incrementer():
        valeur += 1   # ❌ Quelle valeur ? Celle de quel compteur ?
```

Si on crée deux compteurs distincts, comment Python saurait-il lequel modifier ? `self` est la réponse : c'est la **référence à l'objet lui-même**.

### Ce qu'est `self` concrètement

Quand on écrit :

```python
app = PenduApp()
```

Python crée un objet en mémoire et lui donne une adresse. `self` est le nom que Python donne à cet objet **à l'intérieur de la classe**, pour que les méthodes puissent accéder à ses propres données.

```python
class PenduApp(tk.Tk):
    def _nouvelle_partie(self):
        self.mot = choix_mot(LISTE_MOTS)   # self = l'objet app
        self.essais_restants = 10          # self = l'objet app
```

`self.mot` signifie : "la variable `mot` qui appartient **à cet objet précis**".

### `self` est toujours le premier paramètre

Toutes les méthodes d'une classe reçoivent `self` en premier paramètre, mais on ne le passe **jamais manuellement** à l'appel :

```python
# Définition : self est déclaré
def _proposer(self):
    ...

# Appel : on n'écrit pas self
app._proposer()   # Python le passe automatiquement
```

Python traduit `app._proposer()` en `PenduApp._proposer(app)` en interne. `self` reçoit donc la valeur `app`.

### `self` vs variable locale

```python
def _nouvelle_partie(self):
    self.mot = "python"   # attribut d'instance : survit après la fin de la méthode
    mot_local = "python"  # variable locale : disparaît quand la méthode se termine
```

Un attribut `self.xxx` est **persistant** : il est accessible depuis n'importe quelle méthode de la classe, à tout moment. Une variable locale n'existe que le temps d'exécution de sa méthode.

### Récapitulatif

| | `self.variable` | `variable_locale` |
|---|---|---|
| Portée | Toute la classe | Méthode courante uniquement |
| Durée de vie | Tant que l'objet existe | Jusqu'à la fin de la méthode |
| Accessible depuis | N'importe quelle méthode | Seulement dans sa méthode |
| Exemple | `self.essais_restants` | `lettre`, `barres`, `indices` |

---

## 21. Les classes et la Programmation Orientée Objet (POO)

### Qu'est-ce qu'une classe ?

Une **classe** est un modèle (un "plan") qui définit :
- Des **attributs** : les données que l'objet possède (ex : `self.mot`, `self.essais_restants`)
- Des **méthodes** : les actions que l'objet peut faire (ex : `_proposer()`, `_verifier_fin()`)

```python
class PenduApp(tk.Tk):   # <- définition de la classe
    def __init__(self):  # <- méthode
        self.mot = ""    # <- attribut
```

### Qu'est-ce qu'un objet (instance) ?

Un **objet** est une "réalisation concrète" d'une classe. On peut créer autant d'objets qu'on veut à partir d'une même classe, chacun ayant ses propres données.

```python
app = PenduApp()   # on crée UN objet de type PenduApp
```

Ici on ne crée qu'un seul objet, mais on pourrait en créer plusieurs avec des parties différentes.

### Différence entre fonction et méthode

| | Fonction | Méthode |
|---|---|---|
| Définition | En dehors d'une classe | À l'intérieur d'une classe |
| Premier paramètre | Aucun obligatoire | Toujours `self` |
| Appel | `choix_mot(liste)` | `self._proposer()` ou `app._proposer()` |
| Exemple dans le projet | `choix_mot()`, `cacher_mot()` | `_proposer()`, `_build_ui()` |

---

## 22. L'héritage et `super()`

### L'héritage

```python
class PenduApp(tk.Tk):
```

`PenduApp` **hérite** de `tk.Tk`. Cela signifie que `PenduApp` récupère automatiquement toutes les capacités de `tk.Tk` (créer une fenêtre, lui donner un titre, lancer la boucle d'événements...) **sans avoir à les réécrire**.

On dit que :
- `tk.Tk` est la **classe parente** (ou classe mère)
- `PenduApp` est la **classe enfant** (ou sous-classe)

Grâce à l'héritage, on peut appeler `self.title(...)`, `self.configure(...)`, `self.mainloop()` directement dans `PenduApp` comme si ces méthodes y étaient définies.

### `super().__init__()`

```python
def __init__(self):
    super().__init__()   # appelle tk.Tk.__init__()
```

`super()` désigne la classe parente (`tk.Tk`). `super().__init__()` appelle le constructeur de `tk.Tk` pour **initialiser correctement la fenêtre** avant d'y ajouter nos propres éléments.

Si on oubliait ce `super().__init__()`, la fenêtre ne serait pas initialisée et tout planterait. C'est une règle quand on hérite d'une classe qui a son propre constructeur.

---

## 23. Les méthodes spéciales (`__init__`, `__name__`)

Python réserve les noms entourés de **double underscores** (`__xxx__`) pour des usages particuliers. On les appelle **méthodes magiques** ou **dunder methods** (double underscore).

### `__init__`

```python
def __init__(self):
    ...
```

C'est le **constructeur** : Python l'appelle **automatiquement** dès qu'on crée un objet avec `PenduApp()`. On ne l'appelle jamais manuellement.

### `__name__`

```python
if __name__ == "__main__":
```

`__name__` est une variable spéciale que Python définit automatiquement dans chaque fichier :
- Si le fichier est **lancé directement** (`python main.py`), Python met `__name__ = "__main__"`
- Si le fichier est **importé** par un autre (`from main import PenduApp`), Python met `__name__ = "main"`

Ce test permet donc d'avoir du code qui ne s'exécute **que** quand on lance le fichier directement, et pas quand on l'importe.

---

## 24. La convention de nommage avec `_`

Dans le projet, toutes les méthodes "internes" commencent par un underscore :

```python
def _build_ui(self):      # _
def _proposer(self):      # _
def _verifier_fin(self):  # _
```

Le `_` au début est une **convention Python** (pas une règle du langage) qui signifie : "cette méthode est privée, elle est faite pour être utilisée **à l'intérieur de la classe seulement**, pas depuis l'extérieur".

De même, dans `_dessiner_etape` :

```python
_nom, fn = ETAPES_DESSIN[numero_etape]
```

La variable `_nom` commence par `_` pour indiquer qu'on ne va **pas l'utiliser**. C'est une convention pour dire "je dois décompacter ce tuple mais ce premier élément ne m'intéresse pas".

---

## 25. Les types de données Python utilisés

### `str` — Chaîne de caractères

```python
mot = "python"
lettre = "p"
```

Une suite de caractères entre guillemets. Immuable : on ne peut pas modifier un caractère directement. Méthodes utilisées dans le projet :

| Méthode | Exemple | Résultat |
|---|---|---|
| `.strip()` | `" p ".strip()` | `"p"` |
| `.lower()` | `"P".lower()` | `"p"` |
| `.upper()` | `"p".upper()` | `"P"` |
| `.isalpha()` | `"p".isalpha()` | `True` |
| `.join(liste)` | `" ".join(['a','b'])` | `"a b"` |

### `list` — Liste

```python
mot_cache = ['*', '*', '*']
lettres_proposees = []
```

Une collection ordonnée et **modifiable**. On peut ajouter, supprimer, modifier des éléments. Méthodes utilisées :

| Méthode / Opération | Exemple | Résultat |
|---|---|---|
| `.append(x)` | `liste.append("a")` | Ajoute `"a"` à la fin |
| `liste[i] = x` | `mot_cache[0] = "p"` | Remplace l'élément à l'indice 0 |
| `x in liste` | `"a" in lettres_proposees` | `True` si `"a"` est dans la liste |
| `len(liste)` | `len(mot_cache)` | Nombre d'éléments |

### `tuple` — Tuple

```python
indices = (0, 3, 5)
etape = ("socle", lambda c: ...)
```

Comme une liste mais **immuable** (on ne peut pas la modifier après création). Utilisé pour les indices de `chercher_lettre` et les étapes de `ETAPES_DESSIN`. On peut décompacter un tuple :

```python
_nom, fn = ("socle", lambda c: ...)
# _nom reçoit "socle", fn reçoit la lambda
```

### `int` — Entier

```python
NB_ESSAIS = 10
self.essais_restants = 10
```

Nombre entier. Opérateurs utilisés dans le projet :

| Opérateur | Exemple | Signification |
|---|---|---|
| `-=` | `self.essais_restants -= 1` | Soustrait 1 et réassigne (équivalent à `= essais_restants - 1`) |
| `==` | `essais_restants == 0` | Égalité (test, retourne `True` ou `False`) |
| `!=` | `len(lettre) != 1` | Différent de |
| `<=` | `0 <= numero_etape` | Inférieur ou égal |
| `<` | `numero_etape < len(...)` | Strictement inférieur |

### `bool` — Booléen

```python
self.partie_finie = False
self.partie_finie = True
```

Un booléen ne peut valoir que `True` (vrai) ou `False` (faux). Il est souvent utilisé comme **drapeau** (flag) pour mémoriser un état. Ici, `partie_finie` indique si la partie est terminée.

Les opérateurs booléens utilisés :

| Opérateur | Exemple | Signification |
|---|---|---|
| `not` | `not lettre.isalpha()` | Inverse le booléen (`not True` → `False`) |
| `or` | `condition1 or condition2` | Vrai si au moins une condition est vraie |
| `and` | `condition1 and condition2` | Vrai si les deux conditions sont vraies |
| `in` | `lettre in liste` | Vrai si l'élément est dans la collection |
| `not in` | `"*" not in mot_cache` | Vrai si l'élément est absent de la collection |

---

## 26. Les f-strings

```python
self.var_essais_nb.set(f"{self.essais_restants} / {NB_ESSAIS}")
self.var_msg.set(f"✗  '{lettre}' n'est pas dans le mot.")
```

Un **f-string** (formatted string) est une chaîne précédée de `f`. Les expressions entre `{}` sont **évaluées et insérées** directement dans la chaîne.

**Exemple concret :**
```python
essais = 7
total = 10
texte = f"{essais} / {total}"   # → "7 / 10"
```

C'est équivalent à l'ancienne syntaxe `str(essais) + " / " + str(total)` mais bien plus lisible.

---

## 27. Les structures de contrôle utilisées

### `if / elif / else`

```python
if "*" not in self.mot_cache:
    # victoire
elif self.essais_restants == 0:
    # défaite
else:
    # la partie continue
```

- `if` : teste la première condition
- `elif` : teste une condition alternative si le `if` est faux
- `else` : s'exécute si toutes les conditions précédentes sont fausses

### `return` sans valeur

```python
def _proposer(self):
    if self.partie_finie:
        return   # sort immédiatement de la fonction
```

`return` seul (sans valeur) interrompt l'exécution de la méthode et rend la main à l'appelant. C'est utile pour des "sorties anticipées" en cas d'erreur ou de condition particulière, plutôt que d'imbriquer tout le code dans des `else`.

### Boucle `for` dans `functions.py`

```python
for indice in range(len(mot)):
    if mot[indice] == lettre:
        liste_indices.append(indice)
```

- `range(len(mot))` : génère une séquence d'entiers de `0` à `len(mot)-1`
- `len(mot)` : donne le nombre de caractères du mot
- À chaque tour, `indice` prend la valeur suivante et on teste le caractère à cette position

### `assert`

```python
assert type(mot) == str
assert type(lettre) == str
```

`assert` vérifie qu'une condition est vraie. Si elle est fausse, Python lève une `AssertionError` et le programme s'arrête. C'est utilisé dans `functions.py` pour vérifier que les paramètres sont du bon type.

---

## 28. La programmation événementielle avec Tkinter

Le jeu du pendu fonctionne selon un modèle **événementiel**, très différent d'un programme séquentiel classique.

### Programme séquentiel (l'ancien `main.py` en console)

```
début
  → choisir un mot
  → afficher le mot caché
  → boucle : saisir lettre → traiter → afficher
  → afficher résultat
fin
```

Le programme "commande" l'utilisateur : il lui demande une saisie et attend.

### Programme événementiel (Tkinter)

```
début
  → construire l'interface
  → lancer mainloop()  ← on attend ici indéfiniment
       ↓ événement (clic, touche)
  → appeler la fonction associée
       ↓ retourner à mainloop()
  → attendre le prochain événement...
```

Le programme est **passif** : il attend que l'utilisateur fasse quelque chose, puis réagit. C'est `mainloop()` qui gère cette attente en permanence.

### Les événements dans le projet

| Événement utilisateur | Mécanisme Tkinter | Fonction appelée |
|---|---|---|
| Clic sur "VALIDER" | `command=self._proposer` | `_proposer()` |
| Appui sur Entrée | `bind("<Return>", ...)` | `_proposer()` |
| Clic sur "NOUVELLE PARTIE" | `command=self._nouvelle_partie` | `_nouvelle_partie()` |
| Fermeture de la fenêtre | géré par `tk.Tk` | arrêt de `mainloop()` |

---

## 29. Le chaînage de méthodes

```python
lettre = self.entry.get().strip().lower()
```

Python permet d'appeler des méthodes **en chaîne** : le résultat de chaque méthode est immédiatement utilisé pour appeler la suivante.

Décomposé :
```python
texte_brut = self.entry.get()      # "  P  "
sans_espaces = texte_brut.strip()  # "P"
en_minuscules = sans_espaces.lower() # "p"
lettre = en_minuscules             # "p"
```

Le chaînage est plus concis mais identique en résultat.

---

## 30. La décompaction de tuple (tuple unpacking)

```python
_nom, fn = ETAPES_DESSIN[numero_etape]
```

`ETAPES_DESSIN[numero_etape]` retourne un tuple à deux éléments, par exemple `("socle", <lambda>)`.

La **décompaction** permet d'assigner chaque élément du tuple à une variable distincte en une seule ligne. C'est équivalent à :

```python
tuple_etape = ETAPES_DESSIN[numero_etape]
_nom = tuple_etape[0]   # "socle"
fn   = tuple_etape[1]   # <lambda function>
```

La version avec décompaction est plus lisible et pythonique.

---

## 31. La répétition de chaîne avec `*`

```python
barres = "█" * self.essais_restants + "░" * (NB_ESSAIS - self.essais_restants)
```

En Python, l'opérateur `*` appliqué à une chaîne et un entier **répète la chaîne** ce nombre de fois :

```python
"█" * 3   →  "███"
"░" * 2   →  "░░"
"ab" * 3  →  "ababab"
"x" * 0   →  ""      (chaîne vide)
```

C'est également valable pour les listes : `[0] * 5` → `[0, 0, 0, 0, 0]`.

---

## 32. `len()` et `range()`

### `len(x)`

Retourne le **nombre d'éléments** de `x` :

```python
len("python")             # → 6  (nombre de caractères)
len(['*','*','*'])        # → 3  (nombre d'éléments)
len((0, 3, 5))            # → 3  (nombre d'éléments du tuple)
len([])                   # → 0  (liste vide)
```

Utilisé dans le projet pour : vérifier qu'une lettre a bien été tapée (`len(lettre) != 1`), vérifier qu'une lettre est absente (`len(indices) == 0`), borner l'index du dessin (`numero_etape < len(ETAPES_DESSIN)`).

### `range(n)`

Génère une séquence d'entiers de `0` à `n-1`. Utilisé dans les boucles `for` de `functions.py` :

```python
range(6)   →  0, 1, 2, 3, 4, 5
range(len("python"))  →  0, 1, 2, 3, 4, 5
```

---

## 33. `list()` — Convertir en liste

```python
self.var_mot.set("  ".join(list(self.mot)))
```

`list("python")` convertit la chaîne en liste de caractères :

```python
list("python")  →  ['p', 'y', 't', 'h', 'o', 'n']
```

C'est nécessaire ici car `.join()` attend une liste (ou tout objet itérable), et on veut insérer des espaces entre chaque lettre du mot révélé.

---

## 34. `random.choice()` — Choix aléatoire

```python
import random
mot = random.choice(list)
```

`random.choice(sequence)` choisit et retourne **un élément au hasard** dans la séquence. Chaque élément a la même probabilité d'être choisi. La séquence originale n'est pas modifiée.

L'import est fait **à l'intérieur** de la fonction `choix_mot`. C'est possible en Python (import local), mais la convention habituelle est de mettre tous les imports en haut du fichier. Ici c'est un choix du développeur.