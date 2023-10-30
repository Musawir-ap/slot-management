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

urlpatterns = [
    path('', TokenListView.as_view(), name='token-home'),
    path('token/<int:pk>/', TokenDetailView.as_view(), name='token-detail'),
    path('token/new/', TokenCreateView.as_view(), name='token-create'),
    path('token/<int:pk>/update/', TokenUpdateView.as_view(), name='token-update'),
    path('token/<int:pk>/delete/', TokenDeleteView.as_view(), name='token-delete'),
    path('about/', views.about, name='token-about'),
]