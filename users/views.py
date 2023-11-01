from django.http import JsonResponse
from .models import Role, SubRole, CustomUser
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MyAuthForm, CustomUserCreationForm
from django.contrib.auth.views import LoginView

def home(request):
    return render(request, 'users/home.html')


def get_subroles(request):
    role = request.GET.get("role")
    sub_roles = SubRole.objects.filter(main_role__name=role)
    data = [{"name": sub_role.name} for sub_role in sub_roles]
    return JsonResponse(data, safe=False)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'{username} registered :)')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    authentication_form = MyAuthForm
    def form_valid(self, form):
        username = form.cleaned_data['username']
        messages.success(self.request, f"{username} logged in  successfully :)")
        return super().form_valid(form)
    
    

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         p_form = ProfileUpdateForm(request.POST, 
#                                    request.FILES, 
#                                    instance=request.user.profile)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, 'profile updated :)')
#             return redirect('profile')
#     else:
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = ProfileUpdateForm(instance=request.user.profile)

#     context = {
#         'u_form' : u_form,
#         'p_form' : p_form
#     }
    
#     return render(request, 'users/profile.html', context)