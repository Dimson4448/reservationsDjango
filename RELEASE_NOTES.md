# Ultimate SPT - Release v1.2.0

## Objectif

Version de travail avancee du projet personnel Ultimate SPT sur la branche `api`.

Cette release couvre le parcours principal d'un site de reservation de spectacles : consultation du catalogue, compte utilisateur, reservation, billet, espace staff, API REST et administration Django personnalisee.

## Nouveautes principales

- Branding public stabilise sur `Ultimate SPT`.
- Page d'accueil avec image plein ecran et style coherent.
- Page `A propos` pour presenter le projet.
- Liste des spectacles avec recherche, filtre par disponibilite et pagination.
- Liste des artistes avec recherche et pagination.
- Fiche spectacle avec representations, lieu, tarifs, disponibilite et avis valides.
- Creation de reservation avec validation de quantite et controle du tarif choisi.
- Panier avant paiement avec preparation Stripe Checkout pour carte bancaire, Bancontact et Klarna.
- Webhook Stripe pour confirmer le paiement meme si l'utilisateur ne revient pas correctement sur le site.
- Page de confirmation apres paiement.
- Billet imprimable uniquement apres paiement confirme.
- Profil utilisateur avec historique, filtre par statut et annulation asynchrone.
- Avis utilisateur soumis en attente de validation.

## Espace staff

- Tableau de bord staff avec statistiques principales.
- Gestion staff des reservations avec filtre, pagination, annulation et reactivation.
- Export CSV des reservations.
- Moderation staff des avis en attente.
- Listes staff paginees pour garder l'interface utilisable avec plus de donnees.

## Administration Django

- Branding admin `Ultimate SPT Administration`.
- Theme admin harmonise avec les couleurs du site public.
- Raccourcis admin vers le site, le tableau de bord, les reservations et les avis.
- Listes admin enrichies pour spectacles, reservations, avis, lieux, tarifs et liaisons spectacle/tarif.
- Champs relationnels en recherche autocomplete.
- Champs calcules et dates sensibles en lecture seule.

## API

- Authentification JWT.
- Endpoints artistes.
- Endpoints spectacles.
- Endpoints representations.
- Endpoints reservations utilisateur.
- Endpoint d'annulation de reservation.
- Endpoint de creation d'avis sur un spectacle.
- URL de confirmation retournee apres creation de reservation par API.

## Technique

- Backend : Django 5.0.14.
- API : Django REST Framework 3.16.1.
- Authentification API : Simple JWT 5.5.1.
- Base locale : MySQL/MariaDB selon la configuration du projet.
- Configuration sensible preparee via `.env` et `.env.example`.
- Documentation de deploiement disponible dans `DEPLOYMENT.md`.
- Etat projet et checklist finale disponibles dans `PROJECT_STATUS.md`.
- Le dossier `PID_Groupe3/` reste exclu du travail sur ce projet personnel.

## Verification

Commandes validees localement :

```powershell
.\venv312\Scripts\python.exe manage.py check
.\venv312\Scripts\python.exe makemigrations --check --dry-run
.\venv312\Scripts\python.exe manage.py test --noinput
```

Resultat :

- system check OK ;
- aucune migration manquante ;
- 71 tests OK.

## Points restants avant fusion vers `main`

- Test manuel complet du parcours public.
- Test manuel du parcours utilisateur : inscription, connexion, reservation, billet, annulation.
- Test manuel du parcours staff : tableau de bord, moderation, export CSV, gestion des reservations.
- Validation visuelle finale de l'admin Django.
- Fusion `api` vers `main` uniquement apres confirmation explicite.

## Points restants avant deploiement

- Choisir l'hebergeur.
- Completer le fichier `.env` de production.
- Configurer `DJANGO_ALLOWED_HOSTS`.
- Passer `DJANGO_DEBUG=False`.
- Lancer `collectstatic` si necessaire.
- Lancer `python manage.py check --deploy`.
