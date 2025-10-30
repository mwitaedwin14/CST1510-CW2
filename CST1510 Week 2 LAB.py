#Threshold 1. Password strength checker
password = str(input("Enter your Password: "))
if len(password) < 8 :
    print("Weak")
elif len(password) <= 12 :
    print("Moderate")
elif len(password) >= 12:
    print("Strong")
else:
    print("Invalid")

    print("\n")

#Threshold 2.
import random

number1 = random.randint(0,9)
number2 = random.randint(0,9)

question = input(f"{number1} * {number2} ?")
user_answer = int(question)
correct_answer = number1 * number2

if user_answer == correct_answer:
    print("Correct!")
else:
        print(f"Wrong. The correct answer is {correct_answer}.")
print("\n")

#Threshold 3. Even or Odd number
num = int(input("Enter a number: "))
if num % 2 == 0:
    print(f"{num} is an even number.")
else:
    print(f"{num} is an odd number.")

    print("\n")

#Threshold 4. Body Mass Index
# 1Ib = 0.45359237kg, 1inch = 0.0254 meters
height = float(input("Enter a height: "))
weight = float(input("Enter a weight: "))
bmi = weight / (height * height)
print(f"Your BMI is {bmi}.")
if bmi < 18.5:
       print("Underweight")
elif 18.5 <= bmi < 25.0:
       print("Normal")
elif 25.0 <= bmi < 30.0:
       print("Overweight")
else:
    print("Obese")






