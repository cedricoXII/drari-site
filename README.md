# Drari · site

Le site de Drari : les petits transporteurs Europe-Maghreb et les familles de la diaspora.

## Comment ça marche

- Le projet « Drari » dans Aura contient une petite page de chargement (copie dans `aura/index.html`).
- Cette page va chercher `index.html` dans ce dépôt, à une version précise (le numéro d'un commit), puis l'affiche à sa place.
- Elle passe par jsDelivr, et par GitHub en secours.
- Dans `index.html`, `__DRARI_BASE__` et `__DRARI_RAW__` sont remplacés par l'adresse de ce dépôt au moment du chargement.

Pour mettre en ligne une nouvelle version : mettre le numéro du nouveau commit dans `VERSION`, dans la page Aura.

## Construire

`index.html` est fabriqué, il ne se modifie pas à la main :

1. `tools/make_routes.py` écrit `data/treks-data.js` (les 5 trajets, textes et sources en tête du fichier).
2. `tools/make_terrain.py` écrit `data/terrain-data.js` (le relief des 5 cartes, d'après ETOPO).
3. `tools/build.py` part du template (`base/fold-line-v7.html`), y met les données et applique les remplacements de `tools/patches.py`.

Les deux premiers scripts lisent ETOPO 10' converti en `.npz` (fichier non versionné, 45 Mo à l'origine).

## Versions

- v0.1 (commit `3d2c35a`) : copie du template Fold Line, telle quelle.
- v0.2 (commit `7a16baa`) : haut de page Drari, en français. Les 5 cartes deviennent 5 trajets (Marseille → Tunis, Marseille → Oran, Paris → Tanger, Bruxelles → Nador, Amsterdam → Agadir), avec leur vrai relief. Le globe pointe les destinations. La plongée dans l'épingle est coupée pour l'instant. Le bas de page est encore celui du template, en anglais.

- v0.3 (commit `033325d`) : bas de page en français (traversées, inclus, transporteurs, quand partir, FAQ, inscription, pied de page). Les cartes des transporteurs sont des exemples vides : pas de faux profils. Les formulaires n'envoient encore rien (ils le disent), et l'adresse email du pied de page est provisoire.

- v0.4 (commit `05185dd`) : décors Drari. Le randonneur devient une camionnette chargée (dans la page et sur la table en papier). Section 01 : un ferry sur la mer, le rocher de Gibraltar avec la médina de Tanger et un petit ferry, l'Atlas avec une kasbah. Pied de page : la maison et la camionnette garée.

À faire : brancher l'envoi des formulaires, une vraie adresse email et les vrais comptes, puis la plongée dans le trajet (camionnette à la place du randonneur, ferry). En v0.2, les clés internes des trajets restent celles du template (`tongariro`, `inca`…), pour ne rien casser.

## Crédits

- Base : template « Fold Line » de Sam (samaing1983), sur Aura, inclus dans l'abonnement Pro.
- Three.js (licence MIT), GSAP et ScrollTrigger (licence standard GSAP), Lenis.
- Reliefs des trajets : ETOPO 10' (NOAA, domaine public). Tracés du template : OpenStreetMap ; reliefs du template : AWS Terrain Tiles.
