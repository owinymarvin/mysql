from django.db import connection
from django.shortcuts import render
from .models import *
from django.db.models import Q


from django.db.models import Q


def home(request):
    page = 'home'

    if request.method == 'POST':
        branch_number = request.POST.get('branch_number')
        staff_number = request.POST.get('staff_number')
        rented_video = request.POST.get('rented_video')
        video = request.POST.get('video')
        category = request.POST.get('category')
        members = request.POST.get('members')

        if branch_number:
            branch_search = Branch.objects.filter(branch_number=branch_number)
            context = {'page': 'branch', 'branch': branch_search}
            return render(request, 'website/branch.html', context)

        if staff_number:
            staff_search = Staff.objects.filter(
                Q(staff_names__icontains=staff_number))
            context = {'page': 'staff', 'staff': staff_search}
            return render(request, 'website/staff.html', context)

        if rented_video:
            rented_video_search = RentedVideo.objects.filter(
                rental_number=rented_video)
            context = {'page': 'rented', 'rentedvideo': rented_video_search}
            return render(request, 'website/rentedvideo.html', context)

        if video:
            video_search = Video.objects.filter(
                Q(title__icontains=video) | Q(
                    actor__icontains=video)
            )
            context = {'page': 'video', 'video': video_search}
            return render(request, 'website/video.html', context)


        if category:
            category_search = Category.objects.filter(
                Q(category_id__icontains=video) | Q(category_name__icontains=video)
            )
            context = {'page': 'category', 'category': category_search}
            return render(request, 'website/category.html', context)


        if members:
            members_search = Members.objects.filter(
                Q(member_number__icontains=members) | Q(first_name__icontains=members) | Q(last_name__icontains=members)
            )
            context = {'page': 'members', 'members': members_search}
            return render(request, 'website/members.html', context)


    context = {'page': page}
    return render(request, 'website/home.html', context)


def branch(request):
    page = 'branch'
    branch = Branch.objects.all()
    context = {'page': page, 'branch': branch}
    return render(request, 'website/branch.html', context)


def staff(request):
    page = 'staff'
    staff = Staff.objects.all()
    context = {'page': page, 'staff': staff}
    return render(request, 'website/staff.html', context)


def rentedvideo(request):
    page = 'rented_video'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                rv.rental_number AS Rental_Number,
                v.title AS Movie_Title,
                m.first_name as First_Name,
                m.last_name as Last_Name,
                cat.category_name AS Category_Name,
                rv.date_of_rent AS Date_of_Rent,
                rv.due_date AS Due_Date,
                IFNULL(rv.date_of_return, CURDATE()) AS Date_of_Return
            FROM
                website_rentedvideo AS rv
                LEFT JOIN website_video AS v ON rv.catalog_number_id = v.catalog_number
                LEFT JOIN website_members AS m ON rv.member_number_id = m.member_number
                LEFT JOIN website_category AS cat ON v.category_id = cat.category_id;     
        """)

        db_query_report = cursor.fetchall()

    context = {'page': page, 'rentedvideo': db_query_report}
    return render(request, 'website/rentedvideo.html', context)

    


def video(request):
    page = 'video'
    video = Video.objects.all()
    context = {'page': page, 'video': video}
    return render(request, 'website/video.html', context)


def category(request):
    page = 'category'
    category = Category.objects.all()
    context = {'page': page, 'category': category}
    return render(request, 'website/category.html', context)


def members(request):
    page = 'members'
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

    context = {'page': page, 'db_query_report': db_query_report}
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

    context = {'page': page, 'earnings_summary': earnings_summary}
    return render(request, 'website/earnings_summary.html', context)


def movie_sales_report(request):
    page = 'movie_sales_report'
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        print(f"Start Date: {start_date}, End Date: {end_date}")

        sales = RentedVideo.objects.filter(
            date_of_rent__range=[start_date, end_date]
        ).extra(
            select={
                'sales_amount': 'category_price * DATEDIFF(IFNULL(date_of_return, CURDATE()), date_of_rent)'}
        )
        print(f"Sales Query: {sales.query}")

    else:
        sales = []

    context = {'page': page, 'sales': sales}
    return render(request, 'website/movie_sales_report.html', context)


def query_2(request):
    page = 'query_2'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                m.first_name AS Customer_First_Name,
                m.last_name AS Customer_Last_Name,
                v.title AS Video_Title,
                IFNULL(rv.date_of_return, CURDATE()) AS Due_Date
            FROM
                website_members AS m
                LEFT JOIN website_rentedvideo AS rv ON m.member_number = rv.member_number_id
                LEFT JOIN website_video AS v ON rv.catalog_number_id = v.catalog_number;
        """)

        db_query_report = cursor.fetchall()

    context = {'page': page, 'query_2': db_query_report}
    return render(request, 'website/query_2.html', context)


def query_3(request):
    page = 'query_3'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                m.member_number AS Customer_ID,
                m.first_name AS Customer_First_Name,
                m.last_name AS Customer_Last_Name,
                v.title AS Video_Title,
                IFNULL(rv.date_of_return, CURDATE()) AS Due_Date,
                (v.copies - COALESCE((SELECT COUNT(*) FROM website_rentedvideo AS r WHERE r.catalog_number_id = v.catalog_number AND r.date_of_return IS NULL), 0)) AS Copies_Remaining,                       
                CASE
                    WHEN v.copies >= 1 THEN 'Available'
                    ELSE 'Unavailable'
                END AS State,
                (SELECT COUNT(DISTINCT r.catalog_number_id) FROM website_rentedvideo AS r WHERE r.member_number_id = m.member_number AND r.date_of_return IS NULL) AS Total_Videos_Borrowed
            FROM
                website_members AS m
                LEFT JOIN website_rentedvideo AS rv ON m.member_number = rv.member_number_id
                LEFT JOIN website_video AS v ON rv.catalog_number_id = v.catalog_number;
        """)

        db_query_report = cursor.fetchall()

    context = {'page': page, 'query_3': db_query_report}
    return render(request, 'website/query_3.html', context)


def query_4(request):
    page = 'query_4'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                video.catalog_number AS Movie_Number,
                video.title AS Movie_Title,
                category.price AS Movie_Cost
            FROM website_video AS video
            JOIN website_category AS category ON video.category_id = category.category_id
            WHERE category.price > 1500
            ORDER BY video.title ASC;
        """)
        db_query_report = cursor.fetchall()

    context = {'page': page, 'query_4': db_query_report}
    return render(request, 'website/query_4.html', context)


def query_5(request):
    page = 'query_5'

    with connection.cursor() as cursor:
        cursor.execute("""
          SELECT
            video.catalog_number AS Video_Number,
            video.title AS Movie_Title,
            rented.due_date AS Due_Date,
            rented.date_of_return AS Date_of_Return,
            DATEDIFF(rented.date_of_return, rented.due_date) AS Overdue_Days
        FROM
            website_video AS video
            JOIN website_rentedvideo AS rented ON video.catalog_number = rented.catalog_number_id
        WHERE
            rented.date_of_return > rented.due_date;
        """)
        db_query_report = cursor.fetchall()

    context = {'page': page, 'query_5': db_query_report}
    return render(request, 'website/query_5.html', context)


def query_6(request):
    page = 'query_6'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                website_video.catalog_number,
                website_video.title AS Movie_Title,
                website_category.price AS Movie_Cost,
                website_category.category_name AS Genre
            FROM website_video
            JOIN website_category ON website_video.category_id = website_category.category_id
            WHERE website_video.title LIKE '%s';


        """)
        db_query_report = cursor.fetchall()

    context = {'page': page, 'query_6': db_query_report}
    return render(request, 'website/query_6.html', context)


def query_7(request):
    page = 'query_7'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                website_category.category_id as category_id,
                website_category.category_name as category_name,
                website_category.price as price
            FROM
                website_category
            WHERE
                website_category.price > 1600
            GROUP BY
                category_id,category_name,price;

        """)
        db_query_report = cursor.fetchall()

    context = {'page': page, 'query_7': db_query_report}
    return render(request, 'website/query_7.html', context)




def query_8(request):
    page = 'query_8'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                m.member_number AS Membership_Number,
                m.first_name AS First_Name,
                m.last_name AS Last_Name,
                10 - COALESCE((
                    SELECT COUNT(*)
                    FROM website_rentedvideo AS rv
                    WHERE rv.member_number_id = m.member_number
                ), 0) AS Balance_of_Membership
            FROM
                website_members AS m
            WHERE
                EXISTS (
                    SELECT 1
                    FROM website_rentedvideo AS rv
                    WHERE rv.member_number_id = m.member_number
                );
        """)
        db_query_report = cursor.fetchall()

    context = {'page': page, 'query_8': db_query_report}
    return render(request, 'website/query_8.html', context)


def query_9(request):
    page = 'query_9'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                video.catalog_number AS Video_Number,
                video.title AS Movie_Title,
                website_category.category_name AS Category_Name,
                website_category.price AS Movie_Cost
            FROM
                website_video AS video
            JOIN 
                website_category ON website_category.category_id = video.category_id
            WHERE
                website_category.price > ALL (
                    SELECT
                        MAX(category.price)
                    FROM
                        website_category AS category
                    WHERE
                        category.category_name = 'Drama'
                );

        """)
        db_query_report = cursor.fetchall()

    context = {'page': page, 'query_9': db_query_report}
    return render(request, 'website/query_9.html', context)


def query_10(request):
    page = 'query_10'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                video.title AS Movie_Title,
                video.movie_year AS Movie_Year,
                category.category_name AS Category_Name,
                category.price AS Category_Price
            FROM
                website_video AS video
            JOIN 
                website_category AS category ON video.category_id = category.category_id
            WHERE
                category.category_name IN ('Sci-Fi', 'Adult', 'Drama');
        """)
        db_query_report = cursor.fetchall()

    context = {'page': page, 'query_10': db_query_report}
    return render(request, 'website/query_10.html', context)




def query_11(request):
    page = 'query_11'

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                m.member_number AS Membership_Number,
                m.first_name AS First_Name,
                m.last_name AS Last_Name,
                10 - COALESCE((
                    SELECT COUNT(*)
                    FROM website_rentedvideo AS rv
                    WHERE rv.member_number_id = m.member_number
                ), 0) AS Balance_of_Membership
            FROM
                website_members AS m
            WHERE
                EXISTS (
                    SELECT 1
                    FROM website_rentedvideo AS rv
                    WHERE rv.member_number_id = m.member_number
                );
        """)
        db_query_report = cursor.fetchall()

    context = {'page': page, 'query_11': db_query_report}
    return render(request, 'website/query_11.html', context)


def query_12(request):
    page = 'query_12'

    with connection.cursor() as cursor:
        cursor.execute("""
           SELECT
            video.catalog_number AS Video_Number,
            video.title AS Movie_Title,
            rented.due_date AS Due_Date,
            rented.date_of_return AS Date_of_Return,
            DATEDIFF(rented.date_of_return, rented.due_date) AS Overdue_Days
        FROM
            website_video AS video
            JOIN website_rentedvideo AS rented ON video.catalog_number = rented.catalog_number_id
        WHERE
            rented.date_of_return > rented.due_date;

        """)
        db_query_report = cursor.fetchall()

    context = {'page': page, 'query_12': db_query_report}
    return render(request, 'website/query_12.html', context)




def query_13(request):
    page = 'query_13'

    with connection.cursor() as cursor:
        cursor.execute("""
                       
        SELECT
            v.catalog_number AS Video_Number,
            v.title AS Movie_Title,
            v.movie_year AS Movie_Year
        FROM
            website_video AS v
        WHERE
            v.copies = (
                SELECT
                    COUNT(*)
                FROM
                    website_rentedvideo AS rv
                WHERE
                    rv.catalog_number_id = v.catalog_number
                    AND rv.date_of_return IS NULL
            );

        """)
        db_query_report = cursor.fetchall()

    context = {'page': page, 'query_13': db_query_report}
    return render(request, 'website/query_13.html', context)
