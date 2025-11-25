import asyncio
import time


def sync_task():
    """
    sync_task() is a blocking function — it uses time.sleep(5).
    If you called it directly inside an async function,
    it would freeze the event loop for 5 seconds,
    stopping all other async tasks.
    """
    print("Starting a slow sync task...")
    time.sleep(5)  # Simulating a long task
    print("Finished the slow task.")


async def async_wrapper():
    # gets event loop
    loop = asyncio.get_running_loop()
    # runs sync_task in a separate thread
    # & waits asynchronously for it to complete
    await loop.run_in_executor(None, sync_task)


async def main():
    await asyncio.gather(
        async_wrapper(),
        # Imagine other async tasks here
    )

asyncio.run(main())
