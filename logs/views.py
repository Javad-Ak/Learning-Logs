from django import http
from django.shortcuts import render, redirect
from django.urls.exceptions import NoReverseMatch

from .forms import *
from .models import Topic
from django.contrib.auth.decorators import login_required


def index(request):
    """The home page for Learning Log."""
    return render(request, 'logs/index.html')


def topics(request):
    """Show all topics."""
    objects = Topic.objects.order_by('date_added').reverse()
    if objects:
        objects.reverse()

    context = {'topics': objects}
    return render(request, 'logs/topics.html', context)


def topic(request, topic_id):
    """Show topic's details."""
    obj = Topic.objects.get(id=topic_id)

    if request.method == "POST" and request.POST.get("_method") == "DELETE":
        if request.user != obj.owner:
            raise http.Http404("You are not allowed.")

        obj.delete()
        return render(request, 'logs/topics.html', {"topics": Topic.objects.all()})
    else:
        objects = obj.entry_set.order_by('date_added').reverse()
        context = {'topic': obj, 'entries': objects}
        return render(request, 'logs/topic.html', context)


@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('logs:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)

    if request.user != topic.owner:
        raise http.Http404("You are not allowed.")

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('logs:topic', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.user != topic.owner:
        raise http.Http404("You are not allowed.")

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'logs/edit_entry.html', context)
