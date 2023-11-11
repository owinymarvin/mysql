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
    path('query_2/', views.query_2,name='query_2'),
    path('query_3/', views.query_3, name='query_3'),
    path('query_4/', views.query_4, name='query_4'),
    path('query_5/', views.query_5, name='query_5'),
    path('query_6/', views.query_6, name='query_6'),
    path('query_7/', views.query_7, name='query_7'),
    path('query_8/', views.query_8, name='query_8'),
    path('query_9/', views.query_9, name='query_9'),
    path('query_10/', views.query_10, name='query_10'),
    path('query_11/', views.query_11, name='query_11'),
    path('query_12/', views.query_12, name='query_12'),
    path('query_13/', views.query_13, name='query_13'),

]
