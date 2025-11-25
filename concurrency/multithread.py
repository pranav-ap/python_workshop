from concurrent.futures import ThreadPoolExecutor
import requests
import asyncio
from threading import Lock, RLock


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


async def main_asyncio_thread():
    urls = ['https://www.example.com' for _ in range(10)]
    tasks = [asyncio.to_thread(get_status_code, url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)


counter = 0
counter_lock = Lock()


def increment():
    global counter
    for _ in range(1000):
        with counter_lock:   # prevent race condition
            counter += 1


async def main_thread_lock():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=5) as pool:
        tasks = [loop.run_in_executor(pool, increment) for _ in range(5)]
        await asyncio.gather(*tasks)

    print("Final counter value:", counter)


counter_r = 0
counter_r_lock = RLock()


def recursive_increment(n):
    global counter_r
    with counter_r_lock:
        if n == 0:
            return
        counter_r += 1
        recursive_increment(n - 1)


def run_task():
    recursive_increment(5)


async def main_thread_rlock():
    """
    A reentrant lock is a special kind of lock
    that can be acquired by the same thread more than once,
    allowing that thread to “reenter” critical sections.
    """
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=5) as pool:
        tasks = [loop.run_in_executor(pool, run_task) for _ in range(5)]
        await asyncio.gather(*tasks)

    print("Final counter value:", counter_r)


async def delay(delay_seconds: int) -> int:
    print(f'sleeping for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    print(f'finished sleeping for {delay_seconds} second(s)')
    return delay_seconds


async def a(lock: asyncio.Lock):
    print('Coroutine a waiting to acquire the lock')
    async with lock:
        print('Coroutine a is in the critical section')
        await delay(2)
        print('Coroutine a released the lock')


async def b(lock: asyncio.Lock):
    print('Coroutine b waiting to acquire the lock')
    async with lock:
        print('Coroutine b is in the critical section')
        await delay(2)
        print('Coroutine b released the lock')


async def main_asyncio_lock():
    lock = asyncio.Lock()
    await asyncio.gather(a(lock), b(lock))


async def operation(semaphore: asyncio.Semaphore):
    print('Waiting to acquire semaphore...')
    async with semaphore:
        print('Semaphore acquired!')
        await asyncio.sleep(2)
        print('Semaphore released!')


async def main_asyncio_semaphore():
    """
    A semaphore allows a fixed number of threads or tasks to access a resource at the same time.
    When the limit is reached, new tasks must wait until one finishes and releases a “permit”.
    """
    semaphore = asyncio.Semaphore(2)
    await asyncio.gather(*[operation(semaphore) for _ in range(4)])


async def main_asyncio_bounded_semaphore():
    """
    A regular semaphore lets you .release() as many times as you want,
    even more than you acquired.
    So, if you call .release() extra times by mistake,
    the internal counter keeps increasing.
    """
    semaphore = asyncio.BoundedSemaphore(1)
    await semaphore.acquire()
    semaphore.release()
    semaphore.release()


if __name__ == "__main__":
    asyncio.run(main_asyncio_bounded_semaphore())
