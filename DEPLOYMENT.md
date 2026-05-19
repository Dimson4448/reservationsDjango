# Deploiement Ultimate SPT

## Preparation

1. Copier `.env.example` vers `.env`.
2. Modifier les variables de production :
   - `DJANGO_SECRET_KEY`
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS`
   - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
   - les variables `DJANGO_SECURE_*` si le site est servi en HTTPS
   - `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY` et `STRIPE_PAYMENT_METHOD_TYPES` pour le paiement
3. Installer les dependances :

```powershell
pip install -r requirements.txt
```

4. Appliquer les migrations :

```powershell
python manage.py migrate
```

5. Collecter les fichiers statiques si le serveur le demande :

```powershell
python manage.py collectstatic
```

6. Verifier le projet :

```powershell
python manage.py check --deploy
python manage.py test --noinput
```

## Verification apres deploiement

- ouvrir la page d'accueil ;
- verifier `GET /health/` ;
- ouvrir la liste des spectacles ;
- tester une fiche spectacle ;
- tester la connexion ;
- tester une reservation ;
- tester le panier et un paiement Stripe en mode test ;
- tester l'annulation asynchrone d'une reservation ;
- tester l'admin Django.

## Points de vigilance

- ne jamais versionner le fichier `.env` ;
- garder `DJANGO_DEBUG=False` en production ;
- renseigner le domaine reel dans `DJANGO_ALLOWED_HOSTS` ;
- activer `DJANGO_SECURE_SSL_REDIRECT`, `DJANGO_SESSION_COOKIE_SECURE` et `DJANGO_CSRF_COOKIE_SECURE` en production HTTPS ;
- sauvegarder regulierement la base avec `mysqldump`.
- activer et tester les moyens de paiement Stripe voulus : carte, Bancontact et Klarna.
