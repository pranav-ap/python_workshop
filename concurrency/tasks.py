"""
When we call a coroutine directly,
    we don’t put it on the event loop to run.
    Instead, we get a coroutine object that we
        await or
        pass it in to asyncio.run

An await will pause the entire coroutine
    until the result of the await expression comes back.

Tasks are wrappers around a new coroutine.
Once we create a task,
    the current coroutine will continue to run.
    The new coroutine (task) will run concurrently.
"""

import asyncio
from asyncio import CancelledError


async def delay(delay_seconds: int) -> int:
    print(f'sleeping for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    print(f'finished sleeping for {delay_seconds} second(s)')
    return delay_seconds


async def main_one():
    sleep_for_three = asyncio.create_task(delay(3))
    print(type(sleep_for_three))
    result = await sleep_for_three
    print(result)


async def main_many():
    """
    Tasks are scheduled to run “as soon as possible.”
    Generally, this means the first time we hit an await statement
    after creating a task, any tasks that are pending will
    run as await triggers an iteration of the event loop.
    """
    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(3))
    sleep_once_more = asyncio.create_task(delay(3))
    await sleep_for_three
    await sleep_again
    await sleep_once_more


async def main_cancel():
    long_task = asyncio.create_task(delay(10))

    seconds_elapsed = 0
    while not long_task.done():
        print('Task not finished, checking again in a second.')
        await asyncio.sleep(1)
        seconds_elapsed = seconds_elapsed + 1
        if seconds_elapsed == 5:
            long_task.cancel()

    try:
        """
        CancelledError can only be thrown from an await statement.
        Calling cancel won’t magically stop the task in its tracks. 
        If we cancel a task when it's running, 
            that code will run until completion 
            until we hit the next await statement and a CancelledError can be raised. 
        """
        await long_task
    except CancelledError:
        print('Our task was cancelled')


async def main_wait():
    delay_task = asyncio.create_task(delay(2))

    try:
        result = await asyncio.wait_for(delay_task, timeout=1)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print('Got a timeout!')
        print(f'Was the task cancelled? {delay_task.cancelled()}')


async def main_wait_shield():
    task = asyncio.create_task(delay(10))

    try:
        """
        Inform a user that something is taking longer than expected 
        but do not cancel the task when the timeout is exceeded.
        """
        result = await asyncio.wait_for(asyncio.shield(task), 5)
        print(result)
    except TimeoutError:
        print("Task took longer than five seconds, it will finish soon!")
        result = await task
        print(result)


asyncio.run(main_wait_shield())
