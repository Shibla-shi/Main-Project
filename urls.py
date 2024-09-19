
from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [
    path('login/',views.login),
    path('login_post/',views.login_post),
    path('signup/',views.signup),
    path('signup_post/', views.signup_post),
    path('changepassword/',views.changepassword),
    path('changepassword_post/', views.changepassword_post),
    path('uchangepassword/',views.uchangepassword),
    path('uchangepassword_post/', views.uchangepassword_post),
    path('addcategory/',views.addcategory),
    path('addcategory_post/', views.addcategory_post),
    path('updatecategory/<id>',views.updatecategory),
    path('updatecategory_post/', views.updatecategory_post),
    path('viewcategory/',views.viewcategory),
    path('viewcategory_POST/', views.viewcategory_POST),
    path('viewuserpreference/',views.viewuserpreference),
    path('viewuserpreference_POST/', views.viewuserpreference_POST),
    path('deletecategory/<id>',views.deletecategory),
    path('deletepreference/<id>', views.deletepreference),
    path('preference/',views.preference),
    path('preference_post/', views.preference_post),
    path('viewadminnews/',views.viewadminnews),
    path('viewadminnews_post/', views.viewadminnews_post),
    path('viewuserprofile/', views.viewuserprofile),
    path('viewuserprofile_post/', views.viewuserprofile_post),
    path('viewreviews/',views.viewreviews),
    path('viewreviews_post/', views.viewreviews_post),
    path('viewusernews/', views.viewusernews),
    path('viewusernews_post/', views.viewusernews_post),
    path('adminlink/',views.adminlink),
    path('userlink/', views.userlink),
    path('reviews/', views.reviews),
    path('reviews_post/', views.reviews_post),
    path('forgotpassword/', views.forgotpassword),
    path('forgotpassword_post/', views.forgotpassword_post),
    path('getscrapedcontent/', views.getscrapedcontent),
    path('getcontentbbc/', views.getcontentbbc),
    path('getcontenttoi/', views.getcontenttoi),
    path('readnews/', views.readnews)

]
