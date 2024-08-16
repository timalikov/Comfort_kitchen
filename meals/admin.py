from django.contrib import admin
from .models import Meal, Category, MealTime, Menu, MenuMealTime, UserMealSelection

admin.site.register(Meal)
admin.site.register(Category)
admin.site.register(MealTime)
admin.site.register(Menu)
admin.site.register(MenuMealTime)
admin.site.register(UserMealSelection)