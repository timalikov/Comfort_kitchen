from django.urls import path
from . import views

urlpatterns = [
    path('create_menu/', views.create_menu, name='create_menu'),
    path('menu_detail/<int:menu_id>/', views.menu_detail, name='menu_detail'),
    path('select_meals/<int:menu_id>/', views.select_meals, name='select_meals'),
    path('report/<int:menu_id>/', views.kitchen_report, name="report"),
    path('qr_code/', views.generate_qr_code, name='qr_code'),
    path('success/', views.success, name='success'),
]

