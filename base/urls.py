from unicodedata import name
from django.urls import path
from . import views

#import authentication view for password resetting
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.loginPage, name='login'),

    path('logout', views.logoutUser, name='logout'),
    
    path('register', views.userRegister, name='register'),

    path('profile/<str:pk>/', views.userProfile, name='profile'),

    path('', views.home, name="home"),
    path('rooms/<str:pk>/', views.room, name="rooms"),

    path('roomcreate/', views.createRoom, name="roomcreate"),

    path('roomupdate/<str:pk>/', views.updateRoom, name="roomupdate"),

    path('roomdelete/<str:pk>/', views.deleteRoom, name='roomdelete'),

    path('messagedel/<str:pk>/', views.deleteComment, name='messagedel'),
    
    path('updateuser', views.updateUser, name='updateuser'),

    path('motopics', views.allTopics, name='motopics'),

                                            #password reset views
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='base/resetpassword.html'), name='reset_password'), #submit email form

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='base/passwordsent.html'), name='password_reset_done') , # email sent success message
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='base/passwordconfirm.html'), name='password_reset_confirm'), #link to password reset form in email

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='base/passwordresetcomplete.html'), name='password_reset_complete') # password successfully changed message
]

#password reset
# PasswordResetView.as_view()           
#PasswordResetDoneView.as_view()        
#PasswordResetConfirmView.as_view()     
#PasswordResetCompleteView.as_view()     

