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

from io import BytesIO
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from fastapi import File, Form
from app.backend.lib import read_pdf, send_data_to_chatgpt
from app.backend.lib import create_table, create_book, add_pages_number

router = APIRouter()

@router.post("/create_vocabulary",
            response_description="Parse vocabulary")
async def create_vocabulary(file: bytes = File(), 
                            words: str = Form(),
                            columns: str = Form()):
    pages = read_pdf(BytesIO(file))
    content = create_vocabulary_content(pages=pages, 
                                        words=words, columns=columns)
    resp = send_data_to_chatgpt(content)
    print(resp)
    table = create_table(resp.splitlines())
    print(table)
    table = add_pages_number(table, pages)
    book = create_book(table)
    return StreamingResponse(book)    

def create_vocabulary_content(pages, words=10, columns="IPA"):
    text = f"please give me {words} challenging but commonly used vocabularies "\
           f"from these text in table format, including word, {columns}"
    for page in pages:
        text += page
    return text
