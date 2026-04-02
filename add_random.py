import random

number = int(input("Enter a number: "))
random_number = random.randint(1, 5000)
result = number + random_number

print(f"{number} + {random_number} (random) = {result}")
