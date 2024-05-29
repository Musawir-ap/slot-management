from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from users.models import CustomUser, Role
from client.forms import ClientProfileForm, ClientProfileUpdateForm
from users.forms import UserUpdateForm
from client.models import ClientProfile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from tokenapp.models import Token, Status, StatusHistory
from tokenapp.forms import TokenForm
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO
import uuid
from django.utils.text import slugify
from django.core.files.storage import FileSystemStorage


class TokenListView(ListView):
    model = Token
    # template_name = 'client/home.html'  
    context_object_name = 'tokens'
    # ordering = ['token_time']
    paginate_by = 10
    
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role.name == 'USER':
                status = Status.objects.get(name='Pending')
                queryset = Token.objects.filter(user_id=user.id, status=status).order_by('-token_time')

            elif user.role.name == 'STAFF':
                queryset = Token.objects.filter(assigned_staff=user.id).order_by('-token_time')
                
            elif  user.role.name == 'ADMIN':
                queryset = Token.objects.all()
        else:
            queryset = Token.objects.none()
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_empty'] = not Token.objects.filter(user=self.request.user).exists()
        return context
    
    def get_template_names(self):
        if self.request.user.role.name in ('ADMIN', 'STAFF'):
            return ['client/staff_home.html']
        else:
            return ['client/home.html']


class UserTokenListView(ListView, LoginRequiredMixin):  
    model = Token
    template_name = 'client/user_tokens.html'
    context_object_name = 'tokens'
    ordering = ['token_time']
    paginate_by = 10
    
    def get_queryset(self):
        user = self.request.user
        return Token.objects.filter(user_id=user.id).order_by('-token_time')
    

class TokenDetailView(DetailView):
    model = Token
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TokenForm()
        context['history'] = StatusHistory.objects.filter(tracked_object=self.get_object()).order_by('timestamp')
        return context
    

class TokenCreateView(LoginRequiredMixin, CreateView):
    model = Token
    form_class = TokenForm
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('client:token-list')

class TokenUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Token
    form_class = TokenForm
    
    def get_initial(self):
        initial = super(TokenUpdateView, self).get_initial()
        initial['token_date'] = self.object.token_date.strftime('%Y-%m-%d')
        initial['token_time'] = self.object.token_time.strftime('%H:%M:%S')
        return initial
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Token updated successfully")
        return super().form_valid(form)
    
    def test_func(self):
        Token = self.get_object()
        if self.request.user == Token.user:
            return True
        return False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context
    
    def get_success_url(self):
        return reverse_lazy('client:token-detail', kwargs={'pk': self.object.pk})


class TokenDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Token
    success_url = '/'
    
    def test_func(self):
        Token = self.get_object()
        if self.request.user == Token.user:
            return True
        return False
    
    
class ProfileView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'client/client_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = ClientProfile.objects.get(user=self.request.user)
        context['u_form'] = UserUpdateForm()
        context['p_form'] = ClientProfileForm()
        return context
    
    def test_func(self):
        try:
            ClientProfile.objects.get(user=self.request.user)
            return True
        except ClientProfile.DoesNotExist:
            return False


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    success_url = reverse_lazy('client:user-profile')
    # template_name = 'client/clientprofile_form.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, username=self.request.user.username)

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "User updated successfully")
        return super().form_valid(form)
 
    def test_func(self):
        CustomUser = self.get_object()
        if self.request.user == CustomUser:
            return True
        return False
    
    
class ClientProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ClientProfile
    form_class = ClientProfileUpdateForm
    success_url = reverse_lazy('client:user-profile')
    template_name = 'client/clientprofile_form.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(ClientProfile, user=self.request.user)
    
    def get_initial(self):
        initial = super(ClientProfileUpdateView, self).get_initial()
        birth_date = self.object.birth_date
        if birth_date:
            initial['birth_date'] = birth_date.strftime('%Y-%m-%d')
        return initial
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save(commit=False)
        if 'image' in self.request.FILES: 
            img = Image.open(self.request.FILES['image'])
            width, height = img.size
            if width > 300 and height > 300:
                img.thumbnail((width, height))

            if height < width:
                left = (width - height) / 2
                right = (width + height) / 2
                top = 0
                bottom = height
                img = img.crop((left, top, right, bottom))

            elif width < height:
                left = 0
                right = width
                top = 0
                bottom = width
                img = img.crop((left, top, right, bottom))

            if width > 300 and height > 300:
                img.thumbnail((300, 300))

            buffer = BytesIO()
            uid = str(uuid.uuid4())[:8]
            filename = f"{slugify(self.request.user.username)}_{uid}.jpeg"
            img.save(buffer, format='JPEG')
            form.instance.image = ContentFile(buffer.getvalue(), filename)
            # form.instance.image.save(filename, ContentFile(buffer.getvalue(), filename), save=False)
            
        messages.success(self.request, "Profile updated successfully")
        return super().form_valid(form)
    
    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     if form.is_valid():
    #         messages.success(self.request, "Profile updated successfully")
    #     else:
    #         print(form.errors)
    #     return super().form_valid(form)
    
    def test_func(self):
        ClientProfile = self.get_object()
        if self.request.user == ClientProfile.user:
            return True
        return False
    

def about(request):
    return render(request, 'token/about.html')



