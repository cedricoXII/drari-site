# Drari · site

Le site de Drari : les petits transporteurs Europe-Maghreb et les familles de la diaspora.

## Comment ça marche

- Le projet « Drari » dans Aura contient une petite page de chargement.
- Cette page va chercher `index.html` dans ce dépôt, à une version précise (un tag, par exemple `v0.1.0`), puis l'affiche à sa place.
- Elle passe par jsDelivr, et par GitHub en secours.
- Dans `index.html`, `__DRARI_BASE__` et `__DRARI_RAW__` sont remplacés par l'adresse de ce dépôt au moment du chargement.

Pour mettre en ligne une nouvelle version : créer un nouveau tag ici, puis changer le tag dans la page Aura.

## Versions

- `v0.1.0` : copie du template Fold Line, telle quelle. Les photos des guides sont hébergées ici.

## Crédits

- Base : template « Fold Line » de Sam (samaing1983), sur Aura, inclus dans l'abonnement Pro.
- Three.js (licence MIT), GSAP et ScrollTrigger (licence standard GSAP), Lenis.
- Tracés : OpenStreetMap. Reliefs : AWS Terrain Tiles.
