from fastapi import FastAPI


class FastApiTestAppFactory:
    @staticmethod
    def get_app():
        app = FastAPI()

        @app.get(path='/')
        async def home():
            return {"message": "Welcome home"}

        return app

