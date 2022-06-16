from routers import dags
from shared.utils_fastapi import create_app


app = create_app(routers = [dags.router])
