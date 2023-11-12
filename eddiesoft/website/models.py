from django.db import models

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    price = models.IntegerField(choices=[(1200, '1200'), (1500, '1500'), (1800, '1800'), (2000, '2000'), (2500, '2500'), (3000, '3000')])

    def __str__(self):
        return self.category_name


class Video(models.Model):
    catalog_number = models.AutoField(primary_key=True)
    video_number = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    actor = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    copies = models.IntegerField()
    movie_year = models.IntegerField()

    def __str__(self):
        return self.title


class Members(models.Model):
    member_number = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    date_of_registration = models.DateField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class RentedVideo(models.Model):
    rental_number = models.AutoField(primary_key=True)
    member_number = models.ForeignKey(Members, on_delete=models.CASCADE)
    catalog_number = models.ForeignKey(Video, on_delete=models.CASCADE)
    date_of_rent = models.DateField()
    due_date = models.DateField()
    date_of_return = models.DateField(null=True, blank=True)

     # Add the due_date attribute

    def __str__(self):
        return f"Rental Number: {self.rental_number}"


class Branch(models.Model):
    branch_number = models.AutoField(primary_key=True)
    telephone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.address


class Staff(models.Model):
    staff_number = models.AutoField(primary_key=True)
    staff_names = models.CharField(max_length=255)
    salary = models.IntegerField()
    position = models.CharField(max_length=255)
    # Add foreign key for branch
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.staff_names



