from django.urls import path
from .views import NoteList, NotDetail, register, LoginView, logout

urlpatterns = [
    path('notes/', NoteList.as_view()),
    path('notes/<int:pk>/', NotDetail.as_view()),
    path('register/', register),
    path('login/', LoginView.as_view()),
    path('logout/', logout),
]