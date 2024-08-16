from django.shortcuts import render, redirect,  get_object_or_404
from .models import Menu, MealTime, Meal, MenuMealTime, UserMealSelection
from .forms import MenuForm, MenuMealTimeFormSet  
from django.db.models import Count
from collections import defaultdict



def create_menu(request):
    if request.method == "POST":
        menu_form = MenuForm(request.POST)
        meal_time_formset = MenuMealTimeFormSet(request.POST)

        if menu_form.is_valid() and meal_time_formset.is_valid():
            # Save the menu
            menu = menu_form.save()

            # Save the meal times and associated meals
            meal_time_formset.instance = menu
            meal_time_formset.save()

            return redirect('menu_detail', menu_id=menu.id)  # Redirect to a view that shows the created menu

    else:
        menu_form = MenuForm()
        meal_time_formset = MenuMealTimeFormSet()

    return render(request, 'create_menu.html', {
        'menu_form': menu_form,
        'meal_time_formset': meal_time_formset,
    })

def menu_detail(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    meal_times_with_meals = []

    for meal_time in menu.meal_times.all():
        meals = menu.menumealtime_set.filter(meal_time=meal_time).first().meals.all()
        meal_times_with_meals.append((meal_time, meals))

    return render(request, 'menu_detail.html', {
        'menu': menu,
        'meal_times_with_meals': meal_times_with_meals,
    })

def select_meals(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    
    if request.method == "POST":
        table_number = request.POST.get("table_number")
        seat_number = request.POST.get("seat_number")
        
        for meal_time in menu.meal_times.all():
            menu_mealtime = menu.menumealtime_set.get(meal_time=meal_time)
            categories = menu_mealtime.meals.values_list('category_id', flat=True).distinct()

            for category_id in categories:
                selected_meal_id = request.POST.get(f"meal_{meal_time.id}_{category_id}")
                if selected_meal_id:
                    selected_meal = menu_mealtime.meals.get(id=selected_meal_id)
                    UserMealSelection.objects.create(
                        menu_mealtime=menu_mealtime,
                        meal=selected_meal,
                        table_number=table_number,
                        seat_number=seat_number
                    )
        return redirect('menu_detail', menu_id=menu.id)
    
    meal_times_with_options = []
    for meal_time in menu.meal_times.all():
        menu_mealtime = menu.menumealtime_set.get(meal_time=meal_time)
        meals = menu_mealtime.meals.all().order_by('category__name', 'name')
        meal_times_with_options.append((meal_time, meals))
    
    return render(request, 'select_meals.html', {
        'menu': menu,
        'meal_times_with_options': meal_times_with_options,
    })



def kitchen_report(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)

    # Define the seating arrangement (e.g., table 1 has 4 seats, table 2 has 2 seats, etc.)
    seating_arrangement = {
        1: 4,
        2: 4,
        3: 4,
        4: 4,
        5: 2,
        6: 2,
        7: 4,
        8: 4,
        9: 2,
        10: 4,
        # Add more tables as needed
    }

    # Create a list of all possible table and seat combinations
    all_seats = [(table_number, seat_number) for table_number, seat_count in seating_arrangement.items() for seat_number in range(1, seat_count + 1)]

    # Get the list of filled seats from UserMealSelection
    filled_seats = UserMealSelection.objects.filter(menu_mealtime__menu=menu).values_list('table_number', 'seat_number')

    # Determine unfilled seats by comparing all_seats with filled_seats
    unfilled_seats = defaultdict(list)
    for seat in all_seats:
        if seat not in filled_seats:
            unfilled_seats[seat[0]].append(seat[1])
    print(unfilled_seats)

    # Total number of each meal to be prepared
    meals_to_cook = UserMealSelection.objects.filter(menu_mealtime__menu=menu).values('meal__name').annotate(total=Count('meal'))

    # Detailed serving plan (table and seat assignments)
    serving_plan = UserMealSelection.objects.filter(menu_mealtime__menu=menu).order_by('table_number', 'seat_number')

    # Calculate the total number of unique people who have completed their selections
    total_people = filled_seats.distinct().count()

    return render(request, 'kitchen_report.html', {
        'menu': menu,
        'meals_to_cook': meals_to_cook,
        'serving_plan': serving_plan,
        'total_people': total_people,
        'unfilled_seats': dict(unfilled_seats),  # Pass the unfilled seats dictionary to the template
    })