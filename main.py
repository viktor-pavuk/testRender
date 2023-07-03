from typing import Optional
import requests
from fastapi import FastAPI
from fastapi import HTTPException
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup

app = FastAPI()

@app.post('/extract_text')
async def extract_text(url: str):
    # Download the PDF file
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to download PDF")

    with open('temp.pdf', 'wb') as f:
        f.write(response.content)

    # Open the PDF file and extract text
    with open('temp.pdf', 'rb') as f:
        reader = PdfReader(f)
        num_pages = len(reader.pages)
        text = ''
        for page in range(num_pages):
            page_obj = reader.pages[page]
            text += page_obj.extract_text()

    # Delete the temporary PDF file
    # Comment out the following line if you want to keep the downloaded file
    import os
    os.remove('temp.pdf')

    return {'text': text}
    
@app.get("/horoskop")
async def root(sign: str):
    signs = {
        "aries": 1,
        "taurus": 2,
        "gemini": 3,
        "cancer": 4,
        "leo": 5,
        "virgo": 6,
        "libra": 7,
        "scorpio": 8,
        "sagittarius": 9,
        "capricorn": 10,
        "aquarius": 11,
        "pisces": 12,
    }
    
    URL = "https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=" + \
        str(signs[sign])
    
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    container = soup.find("p")
    
    print()
    return {
        "text": container.text.strip()
    }
