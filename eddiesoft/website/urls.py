from django.urls import path
from website import views

urlpatterns = [
    path('',views.home, name='home'),
    path('branch/',views.branch, name = "branch"),
    path('staff/', views.staff, name="staff"),
    path('rented_videos/', views.rentedvideo, name="rented_video"),
    path('videos/', views.video, name="video"),
    path('category/', views.category, name="category"),
    path('members/', views.members, name="members"),
    path('movie_sales_report/', views.movie_sales_report,name='movie_sales_report'),
]
