from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse
from .forms import ExerciseSetForm,ProtienCalForm,CalCountForm
from .models import User,Workout
from django.utils import timezone
from django.core.paginator import Paginator
from django.forms import formset_factory
from decimal import Decimal

# Create your views here.
def index(request):
    return render(request,'fittrack/index.html')


@login_required
def log_workout(request):
    ExerciseSetFormSet = formset_factory(ExerciseSetForm, extra=1)  
    if request.method == "POST":
        exercise_set_formset = ExerciseSetFormSet(request.POST)
        if exercise_set_formset.is_valid():
            workout = Workout(user=request.user, date=timezone.now())
            workout.save()

            for form in exercise_set_formset:
                exercise_set = form.save(commit=False)
                exercise_set.workout = workout
                exercise_set.save()

            return HttpResponseRedirect(reverse("workout_history"))
    else:
        exercise_set_formset = ExerciseSetFormSet()


    return render(request, 'fittrack/workout_loging.html', {
        'exercise_set_formset': exercise_set_formset,
    })


# View for Workout History 
@login_required
def workout_history(request):
    history = Workout.objects.filter(user=request.user).order_by('-date')
   
    paginator = Paginator(history,1)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    
    context = {
        'page_obj':page_obj,
    }
    return render (request, 'fittrack/workout_history.html',context)

# View for Protien Calculator
@login_required
def protein_cal(request):
    if request.method == 'POST':
        form = ProtienCalForm(request.POST)
        if form.is_valid():
            user = request.user
            weight = form.cleaned_data['weight']
            activity = form.cleaned_data['activity']

            activity_multiplier = {
                'Sedentary': Decimal('1.2'),
                'Light': Decimal('1.375'),
                'Moderate': Decimal('1.55'),
                'Active': Decimal('1.725'),
                'VeryActive': Decimal('1.9'),
                'ExtraActive': Decimal('2.0')
            }
            
            weight = Decimal(str(weight))

            protein_needs = activity_multiplier[activity] * weight

            protein_cal = form.save(commit=False)
            protein_cal.user = user
            protein_cal.save()

            return render(request, 'fittrack/pro_result.html', {'protein_cal': protein_cal, 'protein_needs': protein_needs})
    else:
        form = ProtienCalForm()
    context = {
        'form':form
    }
    return render (request,'fittrack/protein_cal.html',context)


# View for Calories Calculator
@login_required
def cal_count(request):
    if request.method == 'POST':
        form = CalCountForm(request.POST)
        if form.is_valid():
            user = request.user
            weight = Decimal(str(form.cleaned_data['weight']))  # Convert weight to Decimal
            age = form.cleaned_data['age']
            height = Decimal(str(form.cleaned_data['height']))  # Convert height to Decimal
            activity = form.cleaned_data['activity']
            gender = form.cleaned_data['gender']
            goal = form.cleaned_data['goal']

            # Using Harris-Benedict equation
            if gender == 'Male':
                bmr = Decimal('66.5') + (Decimal('13.75') * weight) + (Decimal('5.003') * height) - (Decimal('6.75') * age)
            else:
                bmr = Decimal('655.1') + (Decimal('9.563') * weight) + (Decimal('1.850') * height) - (Decimal('4.676') * age)

            activity_multiplier = {
                'Sedentary': Decimal('1.2'),
                'Light': Decimal('1.375'),
                'Moderate': Decimal('1.55'),
                'Active': Decimal('1.725'),
                'VeryActive': Decimal('1.9'),
                'ExtraActive': Decimal('2.0')
            }

            total_cal = activity_multiplier[activity] * bmr
            # Adjust calories based on the selected goal
            if goal == 'Weight Loss':
                total_cal -= Decimal('500')  # Create a calorie deficit for weight loss
            elif goal == 'Weight Gain':
                total_cal += Decimal('500')  # Create a calorie surplus for weight gain



            cal_count = form.save(commit=False)
            cal_count.user = user
            cal_count.save()

            return render(request, 'fittrack/cal_result.html', {'cal_count': cal_count, 'total_cal': total_cal})
    else:
        form = CalCountForm()
    context = {
        'form': form
    }
    return render(request, 'fittrack/cal_count.html', context)



# View for Login, Register and Logout
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "fittrack/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "fittrack/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "fittrack/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "fittrack/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "fittrack/register.html")