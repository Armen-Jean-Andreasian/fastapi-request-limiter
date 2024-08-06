from .requests_archive import RequestsArchive
from .whitelisted_addresses import WhitelistedIpAddresses
import json
from fastapi import Request
from fastapi import HTTPException


class RequestLimitMiddleware:
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from fastapi import FastAPI

    def __init__(self,
                 app: "FastAPI",
                 whitelisted_ip_addresses: tuple[str],
                 seconds: int = 5,
                 limit_http: bool = True,
                 limit_websocket: bool = True):

        self.app = app
        self.seconds = seconds
        self.scopes_to_limit = ('http' if limit_http else None, 'websocket' if limit_websocket else None)
        self.whitelisted_ip_addresses = WhitelistedIpAddresses(whitelisted_ip_addresses)
        self.requests_archive = RequestsArchive()

    async def __call__(self, scope, receive, send) -> dict:
        """
        Method Flow:

        1. Checking, if the request type should not be limited then proceeding the request immediately.

        2. Getting the client IP.
            Proceeding the request immediately if:
                The IP is whitelisted

        3. Limiting

            If the IP requests the API for the first time:
                Applying self.seconds waiting penalty
                Proceeding the request

            If the IP previously sent requests to API:
                Checking the remaining penalty time for the IP:

                    If penalty time expired:
                        Setting self.seconds new penalty
                        Proceeding the request

                    If penalty hasn't expired yet:
                        Rejecting with 429 status code
                        Sending the remaining time in message body

        """

        if scope['type'] not in self.scopes_to_limit:
            return await self.app(scope, receive, send)

        client_ip = Request(scope).client.host

        # IP is whitelisted
        if client_ip in self.whitelisted_ip_addresses:
            return await self.app(scope, receive, send)

        # first time
        if client_ip not in self.requests_archive:
            self.requests_archive.add_ip(ip=client_ip, seconds=self.seconds)
            return await self.app(scope, receive, send)

        else:
            # old client
            remaining_time = self.requests_archive.get_remaining_time(ip=client_ip)

            # permanently blacklisted IP
            if remaining_time is False:
                raise HTTPException(status_code=429, detail="You are blocked.")

            # if something went wrong (it should not be None)
            elif remaining_time is None:
                raise HTTPException(status_code=500, detail="Server side error. Waiting time expected float, None found")

            # familiar IP
            elif type(remaining_time) is float:

                # no limit
                if remaining_time <= 0:
                    self.requests_archive.extend_time(ip=client_ip, seconds=self.seconds)
                    return await self.app(scope, receive, send)

                # limit found
                else:
                    readable_remaining_time = "{:.8f}".format(float(remaining_time))
                    message = {"HTTPException": f"Rate limit exceeded. Wait for {readable_remaining_time} seconds."}

                    response = {
                        "type": "http.response.start",
                        "status": 429,
                        "headers": [(b"content-type", b"application/json")],
                        "body": json.dumps(message).encode("utf-8")
                    }
                    await send(response)
