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
    path('movie_rental_report/', views.movie_rental_report,name='movie_rental_report'),
    path('earnings_summary_report/', views.earnings_summary,name='earnings_summary'),
    path('query_customer_video/', views.query_customer_video,name='query_customer_video'),


]
