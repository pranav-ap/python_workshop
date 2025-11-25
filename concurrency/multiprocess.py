import asyncio
import multiprocessing
import time
from asyncio import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from multiprocessing import Pool, Process, Value, Array
from typing import List


def count_with_time(count_to: int) -> int:
    start = time.time()
    counter = 0

    while counter < count_to:
        counter = counter + 1
        end = time.time()

        print(f'Finished counting to {count_to} in {end - start}')

    return counter


def count(count_to: int) -> int:
    counter = 0
    while counter < count_to:
        counter = counter + 1
    return counter


def say_hello(name: str) -> str:
    return f'Hi there, {name}'


def main_process():
    start_time = time.time()

    to_one_hundred_million = Process(target=count_with_time, args=(10000000,))
    to_two_hundred_million = Process(target=count_with_time, args=(20000000,))

    to_one_hundred_million.start()
    to_two_hundred_million.start()
    to_one_hundred_million.join()
    to_two_hundred_million.join()

    end_time = time.time()
    print(f'Completed in {end_time - start_time}')


def main_process_pool():
    print(f'Number of CPU cores: {multiprocessing.cpu_count()}')

    # create Python processes equal to the number of CPU cores on the machine
    with Pool() as process_pool:
        hi_jeff = process_pool.apply_async(say_hello, args=('Jeff',))
        hi_john = process_pool.apply_async(say_hello, args=('John',))
        print(hi_jeff.get())
        print(hi_john.get())


def main_process_pool_executor():
    with ProcessPoolExecutor() as process_pool:
        numbers = [1, 3, 5, 22, 100]
        # order is maintained but they are sequentially waited on
        for result in process_pool.map(count_with_time, numbers):
            print(result)


async def main_asyncio_pools():
    with ProcessPoolExecutor() as process_pool:
        nums = [1, 3, 5, 22, 100]
        calls: List[partial[int]] = [partial(count, num) for num in nums]

        loop: AbstractEventLoop = asyncio.get_running_loop()
        futures = [loop.run_in_executor(process_pool, call) for call in calls]
        results = await asyncio.gather(*futures)

        for result in results:
            print(result)


def increment_value(shared_int: Value):
    shared_int.value = shared_int.value + 1


def increment_array(shared_array: Array):
    for index, integer in enumerate(shared_array):
        shared_array[index] = integer + 1


def main_race_condition():
    """
    Leads to race conditions
    """
    for _ in range(100):
        integer = Value('i', 0)
        integer_array = Array('i', [0, 0])

        procs = [
            Process(target=increment_value, args=(integer,)),
            Process(target=increment_value, args=(integer,)),
        ]

        [p.start() for p in procs]
        [p.join() for p in procs]

        print(integer.value)
        print(integer_array[:])


def increment_value_locked(shared_int: Value):
    with shared_int.get_lock():
        """
        To avoid race conditions, we make our parallel code sequential 
        in critical sections. This can hurt the performance of 
        our multiprocessing code.
        """
        shared_int.value = shared_int.value + 1


def main_locks():
    """
    Uses locks to prevent race conditions
    """
    for _ in range(10):
        integer = Value('i', 0)
        procs = [
            Process(target=increment_value_locked, args=(integer,)),
            Process(target=increment_value_locked, args=(integer,)),
        ]

        [p.start() for p in procs]
        [p.join() for p in procs]

        print(integer.value)
        assert (integer.value == 2)


shared_counter: Value


def init(counter: Value):
    """
    This function runs once per worker process in the process pool.
    It sets the worker’s global shared_counter variable
        to point to the same shared memory object created in the main process.
    So every process has a reference to the same underlying memory, but
        just different Python objects pointing to it.
    """
    global shared_counter
    shared_counter = counter


def increment_shared_counter():
    with shared_counter.get_lock():
        shared_counter.value += 1


async def share_data_with_process_pools():
    counter = Value('d', 0)

    with ProcessPoolExecutor(initializer=init, initargs=(counter,)) as pool:
        await asyncio.get_running_loop().run_in_executor(
            pool,
            increment_shared_counter,
        )

        print(counter.value)


if __name__ == "__main__":
    # main_process_pool_executor()
    # asyncio.run(main_asyncio_pools())
    # main_locks()
    asyncio.run(share_data_with_process_pools())
