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
from app.backend.lib import read_pdf, split_chunks
from app.backend.lib import get_data_from_chatgpt, send_data_to_chatgpt
from app.backend.lib import create_table, create_book, add_pages_number
from app.backend.lib import create_text, filter_response
from app.backend.lib import parse_columns
from app.backend.lib import create_task_with_timeout
import asyncio


router = APIRouter()

@router.post("/create_vocabulary",
            response_description="Parse vocabulary")
async def create_vocabulary(file: bytes = File(), 
                            words: int = Form(),
                            columns: str = Form()):
    """
    Parse a PDF file, send each chunk of text to the ChatGPT API, and create a vocabulary book.

    Args:
        file (bytes): The PDF file to parse.
        words (int): The number of vocabulary words to extract.
        columns (str): A comma-separated string of column names for the expected response.

    Returns:
        StreamingResponse: A streaming response object containing the resulting vocabulary book.
    """
    columns = parse_columns(columns)
    pages = read_pdf(BytesIO(file))
    text = create_text(pages)
    chunks, chunk_words = split_chunks(text, words)
    tasks = []
    for chunk in chunks:
        content = create_content(chunk, columns, chunk_words)
        task = send_data_to_chatgpt(content)
        print('[*] create task: ', task)
        tasks.append(create_task_with_timeout(task))
    raw_data = await asyncio.gather(*tasks)
    data = filter_response(raw_data)
    table = create_table(data, columns, words)
    table = add_pages_number(table, pages)
    book = create_book(table)
    return StreamingResponse(book)

def create_content(text, columns, chunk_words):
    """
    Create a string containing a message and a table header based on given columns.

    Args:
        text (str): The text to be included in the message.
        columns (list): A list of column names.
        chunk_words (str): The word that was chunked from the text.

    Returns:
        str: The message with the formatted table header.
    """
    columns_table = ','.join([ f'"{x}"' for x in columns ])
    columns = ','.join(columns[1:])
    content = f'Please provide me with the {columns} for {chunk_words} vocabulary word found in the following text, formatted in a table with separator "|" and with the columns {columns_table}'
    content += text
    return content