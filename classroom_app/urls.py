from django.urls import path
from . import views

urlpatterns = [
    # API Endpoint for token generation

    # Route the empty string (home page) to our new template view
    path('', views.home_classroom, name='classroom_home'),
    
    path('api/token/', views.get_livekit_token, name='get_livekit_token'),
]