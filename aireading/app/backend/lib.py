import os
import openai
import PyPDF2
import xlsxwriter
from io import BytesIO
from app.config import OPENAI_API_KEY
import asyncio

openai.api_key = OPENAI_API_KEY

BATCH_LIMIT = 15000

def parse_columns(columns_raw: str) -> list:
    """
    Parse raw column string into a list of column names.

    Args:
        columns_raw (str): A comma-separated string of column names.

    Returns:
        list: A list of column names.
    """
    columns = ["word",]
    columns_raw = columns_raw.split(', ')
    columns.extend(columns_raw)
    return columns

def read_pdf(file) -> list:
    """
    Read a PDF file and return its text contents as a list of strings.

    Args:
        file (bytes): The file  of the PDF to read.

    Returns:
        list: A list of strings containing the text of each page in the PDF.
    """
    reader = PyPDF2.PdfReader(file)
    data = []
    for page in reader.pages:
        data.append(page.extract_text())
    return data

def create_text(pages: list) -> str:
    """
    Concatenate a list of text pages into a single string.

    Args:
        pages (list): A list of strings containing the text of each page.

    Returns:
        str: A single string containing all the text from the input pages.
    """
    return ''.join(pages)

def split_chunks(text: str, words: int) -> tuple:
    """
    Split a long string of text into smaller chunks and calculate the number of chunks needed.

    Args:
        text (str): The text to be split into chunks.
        words (int): The number of words in the text.

    Returns:
        tuple: A tuple containing a list of text chunks and the number of chunks needed.
    """
    chunk_size = len(text) // 19
    if words < 20:
        num_chunks = 1
    else:
        num_chunks = words // 20 + 1
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks, num_chunks

async def get_data_from_chatgpt(chunks, columns, chunk_words):
    """
    Asynchronously send data to the ChatGPT API for each chunk of text and gather the responses.

    Args:
        chunks (List[str]): A list of text chunks to send to the ChatGPT API.
        columns (List[str]): A list of column names for the expected response.
        chunk_words (str): A string describing the vocabulary word for each chunk.

    Returns:
        List[str]: A list of responses from the ChatGPT API.
    """
    tasks = []
    for chunk in chunks:
        content = create_content(chunk, columns, chunk_words)
        task = send_data_to_chatgpt(content)
        tasks.append(create_task_with_timeout(task))
    return await asyncio.gather(*tasks)

async def create_task_with_timeout(task):
    """
    Run an asyncio task with a timeout.

    Args:
        task (asyncio.Future): An asyncio task to be executed.
        timeout (float, optional): The maximum amount of time to wait for the task to complete.
            Defaults to 16 seconds.

    Returns:
        any: The result of the task execution, or an empty string 
        if the task timed out.

    Raises:
        asyncio.TimeoutError: If the task does not complete within the specified timeout.
    """
    try:
        result = await asyncio.wait_for(task, timeout=60)
    except asyncio.TimeoutError:
        print("Timeout occurred while waiting for task to complete.")
        result = ""
    return result

async def send_data_to_chatgpt(text=""):
    """
    send text to chatGPT
    :param text: text to send to API
    :return: completition from API
    """
    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "user", 
            "content": text[:BATCH_LIMIT],
            },
        ],
        temperature=0,
        stream=True,
    )
    data = ""
    async for resp in completion:
        delta = resp.choices[0].delta
        text = delta.get('content', '')
        data += text
    return data

def filter_response(response: list) -> list:
    """
    Filter response to only contain lines with '|' separator.

    Args:
        response (list): A list of strings.

    Returns:
        list: A list of strings containing the lines with '|' separator.
    """
    filtered_data = []
    for r in response:
        r_split = r.splitlines()
        lines_with_separator = [line for line in r_split if '|' in line]
        if len(lines_with_separator) < 2:
            continue
        filtered_data.extend(lines_with_separator[2:])
    return filtered_data

def create_table(data, columns, words):
    """
    create table from row data with delimeter
    :param data: raw data
        Word | IPA | Chinese Translation | English Translation | Example 
        --- | --- | --- | ---| ---
        Spoiled | spɔɪld | 被宠坏的，娇惯的 | Treated too well, resulting in bad behavior | Veruca Salt is a spoiled girl who always gets her way.
    :return: 
        [
            ['Word', 'IPA', 'Chinese Translation', 'English Translation', 'Example'], 
            ['Spoiled', 'spɔɪld', '被宠坏的，娇惯的', 'Treated too well, resulting in bad behavior', 'Veruca Salt is a spoiled girl who always gets her way.']
        ]
    """
    table = []
    table.append(columns)
    found_words = []

    for row in data:
        cells = []
        row = row.split('|')
        row = [ x for x in row if x ]
        for cell in row:
            cell = cell.strip()
            if cell == '---':
                break
            cells.append(cell)
        if len(cells) > 1:
            word = cells[0]
            if word in found_words:
                continue
            found_words.append(word)
            if len(table) > words:
                break
            table.append(cells)
    return table

def add_pages_number(table, pages):
    """
    add pages numbers to table table
    :param table: raw data
    :param pages: text data from pdf file
        [
            ['Word', 'IPA', ...], 
            ['Spoiled', 'spɔɪld', ...]
        ]
    :return: table with "Pages number" column
        [
            ['Word', 'IPA', ..., 'Pages number'], 
            ['Spoiled', 'spɔɪld', ..., '1,63']
        ]
    """    
    table_with_pages = []
    table[0].append('Pages number')
    table_with_pages.append(table[0])
    for row in table[1:]:
        if len(row) < 4:
            continue
        cell = row[4]
        # get example cell: "There are five children in this book"
        cell = cell[1:20]
        # split example cell: There are five chil
        row_with_pages = row
        pages_number = []
        for page in pages:
            if cell[:15].lower() in page.lower():
                pages_number.append(str(pages.index(page) + 1))
                break
        row_with_pages.append(','.join(pages_number))
        table_with_pages.append(row_with_pages)
    return table_with_pages

def create_book(table):
    """
    create book in xlsx format from table
    :param table: 
        [
            ['Word', 'IPA', ..., 'Pages number'], 
            ['Spoiled', 'spɔɪld', ..., '1,63']
        ]
    :return: xlsx book in stream
    """
    stream = BytesIO()
    workbook = xlsxwriter.Workbook(stream)
    worksheet = workbook.add_worksheet()
    for row in table:
        for cell in row:
            worksheet.write(table.index(row), row.index(cell), cell)
    workbook.close()
    stream.seek(0)
    return stream
