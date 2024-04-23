
# 🧮 L3 Projet : Théorie des Graphes

Projet de Théorie des Graphes de 3ᵉ année à l'EFREI Paris du groupe B3.<br />
Le projet doit s'exécuter sur une série de 14 tables de test. Afin d'explorer tout le potentiel du programme, nous avons créé la `table 15.txt` comportant des arcs négatifs.


## 🖊️ Auteurs 

- [Amna Boulouha](https://github.com/blhmna)
- [Kevin Kurtz](https://github.com/ktzkvin)
- [Romane Segui](https://github.com/Airseg)
- [Salomé Clavière](https://github.com/salobinks)
	

## 💾 Installation 

### Prérequis :
- Python 3.8 ou supérieur
- Graphviz sur votre machine (pour l'affichage graphique)

Pour installer Graphviz sur votre machine, veuillez suivre les instructions suivantes :<br />

#### Télécharger la version correspondante à votre système d'exploitation :
- [Windows](https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/10.0.1/windows_10_cmake_Release_graphviz-install-10.0.1-win64.exe.sha256)
- [Autres systèmes d'exploitation](https://gitlab.com/graphviz/graphviz/-/releases)

Lors de l'installation, veuillez cocher la case "_Add Graphviz to the system PATH for all users_" pour que l'installation soit effective.<br /><br />
![Installation](https://cdn.discordapp.com/attachments/422113586597593088/1230474163651739648/Screenshot_1_1.png?ex=6633735d&is=6620fe5d&hm=1de86b77a671c6c1191d12f03362da7cfc07d63520c5c1248dee86b2cb630aa5&)


### Installation du projet :

Toutes commandes à suivre sont à exécuter dans le terminal de votre IDE.

#### Clôner le depôt github :
```bash
    git clone https://github.com/ktzkvin/GraphProjectL3.git
```

#### Naviguer dans le répertoire `GraphProjectL3` :
```bash
    cd GraphProjectL3
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

Chaque étape du processus d'ordonnancement est illustrée ci-dessous avec un GIF démonstratif :

### 0. Lecture du Tableau de Contraintes : Menu principal
Le programme lit un tableau de contraintes à partir d'un fichier texte et stocke les informations en **mémoire**.<br />
Puis, un **menu** est affiché pour choisir une fonctionnalité à lancer sur le tableau de contraintes.

![Lecture du tableau de contraintes](https://cdn.discordapp.com/attachments/1222083642206060687/1229878743158489158/sequence_1.gif?ex=663148d6&is=661ed3d6&hm=e4135b787fb987a96f9e82b9ff23af729719b1f6d279df1ad27382bb1a3b2893&)<br />
_Menu principal_

### 1. Affichage du Tableau de Contraintes
Le graphe mémorisé est généré sous forme de **tableau**, y compris les sommets fictifs 0 (α) et N+1 (ω).<br />
De même, le graphe est affiché sous forme de **triplets** pour une meilleure compréhension.

![Tableau de contraintes](https://cdn.discordapp.com/attachments/1222083642206060687/1229881122352140338/Screenshot_1_1.png?ex=66314b0d&is=661ed60d&hm=49c0593b03a90ebd4d06c194372392a9207eedfebae8cce2d071c140221bf430&)
![Affichage par triplets](https://cdn.discordapp.com/attachments/422113586597593088/1230088344990388305/Screenshot_1.png?ex=66320c0b&is=661f970b&hm=9c0ff0fc416e8b117396c5d6bbad9297ce5a3284ef338e8e32b4d9a40a3f295c&)<br />
_Tableau de contraintes et affichage sous forme de triplets_

### 2. Affichage Matriciel
Le graphe mémorisé est généré sous forme **matricielle**, y compris les sommets fictifs 0 (α) et N+1 (ω).

![Affichage matriciel](https://cdn.discordapp.com/attachments/1222083642206060687/1229883670949662750/Screenshot_3.png?ex=66314d6d&is=661ed86d&hm=1955062260d09e6bd5ca3289814b1c8391fec56691d04f9b5f8ed68f1487c1d5&)<br />
_Affichage matriciel_

### 3.1 Vérification des Propriétés du Graphe
Le graphe est examiné pour s'assurer que toutes les valeurs d'arc sont positives et qu'il ne contient pas de circuit.

![Vérification arc négatif](https://cdn.discordapp.com/attachments/1222083642206060687/1229887060698071191/Screenshot_7.png?ex=66315095&is=661edb95&hm=106a00905844223bc3cf088b13b26b42f28ca35e998b45e748a069faf18714fe&)<br />
_Vérification des arcs_
<br />


![Vérification des circuits](https://cdn.discordapp.com/attachments/1222083642206060687/1229884943111557230/Screenshot_5.png?ex=66314e9c&is=661ed99c&hm=7641dbe48174e401191f2ba27d8e84e5f47cb1447e0a6fafb6f9f162433c030c&)<br />
_Vérification de la présence de circuit_
<br />


Si aucun arc à valeur négative n'a été trouvé et que le graphe ne comporte aucun circuit, alors une proposition de **calcul des calendriers** est lancée _(cf. 3.2)_ :

![Proposition du calcul des calendriers](https://cdn.discordapp.com/attachments/1222083642206060687/1229884943459418122/Screenshot_6.png?ex=66314e9c&is=661ed99c&hm=49456bdb5f476e45034870e8432cae655998f5fde0b1c3a351b741e8e9ae7d9a&)<br />

### 3.2 Calcul des calendriers
Pour calculer les calendriers, l'algorithme aura d'abord besoin de **calculer les rangs** :

![Calcul des rangs 1](https://cdn.discordapp.com/attachments/1222083642206060687/1229893465983291492/Screenshot_10_1.png?ex=6631568c&is=661ee18c&hm=268335502323ff0cf362313224ca3e3ae4dc284c90c759091310514372b78d99&)
![Calcul des rangs 2](https://cdn.discordapp.com/attachments/1222083642206060687/1229893466285412423/Screenshot_11_1.png?ex=6631568c&is=661ee18c&hm=bfebfb5b6072b7be7cbc463681c9a20a05b5c814bf6f3c1e1caab7ae17e8a56b&)<br />
_Calcul des rangs_


Enfin, l'algorithme calcule les **dates au plus tôt**, les **dates au plus tard** ainsi que les **marges** et le **chemin critique** final.

![Calcul des calendriers](https://cdn.discordapp.com/attachments/422113586597593088/1230138852031729724/Screenshot_3.png?ex=66323b15&is=661fc615&hm=4e4acfe0156c0dd4abb7650b11c934becc0b3d6bcccd08f4f58bcd41fd26eac6&)
_Tableau des calendriers_


Pour un meilleur affichage, une fenêtre s'ouvre automatiquement dans le navigateur par défaut nous affichant le graphe et son chemin critique _(flèches rouges)_. 

![Affichage du graphe et de son chemin critique](https://cdn.discordapp.com/attachments/1222083642206060687/1229892638635986944/Screenshot_14.png?ex=663155c7&is=661ee0c7&hm=98c3af530224dd93a339c093923e799d1c35e60ee6bb64244a10c115bb7de9fb&)<br />
_Affichage du graphe et de son chemin critique_


### 4. BONUS : Affichage du graphe
Ne faisant par partie du cahier des charges du sujet, nous avons décidé d'importer un affichage graphique afin d'avoir une meilleure compréhension visuelle du graphe.

![Affichage du graphe](https://cdn.discordapp.com/attachments/1222083642206060687/1229893871022903409/Screenshot_15.png?ex=663156ed&is=661ee1ed&hm=5ba5fc4f1f43edad650caef784d46686e3b72d02dd7862ae800e899320b312e3&)<br />
_Affichage du graphe_

Note : dans certains cas d'égalité, le graphe peut posséder plusieurs chemins critiques. Ces cas sont pris en charge par l'algorithme qui annonce le nombre de chemins et précise lesquels, puis ouvre un affichage par chemin critique trouvé. 

### 5. Changer la table de contraintes
Pour éviter toute interruption du code, il est également possible de choisir une nouvelle table de contraintes à étudier.

![Affichage par triplets](https://cdn.discordapp.com/attachments/422113586597593088/1229912143504085122/Sequence_02_6.gif?ex=663167f1&is=661ef2f1&hm=ad1f7531012bd831358ecf1109053f7ff004abd6f1efcee3925a52813a6e053a&)<br />
_Changer la table de contraintes_
