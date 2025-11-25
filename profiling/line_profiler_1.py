"""
>> LINE_PROFILE=1 uv run profiling/line_profiler_1.py
>> uv run python -m line_profiler -rtmz profile_output.lprof
"""

from line_profiler import profile


@profile
def is_prime(n):
    '''
    Check if the number "n" is prime, with n > 1.

    Returns a boolean, True if n is prime.
    '''
    max_val = n ** 0.5
    stop = int(max_val + 1)
    for i in range(2, stop):
        if n % i == 0:
            return False
    return True


@profile
def find_primes(size):
    primes = []
    for n in range(size):
        flag = is_prime(n)
        if flag:
            primes.append(n)
    return primes


@profile
def main():
    print('start calculating')
    primes = find_primes(100)
    print(f'done calculating. Found {len(primes)} primes.')


if __name__ == '__main__':
    main()
