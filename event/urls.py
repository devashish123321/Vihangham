from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Home Page
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),

    # Contact Page
    path('contact/', views.contact, name='contact'),

    # Event List Page
    path('events/', views.event_list, name='event_list'),
    # path('events/', views.events, name='event_list'),


    # Event Registration Form
    path('event/<int:event_id>/register/', views.register_event_page, name='register_event_page'),
    path('event/<int:event_id>/submit/', views.register_event, name='register_event'),


    # Success Page after registration
    path('success/', views.success_page, name='success_page'),
 

    # Faculty Login & Home
    path('faculty_login/', views.faculty_login, name='faculty_login'),
    path('faculty_home/', views.faculty_home, name='faculty_home'),


    # Create Event (Faculty)
    path('create_event/', views.create_event, name='create_event'),


    #winner name entries and check ;list  
    path('enter-winners/<int:event_id>/', views.enter_winners, name='enter_winners'),

  
# winner display page (optional)# urls.py
    path('event-winners/<int:event_id>/', views.event_winners, name='event_winners'),
# path('event/<int:event_id>/winners/', views.event_winners, name='event_winners')

    
    # Thank You Page
    path('thankyou/', views.thank_you_page, name='thank_you_page'),
   

    path('participation/', views.participation, name='participation'),
    # path('night_pass/', views.night_pass_form, name='night_pass_form'),


    path("night_pass/", views.night_pass_form, name="night_pass"),

    path("verify/<int:pass_id>/", views.verify_qr, name="verify_qr"),
    
    # path("get-pass/", views.get_pass, name="get_pass"),
     

    path('faculty_show_event/', views.faculty_show_event, name='faculty_show_event'),
 
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),


    path("export-participants-excel/<int:event_id>/", views.export_participants_excel, name="export_participants_excel"),

]
  


# Media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


