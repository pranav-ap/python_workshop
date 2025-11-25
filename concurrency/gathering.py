import asyncio
import logging

import aiohttp
from aiohttp import ClientSession


async def delay(delay_seconds: int) -> int:
    print(f'sleeping for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    print(f'finished sleeping for {delay_seconds} second(s)')
    return delay_seconds


async def fetch_status(session: ClientSession, url: str, delay: int = 0) -> int:
    await asyncio.sleep(delay)
    async with session.get(url) as result:
        return result.status


async def main_task_list_bad() -> None:
    delay_times = [3, 3, 3]
    [await asyncio.create_task(delay(seconds)) for seconds in delay_times]

    """
    sleeping for 3 second(s)
    finished sleeping for 3 second(s)
    sleeping for 3 second(s)
    finished sleeping for 3 second(s)
    sleeping for 3 second(s)
    finished sleeping for 3 second(s)
    """


async def main_task_list_better() -> None:
    delay_times = [3, 3, 3]
    """
    we don’t do any awaiting until all the tasks have been created
    """
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    [await task for task in tasks]

    """
    sleeping for 3 second(s)
    sleeping for 3 second(s)
    sleeping for 3 second(s)
    finished sleeping for 3 second(s)
    finished sleeping for 3 second(s)
    finished sleeping for 3 second(s)
    
    Problems: 
    - If one of our coroutines finishes long before the others, 
        we’ll be trapped in the second list comprehension waiting for 
        all other coroutines to finish. 
    - If one of our coroutines has an exception, 
        it will be thrown when we await that failed task. Execution will halt. 
        This means we won’t be able to process any other successfull task
    """


async def main_task_list_gather():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com' for _ in range(10)]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)

    """
    Problems:
    - need to wait for all awaitables to finish
    - Imagine we’re making requests to the same server and we hit a rate limit.
        When one request hits a rate limit, 
            we must cancel others requests as well.
        But his is hard to do when our coroutines are 
        wrapped in tasks in the background.
    """


async def main_gather_order():
    """
    we are guaranteed the results will be returned
    in the order we passed them in
    """
    results = await asyncio.gather(delay(3), delay(1))
    print(results)


async def main_gather_throw_exceptions():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com', 'python://example.com']
        tasks = [fetch_status(session, url) for url in urls]
        """
        If more than one exception happens, 
            we’ll only see the first one that occurred when we await the gather
        """
        status_codes = await asyncio.gather(*tasks)

        print(status_codes)


async def main_gather_return_exceptions():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com', 'python://example.com']
        tasks = [fetch_status(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        exceptions = [res for res in results if isinstance(res, Exception)]
        successful_results = [res for res in results if not isinstance(res, Exception)]

        print(f'All results: {results}')
        print(f'Finished successfully: {successful_results}')
        print(f'Threw exceptions: {exceptions}')


async def main_process_as_they_complete():
    """
    You want to process each result immediately when it finishes,
    instead of waiting for all of them to complete first like in gather()
    """
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, 'https://www.example.com', 1),
            fetch_status(session, 'https://www.example.com', 1),
            fetch_status(session, 'https://www.example.com', 10),
        ]

        for finished_task in asyncio.as_completed(fetchers):
            # You get results in order of completion, not in the original order.
            print(await finished_task)


async def main_as_completed_timeout():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, 'https://example.com', 1),
            fetch_status(session, 'https://example.com', 10),
            fetch_status(session, 'https://example.com', 10),
        ]

        for done_task in asyncio.as_completed(fetchers, timeout=2):
            try:
                result = await done_task
                print(result)
            except asyncio.TimeoutError:
                print('We got a timeout error!')

        for task in asyncio.tasks.all_tasks():
            """
            You will see that timeout does not cancel the 10-second tasks; 
            they are still running in the background.
            """
            print(task)


async def main_wait():
    async with aiohttp.ClientSession() as session:
        good_request = fetch_status(session, 'https://www.example.com')
        bad_request = fetch_status(session, 'python://bad')

        fetchers = [
            asyncio.create_task(good_request),
            asyncio.create_task(bad_request),
        ]

        """
        The done set contains all tasks that finished either 
        successfully or with exceptions.
        
        The pending set contains all tasks that have not finished yet.
        """
        done, pending = await asyncio.wait(
            fetchers,
            return_when=asyncio.FIRST_COMPLETED,
        )

        """
        If one of our requests throws an exception, 
        it won’t be thrown at the asyncio.wait call 
        in the same way that asyncio.gather did.
        """

        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

    for done_task in done:
        # await ensures that exceptions are raised here
        result = await done_task
        print(result)


async def main_wait_no_throw_exceptions():
    async with aiohttp.ClientSession() as session:
        good_request = fetch_status(session, 'https://www.example.com')
        bad_request = fetch_status(session, 'python://bad')

        fetchers = [
            asyncio.create_task(good_request),
            asyncio.create_task(bad_request),
        ]

        done, pending = await asyncio.wait(fetchers)
        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        """
        We don’t want to throw an exception.
        To simply print the task exceptions,
            use the methods on the Task object. 
        """
        for done_task in done:
            # check to see if we have an exception
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("Request got an exception", exc_info=done_task.exception())


async def fail_fast_behavior():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            asyncio.create_task(fetch_status(session, 'python://bad.com')),
            asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=3)),
            asyncio.create_task(fetch_status(session, 'https://www.example.com', delay=3)),
        ]

        done, pending = await asyncio.wait(
            fetchers,
            return_when=asyncio.FIRST_EXCEPTION,
        )

        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

    for done_task in done:
        if done_task.exception() is None:
            print(done_task.result())
        else:
            logging.error("Request got an exception", exc_info=done_task.exception())

    for pending_task in pending:
        pending_task.cancel()


async def main_wait_first_completed():
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'

        fetchers = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
        ]

        """
        Makes the wait coroutine return as soon as it has at least one result. 
        This can either be a coroutine that failed or one that ran successfully. 
        We can then either cancel the other running coroutines 
        or adjust which ones to keep running. 
        
        done will have one complete request
        pending will contain anything still running
        """
        done, pending = await asyncio.wait(
            fetchers,
            return_when=asyncio.FIRST_COMPLETED,
        )

        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        for done_task in done:
            print(await done_task)


async def first_done_first_serve():
    """
    The above function's approach lets us respond right away
    when our first task completes.

    What if we want to process the rest of the results
    as they come in like as_completed?
    """
    async with aiohttp.ClientSession() as session:
        url = 'https://www.example.com'

        pending = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
        ]

        while pending:
            done, pending = await asyncio.wait(
                pending,
                return_when=asyncio.FIRST_COMPLETED,
            )

            print(f'Done task count: {len(done)}')
            print(f'Pending task count: {len(pending)}')

            for done_task in done:
                print(await done_task)


async def wait_with_timeout():
    async with aiohttp.ClientSession() as session:
        url = 'https://example.com'
        fetchers = [
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url)),
            asyncio.create_task(fetch_status(session, url, delay=3)),
        ]

        """
        In the done set we’ll see our two fast requests, 
        as they finished within 1 second.
        
        Our slow request is still running and is, 
        therefore, in the pending set.
        """
        done, pending = await asyncio.wait(fetchers, timeout=1)
        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

    """
    Our tasks in the pending set are not canceled and will continue to
    run despite the timeout.
    
    Cancel them if you want. 
    """
    for done_task in done:
        result = await done_task
        print(result)


asyncio.run(wait_with_timeout())
