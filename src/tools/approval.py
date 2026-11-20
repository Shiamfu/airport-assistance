import asyncio

from database.db import get_request


async def wait_for_approval(
    request_id,
    timeout_seconds=300
):
    elapsed = 0

    while elapsed < timeout_seconds:
        request = get_request(request_id)

        if request is None:
            return "REQUEST_NOT_FOUND"

        status = request[7]

        if status in ("APPROVED", "REJECTED"):
            return status

        await asyncio.sleep(2)
        elapsed += 2

    return "TIMEOUT"

