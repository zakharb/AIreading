import os
import openai
import PyPDF2

openai.api_key = os.getenv("OPENAI_API_KEY", "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")

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

def send_data_to_chatgpt(text=""):
    """
    send text to chatGPT
    :param text: text to send to API
    :return: completition from API
    """
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{
        "role": "user", 
        "content": text[:1096],
      }]
    )
    return completion.choices[0].message.content

def create_table(data):
    table = {}
    row_count = 0
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
            row_count += 1
            table[row_count] = cells
    return table

def create_book(table):
    stream = BytesIO()
    workbook = xlsxwriter.Workbook(stream)
    worksheet = workbook.add_worksheet()
    for row, cells in table.items():
        for cell in cells:
            worksheet.write(row, cells.index(cell), cell)
    workbook.close()
    stream.seek(0)
    return stream

def find_word_in_pages(words={}, pages=[]):
    data = []
    for word in words:
        word['pages'] = []
        for page in pages:
            if word['word'] in page:
                word['pages'].append(pages.index(page))
        data.append(word)
    return data

