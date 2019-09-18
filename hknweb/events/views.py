from __future__ import print_function
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt #doing this for now bc idk how to make csrf work
from django.db.models import F # Avoids changing database values without risking a race condition

from .models import Event, Rsvp
from .forms import EventForm
from hknweb.models import Profile

#Google calendar

import datetime
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

def index(request):
    events = Event.objects.order_by('-start_time')
    context = {
        'events': events,
    }
    return render(request, 'events/index.html', context)

def show_details(request, id):
    event = Event.objects.get(pk=id)
    rsvp = Rsvp.objects.filter(user=request.user, event=event).exists()
    context = {
        'event': event,
        'rsvp': rsvp,
    }
    if request.user.is_authenticated:
        return render(request, 'events/show_details.html', context)
    return redirect('/events')

@csrf_exempt  #doing this for now bc idk how to make csrf work
def rsvp(request, id):
    if request.method != 'POST':
        raise Http404()

    event = Event.objects.get(pk=id)
    if request.user.is_authenticated and event.rsvps < event.rsvp_limit:
        event.rsvps = F("rsvps") + 1
        Rsvp.objects.create(user=request.user, event=event)
        messages.success(request, 'RSVP\'d!')
    else:
        messages.error(request, 'Could not RSVP; the RSVP limit has been reached.')
    return redirect('/events/' + str(id))

@csrf_exempt  #doing this for now bc idk how to make csrf work
def unrsvp(request, id):
    if request.method != 'POST':
        raise Http404()

    event = Event.objects.get(pk=id)
    if request.user.is_authenticated and event.rsvps < event.rsvp_limit:
        #check if rsvp for this event and this user already exists; if false, then set true
        event.rsvps = F("rsvps") - 1
        Rsvp.objects.get(user=request.user, event=event).delete()
        messages.success(request, 'un-RSVP\'d :(')
    else:
        messages.error(request, 'Something went wrong; could not un-RSVP.')
    return redirect('/events/' + str(id))

def add_event(request):
    form = EventForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            # create_event(form)
            event = form.save()
            new_google_calendar(event)
            messages.success(request, 'Event has been added!')
            return redirect('/events')
        else:
            print(form.errors)
            messages.success(request, 'Something went wrong oops')
            return render(request, 'events/add_event.html', {'form': EventForm(None)})
    return render(request, 'events/add_event.html', {'form': EventForm(None)})

def new_google_calendar(event):
    service = build_service()
    google_calendar_event = {
        'summary': "(" + event.event_type.type + ")" + event.name,
        'location': event.location,
        'description': event.description,
        'start': {
            'dateTime': event.start_time.isoformat(),
            'timeZone': 'America/Los_Angeles'
        },
        'end': {
            'dateTime': event.end_time.isoformat(),
            'timeZone': 'America/Los_Angeles'
        }
    }
    event = service.events().insert(calendarId= 'primary', body = google_calendar_event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))

def build_service():
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes = SCOPES)
    creds = flow.run_console()
    # creds = flow.run_local_server(port = 0)
    service = build('calendar', 'v3', credentials = creds)  
    return service
