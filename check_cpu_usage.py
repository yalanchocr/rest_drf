import psutil
import time

# Measure CPU usage over an interval of 1 second
cpu_usage = psutil.cpu_percent(interval=1)
print(f"CPU Usage: {cpu_usage}%")

# Get the number of logical CPU cores
cpu_cores = psutil.cpu_count(logical=True)
print(f"Number of CPU Cores: {cpu_cores}")

# Example function to measure performance
def example_function():
    start_time = time.time()
    # Your code here
    end_time = time.time()
    print(f"Execution Time: {end_time - start_time} seconds")

# Call the example function
example_function()