import asyncio


async def async_operation(future, data):
    await asyncio.sleep(1)

    # Set the result or exception based on the input data
    # This marks the future as done and triggers its callbacks.
    if data == "success":
        future.set_result("Operation succeeded")
    else:
        future.set_exception(RuntimeError("Operation failed"))


# A callback function to be called when the Future is done
def future_callback(future):
    try:
        print("Callback:", future.result())
    except Exception as exc:
        print("Callback:", exc)


async def main():
    """
    A future contains a single value that you expect to get at some
    point in the future but may not yet have.

    Usually, when you create a future,
        it does not have any value because it doesn’t yet exist.
        In this state, it is considered
            incomplete, unresolved, or simply not done.
    """
    future = asyncio.Future()
    # Add a callback to be run when the Future is done
    future.add_done_callback(future_callback)

    # Start the asynchronous operation and pass the Future
    await async_operation(future, "success")

    # Check if the Future is done and print its result
    if future.done():
        try:
            """
            We don’t call the result method before the result is set 
            because the result method will throw 
            an invalid state exception.
            """
            print("Main:", future.result())
        except Exception as exc:
            print("Main:", exc)


asyncio.run(main())

