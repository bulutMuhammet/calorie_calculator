from django.contrib import messages
from django.shortcuts import render

def calculate_required_calorie(gender,age,height,weight):
    if gender=="male":
        return int(66 + 13.7 * weight + 5 * height - 6.8 * age)
    elif gender=="female":
        return int(655 + 9.6 * weight + 1.8 * height - 4.7 * age)

def index(request):

    # Source:  USDA
    calories={
        "apple":[52.1,0.3],   # 0=calorie , 1=protein
        "pasta":[131,5],
        "banana":[88.7,1.1],
        "chocolate":[545.6,4.9],
        "fish":[205.8,22],
        "chicken":[239,27],
        "meatball":[197,21],
        "chips":[536.1,7],
        "bread":[264.6,9],
        "beef":[250.5,26],
    }

    gender=request.POST.getlist("gender")
    age=request.POST.get("age")
    weight=request.POST.get("weight")
    height=request.POST.get("height")
    values=calories.keys()
    context = {"values":values}
    if request.method == 'POST':
        required_calorie=calculate_required_calorie(gender[0],int(age),int(weight),int(height))
        print(required_calorie)
        foods=request.POST.getlist('foods')
        calorie=0
        protein=0
        if len(foods)==0:
            messages.info(request,"Please select at least one food.")
        for i in foods:
            calorie+=calories.get(i)[0]
            protein+=calories.get(i)[1]

            rate=(int(calorie)/int(required_calorie))*100

            context.update({"rate":int(rate),"calorie":int(calorie),"protein":protein,"required_calorie":int(required_calorie),"status":int(required_calorie-calorie)})
        messages.info(request, "Succesfuly calculated! ")

    return render(request,"index.html",context=context)