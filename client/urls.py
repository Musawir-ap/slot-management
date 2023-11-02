from django.urls import path
from .views import (
    TokenListView, 
    TokenDetailView, 
    TokenCreateView, 
    TokenUpdateView, 
    TokenDeleteView,
    UserTokenListView,
)
from . import views

app_name = 'client'

urlpatterns = [
    path('', UserTokenListView.as_view(), name='client-token-home'),
    path('token/<int:pk>/', TokenDetailView.as_view(), name='client-token-detail'),
    path('token/new/', TokenCreateView.as_view(), name='client-token-create'),
    path('token/<int:pk>/update/', TokenUpdateView.as_view(), name='client-token-update'),
    path('token/<int:pk>/delete/', TokenDeleteView.as_view(), name='client-token-delete'),
    path('about/', views.about, name='client-token-about'),
]