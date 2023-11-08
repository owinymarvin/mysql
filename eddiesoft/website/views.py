from django.db import connection
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


def movie_rental_report(request):
    page = 'movie_rental_report'
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                website_rentedvideo.rental_number,
                website_video.title,
                website_category.category_name,
                website_category.price AS category_price,
                website_rentedvideo.date_of_rent,
                IFNULL(website_rentedvideo.date_of_return, CURDATE()) AS date_of_return,
                DATEDIFF(IFNULL(website_rentedvideo.date_of_return, CURDATE()), website_rentedvideo.date_of_rent) AS days_taken,
                (
                    CASE
                        WHEN website_category.price = '1200' THEN 1200
                        WHEN website_category.price = '1500' THEN 1500
                        WHEN website_category.price = '1800' THEN 1800
                        WHEN website_category.price = '2000' THEN 2000
                        WHEN website_category.price = '2500' THEN 2500
                        WHEN website_category.price = '3000' THEN 3000
                    END
                ) * DATEDIFF(IFNULL(website_rentedvideo.date_of_return, CURDATE()), website_rentedvideo.date_of_rent) AS daily_rental_cost,
                website_video.copies - COALESCE(
                    (SELECT COUNT(*) FROM website_rentedvideo AS r WHERE r.catalog_number_id = website_video.catalog_number AND r.date_of_return IS NULL), 0
                ) AS remaining_copies
            FROM website_rentedvideo
            JOIN website_video ON website_rentedvideo.catalog_number_id = website_video.catalog_number
            JOIN website_category ON website_video.category_id = website_category.category_id;
        """)

        db_query_report = cursor.fetchall()

    context = {'page':page,'db_query_report': db_query_report}
    return render(request, 'website/movie_rental_report.html', context)



def earnings_summary(request):
    page = 'earnings_summary'
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                SUM(
                    CASE
                        WHEN website_category.category_name = 'Children' THEN website_category.price * DATEDIFF(IFNULL(website_rentedvideo.date_of_return, CURDATE()), website_rentedvideo.date_of_rent)
                        ELSE 0
                    END
                ) AS children_earnings,
                SUM(
                    CASE
                        WHEN website_category.category_name = 'Drama' THEN website_category.price * DATEDIFF(IFNULL(website_rentedvideo.date_of_return, CURDATE()), website_rentedvideo.date_of_rent)
                        ELSE 0
                    END
                ) AS drama_earnings,
                SUM(
                    CASE
                        WHEN website_category.category_name = 'Horror' THEN website_category.price * DATEDIFF(IFNULL(website_rentedvideo.date_of_return, CURDATE()), website_rentedvideo.date_of_rent)
                        ELSE 0
                    END
                ) AS horror_earnings,
                SUM(
                    CASE
                        WHEN website_category.category_name = 'Action' THEN website_category.price * DATEDIFF(IFNULL(website_rentedvideo.date_of_return, CURDATE()), website_rentedvideo.date_of_rent)
                        ELSE 0
                    END
                ) AS action_earnings,
                SUM(
                    CASE
                        WHEN website_category.category_name = 'Adult' THEN website_category.price * DATEDIFF(IFNULL(website_rentedvideo.date_of_return, CURDATE()), website_rentedvideo.date_of_rent)
                        ELSE 0
                    END
                ) AS adult_earnings,
                SUM(
                    CASE
                        WHEN website_category.category_name = 'Sci-Fi' THEN website_category.price * DATEDIFF(IFNULL(website_rentedvideo.date_of_return, CURDATE()), website_rentedvideo.date_of_rent)
                        ELSE 0
                    END
                ) AS scifi_earnings,
                SUM(
                    CASE
                        WHEN website_category.category_name IN ('Children','Drama','Action','Horror', 'Adult','Sci-Fi') THEN website_category.price * DATEDIFF(IFNULL(website_rentedvideo.date_of_return, CURDATE()), website_rentedvideo.date_of_rent)
                        ELSE 0
                    END
                ) AS total_earnings
            FROM website_rentedvideo
            JOIN website_video ON website_rentedvideo.catalog_number_id = website_video.catalog_number
            JOIN website_category ON website_video.category_id = website_category.category_id;
        """)

        earnings_summary = cursor.fetchone()

    context = {'page':page,'earnings_summary': earnings_summary}
    return render(request, 'website/earnings_summary.html', context)




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


def query_customer_video(request):
    page = 'query_customer_video'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                m.member_number AS Customer_ID,
                m.first_name AS Customer_First_Name,
                m.last_name AS Customer_Last_Name,
                v.title AS Video_Title,
                IFNULL(rv.date_of_return, CURDATE()) AS Due_Date,
                CASE
                    WHEN v.copies >= 1 THEN 'Available'
                    ELSE 'Unavailable'
                END AS State,
                (SELECT COUNT(*) FROM website_rentedvideo AS r WHERE r.member_number_id = m.member_number) AS Total_Videos_Borrowed
            FROM
                website_members AS m
                LEFT JOIN website_rentedvideo AS rv ON m.member_number = rv.member_number_id
                LEFT JOIN website_video AS v ON rv.catalog_number_id = v.catalog_number;
        """)
        
        db_query_report = cursor.fetchall()

    context = {'page': page, 'query_customer_video': db_query_report}
    return render(request, 'website/query_customer_video.html', context)
