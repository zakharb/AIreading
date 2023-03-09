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
        Routers for operations with API
"""
from fastapi import APIRouter
from fastapi import File
from app.backend.lib import read_pdf, send_data_to_chatgpt

router = APIRouter()

@router.post("/create_similarity",
            response_description="Show similar texts")
async def create_similarity(file: bytes = File()): 
    pages = read_pdf(BytesIO(file))
    content = create_similarity_content(pages=pages)
    resp = send_data_to_chatgpt(content)
    return resp

def create_similarity_content(pages):
    text = "wrile list of 5 similar texts to this text:"
    for page in pages:
        text += page
    return text