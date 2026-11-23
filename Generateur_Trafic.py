"""Générateur automatique de trafic aérien.

Produit un fichier texte décrivant des avions qui vont entrer dans le secteur.
Une ligne = un avion, champs séparés par des points-virgules :

    indicatif;balise_entree;t_entree;niveau_vol;cap_deg;vitesse_kt;taux_montee_ft_min;taux_descente_ft_min

Exemple (AF1234 entre par BAL2 au pas de temps 412, au FL350, cap 087) :

    AF1234;BAL2;412;350;087;450;2500;1250

Les vols sont triés par heure d'entrée croissante.

Utilisation en ligne de commande :

    python Generateur_Trafic.py 20 -o trafic.txt --graine 42
    python Generateur_Trafic.py 20 --duree 7200
    python Generateur_Trafic.py 20 --balises ALPHA BRAVO CHARLIE

Utilisation depuis un autre module :

    from Generateur_Trafic import generer_trafic, ecrire_trafic, lire_trafic
    vols = generer_trafic(20, graine=42)
    ecrire_trafic(vols, "trafic.txt")
    vols = lire_trafic("trafic.txt")
"""

import argparse
import random
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Paramètres fixes pour l'instant (on les fera varier plus tard)
# ---------------------------------------------------------------------------

VITESSE_KT = 450               # vitesse (kt) : valeur provisoire, à ajuster
TAUX_MONTEE_FT_MIN = 2500      # taux de montée (ft/min)
TAUX_DESCENTE_FT_MIN = 1250    # taux de descente (ft/min)

# Niveaux de vol possibles à l'entrée (en centaines de pieds : 350 = FL350),
# tirés de 10 en 10 entre le minimum et le maximum (inclus).
NIVEAU_MIN = 290
NIVEAU_MAX = 410
PAS_NIVEAU = 10

# Les heures d'entrée sont tirées entre 0 et cette durée (en pas de temps).
DUREE_DEFAUT = 3600

# Balises d'entrée/sortie du secteur : noms provisoires, à remplacer par les
# vraies balises dès que le secteur sera défini.
BALISES = ["BAL1", "BAL2", "BAL3", "BAL4"]

# Codes IATA de compagnies (2 caractères) utilisés pour fabriquer les indicatifs.
COMPAGNIES_IATA = [
    "AF", "KL", "LH", "BA", "IB", "LX", "SN", "TP",
    "AZ", "U2", "FR", "VY", "TO", "EW",
]

ENTETE = ("# indicatif;balise_entree;t_entree;niveau_vol;cap_deg;vitesse_kt;"
          "taux_montee_ft_min;taux_descente_ft_min")


@dataclass
class Vol:
    """Un avion généré.

    - indicatif : code IATA de la compagnie + numéro de vol (ex. "AF1234")
    - balise_entree : nom de la balise par laquelle l'avion entre dans le secteur
    - t_entree : heure d'entrée dans le secteur (en pas de temps de la simulation)
    - niveau_vol : niveau de vol à l'entrée (ex. 350 pour FL350)
    - cap : cap voulu en degrés (1 à 360)
    - vitesse : vitesse en nœuds
    - taux_montee : taux de montée en ft/min
    - taux_descente : taux de descente en ft/min
    """
    indicatif: str
    balise_entree: str
    t_entree: int
    niveau_vol: int
    cap: int
    vitesse: int = VITESSE_KT
    taux_montee: int = TAUX_MONTEE_FT_MIN
    taux_descente: int = TAUX_DESCENTE_FT_MIN

    def en_ligne(self):
        """Ligne de texte correspondant au vol (sans retour à la ligne)."""
        return (f"{self.indicatif};{self.balise_entree};{self.t_entree};"
                f"{self.niveau_vol};{self.cap:03d};{self.vitesse};"
                f"{self.taux_montee};{self.taux_descente}")

    @classmethod
    def depuis_ligne(cls, ligne):
        """Relit un vol à partir d'une ligne produite par `en_ligne`."""
        champs = ligne.strip().split(";")
        if len(champs) != 8:
            raise ValueError(f"Ligne invalide (8 champs attendus) : {ligne!r}")
        indicatif, balise, t_entree, niveau, cap, vitesse, montee, descente = champs
        return cls(indicatif, balise, int(t_entree), int(niveau), int(cap),
                   int(vitesse), int(montee), int(descente))


def generer_trafic(nb_vols, balises=None, graine=None, duree=DUREE_DEFAUT):
    """Génère `nb_vols` avions aléatoires.

    Args:
        nb_vols: (int) nombre d'avions à créer.
        balises: (list[str]) balises d'entrée possibles (`BALISES` par défaut).
        graine: (int) graine du générateur aléatoire, pour obtenir
            le même trafic à chaque lancement (None = trafic différent à
            chaque fois).
        duree: (int) les heures d'entrée sont tirées entre 0 et `duree`
            (en pas de temps).

    Returns:
        Une liste de `Vol` triée par heure d'entrée croissante, avec des
        indicatifs tous différents.
    """
    if balises is None:
        balises = BALISES
    if not balises:
        raise ValueError("Il faut au moins une balise d'entrée.")
    if nb_vols > len(COMPAGNIES_IATA) * 9999:
        raise ValueError("Trop de vols demandés pour avoir des indicatifs uniques.")

    if duree < 0:
        raise ValueError("La durée doit être positive.")

    alea = random.Random(graine)
    niveaux = range(NIVEAU_MIN, NIVEAU_MAX + 1, PAS_NIVEAU)
    indicatifs_utilises = set()
    vols = []
    while len(vols) < nb_vols:
        indicatif = f"{alea.choice(COMPAGNIES_IATA)}{alea.randint(1, 9999)}"
        if indicatif in indicatifs_utilises:
            continue
        indicatifs_utilises.add(indicatif)
        vols.append(Vol(
            indicatif=indicatif,
            balise_entree=alea.choice(balises),
            t_entree=alea.randint(0, duree),
            niveau_vol=alea.choice(niveaux),
            cap=alea.randint(1, 360),
        ))
    vols.sort(key=lambda vol: vol.t_entree)
    return vols


def ecrire_trafic(vols, chemin):
    """Écrit la liste de vols dans un fichier texte (une ligne par vol)."""
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(ENTETE + "\n")
        for vol in vols:
            f.write(vol.en_ligne() + "\n")


def lire_trafic(chemin):
    """Lit un fichier produit par `ecrire_trafic` et renvoie la liste de `Vol`.

    Les lignes vides et les lignes commençant par '#' sont ignorées.
    """
    vols = []
    with open(chemin, encoding="utf-8") as f:
        for ligne in f:
            if ligne.strip() and not ligne.startswith("#"):
                vols.append(Vol.depuis_ligne(ligne))
    return vols


def main():
    parseur = argparse.ArgumentParser(
        description="Génère un fichier texte de trafic aérien.")
    parseur.add_argument("nb_vols", type=int, help="nombre d'avions à générer")
    parseur.add_argument("-o", "--sortie", default="trafic.txt",
                         help="fichier de sortie (défaut : trafic.txt)")
    parseur.add_argument("--graine", type=int, default=None,
                         help="graine aléatoire (trafic reproductible)")
    parseur.add_argument("--duree", type=int, default=DUREE_DEFAUT,
                         help="les heures d'entrée sont tirées entre 0 et cette "
                              "durée, en pas de temps (défaut : %d)" % DUREE_DEFAUT)
    parseur.add_argument("--balises", nargs="+", default=None,
                         help="noms des balises d'entrée (défaut : %s)"
                              % " ".join(BALISES))
    args = parseur.parse_args()

    vols = generer_trafic(args.nb_vols, args.balises, args.graine, args.duree)
    ecrire_trafic(vols, args.sortie)
    print(f"{len(vols)} vols écrits dans {args.sortie}")


if __name__ == "__main__":
    main()
