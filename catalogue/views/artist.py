from django.shortcuts import render, redirect
from django.http import Http404

from catalogue.models import Artist
from catalogue.forms import ArtistForm


def index(request):
    artists = Artist.objects.all()
    title = 'Liste des artistes'
    return render(request, 'artist/index.html', {
        'artists': artists,
        'title': title
    })


def show(request, artist_id):
    try:
        artist = Artist.objects.get(id=artist_id)
    except Artist.DoesNotExist:
        raise Http404('Artist inexistant')

    title = 'Fiche d\'un artiste'
    return render(request, 'artist/show.html', {
        'artist': artist,
        'title': title
    })


def create(request):
    form = ArtistForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('catalogue:artist-index')

    return render(request, 'artist/create.html', {
        'form': form,
    })


def edit(request, artist_id):
    # Récupération de l'objet à modifier
    artist = Artist.objects.get(id=artist_id)

    # Passage de l'objet comme instance dans le formulaire
    form = ArtistForm(request.POST or None, instance=artist)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'PUT':
            if form.is_valid():
                form.save()
                return render(request, "artist/show.html", {
                    'artist': artist,
                })

    return render(request, 'artist/edit.html', {
        'form': form,
        'artist': artist,
    })
