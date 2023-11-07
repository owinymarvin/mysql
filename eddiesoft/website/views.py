from django.shortcuts import render
from .models import *


def home(request):
    page='home'

    if request.method == 'POST':
        branch_number = request.POST['branch_number']
        if branch_number:
            branch_search = Branch.objects.filter(branch_number = branch_number)
            context = {'page':'branch','branch': branch_search}
            return render(request, 'website/branch.html', context)
        

        staff_number = request.POST['staff_number']
        if staff_number:
            staff_search = Staff.objects.filter(staff_number=staff_number)
            context = {'page': 'staff', 'staff': staff_search}
            return render(request, 'website/staff.html', context)
        

        rented_video = request.POST['rented_video']
        if rented_video:
            rented_video_search = RentedVideo.objects.filter(rental_number=rented_video)
            context = {'page':'rented', 'rentedvideo': rented_video_search}
            return render(request, 'website/rentedvideo.html', context)
        

        video = request.POST['video']
        if video:
            video_search = Video.objects.filter(catalog_number = video)
            context = {'page': 'video', 'video': video_search}
            return render(request, 'website/video.html', context)
        

        category = request.POST['category']
        if category:
            category_search = Category.objects.filter(category_id = category)
            context = {'page': 'category', 'category': category_search}
            return render(request, 'website/category.html', context)
        
        members = request.POST['members']
        if members:
            members_search = Members.objects.filter(member_number=members)
            context = {'page': 'members', 'members': members_search}
            return render(request, 'website/members.html', context)

        
    context = {'page':page}
    return render(request, 'website/home.html', context)


def branch(request):
    page = 'branch'
    branch = Branch.objects.all()
    context = {'page': page, 'branch': branch}
    return render(request, 'website/branch.html', context)


def staff(request):
    page='staff'
    staff = Staff.objects.all()
    context = {'page': page, 'staff': staff}
    return render(request, 'website/staff.html', context)


def rentedvideo(request):
    page='rented'
    rentedvideo = RentedVideo.objects.all()
    context = {'page': page, 'rentedvideo': rentedvideo}
    return render(request, 'website/rentedvideo.html', context)


def video(request):
    page='video'
    video = Video.objects.all()
    context = {'page': page, 'video': video}
    return render(request, 'website/video.html', context)


def category(request):
    page='category'
    category = Category.objects.all()
    context = {'page': page, 'category': category}
    return render(request, 'website/category.html', context)


def members(request):
    page='members'
    members = Members.objects.all()
    context = {'page': page, 'members': members}
    return render(request, 'website/members.html', context)


def movie_sales_report(request):
    page='movie_sales_report'
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        print(f"Start Date: {start_date}, End Date: {end_date}")

        sales = RentedVideo.objects.filter(
            date_of_rent__range=[start_date, end_date]
        ).extra(
            select={'sales_amount': 'category_price * DATEDIFF(IFNULL(date_of_return, CURDATE()), date_of_rent)'}
        )
        print(f"Sales Query: {sales.query}")

    else:
        sales = []

    context = {'page': page, 'sales': sales}
    return render(request, 'website/movie_sales_report.html', context)
