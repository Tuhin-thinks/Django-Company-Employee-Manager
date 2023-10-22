from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomUserForm, UserUpdateForm
from .models import Company


# Create your views here.
def user_login(request):
    if request.method == "POST":
        form_data = request.POST
        user_email = form_data.get("user_email")
        user_password = form_data.get("user_password")
        existing_user = get_user_model().objects.filter(email=user_email).first()
        if existing_user:
            if existing_user.check_password(user_password):
                login(request, existing_user)
                if request.GET.get("redirect_to"):
                    return redirect(request.GET.get("redirect_to"))
                return redirect("companyusers:user_home")
            else:
                return render(
                    request,
                    "companyandusers/user_login.html",
                    {"error": "Incorrect Password"},
                )
        else:
            return render(
                request,
                "companyandusers/user_login.html",
                {"error": "User does not exist"},
            )

    # GET request
    return render(request, "companyandusers/user_login.html")


def user_register(request):
    all_company_names = Company.objects.values("name", "location")

    if request.method == "POST":
        user_form = CustomUserForm(request.POST)
        company_name = request.POST.get("company")
        company = Company.objects.filter(name=company_name).first()
        user_form.fields["company"].initial = company

        if user_form.is_valid():
            user = user_form.save(commit=False)
            Company.objects.get_or_create(name=company_name)
            user.company = Company.objects.get(name=company_name)
            user.save()
            # login the user
            login(request, user)
            return redirect("companyusers:user_home")
        else:
            return render(
                request,
                "companyandusers/user_register.html",
                {"form": user_form, "companies": list(all_company_names)},
            )

    # GET request
    return render(
        request,
        "companyandusers/user_register.html",
        {"companies": list(all_company_names)},
    )


@login_required(
    login_url="companyusers:user_login", redirect_field_name="redirect_to"
)
def user_home(request):
    user = request.user
    if request.method == "POST":
        form_data = request.POST

        user_form = UserUpdateForm(form_data, instance=user)
        if user_form.is_valid():
            user_form.save()
            return redirect("companyusers:user_home")
        else:
            print(user_form.errors)
            return render(
                request, "companyandusers/user_home.html", {"form": user_form}
            )

    user_form = UserUpdateForm(instance=user)
    return render(request, "companyandusers/user_home.html", {"form": user_form})


def user_logout(request):
    logout(request)
    return redirect("companyusers:user_login")


def company_list(request):
    companies = Company.objects.all().values(
        "name", "location", "ceo", "employees", "slug"
    )

    # exclude slug from the list to view to the user, only used for redirecting to company detail page
    return render(
        request,
        "companyandusers/company_list.html",
        {
            "data": list(companies),
            "data_keys": ["name", "location", "ceo", "employees"],
            "excluded": ["slug"],
        },
    )


@login_required(
    login_url="companyusers:user_login", redirect_field_name="redirect_to"
)
def company_detail(request, slug):
    company = get_object_or_404(Company, slug=slug)
    return render(
        request, "companyandusers/company_detail.html", {"company": company}
    )
