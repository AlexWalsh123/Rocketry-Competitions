import csv
import random
import time

x_value = 0
total_1 = 0
total_2 = 0

peaked = False


fieldnames = ["x_value", "total_1", "total_2"]


with open('data.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:

    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "x_value": x_value,
            "total_1": total_1,
            "total_2": total_2
        }

        csv_writer.writerow(info)
        print(x_value, total_1, total_2)

        x_value += 1


        if(total_1 > 1000):

            peaked = True

        if(peaked == False):

            total_1 = total_1 + 10 + random.randint(-3, 3)

        elif(peaked):

            total_1 = total_1 - 10 - random.randint(-3, 3)

        total_2 = total_2 + random.randint(-5, 6)

    time.sleep(0.1)