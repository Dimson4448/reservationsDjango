# Reservations Django

Projet personnel de reservation de spectacles en ligne.

## Branche `api`

Cette branche contient le socle du jour 1 avec :

- catalogue des spectacles et detail d'un spectacle ;
- formulaire de reservation depuis une representation ;
- pages d'authentification, profil et gestion de compte ;
- administration Django enrichie ;
- API REST pour les artistes avec permissions ;
- authentification JWT pour l'API ;
- tests backend pour le parcours web et l'API.

Le dossier `PID_Groupe3/` est ignore et ne fait pas partie de ce projet personnel.

## Installation locale

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Avec l'environnement local deja present sur ce poste, les commandes de verification ont ete lancees avec :

```powershell
.\.virtualenvs\djangodev\Scripts\python.exe manage.py check
.\.virtualenvs\djangodev\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.virtualenvs\djangodev\Scripts\python.exe manage.py test --noinput
```

## Endpoints utiles

- `GET /` : accueil
- `GET /shows/` : liste des spectacles
- `GET /shows/<id>` : detail d'un spectacle
- `GET|POST /representation/<id>/reserve` : creation d'une reservation
- `GET|POST /api/artists/` : liste et creation d'artistes
- `GET|PUT|PATCH|DELETE /api/artists/<id>/` : detail, modification et suppression d'un artiste
- `POST /api/token/` : obtention d'un token JWT
- `POST /api/token/refresh/` : renouvellement du token JWT

