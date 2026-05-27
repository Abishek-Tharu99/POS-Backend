from django.urls import path
from .views import end_session,start_session,clear_sessions

urlpatterns = [
    path('end/', end_session, name='end-session'),   
    path('start/', start_session, name='start-session'),
    path("clear_sessions/", clear_sessions),

]