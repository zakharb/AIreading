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
from fastapi import File
from app.backend.lib import read_pdf, split_chunks
from app.backend.lib import send_data_to_chatgpt
from app.backend.lib import create_text, create_task_with_timeout
import asyncio

router = APIRouter()

@router.post("/create_similarity",
            response_description="Show similar texts")
async def create_similarity(file: bytes = File()): 
    pages = read_pdf(BytesIO(file))
    text = create_text(pages)
    chunks, chunk_words = split_chunks(text, 1)
    tasks = []
    for chunk in chunks[:5]:
        content = create_content(chunk)
        task = send_data_to_chatgpt(content)
        tasks.append(create_task_with_timeout(task))
    raw_data = await asyncio.gather(*tasks)
    return raw_data

def create_content(text):
    """
    Create a string containing a message and a table header based on given columns.

    Args:
        text (str): The text to be included in the message.
        columns (list): A list of column names.
        chunk_words (str): The word that was chunked from the text.

    Returns:
        str: The message with the formatted table header.
    """
    content = f'Wrile one similar book with autor for this text:'
    content += text
    return content
