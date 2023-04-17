from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from dateutil.relativedelta import relativedelta
from datetime import date
from datetime import datetime


# Create your models here.

USAGE_GOAL_CHOICES = [

    ("B", "Buyer"),
    ("S", "Seller")
]

PRODUCT_CATEGORY_CHOICES = [

    ("Mobile", "Mobile"),
    ("Headphones", "Headphones"),
    ("Accessories", "Accessories")

]

PRODUCT_CONDITION_CHOICES = [

    ("Used", "Used"),
    ("Used like new", "Used like new"),
    ("New", "New"),

]

COUNTRY_CHOICES = [
    ("EG", "EGYPT"),
    ("DE", "GERMANY"),
    ("KW", "KUWAIT"),
    ("KSA", "Saudi Arabia"),
    ("USA", "AMERICA"),
]


CURRENCY_CHOICES = [
    ("EG", "EGP"),
    ("DE", "EUR"),
    ("KW", "KWD"),
    ("KSA", "SAR"),
    ("USA", "USD"),
]


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Countrys (models.Model):
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES,default="EGP")

    def save(self, *args, **kwargs):
        if self.country:
            chosen = next((i for i, choice in enumerate(COUNTRY_CHOICES) if choice[0] == self.country), None)
            if chosen is not None:
                self.currency = CURRENCY_CHOICES[chosen][0]
        super().save(*args, **kwargs)
        super(Countrys, self).save(*args, **kwargs)

class users(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,)
    username = models.CharField(max_length=30,unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, null=True, blank=False)
    usage_goal = models.CharField(max_length=1, choices=USAGE_GOAL_CHOICES)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Category (models.Model):
    type = models.CharField(max_length=15, choices=PRODUCT_CATEGORY_CHOICES)


class Products(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=20)
    price = models.FloatField()
    condition = models.CharField(max_length=15, choices=PRODUCT_CONDITION_CHOICES)
    description = models.TextField()
    qty = models.IntegerField()
    barcode = models.IntegerField(unique=True)
    date_of_entry = models.DateField()
    valid_to = models.DateField()
    expired = models.BooleanField(default=False)
    # in_stock=models.BooleanField(default=True)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, blank=True)

    def expired_status(self):
        "Updates the product's expired status based on the current date and the valid_to date."
        today = date.today()
        if today > self.valid_to:
            self.expired = True
        else:
            self.expired = False

    def stock(self):
        available = True
        if self.qty > 0:
            self.available = True
            return "In Stock"
        else:
            self.available = False
            return "Out Of Stock"



    def save(self, *args, **kwargs):
        self.expired_status()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name


class Cart_Owner (models.Model):

    user = models.ForeignKey(users, on_delete=models.CASCADE,verbose_name="Cart Owner")
    # def get_products(self):
    #     return ",".join([str(p) for p in self.products.all()]) #iterate
    def __str__(self):
        return self.user.username

class Cart_detail (models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE,)
    cart_owner = models.ForeignKey(Cart_Owner, on_delete=models.CASCADE, verbose_name="cart owner")

    def coast_of_product(self):
        return self.products.price


    def cart_owner_name(self):
        return self.cart_owner.user.username



class Order (models.Model):
    cart = models.ForeignKey(Cart_Owner, on_delete=models.CASCADE)



    def num_of_products(self):
        return self.cart.cart_detail_set.count()

    def coast_of_products(self):
        total_cost = 0
        for cart_detail in self.cart.cart_detail_set.all():
            total_cost += cart_detail.coast_of_product()
        return "{} $" .format(total_cost)

    def deliver_to(self):
        user_country = self.cart.user.get_country_display()
        return user_country

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)