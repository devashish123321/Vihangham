from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return self.title


class Participant(models.Model):
    name = models.CharField(max_length=200)
    
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    college = models.CharField(max_length=200, blank=True, null=True)
    registration_date = models.DateTimeField(default=timezone.now)

    branch = models.CharField(max_length=200, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

     
 
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    
    event_name = models.CharField(max_length=200)  # <-- Event ka name database me visible
  
 
    def __str__(self):
        return f"{self.name} - {self.event_name}"
   

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    college = models.CharField(max_length=150)
    branch = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"



class Faculty(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100,default="Unknown")

    def __str__(self):
        return f"{self.name} ({self.department})"




class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    









 


from django.db import models

class NightPass(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    qr_code_file = models.ImageField(upload_to="qrcodes/", blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email
####################################################3

class Winner(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE,related_name='winner' )
    first_winner = models.CharField(max_length=100, blank=True, null=True)
    second_winner = models.CharField(max_length=100, blank=True, null=True)
    third_winner = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Winners - {self.event.title}" 
         