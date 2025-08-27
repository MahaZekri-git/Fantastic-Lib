from . import views
from django.urls import path




urlpatterns = [
    path('',views.index),
    path('signin',views.signin_page),
    path('signup',views.signup_page),
    path('contact',views.contact_page),
    path('categories',views.category_page),
    path('about',views.about_page),
    path('book_list',views.book_list), 
    path('<slug:slug>',views.book_detail,),  
    path('author/author_list',views.author_list),
    path('<slug:slug>/author',views.author_detail),
    path('<slug:slug>/books',views.author_book_list),
    path('user/logout',views.logout),
    path('download/<slug:slug>',views.DownloadBook),
    path('delete/<slug:slug>',views.delete_testimonial)


    
    ]