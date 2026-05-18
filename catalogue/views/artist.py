from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from catalogue.forms import ArtistForm
from catalogue.models import Artist


def index(request):
    query = request.GET.get("q", "").strip()
    artists = Artist.objects.all().order_by("lastname", "firstname")
    if query:
        artists = artists.filter(
            Q(firstname__icontains=query)
            | Q(lastname__icontains=query)
        )
    paginator = Paginator(artists, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "artist/index.html", {
        "artists": page_obj,
        "page_obj": page_obj,
        "title": "Liste des artistes",
        "query": query,
        "pagination_query": f"q={query}",
    })


def show(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    return render(request, "artist/show.html", {
        "artist": artist,
        "title": "Fiche d'un artiste",
    })


@login_required
@permission_required("catalogue.add_artist", raise_exception=True)
def create(request):
    form = ArtistForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Nouvel artiste cree avec succes.")
            return redirect("catalogue:artist-index")
        messages.error(request, "Echec de l'ajout d'un nouvel artiste.")

    return render(request, "artist/create.html", {"form": form})


@login_required
@permission_required("catalogue.change_artist", raise_exception=True)
def edit(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)
    form = ArtistForm(request.POST or None, instance=artist)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Artiste modifie avec succes.")
        return redirect("catalogue:artist-show", artist_id=artist.id)

    return render(request, "artist/edit.html", {
        "form": form,
        "artist": artist,
    })


@login_required
@permission_required("catalogue.delete_artist", raise_exception=True)
def delete(request, artist_id):
    artist = get_object_or_404(Artist, id=artist_id)

    if request.method == "POST" and request.POST.get("_method", "").upper() == "DELETE":
        artist.delete()
        messages.success(request, "Artiste supprime avec succes.")
        return redirect("catalogue:artist-index")

    messages.error(request, "Echec de la suppression de l'artiste.")
    return redirect("catalogue:artist-show", artist_id=artist.id)
