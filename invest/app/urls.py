from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  
from . import views  
from .views import register, user_login  

urlpatterns = [
     path("register/", register, name="register"),
   
    path("signup/", views.signup_view, name="signup"),
    path('admin/', admin.site.urls),
    
    # Other App Routes
    path('', views.index, name='index'),


    path('questioning/', views.questioning, name='questioning'),
    path('startupcard/', views.startupcard, name='startupcard'),
    path('loading/', views.loading, name='loading'),
    path('investoroption/', views.investoroption, name='investoroption'),
    path('home/', views.home, name='home'),
    path('riskforstartup/', views.riskforstartup, name='riskforstartup'),
    path('quiz/<int:question_id>/', views.quiz_view, name='quiz'),
    path('risk/', views.risk, name='risk'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('endgame/', views.endgame, name='endgame'),
    path('quizforinvestor/<int:question_id>/', views.quizforinvestor, name='quizforinvestor'),
    path("login/", views.user_login, name="login"),
    path("introduce/", views.introduce_view, name="introduce"),  
    path("showstartup/",views.showstartup,name='showstartup'),
    path("introquiz/",views.introquiz,name='introquiz'),
    path("intro/",views.kuttyintro,name="kuttyintro"),
    path("notification/",views.notification,name="notification"),
]
