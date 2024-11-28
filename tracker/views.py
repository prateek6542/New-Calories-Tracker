from django.shortcuts import render, redirect
from .models import FoodItem, Meal, MealFoodItem, DailyLog
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

def dashboard(request):
    today = now().date()
    
    if request.method == 'POST':
        food_id = request.POST.get('food_item')
        quantity = float(request.POST.get('quantity'))
        food_item = FoodItem.objects.get(id=food_id)
        DailyLog.objects.create(food_item=food_item, quantity=quantity, date=today)
        
    logs = DailyLog.objects.filter(date=today)
    total_calories = sum(log.calories for log in logs)
    total_protein = sum(log.protein for log in logs)
    total_carbs = sum(log.carbs for log in logs)
    total_fats = sum(log.fats for log in logs)

    context = {
        'logs': logs,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_carbs': total_carbs,
        'total_fats': total_fats,
        'food_items': FoodItem.objects.all(),
    }
    return render(request, 'tracker/dashboard.html', context)

def delete_log(request, log_id):
    log = DailyLog.objects.get(id=log_id)
    log.delete()
    return redirect('home')

def daily_log(request):
    today = now().date()
    if request.method == 'POST':
        food_id = request.POST.get('food_item')
        quantity = float(request.POST.get('quantity'))
        food_item = FoodItem.objects.get(id=food_id)
        DailyLog.objects.create(food_item=food_item, quantity=quantity, date=today)

    logs = DailyLog.objects.filter(date=today)
    total_calories = sum(log.calories for log in logs)
    total_protein = sum(log.protein for log in logs)
    total_carbs = sum(log.carbs for log in logs)
    total_fats = sum(log.fats for log in logs)

    context = {
        'logs': logs,
        'total_calories': total_calories,
        'total_protein': total_protein,
        'total_carbs': total_carbs,
        'total_fats': total_fats,
        'food_items': FoodItem.objects.all(),
    }
    return render(request, 'tracker/daily_log.html', context)


@login_required
def log_meal(request):
    if request.method == "POST":
        meal_name = request.POST['meal_name']
        meal = Meal.objects.create(user=request.user, meal_name=meal_name)

        for key, value in request.POST.items():
            if key.startswith('food_item_') and value:
                food_id = value
                quantity_key = f'quantity_{food_id}'
                quantity = float(request.POST.get(quantity_key, 0))
                if quantity > 0:
                    food_item = FoodItem.objects.get(id=food_id)
                    MealFoodItem.objects.create(meal=meal, food_item=food_item, quantity=quantity)

        return redirect('dashboard')

    food_items = FoodItem.objects.all()
    return render(request, 'tracker/log_meal.html', {'food_items': food_items})

@login_required
def add_food_item(request):
    if request.method == "POST":
        name = request.POST['name']
        calories = float(request.POST['calories'])
        protein = float(request.POST['protein'])
        carbs = float(request.POST['carbs'])
        fats = float(request.POST['fats'])
        default_weight = float(request.POST['default_weight'])
        FoodItem.objects.create(
            name=name,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fats=fats,
            default_weight=default_weight,
        )
        return redirect('log_meal')
    return render(request, 'tracker/add_food_item.html')
