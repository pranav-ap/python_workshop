import timeit


def my_function():
    a = [1, 2, 3, 4]
    b = [i**2 for i in a]
    return b


"""
will execute the code multiple times and return the average execution time
"""
execution_time = timeit.timeit(my_function, number=10_000)
print(f"Execution time: {execution_time:.6f} seconds")
