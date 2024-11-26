from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class FoodItem(models.Model):
    name = models.CharField(max_length=100, unique=True)
    calories = models.FloatField()  
    protein = models.FloatField() 
    carbs = models.FloatField()  
    fats = models.FloatField()  
    default_weight = models.FloatField(default=100)  

    def __str__(self):
        return self.name

class MealFoodItem(models.Model):
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE, related_name='meal_food_items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.FloatField() 

    def calculated_calories(self):
        return (self.food_item.calories / self.food_item.default_weight) * self.quantity

    def calculated_protein(self):
        return (self.food_item.protein / self.food_item.default_weight) * self.quantity

    def calculated_carbs(self):
        return (self.food_item.carbs / self.food_item.default_weight) * self.quantity

    def calculated_fats(self):
        return (self.food_item.fats / self.food_item.default_weight) * self.quantity

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    meal_name = models.CharField(max_length=50)

    def total_calories(self):
        return sum(item.calculated_calories() for item in self.meal_food_items.all())

    def total_protein(self):
        return sum(item.calculated_protein() for item in self.meal_food_items.all())

    def total_carbs(self):
        return sum(item.calculated_carbs() for item in self.meal_food_items.all())

    def total_fats(self):
        return sum(item.calculated_fats() for item in self.meal_food_items.all())


class DailyLog(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.FloatField(help_text="Quantity in grams")
    date = models.DateField(default=now)
    calories = models.FloatField(editable=False)
    protein = models.FloatField(editable=False)
    carbs = models.FloatField(editable=False)
    fats = models.FloatField(editable=False)

    def save(self, *args, **kwargs):
        factor = self.quantity / self.food_item.default_weight
        self.calories = self.food_item.calories * factor
        self.protein = self.food_item.protein * factor
        self.carbs = self.food_item.carbs * factor
        self.fats = self.food_item.fats * factor
        super().save(*args, **kwargs)