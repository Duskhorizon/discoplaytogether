from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import EventForm
from .models import Event, Participation


@login_required
def homepage(request):
    events = Event.objects
    return render(request, 'main.html', {'events': events})


@login_required
def create(request):
    if request.method == "POST":
        formset = EventForm(request.POST)
        if formset.is_valid():
            event = formset.save(commit=False)
            event.creator = request.user
            part = Participation(player=request.user, event=event, notify=True)
            event.save()
            part.save()
            return redirect('homepage')
    else:
        formset = EventForm()
    return render(request, 'create.html', {'formset': formset})


@login_required
def participate(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, pk=event_id)
        if request.user in event.players.all():
            part_to_clear = Participation.objects.get(player=request.user, event=event)
            part_to_clear.delete()
        else:
            if 'notify' in request.POST:
                part = Participation(player=request.user, event=event, notify=True)
                part.save()
            else:
                part = Participation(player=request.user, event=event, notify=False)
                part.save()

    return redirect('detail', event_id)


@login_required
def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'detail.html', {'event': event})
