from routers import graphs
from shared.utils_fastapi import create_app


app = create_app(routers = [graphs.router])
