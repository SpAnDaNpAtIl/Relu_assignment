import cv2
import pytesseract
from requests_html import HTMLSession
import urllib.request
import numpy as np
from amazoncaptcha import AmazonCaptcha

session = HTMLSession()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


url = 'https://www.amazon.com/errors/validateCaptcha'
r = session.get(url)
imgData = r.html.find('img')[0].attrs['src']

print(imgData, AmazonCaptcha.fromlink(imgData).solve()) #trained from this

#alternate solution using pytesseract but it fails somehow
imgData = urllib.request.urlopen(imgData)
arr = np.asarray(bytearray(imgData.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1)
text = pytesseract.image_to_string(img)
print(text)

cv2.imshow('image', img)
cv2.waitKey(10000)


