# Black hole explorer

🚧 Projet en cours, ceci n'est pas la version finale 🚧

## Objectif

Le but de ce projet est d'extraire, transformer et collecter les données de sondes spatiales pour ensuite faire de l'analyse exploratoire afin de reconnaître ce qui différencie les quasars des étoiles.
Ensuite, développer un modèle ML pour prédire si l'objet observé est un quasar en fonction de ses données.


### Ce qu'il faut savoir

Les quasars sont des **trous noirs supermassifs**, souvent au centre d'une galaxie, qui accrètent **du gaz et de la poussière** chauffées à très haute température qui émettent de la lumière très énergétique et brillante.
De tels objets n'existent que très loin de notre galaxie, et ont autant de **magnitude** (luminosité apparente) que les étoiles environnantes.
Ceci dit, ces objets ont des particularités par rapport aux étoiles : Leur spectre électromagnetique tend vers le **bleu/violet** ainsi que les **hauts infrarouges**, et leur distance est si grande qu'ils paraissent presque immobiles même avec la méthode de la **parallaxe**.
L'infrarouge, le bleu et la parallaxe seront donc nos principaux KPIs pour identifier les quasars.


### Jeux de données

J'utilise les catalogues suivants : 
- **SDSS** : cette sonde observe les objets dans le domaine visible
- **WISE** : cette sonde observe les objets dans le domaine de l'infrarouge
- **Gaia** : cette sonde observe la distance et le mouvement des objets


### Étapes clés

1 : Requêtes SQL directement sur le site du catalogue SDSS (http://skyserver.sdss.org) 
    On essaie d'avoir autant d'étoiles que de quasars

2 : Jointure du dataset WISE par cross-matching grâce aux coordonnées ra/dec qui sont nos repères dans l'espace

3 : Jointure du dataset Gaia également par cross-matching avec les coordonnées

4 : Création de colonnes qui seront nos KPIs pour identifier les quasars (forte couleur bleue, hauts infrarouges, lointain)

5 : Entrainement du modèle machine learning pour reconnaître la signature visuelle des quasars

6 : Appliquer ce modèle sur des données de potentiels quasars 


### Aperçu de l'analyse exploratoire

`W1-W2(infrarouge), u-g(bleu) et parallaxe(distance) pour chaque classe "STAR" (étoile) et "QSO" (quasar).
Ces graphiques nous permettent de comprendre les différences observables entre ces deux types d'objet
Ils prouvent aussi que ces données seront très utiles au modèle ML`

[Pairplot](assets/pairplot.png)

Dans ce pairplot, on observe des tendances distinctes entre les étoiles et les quasars.

**W1-W2 :** Plus la valeur est haute, plus l'objet tend vers le "haut infrarouge"
**U-G :** Plus la valeur est basse, plus l'objet tend vers le bleu.

_La tendance des étoiles :_ 
Valeurs (W1-W2) faible & (u-g) élevée : bas infrarouge + couleur moins bleue

_La tendance des quasars:_
Valeurs (W1-W2) élevée & (u-g) faible : haut infrarouge + couleur bleue

👉 [Consulter le Notebook détaillé](notebooks/eda2.ipynb)






Flo
Avril 2026