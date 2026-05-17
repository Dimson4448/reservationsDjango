# Ultimate SPT - Release v1.1.0

## Objectif

Premiere version exploitable du projet personnel Ultimate SPT sur la branche `api`.

Cette release pose le socle du site de reservation de spectacles en ligne avec une interface web Django, un debut d'API REST et les tests principaux du jour 1.

## Nouveautes

- Branding public renomme en `Ultimate SPT`.
- Page d'accueil Django pour presenter le catalogue de spectacles.
- Liste et detail des spectacles.
- Parcours de reservation depuis une representation.
- Pages de connexion, inscription, profil et gestion du compte.
- Gestion des artistes cote interface web.
- API REST pour les artistes.
- Authentification JWT pour l'API.
- Administration Django enrichie.
- Documentation de demarrage dans le README.

## Technique

- Backend : Django 5.0.14.
- API : Django REST Framework 3.16.1.
- Authentification API : Simple JWT 5.5.1.
- Base de donnees locale : MySQL selon la configuration du projet.
- Dossiers locaux exclus du depot : environnements virtuels, caches Python, base locale, `mysql/` et `PID_Groupe3/`.

## Verification

Commandes validees localement :

```powershell
.\venv312\Scripts\python.exe manage.py check
.\venv312\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv312\Scripts\python.exe manage.py test --noinput
```

Resultat :

- system check OK ;
- aucune migration manquante ;
- 8 tests OK.

## Points a continuer

- Ajouter une interface plus complete pour le choix des places et des tarifs.
- Ameliorer le design responsive.
- Ajouter plus de controles sur les reservations.
- Etendre l'API aux spectacles, representations et reservations.
- Ajouter des donnees de demonstration propres pour les tests utilisateur.
