"""
>> uv run python -m  cProfile  profiling/cprofile_1.py

>> uv run python -m  cProfile -o output.out profiling/cprofile_1.py
>> uv run snakeviz output.out
"""

def my_function():
    b = []
    for i in range(500000):
        b.append(i**2)
    return b


my_function()
