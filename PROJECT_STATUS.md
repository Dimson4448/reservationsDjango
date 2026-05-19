# Etat du projet Ultimate SPT

Derniere mise a jour : 19 mai 2026.

## Fonctionnalites realisees

- Frontend Django coherent avec le nom Ultimate SPT.
- Page d'accueil avec image plein ecran.
- Catalogue des spectacles avec recherche, filtres et pagination.
- Catalogue des artistes avec recherche et pagination.
- Fiche spectacle avec representations, tarifs, disponibilite et avis valides.
- Reservation utilisateur avec validation de quantite et controle des tarifs.
- Panier avant paiement avec integration Stripe Checkout preparee pour carte, Bancontact et Klarna.
- Webhook Stripe pour confirmer les paiements cote serveur.
- Confirmation de reservation et billet imprimable uniquement apres paiement confirme.
- Profil utilisateur avec historique, filtre par statut et annulation asynchrone.
- API REST avec JWT pour les principales ressources.
- Tableau de bord staff avec statistiques.
- Gestion staff des reservations avec filtre, pagination, annulation et reactivation.
- Moderation staff des avis avec validation.
- Export CSV des reservations.
- Administration Django personnalisee et harmonisee avec le style du site.
- Configuration de deploiement preparee, sans deploiement effectif.
- Route `/health/` disponible pour une verification rapide de l'application.
- Tests automatises pour les parcours principaux.

## Points a verifier manuellement

- Tester une reservation complete avec un compte utilisateur.
- Tester le panier et un paiement Stripe en mode test.
- Tester le webhook Stripe avec la CLI Stripe ou le tableau de bord Stripe.
- Tester l'impression du billet.
- Tester la validation d'un avis avec un compte staff.
- Tester l'export CSV depuis le tableau de bord staff.
- Tester l'admin Django sur `/admin/`.
- Relire les textes visibles sur mobile et desktop.

## Avant fusion `api` vers `main`

Executer :

```powershell
.\venv312\Scripts\python.exe manage.py check
.\venv312\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv312\Scripts\python.exe manage.py test --noinput
```

Ensuite, fusionner uniquement si le site est valide fonctionnellement.

## Avant deploiement

- Completer `.env` a partir de `.env.example`.
- Mettre `DJANGO_DEBUG=False`.
- Renseigner `DJANGO_ALLOWED_HOSTS`.
- Verifier la base de donnees de production.
- Lancer `collectstatic` si l'hebergeur le demande.
- Lancer `python manage.py check --deploy`.
