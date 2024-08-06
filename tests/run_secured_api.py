from fastapi import FastAPI
from request_limiter_middleware import RequestLimitMiddleware
from request_limiter_middleware import Backup, BanHammer

app = FastAPI()

# Enabling request limiting
app.add_middleware(RequestLimitMiddleware, whitelisted_ip_addresses=(),
                   limit_http=True, limit_websocket=True, seconds=7)

# loading history backup
Backup.load_archive('file.json')


@app.get(path='/')
async def home():
    return {"message": "Welcome home"}


if __name__ == '__main__':
    import uvicorn
    print()

    uvicorn.run(app, host="127.0.0.1", port=8000)
