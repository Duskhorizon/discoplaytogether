from django import forms
from django.forms import ModelForm
from .models import Event, Game
from .widgets import XDSoftDateTimePickerInput


class EventForm(ModelForm):
    title = forms.CharField(label='Nazwa wydarzenia:')
    description = forms.CharField(label='Opis:')
    game = forms.ModelChoiceField(queryset=Game.objects.all(), label='Gra:')
    start_time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=XDSoftDateTimePickerInput(), label='Rozpoczęcie:'
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'game', 'server']


class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=XDSoftDateTimePickerInput()
    )
