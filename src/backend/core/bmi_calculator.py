"""
Module to calculate BMI and determine weight category.

Steps to calculate BMI:
1. Convert height from centimeters to meters.
2. Use the formula: BMI = weight (kg) / (height (m) * height (m))
3. Determine weight category based on BMI value:

If BMI is less than 18.5, the person is underweight.
If BMI is between 18.5 and 24.9, the person has a normal weight.
If BMI is between 25 and 29.9, the person is overweight.
If BMI is 30 or more, the person is obese.

Displays the BMI value and the weight category.

"""

def bmi_calculator(height, weight):
    # Calculate BMI
    height_m = height / 100
    bmi = weight / (height_m * height_m)
    return round(bmi, 2)

def get_bmi_category(bmi):
    # Calculate category
    category = ""
    if bmi < 18.5:
        category = "underweight"
    elif 18.5 <= bmi < 25:
        category = "normal"
    elif 25 <= bmi < 30:
        category = "overweight"
    else:
        category = "obese"

    return category

