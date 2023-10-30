from django.shortcuts import render, get_object_or_404
from users.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from tokenapp.models import Token
from tokenapp.forms import TokenForm
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
)


class TokenListView(ListView):
    model = Token
    # template_name = 'Token/home.html'  
    context_object_name = 'tokens'
    ordering = ['token_time']
    paginate_by = 10


class UserTokenListView(ListView):
    model = Token
    template_name = 'token/user_home.html'
    context_object_name = 'tokens'
    ordering = ['token_time']
    paginate_by = 10
    
    def get_query_set(self):
        user = get_object_or_404(CustomUser, username=self.kwargs.get['username'])
        return Token.objects.filter(user_id=user.id).order_by('-token_time')
    

class TokenDetailView(DetailView):
    model = Token
    

class TokenCreateView(LoginRequiredMixin, CreateView,):
    model = Token
    form_class = TokenForm
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TokenUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView,):
    model = Token
    form_class = TokenForm
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        Token = self.get_object()
        if self.request.user == Token.user:
            return True
        return False


class TokenDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Token
    success_url = '/'
    
    def test_func(self):
        Token = self.get_object()
        if self.request.user == Token.user:
            return True
        return False

def about(request):
    return render(request, 'token/about.html')