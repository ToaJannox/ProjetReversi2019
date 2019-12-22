MONTFERME Robin
VIGNEAU Paul

Projet Reversi 2019-2020.
Description de l'IA:

Algorithme d'exploration utilisé:
Nega Alpha-Beta avec coupure et  atténuation d'horizon

Description de l'heurisitique:
L'heurisitique permet d'évaluer le plateau en calculant:
-Le nombre de coins possèdé
-La mobilité de chaque joueur (le nombre de mouvements possible par joueur pour un plateau)
-Le score de stabilité de chaque joueur. La stabilité d'une pièce est  la possiblité qu'une pièce à d'être retournée 
 ou pas si après le mouvement d'un joueur. Si une pièce ne peut être retournée alors elle est stable. Elle sera instable sinon.
 On veut donc savoir pour chaque joueur le nombre de pièce stable qu'il possède.
On différencie chaque joueur en multipliant par 1 les valeurs pour le joueur ami et par -1 les valeurs du joueur ennemi.

On multiplie par 100 chacune de ces valeurs et ont les additionne. On retourne ce résultat comme valeur heurisitique.

Si la partie est terminée on renvoies la valeur de parité (le nombre de pièces possèdé selon le joueur).

Mécanismes supplémentaires mis en place:

-Utilisation du module multi-processing afin de réaliser les calculs en parallèle. Le nombre de thread
créer dépend du nombre de coeur disponible sur la machine.

-Utilisation d'une table de transposition. On note dans une table de transposition un hash du plateau actuel. Cela permet de garder en mémoire
les valeurs d'heurisitique déjà calculées pour un mouvement. Cette table est utile si on permet une exploration profonde de l'arbre.

-Limitation en temps. Un mécansime à été mis en place pour permettre d'éviter les dépassement en temps de l'IA.
Si l'IA mets un temps conséquent pour jouer un coup alors au tour suivant elle diminuera sa profondeur d'exploration.