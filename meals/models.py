from django.db import models

# Create your models here.

class Meal(models.Model):
    DIET_CHOICES = [
        (1, 'Diet 1'),
        (2, 'Diet 2'),
        (3, 'Diet 3'),
        (4, 'Diet 4'),
        (5, 'Diet 5'),
        (6, 'Diet 6'),
        (7, 'Diet 7'),
        (8, 'Diet 8'),
        (9, 'Diet 9'),
        (10, 'Diet 10'),
        (11, 'Diet 11'),
        (12, 'Diet 12'),
        (13, 'Diet 13'),
        (14, 'Diet 14'),
        (15, 'Diet 15'),
    ]

    name = models.CharField(max_length=100)
    kcal = models.IntegerField()
    diet_category = models.IntegerField(choices=DIET_CHOICES)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MealTime(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    meal_times = models.ManyToManyField(MealTime, through='MenuMealTime')

    def __str__(self):
        return f"{self.name} ({self.date})"

class MenuMealTime(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    meal_time = models.ForeignKey(MealTime, on_delete=models.CASCADE)
    meals = models.ManyToManyField(Meal)

    def __str__(self):
        return f"{self.menu} - {self.meal_time}"

    class Meta:
        unique_together = ('menu', 'meal_time')

class UserMealSelection(models.Model):
    menu_mealtime = models.ForeignKey('MenuMealTime', on_delete=models.CASCADE)
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE)
    table_number = models.IntegerField()
    seat_number = models.IntegerField()
    date_selected = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Table {self.table_number}, Seat {self.seat_number} selected {self.meal.name} for {self.menu_mealtime.meal_time.name}"