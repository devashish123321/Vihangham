from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, EventRegistration
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import EventForm
from .forms import EventRegistrationForm
from .forms import ContactMessageForm


# ---------------- Home Page ----------------

def home(request):
    return render(request, 'home.html')



# ---------------- Contact Page ----------------

def contact(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()  # Save the message to database
            # Optional: redirect to same page with a success flag
            return render(request, 'contact.html', {'form': ContactMessageForm(), 'success': True})
    else:
        form = ContactMessageForm()

    return render(request, 'contact.html', {'form': form})
 


 # ---------------- Event List ----------------

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})


# ---------------- Event Registration Form Page ----------------

def register_event_page(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Provide an empty registration form when displaying the page
    from .forms import EventRegistrationForm
    form = EventRegistrationForm()
    return render(request, 'register_event.html', {'event': event, 'form': form})


#  from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Participant

def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        college = request.POST.get("college")
        branch = request.POST.get("branch")
        year = request.POST.get("year")
        notes = request.POST.get("notes")

        participant = Participant(
            name=name,
            email=email,
            phone=phone,
            college=college,
            branch=branch,
            year=year,
            notes=notes,
            event=event,               # ForeignKey (event id)
            event_name=event.title     # direct event ka naam
        )
        participant.save()
        return redirect(f"/success/?event={event.title}")


        # return redirect("success_page")  # Your success page

    return render(request, "register_event.html", {"event": event})



# # ---------------- Success Page ----------------

def success_page(request):
    event_name = request.GET.get("event")

    return render(request, "success.html", {
        "event_name": event_name
    })



# ---------------- Faculty Login ----------------
 
from django.shortcuts import render, redirect
from .models import Faculty
from django.contrib import messages



from django.db import transaction 

def faculty_login(request):
    if request.method == "POST":
        name = request.POST.get("name")
        department = request.POST.get("department")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Password check
        if password != "faculty123":
            messages.error(request, "Invalid password!")
            return render(request, "faculty_login.html")

        # SAFE QUERY (no lock)
        try:
            faculty = Faculty.objects.get(email=email)
            messages.success(request, f"Welcome back, {faculty.name}")

        except Faculty.DoesNotExist:
            # Create inside atomic block → prevents DB lock
            with transaction.atomic():
                faculty = Faculty.objects.create(
                    name=name,
                    email=email,
                    department=department
                )
            messages.success(request, f"New Faculty Registered: {name} ({department})")

        # Set session
        request.session["faculty_email"] = faculty.email

        return redirect("faculty_home")

    return render(request, "faculty_login.html")
 

# ---------------- Faculty Home ----------------

def faculty_home(request):
    events = Event.objects.all()
    return render(request, 'faculty_home.html', {'events': events})



# ---------------- Create Event ----------------

def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('faculty_home')  # Redirect to all events page
            
    else:
        form = EventForm()
    return render(request, "create_event.html", {"form": form})

def events_list(request):
    events = Event.objects.all().order_by('-date', '-time')
    return render(request, "events.html", {"events": events})


# ---------------- Thank You Page ----------------

def thank_you_page(request):
    return render(request, 'thankyou.html')


# -----------------------index page------------------------

def index(request):
    return render(request, 'index.html')

# ----------------------participation page-----------------------------------

from .models import Participant 

# def participation(request):
#     # If an event_id is provided via querystring, show only participants for that event.
#     event_id = request.GET.get('event_id')
#     if event_id:
#         # get_object_or_404 will raise 404 if invalid id
#         event = get_object_or_404(Event, id=event_id)
#         participations = Participant.objects.filter(event=event).order_by('-registration_date')
#         event_title = event.title
#     else:
#         participations = Participant.objects.all().order_by('-registration_date')
#         event_title = None

#     return render(request, 'participation.html', {
#         'participations': participations,
#         'event_title': event_title
#     }) 

def participation(request):
    event_id = request.GET.get('event_id')
    
    if event_id:
        # Get specific event
        event = get_object_or_404(Event, id=event_id)
        # Get participants for this specific event only
        participations = Participant.objects.filter(event=event)
        
        return render(request, 'participation.html', {
            'participations': participations,
            'event': event,  # Send single event object
            'event_title': f"{event.title} - Participants"
        })
    else:
        # If no event_id provided, show all participations
        participations = Participant.objects.all()
        events = Event.objects.all()
        return render(request, 'participation.html', {
            'participations': participations,
            'events': events,
            'event': None,
            'event_title': 'All Participants'
        })
#  ---------------------------------

def night_pass(request):
    return render(request, 'night_pass.html')

def enter_winners(request):
    return render(request, 'enter_winners.html')


from django.shortcuts import render
from .models import Event

def faculty_show_event(request):
    events = Event.objects.all()   # SQLite se sari rows fetch
    return render(request, 'faculty_show_event.html', {'events': events})




# ------------------------------------------------------------------------------
   
from django.http import HttpResponse
from .models import Event

def delete_event(request, event_id):

    # ❌ Student cannot delete (no faculty session)
    if 'faculty_email' not in request.session:
        return HttpResponse("❌ Only Faculty can delete events!")

    event = get_object_or_404(Event, id=event_id)
    event.delete()

    return redirect('faculty_show_event')


# -----------------------------------------------------------
 

 
from django.shortcuts import render, get_object_or_404
from .models import NightPass
import qrcode
import os
from django.conf import settings

def night_pass_form(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        # Check if pass already exists
        existing_pass = NightPass.objects.filter(email=email).first()

        if existing_pass:
            # Show existing QR (NO ERROR)
            return render(request, "night_pass_generated.html", {
                "night_pass": existing_pass,
                "message": "Existing QR Loaded"
            })

        # New Pass
        night_pass = NightPass.objects.create(name=name, email=email)

        # QR folder
        qr_folder = os.path.join(settings.MEDIA_ROOT, "qrcodes")
        os.makedirs(qr_folder, exist_ok=True)

        # QR path
        qr_path = os.path.join(qr_folder, f"{email}.png")

        # QR data
        qr_data = f"http://127.0.0.1:8000/verify/{night_pass.id}/"

        qr = qrcode.make(qr_data)
        qr.save(qr_path)

        night_pass.qr_code_file = f"qrcodes/{email}.png"
        night_pass.save()

        return render(request, "night_pass_generated.html", {"night_pass": night_pass})

    return render(request, "night_pass_form.html")


def verify_qr(request, pass_id):
    night_pass = get_object_or_404(NightPass, id=pass_id)
    
    return render(request, "verify_qr.html", {"night_pass": night_pass})




#####################################################3


def enter_winners(request, event_id):
    event = Event.objects.get(id=event_id)

    # Event ke participants list
    participants = Participant.objects.filter(event=event)

    if request.method == "POST":
        winner1 = request.POST.get("winner1")
        winner2 = request.POST.get("winner2")
        winner3 = request.POST.get("winner3")

        # Yaha save karna hai — agar database me “Winner” table bana hua hai
        # Agar chaho to winner model bhi bana dunga

        return redirect("faculty_show_event")

    return render(request, "enter_winners.html", {
        "event": event,
        "participants": participants
    })







# --------------------------------------------------- 

import openpyxl
from django.http import HttpResponse
from .models import Event, Participant
 
# def participation(request):
#     events = Event.objects.all()  # Fetch all events
#     return render(request, 'participation.html', {'events': events})
 
def export_participants_excel(request, event_id):
    event = Event.objects.get(id=event_id)
    participants = Participant.objects.filter(event=event)

    # Excel file create
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"{event.title} Participants"

    # Header
    ws.append(['Name', 'Email', 'Phone', 'College', 'Branch', 'Year', 'Notes', 'Registration Date'])

    # Participant data
    for p in participants:
        ws.append([p.name, p.email, p.phone, p.college, p.branch, p.year, p.notes, p.registration_date.strftime("%Y-%m-%d %H:%M")])

    # Response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={event.title}_participants.xlsx'
    wb.save(response)
    return response



# ----------------------------------------------------------------
 
from .models import Event, Winner 
from django.urls import reverse

def enter_winners(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    winner, created = Winner.objects.get_or_create(event=event)

    if request.method == 'POST':
        winner.first_winner = request.POST.get('first_winner')
        winner.second_winner = request.POST.get('second_winner')
        winner.third_winner = request.POST.get('third_winner')
        winner.save()

        # ✅ CORRECT REDIRECT
        url = reverse('participation')
        return redirect(f'{url}?event_id={event.id}')

    return render(request, 'enter_winners.html', {
        'event': event,
        'winner': winner
    })
  


# -------------------------------------------------------------------------------

# from .models import Event, Winner

# def event_winners(request, event_id):
#     event = get_object_or_404(Event, id=event_id)

#     # Winner table se event-wise data
#     winner = Winner.objects.filter(event=event).first()

#     return render(request, 'event_winners.html', {
#         'event': event,
#         'winner': winner
#     })

from django.shortcuts import render, get_object_or_404
from .models import Event, Winner

def event_winners(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    try:
        winner = Winner.objects.get(event=event)
    except Winner.DoesNotExist:
        winner = None

    return render(request, 'event_winners.html', {
        'event': event,
        'winner': winner
    })

