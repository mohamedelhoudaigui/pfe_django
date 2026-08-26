from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.services.CivilServantService import CivilServantService, JobDetailService
from core.models import CivilServant, Grade, EchelonIndice
from django.contrib import messages
from django.db import IntegrityError
from .forms import CivilServantRegistrationForm
from .decorators import superuser_required


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You're already logged in.")
        return redirect("dashboard:civil_servant_list")
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
    job_detail = JobDetailService.get_jobdetail(civil_servant)
    return render(
        request, "dashboard/civil_servant_detail.html", {
            "civil_servant": civil_servant,
            "job_detail": job_detail,
        },
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


@superuser_required
def load_grades(request):
    """Returns <option> list of grades for the selected categorie."""
    categorie_code = request.GET.get("categorie")
    grades = Grade.objects.filter(categorie__code=categorie_code).order_by("code")
    return render(request, "dashboard/_grade_options.html", {"grades": grades})


@superuser_required
def load_echelons(request):
    """Returns <option> list of echelons (with indice) for the selected categorie+grade."""
    categorie_code = request.GET.get("categorie")
    grade_code = request.GET.get("grade")
    echelons = EchelonIndice.objects.filter(
        grade__categorie__code=categorie_code, grade__code=grade_code
    ).order_by("echelon")
    return render(request, "dashboard/_echelon_options.html", {"echelons": echelons})