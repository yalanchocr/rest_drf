import multiprocessing
import os
import time
from django.core.management.base import BaseCommand, CommandError


def square(x):
    print(f"Process ID: {os.getpid()}")  # Print the process ID
    time.sleep(2)  # Simulate some work
    return x * x

class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        pass
    def handle(self, *args, **options):
        numbers = [2, 3, 5]
        with multiprocessing.Pool() as pool:
            results = pool.map(square, numbers)
        print(results)  # Output: [4, 9, 25]
