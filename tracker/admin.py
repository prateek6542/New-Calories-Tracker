from django.contrib import admin
from .models import FoodItem, Meal, MealFoodItem

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'protein', 'carbs', 'fats', 'default_weight')
    search_fields = ('name',)
    list_filter = ('calories', 'protein', 'carbs', 'fats')

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_name', 'date')
    list_filter = ('date', 'meal_name')
    search_fields = ('user__username', 'meal_name')
    date_hierarchy = 'date'

class MealFoodItemInline(admin.TabularInline):
    model = MealFoodItem
    extra = 1  # Number of empty rows for adding food items directly in Meal

@admin.register(MealFoodItem)
class MealFoodItemAdmin(admin.ModelAdmin):
    list_display = ('meal', 'food_item', 'quantity')
    list_filter = ('meal', 'food_item')
    search_fields = ('meal__meal_name', 'food_item__name')
