# ── Imports ────────────────────────────────────────────────────────────────────
import tkinter as tk               # Bibliothèque graphique standard de Python
from tkinter import font as tkfont # Module pour créer des polices personnalisées
# On importe uniquement les fonctions dont on a besoin depuis functions.py
from functions import choix_mot, cacher_mot, chercher_lettre, remplacer_lettre

# ── Configuration du jeu ───────────────────────────────────────────────────────
LISTE_MOTS = ["python", "programmation", "ordinateur", "clavier", "algorithme",
              "variable", "fonction", "boucle", "liste", "chaine"]

# NB_ESSAIS correspond exactement au nombre d'étapes du dessin (4 potence + 6 bonhomme)
# La partie se termine quand le dessin est entièrement complété (plus d'essais)
NB_ESSAIS = 10

# ── Palette de couleurs ────────────────────────────────────────────────────────
BG       = "#0f0f1a"  # Fond principal (noir bleuté)
SURFACE  = "#1a1a2e"  # Surfaces secondaires (bleu nuit)
BORDER   = "#2a2a4a"  # Bordures des cadres
ACCENT   = "#e94560"  # Accent principal (rouge/rose)
ACCENT2  = "#0f3460"  # Accent secondaire (bleu foncé)
TEXT     = "#eaeaea"  # Texte principal (blanc cassé)
TEXT_DIM = "#6c6c8a"  # Texte secondaire (gris violet)
SUCCESS  = "#4ecca3"  # Messages de succès (vert menthe)
WARNING  = "#f5a623"  # Avertissements (orange)


# ── Les 10 étapes du dessin ────────────────────────────────────────────────────
# Chaque étape est une fonction qui trace une partie sur le canvas.
# Les 4 premières construisent la potence, les 6 suivantes le bonhomme.
# On les définit comme méthode de classe pour accéder à self.canvas.
ETAPES_DESSIN = [
    # -- Potence (4 étapes) --
    ("socle",    lambda c: c.create_line(20, 190, 140, 190, fill="#6c6c8a", width=4)),
    ("poteau",   lambda c: c.create_line(60, 190, 60,  20,  fill="#6c6c8a", width=4)),
    ("poutre",   lambda c: c.create_line(60, 20,  150, 20,  fill="#6c6c8a", width=4)),
    ("corde",    lambda c: c.create_line(150, 20, 150, 50,  fill="#6c6c8a", width=3)),
    # -- Bonhomme (6 étapes) --
    ("tête",     lambda c: c.create_oval(130, 50, 170, 90,  outline="#e94560", width=3)),
    ("corps",    lambda c: c.create_line(150, 90, 150, 145, fill="#e94560", width=3)),
    ("bras_g",   lambda c: c.create_line(150,105, 120, 130, fill="#e94560", width=3)),
    ("bras_d",   lambda c: c.create_line(150,105, 180, 130, fill="#e94560", width=3)),
    ("jambe_g",  lambda c: c.create_line(150,145, 125, 175, fill="#e94560", width=3)),
    ("jambe_d",  lambda c: c.create_line(150,145, 175, 175, fill="#e94560", width=3)),
]


class PenduApp(tk.Tk):

    def __init__(self):
        """Constructeur : initialise la fenêtre et lance une première partie."""
        super().__init__()
        self.title("Le Pendu")
        self.resizable(False, False)
        self.configure(bg=BG)

        # Polices
        self.f_title  = tkfont.Font(family="Courier", size=20, weight="bold")
        self.f_word   = tkfont.Font(family="Courier", size=26, weight="bold")
        self.f_label  = tkfont.Font(family="Courier", size=10)
        self.f_btn    = tkfont.Font(family="Courier", size=10, weight="bold")
        self.f_small  = tkfont.Font(family="Courier", size=9)
        self.f_essais = tkfont.Font(family="Courier", size=13, weight="bold")

        self._build_ui()
        self._nouvelle_partie()


    # ── Construction de l'interface ────────────────────────────────────────────
    def _build_ui(self):
        """
        Mise en page en deux colonnes :
          - Colonne gauche  : essais restants | titre | mot caché | saisie | lettres proposées
          - Colonne droite  : canvas du dessin | bouton nouvelle partie
        """

        # ── Cadre racine qui contient les deux colonnes ────────────────────────
        root_frame = tk.Frame(self, bg=BG)
        root_frame.pack(padx=16, pady=16)

        # ════════════════════════════════════════════════════════════════════════
        # COLONNE GAUCHE
        # ════════════════════════════════════════════════════════════════════════
        col_gauche = tk.Frame(root_frame, bg=BG)
        col_gauche.grid(row=0, column=0, sticky="nsew", padx=(0, 16))

        # -- Cadre "Essais restants" (en haut à gauche, avec bordure) -----------
        cadre_essais = tk.Frame(col_gauche, bg=SURFACE,
                                highlightbackground=BORDER,
                                highlightthickness=1)
        cadre_essais.pack(anchor="w", pady=(0, 14))

        tk.Label(cadre_essais, text="ESSAIS RESTANTS",
                 font=self.f_small, bg=SURFACE, fg=TEXT_DIM).pack(padx=12, pady=(8, 2))

        # StringVar liée au label : se met à jour automatiquement quand la variable change
        self.var_essais_nb = tk.StringVar()
        tk.Label(cadre_essais, textvariable=self.var_essais_nb,
                 font=self.f_essais, bg=SURFACE, fg=WARNING).pack(padx=12, pady=(0, 4))

        # Barre de progression visuelle (blocs █ et ░)
        self.var_barre = tk.StringVar()
        tk.Label(cadre_essais, textvariable=self.var_barre,
                 font=self.f_small, bg=SURFACE, fg=WARNING).pack(padx=12, pady=(0, 8))

        # -- Titre et sous-titre (centré dans la colonne gauche) ----------------
        tk.Label(col_gauche, text="◈ LE PENDU ◈",
                 font=self.f_title, bg=BG, fg=ACCENT).pack(anchor="center", pady=(0, 2))
        tk.Label(col_gauche, text="devinez le mot lettre par lettre",
                 font=self.f_small, bg=BG, fg=TEXT_DIM).pack(anchor="center", pady=(0, 16))

        # -- Mot caché (ex : "p  *  *  h  o  n") --------------------------------
        self.var_mot = tk.StringVar()
        tk.Label(col_gauche, textvariable=self.var_mot,
                 font=self.f_word, bg=BG, fg=TEXT).pack(anchor="center", pady=(0, 8))

        # -- Message d'état (bonne/mauvaise lettre, erreur de saisie) -----------
        self.var_msg = tk.StringVar()
        self.lbl_msg = tk.Label(col_gauche, textvariable=self.var_msg,
                                font=self.f_label, bg=BG, fg=SUCCESS)
        self.lbl_msg.pack(anchor="center", pady=(0, 10))

        # -- Zone de saisie (champ + bouton côte à côte) ------------------------
        frame_saisie = tk.Frame(col_gauche, bg=BG)
        frame_saisie.pack(anchor="center", pady=(0, 8))

        # Champ texte pour taper la lettre
        self.entry = tk.Entry(frame_saisie, width=3, font=self.f_word,
                              bg=SURFACE, fg=ACCENT,
                              insertbackground=ACCENT,  # Couleur du curseur de saisie
                              relief="flat", justify="center")
        self.entry.pack(side="left", ipady=4, padx=(0, 8))
        # Appui sur Entrée = même effet que le bouton Valider
        self.entry.bind("<Return>", lambda e: self._proposer())

        tk.Button(frame_saisie, text="VALIDER", font=self.f_btn,
                  bg=ACCENT, fg="white", relief="flat",
                  activebackground="#c73652", activeforeground="white",
                  cursor="hand2", padx=12, pady=5,
                  command=self._proposer).pack(side="left")

        # -- Lettres déjà proposées (sous la zone de saisie) -------------------
        self.var_lettres = tk.StringVar()
        tk.Label(col_gauche, textvariable=self.var_lettres,
                 font=self.f_small, bg=BG, fg=TEXT_DIM,
                 wraplength=300,      # Retour à la ligne automatique après 300px
                 justify="center").pack(anchor="center", pady=(4, 0))

        # ════════════════════════════════════════════════════════════════════════
        # COLONNE DROITE
        # ════════════════════════════════════════════════════════════════════════
        col_droite = tk.Frame(root_frame, bg=BG)
        col_droite.grid(row=0, column=1, sticky="nsew")

        # -- Canvas de dessin ---------------------------------------------------
        # C'est sur ce canvas que la potence et le bonhomme sont dessinés
        self.canvas = tk.Canvas(col_droite, width=220, height=200,
                                bg=SURFACE, highlightthickness=1,
                                highlightbackground=BORDER)
        self.canvas.pack(pady=(0, 14))

        # -- Bouton Nouvelle Partie ---------------------------------------------
        tk.Button(col_droite, text="↺  NOUVELLE PARTIE", font=self.f_btn,
                  bg=ACCENT2, fg=TEXT, relief="flat",
                  activebackground="#184080", activeforeground=TEXT,
                  cursor="hand2", padx=12, pady=6,
                  command=self._nouvelle_partie).pack(anchor="center")


    # ── Dessin progressif ──────────────────────────────────────────────────────
    def _dessiner_etape(self, numero_etape):
        """
        Exécute l'étape de dessin correspondant à 'numero_etape' (index de 0 à 9).
        Chaque appel ajoute un élément supplémentaire sur le canvas.
        La potence se construit d'abord (étapes 0-3), puis le bonhomme (étapes 4-9).
        """
        if 0 <= numero_etape < len(ETAPES_DESSIN):
            _nom, fn = ETAPES_DESSIN[numero_etape]
            fn(self.canvas)  # On passe le canvas à la fonction lambda


    # ── Initialisation d'une nouvelle partie ──────────────────────────────────
    def _nouvelle_partie(self):
        """Réinitialise toutes les variables et remet l'interface à zéro."""

        # Appel des fonctions de functions.py
        self.mot              = choix_mot(LISTE_MOTS)  # Mot choisi au hasard
        self.mot_cache        = cacher_mot(self.mot)   # Liste de '*' de la même longueur
        self.essais_restants  = NB_ESSAIS              # Compteur d'essais
        self.lettres_proposees = []                    # Historique des lettres tentées
        self.partie_finie     = False                  # Drapeau de fin de partie

        # On efface le canvas : la potence et le bonhomme sont retirés
        self.canvas.delete("all")

        self._actualiser_affichage()
        self.var_msg.set("")
        self.entry.configure(state="normal")
        self.entry.delete(0, "end")
        self.entry.focus()


    # ── Traitement d'une lettre proposée ──────────────────────────────────────
    def _proposer(self):
        """Appelée lors d'un clic sur Valider ou d'un appui sur Entrée."""

        if self.partie_finie:
            return

        # Lecture, nettoyage et mise en minuscules de la saisie
        lettre = self.entry.get().strip().lower()
        self.entry.delete(0, "end")

        # Vérification : exactement une lettre alphabétique
        if len(lettre) != 1 or not lettre.isalpha():
            self.var_msg.set("⚠  Entrez une seule lettre.")
            self.lbl_msg.configure(fg=WARNING)
            return

        # Vérification : lettre pas encore proposée
        if lettre in self.lettres_proposees:
            self.var_msg.set(f"⚠  '{lettre}' déjà proposée !")
            self.lbl_msg.configure(fg=WARNING)
            return

        self.lettres_proposees.append(lettre)

        # Appel de chercher_lettre (functions.py) → tuple des indices de la lettre dans le mot
        indices = chercher_lettre(lettre, self.mot)

        if len(indices) == 0:
            # Mauvaise lettre : on perd un essai et on dessine la prochaine étape
            self.essais_restants -= 1
            # L'étape à dessiner = nombre d'erreurs commises depuis le début
            numero_etape = NB_ESSAIS - self.essais_restants - 1
            self._dessiner_etape(numero_etape)
            self.var_msg.set(f"✗  '{lettre}' n'est pas dans le mot.")
            self.lbl_msg.configure(fg=ACCENT)
        else:
            # Bonne lettre : on révèle ses positions via remplacer_lettre (functions.py)
            self.mot_cache = remplacer_lettre(self.mot_cache, indices, lettre)
            self.var_msg.set(f"✓  Bravo, '{lettre}' est dans le mot !")
            self.lbl_msg.configure(fg=SUCCESS)

        self._actualiser_affichage()
        self._verifier_fin()


    # ── Mise à jour de l'affichage ────────────────────────────────────────────
    def _actualiser_affichage(self):
        """Rafraîchit le mot caché, les compteurs d'essais et les lettres proposées."""

        # Mot caché : espaces entre chaque caractère pour la lisibilité
        self.var_mot.set("  ".join(self.mot_cache))

        # Compteur numérique des essais restants
        self.var_essais_nb.set(f"{self.essais_restants} / {NB_ESSAIS}")

        # Barre visuelle : █ pour les essais restants, ░ pour les essais perdus
        barres = "█" * self.essais_restants + "░" * (NB_ESSAIS - self.essais_restants)
        self.var_barre.set(barres)

        # Liste des lettres déjà tentées
        if self.lettres_proposees:
            self.var_lettres.set(
                "Proposées : " + "  ".join(self.lettres_proposees).upper()
            )
        else:
            self.var_lettres.set("Aucune lettre proposée")


    # ── Vérification de fin de partie ─────────────────────────────────────────
    def _verifier_fin(self):
        """
        Vérifie deux conditions de fin :
          - Victoire : plus aucun '*' dans le mot caché
          - Défaite  : plus aucun essai (dessin entièrement complété)
        """

        if "*" not in self.mot_cache:
            # Toutes les lettres ont été trouvées → victoire
            self.var_msg.set(f"🎉  Félicitations ! Le mot était « {self.mot} ».")
            self.lbl_msg.configure(fg=SUCCESS)
            self.partie_finie = True
            self.entry.configure(state="disabled")

        elif self.essais_restants == 0:
            # Le dessin est entièrement complété → défaite
            self.var_msg.set(f"💀  Perdu ! Le mot était « {self.mot} ».")
            self.lbl_msg.configure(fg=ACCENT)
            self.partie_finie = True
            self.entry.configure(state="disabled")
            # Révèle le mot complet
            self.var_mot.set("  ".join(list(self.mot)))


# ── Lancement ──────────────────────────────────────────────────────────────────
# Ce bloc ne s'exécute que si on lance ce fichier directement (pas si on l'importe)
if __name__ == "__main__":
    app = PenduApp()   # Crée la fenêtre principale
    app.mainloop()     # Lance la boucle d'événements Tkinter