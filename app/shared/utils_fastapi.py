import os, logging
from typing import List, Optional, Union, Callable
from pickle import DICT
from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

logger = logging.getLogger(__name__)


def create_app(routers: Optional[List] = None):

    app = FastAPI()

    origins= [os.getenv("")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if routers:
        [app.include_router(router) for router in routers ]

    return app