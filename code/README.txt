MONTFERME Robin
VIGNEAU Paul

Projet Reversi 2019-2020.

Description de l'IA :

Algorithme d'exploration utilisé :
Nega Alpha-Beta avec coupures et atténuation d'horizon

Description de l'heurisitique :
L'heurisitique permet d'évaluer le plateau en calculant :
- Le nombre de coins possédés
- La mobilité de chaque joueur (le nombre de mouvements possible par joueur pour un état du plateau)
- Le score de stabilité de chaque joueur. La stabilité d'une pièce est la possiblité qu'une pièce a d'être retournée
  ou pas après le mouvement d'un joueur. Si une pièce ne peut être retournée alors elle est stable. Sinon elle est instable.
  On veut donc savoir pour chaque joueur le nombre de pièce stable qu'il possède.

On différencie chaque joueur en multipliant par 1 les valeurs pour le joueur ami et par -1 les valeurs du joueur ennemi.
(Certains détails sont précisés dans des commentaires dans le fichier Evaluator.py)

On multiplie par 100 chacune de ces valeurs et on les additionne. On retourne ce résultat comme valeur de l'heurisitique.

Si la partie est terminée on renvoie la valeur de parité (le nombre de pièces possédées selon le joueur).

Mécanismes supplémentaires mis en place :

- Utilisation du module multi-processing afin de réaliser les calculs en parallèle. Le nombre de threads
  créés dépend du nombre de coeurs disponibles sur la machine.

- Utilisation d'une table de transposition. On note dans une table de transposition un hash du plateau actuel.
  Cela permet de garder en mémoire les valeurs d'heurisitique déjà calculées pour un mouvement. Cette table est utile
  si on permet une exploration profonde de l'arbre.

- Limitation en temps. Un mécansime a été mis en place pour permettre d'éviter les dépassements en temps de l'IA.
  Lors du championnat, le temps de réflexion est de 5 minutes maximum pour chaque joueur au total sur la partie. Pour
  éviter de dépasser, à partir d'un certain seuil, la profondeur d'exploration de l'arbre diminue pour accélérer les
  temps de calculs.

- Bibliothèque d'ouverture. Comme dans plusieurs jeux de plateaux, il existe une bibliothèque d'ouverture qui dicte les
  les coups qu'il est intelligent de jouer en fonction des précédents coups jusqu'à un certain niveau. Nous avons donc
  implémenté une bibliothèque (qui est adaptée à la configuration du plateau, car différente des règles de bases)
  afin d'accélérer les temps de calcul en début de partie.