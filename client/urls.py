from django.urls import path
from .views import (
    TokenListView, 
    TokenDetailView, 
    TokenCreateView, 
    TokenUpdateView, 
    TokenDeleteView,
    UserTokenListView,
    ProfileView,
    ClientProfileUpdateView,
    UserUpdateView
)
from . import views

app_name = 'client'

urlpatterns = [
    path('', TokenListView.as_view(), name='token-home'),
    path('token/', UserTokenListView.as_view(), name='token-list'),
    path('token/<int:pk>/', TokenDetailView.as_view(), name='token-detail'),
    path('token/new/', TokenCreateView.as_view(), name='token-create'),
    path('token/<int:pk>/update/', TokenUpdateView.as_view(), name='token-update'),
    path('token/<int:pk>/delete/', TokenDeleteView.as_view(), name='token-delete'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('profile/user-update/', UserUpdateView.as_view(), name='user-update'),
    path('profile/profile-update/', ClientProfileUpdateView.as_view(), name='user-profile-update'),
    path('about/', views.about, name='token-about'),
]