from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, ModelChoiceField
from django.core.exceptions import ValidationError
from .models import Company


class UserAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user: User):
        if not (user.is_user):
            raise ValidationError(
                self.error_messages["invalid_login"],
                code="invalid_login",
                params={"username": self.username_field.verbose_name},
            )
        else:
            print("User is allowed to login")


class CustomUserForm(ModelForm):
    company = ModelChoiceField(queryset=Company.objects.all(), empty_label=None, required=True, to_field_name="name")

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "company"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["company"].required = True
        self.fields["company"].empty_label = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_user = True
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean_company(self):
        company = self.cleaned_data["company"]
        if not company:
            raise ValidationError("Company is required")
        return company


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "state",
            "country",
            "city",
            "postcode",
            "education",
            "phone",
            "address1",
            "address2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
