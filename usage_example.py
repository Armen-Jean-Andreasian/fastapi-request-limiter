from fastapi import FastAPI
from request_limiter_middleware import RequestLimitMiddleware
from request_limiter_middleware import Backup, BanHammer

app = FastAPI()

# blocking address
BanHammer.block_it(ip="127.0.0.2")

# saving current IP requests' history
Backup.save_archive('file.json')

# Enabling request limiting
app.add_middleware(RequestLimitMiddleware, whitelisted_ip_addresses=("127.0.0.1",),
                   limit_http=True, limit_websocket=True, seconds=7)

# loading history backup
Backup.load_archive('file.json')
