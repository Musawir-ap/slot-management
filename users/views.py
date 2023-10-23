from django.shortcuts import render
from django.http import JsonResponse
from .models import Role, SubRole

def get_subroles(request):
    role = request.GET.get("role")
    sub_roles = SubRole.objects.filter(main_role__name=role)
    data = [{"name": sub_role.name} for sub_role in sub_roles]
    return JsonResponse(data, safe=False)
