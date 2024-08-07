from fastapi_app import FastApiTestAppFactory
from request_limiter_middleware import RequestLimitMiddleware
from request_limiter_middleware import Backup, BanHammer

app = FastApiTestAppFactory.get_app()
middleware = RequestLimitMiddleware


# Enabling request limiting
app.add_middleware(RequestLimitMiddleware, whitelisted_ip_addresses=(),
                   limit_http=True, limit_websocket=True, seconds=7)

# loading history backup
Backup.load_archive('file.json')

if __name__ == '__main__':
    import uvicorn

    print()

    uvicorn.run(app, host="127.0.0.1", port=8000)
