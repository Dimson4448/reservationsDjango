# Ultimate SPT

Projet personnel de reservation de spectacles en ligne.

## Branche `api`

Cette branche contient la version de travail actuelle avec :

- catalogue des spectacles avec recherche, filtres et pagination ;
- liste et fiches artistes ;
- detail d'un spectacle avec representations, tarifs et avis valides ;
- formulaire de reservation securise depuis une representation ;
- panier avant paiement avec Stripe Checkout ;
- paiement prepare pour carte bancaire, Bancontact et Klarna ;
- page de confirmation et billet imprimable apres paiement ;
- profil utilisateur avec historique, filtre par statut et annulation asynchrone ;
- tableau de bord staff avec statistiques, gestion des reservations, moderation des avis et export CSV ;
- administration Django personnalisee aux couleurs du site ;
- API REST pour les artistes, spectacles, representations, reservations et avis ;
- authentification JWT pour l'API ;
- tests backend pour les routes, formulaires, parcours web, API et admin.

Le dossier `PID_Groupe3/` est ignore et ne fait pas partie de ce projet personnel.

## Installation locale

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Avec l'environnement local deja present sur ce poste, les commandes de verification sont lancees avec :

```powershell
.\venv312\Scripts\python.exe manage.py check
.\venv312\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv312\Scripts\python.exe manage.py test --noinput
```

## Dump SQL

Un dump SQL de la base de developpement est disponible dans :

```text
database_dumps/reservations_2026-05-18.sql
```

Pour restaurer la base MySQL locale :

```powershell
mysql --host=127.0.0.1 --port=3307 --user=root reservations < database_dumps\reservations_2026-05-18.sql
```

## Deploiement

La configuration sensible est lue depuis un fichier `.env` non versionne.
Un exemple est disponible dans `.env.example`.

Les consignes de deploiement et de verification sont dans `DEPLOYMENT.md`.

## Paiement

Le paiement en ligne est prepare avec Stripe Checkout.

Variables a renseigner dans `.env` :

```text
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_CURRENCY=eur
STRIPE_PAYMENT_METHOD_TYPES=card,bancontact,klarna
```

Parcours :

1. Le client reserve une representation.
2. La reservation est placee dans le panier avec le statut `pending`.
3. Le client paie via Stripe Checkout.
4. Apres paiement confirme par retour Checkout ou webhook Stripe, la reservation passe en `confirmed` et `paid`.
5. Le billet devient accessible.

## Endpoints utiles

- `GET /` : accueil
- `GET /about/` : presentation du projet
- `GET /health/` : verification rapide de l'etat de l'application
- `GET /catalogue/show/` : liste des spectacles
- `GET /catalogue/show/<id>` : detail d'un spectacle
- `GET /catalogue/artist/` : liste des artistes
- `GET /catalogue/artist/<id>` : detail d'un artiste
- `GET|POST /catalogue/representation/<id>/reserve` : creation d'une reservation
- `GET /catalogue/reservation/<id>/cart` : panier avant paiement
- `POST /catalogue/reservation/<id>/payment` : creation de la session de paiement Stripe
- `GET /catalogue/reservation/<id>/payment/success` : validation du retour paiement
- `GET /catalogue/reservation/<id>/confirmation` : confirmation de reservation
- `GET /catalogue/reservation/<id>/ticket` : billet imprimable
- `POST /catalogue/reservation/<id>/cancel` : annulation d'une reservation
- `GET /catalogue/dashboard/` : tableau de bord staff
- `GET /catalogue/dashboard/reservations/` : gestion staff des reservations
- `GET /catalogue/dashboard/reviews/` : moderation staff des avis
- `GET /catalogue/dashboard/reservations/export/` : export CSV des reservations
- `GET|POST /catalogue/api/artists/` : liste et creation d'artistes
- `GET|PUT|PATCH|DELETE /catalogue/api/artists/<id>/` : detail, modification et suppression d'un artiste
- `GET /catalogue/api/shows/` : liste des spectacles
- `GET /catalogue/api/shows/<id>/` : detail d'un spectacle
- `POST /catalogue/api/shows/<id>/reviews/` : soumission d'un avis sur un spectacle
- `GET /catalogue/api/representations/` : liste des representations
- `GET|POST /catalogue/api/reservations/` : liste et creation des reservations de l'utilisateur connecte
- `POST /catalogue/api/reservations/<id>/cancel/` : annulation d'une reservation de l'utilisateur connecte
- `POST /catalogue/api/token/` : obtention d'un token JWT
- `POST /catalogue/api/token/refresh/` : renouvellement du token JWT

## Checklist avant fusion vers `main`

Avant de fusionner `api` vers `main`, verifier :

- navigation publique : accueil, a propos, spectacles, artistes ;
- compte utilisateur : inscription, connexion, profil, changement de mot de passe ;
- reservation : creation, panier, paiement test, confirmation, billet imprimable, annulation ;
- staff : tableau de bord, export CSV, moderation des avis, gestion des reservations ;
- administration Django : affichage, listes, recherche et formulaires ;
- API : authentification JWT et endpoints principaux ;
- commandes finales :

```powershell
.\venv312\Scripts\python.exe manage.py check
.\venv312\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv312\Scripts\python.exe manage.py test --noinput
```

La fusion vers `main` doit etre faite uniquement apres validation manuelle du site complet.

