from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.services.CivilServantService import CivilServantService
from core.models import CivilServant
from django.contrib import messages
from django.db import IntegrityError
from .forms import CivilServantRegistrationForm
from .decorators import superuser_required


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard:civil_servant_list")
        return render(request, "dashboard/login.html", {"error": "Invalid credentials"})
    return render(request, "dashboard/login.html")


def logout_view(request):
    logout(request)
    return redirect("dashboard:login")


@login_required
def civil_servant_list(request):
    civil_servants = CivilServant.objects.all()
    return render(
        request, "dashboard/civil_servant_list.html", {"civil_servants": civil_servants}
    )


@login_required
def civil_servant_detail(request, pk):
    civil_servant = CivilServantService.get_civil_servant_with_id(id=pk)
    return render(
        request, "dashboard/civil_servant_detail.html", {"civil_servant": civil_servant}
    )


@login_required
def civil_servant_search(request):
    query = request.GET.get("q", "")
    results = (
        CivilServant.objects.filter(nom__icontains=query)
        if query
        else CivilServant.objects.none()
    )
    return render(
        request, "dashboard/_search_results.html", {"civil_servants": results}
    )


@superuser_required
def civil_servant_register(request):
    if request.method == "POST":
        form = CivilServantRegistrationForm(request.POST)
        if form.is_valid():
            try:
                service_dicts = form.get_service_dicts()
                civil_servant = CivilServantService.create_civil_servant(
                    civil_servant_data=service_dicts["civil_servant_data"],
                    job_detail_data=service_dicts["job_detail_data"],
                    login_data=service_dicts["login_data"],
                )
                messages.success(
                    request, f"Civil servant {civil_servant.nom} created successfully."
                )
                return redirect("dashboard:civil_servant_detail", pk=civil_servant.pk)
            except IntegrityError as e:
                form.add_error(None, str(e))
    else:
        form = CivilServantRegistrationForm()

    return render(request, "dashboard/civil_servant_register.html", {"form": form})
