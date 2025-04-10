from django.urls import path
from .views import EventAPIView,EventUserView

urlpatterns = [
    path('event/', EventAPIView.as_view(), name='create-event'),
    path('event/<int:pk>/', EventAPIView.as_view(), name='edit-event'),  
    path('event-user/', EventUserView.as_view(), name='user-event'), 
]
