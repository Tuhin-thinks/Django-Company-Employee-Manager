from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils.text import slugify


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    ceo = models.CharField(max_length=100)
    employees = models.IntegerField()
    slug = models.SlugField(unique=True)

    founded = models.DateField(null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)

    funding_amt = models.DecimalField(
        max_digits=30, decimal_places=2, null=True, blank=True
    )
    funding_rounds = models.IntegerField(null=True, blank=True)
    last_funding_date = models.DateField(null=True, blank=True)

    website_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    crunchbase_url = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(
            f"{self.normalize_name(self.name)} - {self.normalize_name(self.location)}"
        )
        super().save(*args, **kwargs)

    def normalize_name(self, name):
        return name.lower().strip()

    def get_or_create(self, **kwargs):
        name = kwargs.get("name")
        location = kwargs.get("location")
        ceo = kwargs.get("ceo")
        employees = kwargs.get("employees")

        if name and location and ceo and employees:
            name = self.normalize_name(name)
            company = self.objects.filter(name=name).first()
            if not company:
                company = self.objects.create(
                    name=name, location=location, ceo=ceo, employees=employees
                )
            return company
        else:
            raise ValueError("Invalid data")

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_user", True)
        extra_fields.setdefault("is_admin", True)
        return self._create_user(
            email, password, **{**extra_fields, "is_superuser": True}
        )

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_user", True)
        extra_fields.setdefault("is_admin", False)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    password = models.CharField(
        validators=[MaxLengthValidator(20), MinLengthValidator(8)], max_length=20
    )
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # optional fields
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=100, null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address1 = models.CharField(max_length=100, null=True, blank=True)
    address2 = models.CharField(max_length=100, null=True, blank=True)

    token = models.CharField(max_length=100, null=True, blank=True)

    is_user = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "password"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_staff(self):
        return self.is_user
