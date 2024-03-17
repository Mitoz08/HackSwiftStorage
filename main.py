import csv
import pygame

with open('Events.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)


    with open('New.csv','w',newline='') as new_file:
        csv_writer = csv.writer(new_file)

        for line in csv_reader:
            csv_writer.writerow(line)

    new_file.close()
csv_file.close()

with open('New.csv','r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for line in csv_reader:
        print(line)

