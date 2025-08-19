import markdown2
import random
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "This page does not exist."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content)
    })
def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()

    if util.get_entry(query):
        return HttpResponseRedirect(reverse("entry", args=[query]))
    filtered = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": filtered
    })
def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if util.get_entry(title):
            return render(request, "encyclopedia/new.html", {
                "error": "An entry with this title already exists."
            })
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    return render(request, "encyclopedia/new.html")
def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "This page does not exist."
        })
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })
def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    return HttpResponseRedirect(reverse("entry", args=[random_title]))