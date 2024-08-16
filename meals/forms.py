from django import forms
from django.forms import inlineformset_factory
from .models import Menu, MenuMealTime, Meal

class MenuForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',  # This uses the HTML5 date input
                'class': 'form-control',  # You can add Bootstrap classes if you're using Bootstrap
            }
        )
    )

    class Meta:
        model = Menu
        fields = ['name', 'date']

class MenuMealTimeForm(forms.ModelForm):
    meals = forms.ModelMultipleChoiceField(
        queryset=Meal.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Use checkboxes to select multiple meals
        required=True
    )

    class Meta:
        model = MenuMealTime
        fields = ['meal_time', 'meals'] 

# Create the formset for linking MealTime and Meals to the Menu
MenuMealTimeFormSet = inlineformset_factory(
    Menu,
    MenuMealTime,
    form=MenuMealTimeForm,  # Use the custom form
    extra=1,  # Start with one empty form
    can_delete=True  # Allow deletion of meal times if needed
)