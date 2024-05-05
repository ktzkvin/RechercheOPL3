
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
    git clone https://github.com/ktzkvin/RechercheOPL3
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

### 1. Affichage du Tableau de Contraintes
Le graphe mémorisé est généré sous forme de **tableau**, y compris les sommets fictifs 0 (α) et N+1 (ω).<br />
De même, le graphe est affiché sous forme de **triplets** pour une meilleure compréhension.

### 2. Affichage Matriciel
Le graphe mémorisé est généré sous forme **matricielle**, y compris les sommets fictifs 0 (α) et N+1 (ω).

### 3.1 Vérification des Propriétés du Graphe
Le graphe est examiné pour s'assurer que toutes les valeurs d'arc sont positives et qu'il ne contient pas de circuit.

### 3.2 Calcul des calendriers
Pour calculer les calendriers, l'algorithme aura d'abord besoin de **calculer les rangs** :

### 4. BONUS : Affichage du graphe
Ne faisant par partie du cahier des charges du sujet, nous avons décidé d'importer un affichage graphique afin d'avoir une meilleure compréhension visuelle du graphe.

### 5. Changer la table de contraintes
Pour éviter toute interruption du code, il est également possible de choisir une nouvelle table de contraintes à étudier.
