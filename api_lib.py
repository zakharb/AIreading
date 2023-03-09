import os
import openai
import PyPDF2
import json
openai.api_key = os.getenv("OPENAI_API_KEY", "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")

def read_pdf(file_name="example.pdf", number_pages=0):
    """
    read the pdf file and return text data
    :param file_name: name of the pdf file
    :param number_pages: how much pages to read
    :return: list with text in pdf file
    """
    reader = PyPDF2.PdfReader(file_name)
    data = []
    for page in range(0, number_pages):
        data.append(reader.pages[page].extract_text())
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
        "content": text,
      }]
    )
    return completion.choices[0].message.content

def create_content(instruction, pages):
    text = "in json format please give me 20 challenging but commonly used vocabularies from these pages, including words, IPA, Chinese meaning, English meaning, example from the excerpt"
    for page in pages:
        text += page
    return text


def find_word_in_pages(words={}, pages=[]):
    for word in words:
        word['pages'] = []
        for page in pages:
            if word['word'] in page:
                word['pages'].append(pages.index(page))
    return data

if __name__ == "__main__":
    pages = read_pdf(number_pages=3)
    content = create_content(instruction=instruction, pages=pages)
    resp = send_data_to_chatgpt(text)
    print(resp)
    words = json.loads(resp)
    words = find_word_in_pages(words=words, pages=pages)
    json_data = json.dumps(
        data, indent=4, sort_keys=True, default=str)
    print(json_data)    