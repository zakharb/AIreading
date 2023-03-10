"""
    AIreading
    Copyright (C) 2023

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    Author:
        Bengart Zakhar

    Description:
        Main entrypoinr wit App
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.backend import vocabulary_route
from app.backend import brevity_route
from app.backend import similarity_route
from app.frontend import index_route

app = FastAPI(openapi_url="/api/v1/openapi.json", 
              docs_url="/api/v1/docs")
app.mount("/img", StaticFiles(directory="app/frontend/img"), name="img")
app.mount("/js", StaticFiles(directory="app/frontend/js"), name="js")
app.mount("/styles", StaticFiles(directory="app/frontend/styles"), name="styles")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vocabulary_route.router, 
                   prefix='/api/v1/vocabulary', tags=['vocabulary'])
app.include_router(brevity_route.router, 
                   prefix='/api/v1/brevity', tags=['brevity'])
app.include_router(similarity_route.router, 
                   prefix='/api/v1/similarity', tags=['similarity'])
app.include_router(index_route.router, tags=['frontend'])
