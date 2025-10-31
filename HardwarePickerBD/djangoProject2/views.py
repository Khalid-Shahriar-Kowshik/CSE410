from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from guides.models import Guides
from products.models import CPU, MOBO, CPUCooler, RAM, Storage, GPU, PSU, CASE
from userprofile.models import UserProfile
from buildhub.models import BlogPost
from django.db.models import Count
import re
import unicodedata
from datetime import datetime, date
from django.views.decorators.csrf import csrf_exempt

# ---------- Utility Validation Functions ----------

def contains_emoji(text):
    for char in text:
        if unicodedata.category(char).startswith("So"):
            return True
    return False

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def is_valid_name(name):
    return name and not contains_emoji(name) and name.isascii() and re.match(r"^[A-Za-z\s\-']+$", name)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 11

def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

# ---------- Views ----------

def base(request):
    return render(request, 'base.html')


def home(request):
    guides = Guides.objects.all()
    top_blogs = BlogPost.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:3]

    return render(request, 'main/home.html', {
        'guides': guides,
        'top_blogs': top_blogs,
    })


def builder(request):
    return render(request, 'main/builder.html')


def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pw1 = request.POST.get('password1')
        pw2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number') or ""
        address = request.POST.get('address')
        date_of_birth_str = request.POST.get('date_of_birth')
        bio = request.POST.get('bio')

        if not uname or not email or not pw1 or not pw2:
            messages.error(request, "All required fields must be filled.")
            return render(request, 'registration/register.html')

        if pw1 != pw2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'registration/register.html')

        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'registration/register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'registration/register.html')

        if not is_valid_email(email):
            messages.error(request, "Invalid email format.")
            return render(request, 'registration/register.html')

        if not is_valid_name(first_name or '') or not is_valid_name(last_name or ''):
            messages.error(request, "Names must not contain emojis or special characters.")
            return render(request, 'registration/register.html')

        if contains_emoji(uname):
            messages.error(request, "Username must not contain emojis.")
            return render(request, 'registration/register.html')

        if phone_number and not is_valid_phone(phone_number):
            messages.error(request, "Phone number must be 11 digits and numeric.")
            return render(request, 'registration/register.html')

        date_of_birth = None
        if date_of_birth_str:
            try:
                date_of_birth = datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()
                if calculate_age(date_of_birth) < 10:
                    messages.error(request, "Users must be at least 10 years old to register.")
                    return render(request, 'registration/register.html')
            except ValueError:
                messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
                return render(request, 'registration/register.html')

        try:
            my_user = User.objects.create_user(
                username=uname,
                email=email,
                password=pw1,
                first_name=first_name,
                last_name=last_name
            )

            profile = my_user.userprofile
            profile.first_name = first_name
            profile.last_name = last_name
            profile.phone_number = phone_number
            profile.address = address
            profile.date_of_birth = date_of_birth
            profile.bio = bio
            profile.save()

            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('register')

        except Exception as e:
            messages.error(request, f"An error occurred while creating the account: {e}")
            return render(request, 'registration/register.html')

    return render(request, 'registration/register.html')


def LOGIN(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passw = request.POST.get("password")
        user = authenticate(request, username=uname, password=passw)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Username or password is incorrect!")

    return render(request, 'registration/login.html')


def LOGOUT(request):
    logout(request)
    return redirect("home")

