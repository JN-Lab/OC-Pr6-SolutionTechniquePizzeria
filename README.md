# OC-Pr6-SolutionTechniquePizzeria
Repository du projet-6 du parcours Développeur d'Application Python (Openclassrooms)

## Présentation
« OC Pizza » est un jeune groupe de pizzeria en plein essor et spécialisé dans les pizzas livrées ou à emporter. Il compte déjà 5 points de vente et prévoit d’en ouvrir au moins 3 de plus d’ici la fin de l’année. Un des responsables du groupe a pris contact avec vous afin de mettre en place un système informatique, déployé dans toutes ses pizzerias et qui lui permettrait notamment :

d’être plus efficace dans la gestion des commandes, de leur réception à leur livraison en passant par leur préparation ;
de suivre en temps réel les commandes passées et en préparation ;
de suivre en temps réel le stock d’ingrédients restants pour savoir quelles pizzas sont encore réalisables ;
de proposer un site Internet pour que les clients puissent :
passer leurs commandes, en plus de la prise de commande par téléphone ou sur place
payer en ligne leur commande s’ils le souhaitent – sinon, ils paieront directement à la livraison
modifier ou annuler leur commande tant que celle-ci n’a pas été préparée
de proposer un aide mémoire aux pizzaiolos indiquant la recette de chaque pizza
d’informer ou notifier les clients sur l’état de leur commande
Le client a déjà fait une petite prospection et les logiciels existants qu’il a pu trouver ne lui conviennent pas.

## Objectif
Il s'agit de définir le domaine fonctionnel et concevoir l'architecture technique de la solution répondant aux besoins du client.

## Organisation du repository
Le repository est organisé pour rassembler l'ensemble des éléments à fournir pour ce projet:

* deliverables
* SQL_requests
* python_datafeed_pgr

## Installer la base de données
Pour installer la base de données, il suffit d'exécuter le fichier **p6_database.sql** qui se trouve dans le répertoire **SQL_requests**. Ce dernier contient l'ensemble des scripts SQL pour créer les tables et l'ensemble des clefs associées à la base de donnée **p6_project**

## Injecter de la donnée test dans la base de données
Pour injecter de la donnée test dans la base de données et réaliser des tests, il suffit d'exécuter dans le terminal le programme python présent dans le répertoire **python_datafeed_pgr**.

```
python3 main.py
```

## Informations supplémentaires

### Requêtes de sélections test
Quelques requêtes de sélections sont présentées dans le fichier **test_requests.sql** présent dans le répertoire **SQL_requests**.

### Packages utilisées
Les packages supplémentaires utilisés et présents dans le fichier requirements.txt sont:

* pylint
* pymysql
* faker
