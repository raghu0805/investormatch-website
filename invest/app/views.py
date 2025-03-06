from django.shortcuts import render, HttpResponseRedirect,redirect
from django.urls import reverse
from .models import Question,Question1,UserScore
from django.shortcuts import  get_object_or_404
from django.http import Http404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from .forms import RegisterForm  
from django.contrib.auth.models import User
from django.contrib import messages
from app.models import CustomUser  
from django.contrib.auth import get_user_model

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging
logger = logging.getLogger(__name__)
User = get_user_model()


def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Both email and password are required!")
            return redirect("signup")  

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists! Try logging in.")
            return redirect("signup")

        user = CustomUser.objects.create_user(email=email, password=password)
        user.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")  

    return render(request, "app/signup.html")


def user_signup(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

    
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("signup")

      
        user = CustomUser.objects.create_user(email=email, password=password)


        user.save()

        login(request, user)
        messages.success(request, "Signup successful!")
        return redirect("dashboard")  

    return render(request, "app/signup.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            messages.success(request, "Registration successful!")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})




User = get_user_model()

def user_login(request):
    print("🛠 user_login view executed!") 

    if request.method == "POST":
        email = request.POST.get("email").strip().lower() 
        password = request.POST.get("password")

        print(f"📧 Email: {email}, 🔑 Password: {password}")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            print(f"✅ Authentication successful for {user.email}")
            login(request, user)
            return redirect("introduce") 
        else:
            print("❌ Authentication failed!")
            messages.error(request, "Incorrect email or password")  

    return render(request, "app/login.html")

def index(request):
    return render(request,'app/index.html')
def login_view(request):
    return render(request,'app/login.html')
 
def signup(request):
    return render(request,'app/signup.html')
def introduce(request):
    print("🚀 LOGIN FORM SUBMITTED!")  
    return render(request,'app/introduce.html')
def questioning(request):
    return render(request,'app/questioning.html')
def startupcard(request):
    return render(request,'app/startupcard.html')
def loading(request):
    return render(request,'app/loading.html')
def investoroption(request):
    return render(request,'app/investoroption.html')

def risk(request):
  
    final_score = request.session.get("score", 0)  

    print(f"DEBUG: Session Data in Risk View: {request.session.items()}") 
    print(f"DEBUG: Final score retrieved in risk view: {final_score}")  

    return render(request, "app/risk.html", {"final_score": final_score})
def riskforstartup(request):
    final_score = request.session.get("startup_score", 0)  

    print(f"DEBUG: Final score retrieved in risk view: {final_score}") 

    return render(request, "app/risk.html", {"final_score": final_score})

def endgame(request):
    return render(request,'app/endgame.html')
def save_score(request, score):
    user = request.user  
    user_score, created = UserScore.objects.get_or_create(
        username=user.username, 
        defaults={"score": score}  
    )

    if not created:
        user_score.score = max(user_score.score, score)  
        user_score.save()

    print(f"DEBUG: Final Saved Score: {user_score.score}")  

    return render(request, "leaderboard.html", {"scores": UserScore.objects.all()})

def leaderboard(request):
    scores = UserScore.objects.order_by('-score') 
    print("DEBUG: Leaderboard scores from DB:", scores)  

    return render(request, "app/leaderboard.html", {"scores": scores})

def quizforinvestor(request, question_id):

    question = get_object_or_404(Question1, id=question_id) 
 
    if question_id == 1:
        print("DEBUG: Resetting score for a new investor quiz session.")
        request.session["score"] = 0  
        request.session.modified = True

    score = request.session.get("score", 0)  
    print(f"DEBUG: Score at start of quizforinvestor: {score}")

    if request.method == "POST":
        user_answer = request.POST.get("answer")
        question = get_object_or_404(Question1, id=question_id)

        print(f"DEBUG: Before Update - Score: {score}")

        if user_answer == question.correct_option:
            score += 10
            print(f"DEBUG: Correct answer! Score increased to {score}")
        else:
            print(f"DEBUG: Incorrect answer. Score remains {score}")

        request.session["score"] = score
        request.session.modified = True  

        next_question = Question1.objects.filter(id__gt=question_id).order_by('id').first()

        if next_question is None:  
            final_score = request.session.get("score", 0)  
            request.session["final_score"] = final_score  
            request.session.modified = True  

            print(f"DEBUG: Storing Final Score before redirect: {final_score}")  
            print(f"DEBUG: Session Data Before Redirect to Risk: {request.session.items()}") 
            
            return redirect('showstartup')

        return redirect('quizforinvestor', question_id=next_question.id)
    options = [question.option1, question.option2, question.option3]
    return render(request, "app/quizforinvestor.html", {
                "question": question.text,
        "options": options, 
        "question_id": question_id,
        "score": score
    })


def home(request):
    request.session["score"] = 0 
    request.session.modified = True  
    print(f"DEBUG: Score after reset in home: {request.session.get('score', 0)}")

    first_question = Question.objects.order_by('id').first()
    if first_question:
        return redirect('quiz', question_id=first_question.id)

    return render(request, 'app/index.html', {'message': "No questions available."})

def home1(request):
    request.session["score"] = 0  
    request.session.modified = True  
    print(f"DEBUG: Score after reset in home: {request.session.get('score', 0)}")

    first_question = Question.objects.order_by('id').first()
    if first_question:
        return redirect('quiz', question_id=first_question.id)

    return render(request, 'app/index.html', {'message': "No questions available."})


def quiz_view(request, question_id):
    all_question_ids = list(Question.objects.values_list('id', flat=True))

  
    if question_id not in all_question_ids:
        first_question = Question.objects.order_by('id').first()
        if first_question:
            return redirect('quiz', question_id=first_question.id)
        return render(request, 'app/index.html', {'message': "No questions available."})

    question = get_object_or_404(Question, id=question_id)
    current_index = all_question_ids.index(question_id)
    next_question_id = all_question_ids[current_index + 1] if current_index + 1 < len(all_question_ids) else None


    if question_id == all_question_ids[0]:  
        request.session["startup_score"] = 0
        request.session.modified = True  

    if request.method == "POST":
        selected_answer = request.POST.get("answer")

        if selected_answer: 
            if selected_answer == question.correct_option:
                request.session["startup_score"] += 10

            request.session.modified = True  

            if next_question_id is None:
                request.session["final_score"] = request.session.get("startup_score", 0)
                request.session.modified = True  
                return redirect('riskforstartup')  

            return redirect('quiz', question_id=next_question_id)
        else:
            print("DEBUG: No answer selected.")

    options = [opt for opt in [question.option1, question.option2, question.option3] if opt]

    return render(request, 'app/quiz.html', {
        'question': question.text,
        'options': options,
        'question_id': question.id,
        'show_next_button': next_question_id is not None
    })



def quiz_view1(request, question_id):
    question = get_object_or_404(Question1, id=question_id)
    all_question_ids = list(Question1.objects.values_list('id', flat=True))
    try:
        current_index = all_question_ids.index(int(question_id))
        next_question_id = all_question_ids[current_index + 1] if current_index + 1 < len(all_question_ids) else None
    except ValueError:
        next_question_id = None  

  
    if "score" not in request.session or question_id == 1:
        print("DEBUG: Resetting score at start of investor quiz.")
        request.session["score"] = 0
        request.session.modified = True  

    if request.method == "POST":
        selected_answer = request.POST.get("answer")

        print(f"DEBUG: Before Update - Score: {request.session.get('score', 0)}")

        if selected_answer == question.correct_option:
            request.session["score"] += 10  

        print(f"DEBUG: After Update - Score: {request.session['score']}")

        request.session.modified = True  

        if next_question_id is None:
            return redirect('risk')  

        return redirect('quizforinvestor', question_id=next_question_id)

    options = [question.option1, question.option2, question.option3]
    options = [opt for opt in options if opt]

    return render(request, 'app/quizforinvestor.html', {
        'question': question.text,
        'options': options,
        'question_id': question.id,
        'show_next_button': next_question_id is not None
    })


def introduce_view(request):
    return render(request, "app/introduce.html") 

def showstartup(request):
    return render(request,"app/showstartup.html")
def introquiz(request):
    return render(request,"app/introquiz.html")
def kuttyintro(request):
    return render(request,"app/kuttyintro.html")
def notification(request):
    return render(request,"app/notification.html")
