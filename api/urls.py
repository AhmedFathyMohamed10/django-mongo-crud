from django.urls import path
from .views import NoteList, NotDetail

urlpatterns = [
    path('notes/', NoteList.as_view()),
    path('notes/<int:pk>/', NotDetail.as_view()),
]