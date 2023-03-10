import os
import openai
import PyPDF2
import xlsxwriter
from io import BytesIO
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def read_pdf(file=None):
    """
    read the pdf file and return text data
    :param file_name: name of the pdf file
    :param number_pages: how much pages to read
    :return: list with text in pdf file
    """
    reader = PyPDF2.PdfReader(file)
    data = []
    for page in reader.pages:
        data.append(page.extract_text())
    return data

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
            "content": text[:4096],
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

def create_table(data):
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
    for row in data:
        cells = []
        cell_count = 0
        for cell in row.split('|'):
            cell = cell.strip()
            if cell == '---':
                break
            cells.append(cell)
            cell_count += 1
        if len(cells) > 1:
            table.append(cells)
    return table

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
        row_with_pages = row
        pages_number = []
        for page in pages:
            if row[0].lower() in page.lower():
                pages_number.append(str(pages.index(page) + 1))
        row_with_pages.append(','.join(pages_number))
        table_with_pages.append(row_with_pages)
    return table_with_pages