# Bienvenue dans RC-Calc !
>:gb: English version available [here.](README.md) :gb:

Un calculateur ~~peut-être un jour~~ tout-en-un pour les multirotors, avions et autres appareils volants radio-commandés.

Ce projet vise à rassembler en un seul endroit les différents outils que j'ai réalisé sur des feuilles Excel, afin de pouvoir les partager de manière plus conviviale.

## Quelles fonctionnalités sont disponibles actuellement ?
> :warning: Il s'agit d'une version alpha, attendez-vous à des fonctionnalités très limitées et à des bugs !

Le programme se présente actuellement sous la forme d'un serveur web auto-hébergé. Lorsque le programme est lancé, il ouvre une interface ressemblant à un site web mais aucune donnée ne rentre ni ne sort de votre ordinateur.

Pour l'instant, RC-Calc vous permet de :
- Régler le nombre de mV/A de la sonde de tension pour avoir une mesure précise de la consommation d'énergie/courant. Pratique pour des vols long-range en toute sereinité !
- Configurer vos batteries : choisissez vos cellules, le nombre d'éléments en série et en parallèle et obtenez les caractéristiques de la batterie telles que la tension, le courant max, son énergie et autres. Utile pour se lancer dans la création de pack li-ion maison !

## Quelles fonctionnalités sont à prévoir ?
D'autres outils doivent encore être inclus dans ce programme et donneront les fonctionnalités suivantes :
- Un comparateur de batteries, pour mieux observer les différences de performances entre deux packs et faire le bon choix de cellules.
- Un carnet de vol, pour suivre ses temps et distance de vol et pouvoir déterminer rapidement si un nouvel équipement comme un changement de batterie, d'hélice ou autre a un impact sur les performances habituelles.

J'ai également d'autres outils en réserve mais ne suis pas sûr s'ils devraient être inclus, car ils sont très spéciques et ont donné des résultats limités pour l'instant. Par exemple : un calculateur de centre de gravité pour ailes volantes.

Si vous avez des idées d'améliorations, veuillez s'il vous plait consulter la [section contribution](#Contribution).

Aussi, s'il y a une demande pour cela, je pourrais éventuellement héberger le programme en ligne.

## Démarrage

### Installation

Pour l'instant, deux méthodes sont disponibles pour utiliser cet outil :

1. **Depuis le code source** (toutes plateformes) : Ce projet a été codé en Python 3. Tout ce dont vous avez besoin est de télécharger le code source, vous assurez que vous avez Python 3 d'installé ainsi que tous les packages mentionnés dans *[requirements.txt](requirements.txt)* et de lancer le fichier *RC_Calc.py*.
1. **En utilisant la version compilée** (Windows uniquement) : Pour faciliter l'utilisation, une version compilée est disponible pour n'avoir qu'à lancer *RC_Calc.exe* sans installation d'autres logiciels au préalable.

:arrow_forward: Téléchargez les dernières versions stables de ces fichiers sur la [releases page](https://github.com/Gregczc/RC-Calc/releases).:arrow_backward:

Attention, RC-Calc construit une base de données dans le dossier *db*. Pensez à sauvegarder ce dossier lorsque vous téléchargez une version plus récente de RC-Calc.

### Documentation

Une documentation détaillée avec Sphinx est en cours de rédaction.

## Contribution

Un grand merci à [@raymas](https://github.com/raymas) pour son aide dans ce projet !

Si vous avez des idées de fonctionnalités à rajouter dans ce programme, n'hésitez pas à ouvrir une issue. Si vous n'êtes pas familiers avec GitHub, vous pouvez également me contacter par [facebook](https://www.facebook.com/gregoire.cahuzac/) ou par mail (gregoire.cahuzac@outlook.fr).

S'il vous plaît, gardez à l'esprit que je ne suis pas prgrammeur professionnel. Je fais juste ça pendant mon temps libre, pour m'améliore en programmation et à l'utilisation de GitHub !

### Libraries utilisées

[Bootstrap](https://getboostrap.com) : pour l'interface utilisateur  
[Bootstrap-table](https://bootstrap-table.com) : pour les tableaux triables  
[Font Awesome](https://fontawesome.com) : pour les icônes



