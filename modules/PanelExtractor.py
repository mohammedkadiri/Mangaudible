import cv2 as cv
import matplotlib.pyplot as plt 
import urllib.request as ur
import numpy as np
import sys
import math
import re
import pytesseract
from google_trans_new import google_translator
from google.cloud import vision
from googletrans import Translator


pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Convert url to image with python
def url_to_image(url):
    '''
    Returns an a grayscaled image 
    :url: URL of an image 
    '''
    resp = ur.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv.imdecode(image, cv.IMREAD_GRAYSCALE)
    return image

def panelExtraction(img):
    '''
    Returns the number of panels within an image
    :img: Grayscaled image with panels
    '''
    img_copy = img.copy()
    gray = img_copy
    # size contains the width, height of the image
    size = list(img_copy.shape[:2])
    size.reverse()
    # print("Width: "+str(size[0]) + " Height: "+str(size[1]))
    panels = []
    tmin = 180
    tmax = 255
    ret, thresh2 = cv.threshold(gray, tmin, tmax, cv.THRESH_BINARY)
    ret, thresh1 = cv.threshold(gray, tmin, tmax, cv.THRESH_BINARY_INV)
    contours = cv.findContours(thresh1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv.findContours(thresh1, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2:]
    # Get (square) panels out of contours
    for contour in contours:
        arclength = cv.arcLength(contour, True)
        epsilon = 0.01 * arclength
        approx = cv.approxPolyDP(contour, epsilon, True)
        x, y, w, h = cv.boundingRect(approx)
        # exclude very small panels
        if w < size[0]/15 or h < size[1]/15:
            continue
        contourSize = int(sum(size) / 2 * 0.004)
        cv.drawContours(img_copy, [approx], 0, (255, 0, 0), contourSize)
        titles = ['Original Image', 'GrayScale', 'Threshold', 'Inverted', 'Final']
        images = [img, gray, thresh2, thresh1, img_copy]
        panel = [x, y, w, h]
        panels.append(panel)
    # for i in range(5):
    #     plt.subplot(1, 5, i + 1), plt.imshow(images[i], 'gray')
    #     plt.title(titles[i])
    #     plt.xticks([]), plt.yticks([])
    # plt.show()
    return panels


def sort_panels(panels):
    '''
    Returns sorted panels
    :panels: A list of panels to sort
    '''
    temp = sorted(panels, key=lambda x: (x[0], x[1]))
    return temp


def retrieve_panel_text(url):
    '''
    Retrieves the text within each panel in a manga
    :url: Takes a URL of an image
    '''
    # convert the url to an image
    img = url_to_image(url)
    if img is None:
        sys.exit("Could not read image properly")
    # Extract the panels from the image
    panels = panelExtraction(img)
    sorted_panels = sort_panels(panels)
    frames = []
    #Extract the text from each panel
    for panel in range(len(sorted_panels)):
        str = ""
        # Need to create dynamic variables depending on the number of panels
        x, y, w, h = sorted_panels[panel]
        panel = img[y:y + h, x:x + w]
        ret, temp = cv.threshold(panel, 200, 255, cv.THRESH_BINARY)
        # rotated = imutils.rotate_bound(temp, 270)
        # flipped = cv.flip(rotated, 1)
        # flip = cv.flip(img, 1)
        custom_oem_psm_config = r'--psm 5'
        text = pytesseract.image_to_string(temp, lang='jpn_vert', config=custom_oem_psm_config)
        if text not in frames:
            frames.append(text)
    full_text = "".join(frames)
    return full_text

def detect_document_uri(uri):
    """Detects document features in the file located in Google Cloud
    Storage."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri
    jp_text = " "

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            # print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                # print('Paragraph confidence: {}'.format(
                #     paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    # print('Word text: {} (confidence: {})'.format(
                    #     word_text, word.confidence))
                    jp_text += word_text

                    # for symbol in word.symbols:
                    #     # print('\tSymbol: {} (confidence: {})'.format(
                    #     #     symbol.text, symbol.confidence))


    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return jp_text

def calculate_accuracy(panel_text, google_ocr_text):
    '''  
    Returns an percentage of the text in the panels found in google ocr version
    :panel_text: Text retrieved from panels using custom method
    :google_ocr_text: Text retrieved using google ocr 
    '''
    counter = 0
    for char in google_ocr_text:
        if char in panel_text:
            counter += 1

    accuracy = math.ceil((counter / len(google_ocr_text)) * 100)
    return accuracy

def translate_ocr_text(google_ocr_text):
    pattern = r'[a-zA-Z0-9?|!.]'
    google_ocr_text = re.sub(pattern, '', google_ocr_text)
    translator = Translator()
    result = translator.translate(google_ocr_text, dest='en')
    return result.text

def process_image(url):
    '''
    Returns the processed manga page
    :url: Takes a URL for a manga page 
    '''
    image = url_to_image(url)
    # gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) # grayscale
    thresh = cv.threshold(image, 180, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
    comp = cv.connectedComponentsWithStats(thresh)
    numLabels = comp[0]
    labels = comp[1]
    stats = comp[2]
    areas = stats[:, 4]
    maxArea = 200
    minArea = 30
    # Discards any connected components to small or too large 
    for compLabel in range(1, numLabels):
        if areas[compLabel] > maxArea or areas[compLabel] < minArea:
            labels[labels == compLabel] = 0
    labels[labels > 0] = 1
    # Apply a kernel to determine if the blob  is a potential speech bubble 
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (30, 30))
    # Dilate to fill all the blobs with white
    dilate_text = cv.morphologyEx(labels.astype(np.uint8), cv.MORPH_DILATE, kernel)
    comp = cv.connectedComponentsWithStats(dilate_text)
    numLabels = comp[0]
    labels = comp[1]
    stats = comp[2]
    areas = stats[:, 4]

    components = []
    # Add all the connected components coordinates
    for compLabel in range(1, numLabels):
        x1, y1 = stats[compLabel, 0], stats[compLabel, 1]
        x2, y2 = (stats[compLabel, 0]+stats[compLabel, 2]), (stats[compLabel, 1]+stats[compLabel, 3])
        # cv.rectangle(image, (x1, y1), (x2, y2 + 10), (0, 0, 255), 2)
        # Have rect coordinates
        # (y1:y2, x1, x2)
        components.append((x1, y1, x2, y2))


    # plt.imshow(image)
    # plt.show()

    translator = google_translator()

    for panel in components:
        x1,y1,x2,y2 = panel
        # crop each speech bubble 
        temp =  image[y1:y2,x1:x2]
        custom_oem_psm_config = r'--psm 5'
        # Extract text from the speech bubble 
        text = pytesseract.image_to_string(temp, lang='jpn_vert', config=custom_oem_psm_config)
        pattern = r'[a-zA-Z0-9?|!.,*()-:/\\]'
        text = re.sub(pattern, '', text)
        text = re.sub('\s+', ' ', text)
        words = text.replace(" ", "")
        # Translate the extracted text 
        result = translator.translate(words, lang_tgt='en')
        # Check if the component actually contains actual jp chars
        # if words.isalpha():
        # print(result)
        org = (int((x1 + x2) / 2), int((y1 + y2) / 2))
        # Determine the size of the text in english
        (width, height), baseline = cv.getTextSize(result, cv.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        # cv.rectangle(image, (x1, y1), (x2-20, y2-30), (255, 255, 255), cv.FILLED)
        #Draw a white background around the text
        cv.rectangle(image, (org[0], org[1] - height), (org[0] + width, org[1]), (255, 255, 255), cv.FILLED)
        # Place the text back into the center of the speech bubble 
        image = cv.putText(image, result, (org[0] - 20, org[1]), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    return image


# url = "https://storage.googleapis.com/mangaudible/manga/Grand%20Blue/chapter1/10.jpg"

# print( panelExtraction(url_to_image(url)))

# img = process_image(url)

# cv.imshow("image", img)
# cv.waitKey(0)

# panels = [[16, 1889, 380, 287], [9, 18, 873, 338], [567, 365, 319, 330]]
# print(sort_panels(panels))


# panel_text = retrieve_panel_text(url)
# print(panel_text)
# google_ocr_text = detect_document_uri(url)
# accuracy = calculate_accuracy(panel_text, google_ocr_text)
# translated_panel_text = translate_ocr_text(google_ocr_text)
# print(translated_panel_text)
# cv.waitKey(0)










    
