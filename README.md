
# 🧮 L3 Projet : Recherche Opérationnelle

Projet de Recherche Opérationnelle de 3ᵉ année à l'EFREI Paris du groupe B3.<br />
Le projet doit s'exécuter sur une série de 12 tables de test. 

## 🖊️ Auteurs 

- [Amna Boulouha](https://github.com/blhmna)
- [Kevin Kurtz](https://github.com/ktzkvin)
- [Romane Segui](https://github.com/Airseg)
- [Salomé Clavière](https://github.com/salobinks)
	

## 💾 Installation 

### Prérequis :
- Python 3.8 ou supérieur

### Installation du projet :

Toutes commandes à suivre sont à exécuter dans le terminal de votre IDE.

#### Clôner le depôt github :
```bash
    https://github.com/ktzkvin/RechercheOPL3.git
```

#### Naviguer dans le répertoire `RechercheOPL3` :
```bash
    cd RechercheOPL3
```

#### Installer les dépendances nécessaires :
```bash
    pip install -r requirements.txt
```

#### Pour lancer l'application, exécuter la commande suivante :
```bash
    python B3_main.py
```

Ou bien exécuter le fichier B3_main.py à l'aide de votre IDE.
## 🛠️ Fonctionnalités


### 0. Lecture du Tableau de Contraintes : Menu principal
Le programme lit un tableau de contraintes à partir d'un fichier texte et stocke les informations en **mémoire**.<br />
Puis, un **menu** est affiché pour choisir une fonctionnalité à lancer sur le tableau de contraintes.

### 1. Matrice des coûts
Le graphe mémorisé est généré sous forme de **tableau**.<br />

### 2. Proposition de transport (NO/BH)
Possibilité de générer une nouvelle proposition de transport avec Nord-Ouest ou Ballas-Hammer.

### 4. Calcul des coûts potentiels
Calculer les coûts potentiels détaillés avec l'algorithme de Nord-Ouest ou celui de Ballas-Hammer.

### 5. Calcul des coûts marginaux
Calculer les coûts marginaux détaillés avec l'algorithme de Nord-Ouest ou celui de Ballas-Hammer.

### 6. Calcul des coûts totaux
Calculer les coûts totaux détaillés avec l'algorithme de Nord-Ouest ou celui de Ballas-Hammer.

### 8. BONUS : Affichage du graphe
Ne faisant par partie du cahier des charges du sujet, nous avons décidé d'importer un affichage graphique afin d'avoir une meilleure compréhension visuelle du graphe.

### 9. Changer la table de contraintes
Pour éviter toute interruption du code, il est également possible de choisir une nouvelle table de contraintes à étudier.
