# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 23:56:17 2019

@author: Wilsy
"""
import io
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Wilsy/Documents/application_default_credentials.json"


def detect_text(path):
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    
    with io.open(path,"rb") as image_file:
        content = image_file.read()
        
    image = vision.types.Image(content = content)
    
    
    response = client.text_detection(image = image)
    texts = response.text_annotations
   
    print(texts)

    
detect_text("C:/Users/Wilsy/Documents/Adhar card.jpg")