from django import forms
from .models import Event, Participant, EventRegistration, ContactMessage


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'phone', 'college', 'event']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            'college': forms.TextInput(attrs={'placeholder': 'Enter college/school'}),
            'event': forms.Select(),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'venue', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter event title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Write event details...'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'venue': forms.TextInput(attrs={'placeholder': 'Enter venue'}),
            'image': forms.ClearableFileInput(),
        } 
# class EventForm(forms.ModelForm):              
#     class Meta:
#         model = Event
#         fields = '__all__'
#         widgets = {
#             'title': forms.TextInput(attrs={'placeholder': 'Enter Event Title'}),
#             'description': forms.Textarea(attrs={'placeholder': 'Enter Description'}),
#             'date': forms.DateInput(attrs={'type': 'date'}),
#             'time': forms.TimeInput(attrs={'type': 'time'}),
#             'venue': forms.TextInput(attrs={'placeholder': 'Enter Venue'}),
#             'image': forms.FileInput(),  # <-- correct widget for image
#         }

  
class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['name', 'email', 'phone', 'college', 'branch', 'year', 'notes']



class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject of your message'}),
            'message': forms.Textarea(attrs={'placeholder': 'Write your message here...'}),
        }





from django import forms
from .models import NightPass

class NightPassForm(forms.ModelForm):
    class Meta:
        model = NightPass
        fields = ['name', 'email']
