# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 23:56:17 2019

@author: Wilsy
"""
import io
import os
import cv2

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Wilsy/Documents/application_default_credentials.json"
ref_path = "C:/Users/Wilsy/Documents/Aadhar Card_1.jpg"

def detect_text(path, req_id):
    if (not isinstance(path,str)) | (not isinstance(req_id, int)):
        return {"code":400,"message":"Bad input variables"}
    else:
        import math
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()
        
        with io.open(path,"rb") as image_file:
            content = image_file.read()
            
        image = vision.types.Image(content = content)
        img = cv2.imread(path)
        img_height,img_width, img_channels = img.shape
#        print("The dim are: ",img_width,img_height)
        
        response = client.text_detection(image = image)
        texts = response.text_annotations
       
        
    #    k = cv2.waitKey(0) # 0==wait forever
        boundary_vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in texts[0].bounding_poly.vertices])
        box_width = int(boundary_vertices[2].replace("(","").replace(")","").split(",")[0]) - int(boundary_vertices[0].replace("(","").replace(")","").split(",")[0])
        box_height =  int(boundary_vertices[2].replace("(","").replace(")","").split(",")[1]) - int(boundary_vertices[0].replace("(","").replace(")","").split(",")[1])
        
#        print(box_width, box_height)
        
        
        for text in texts:
            vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in text.bounding_poly.vertices])
            x1 = vertices[0].replace("(","").replace(")","").split(",")[0]
            x2 = vertices[0].replace("(","").replace(")","").split(",")[1]
            x3 = vertices[2].replace("(","").replace(")","").split(",")[0]
            x4 = vertices[2].replace("(","").replace(")","").split(",")[1]
    #        print(x1, x2, x3, x4)
    #        print((x1,x2),(x3,x4))
            
    #        a=(vertices[1], vertices[3])
    #        print(b)
    #        print(tuple(int(x[0]), int(x[1])) for x in a)
    #        print('bounds: {}'.format(','.join(vertices)))
            cv2.rectangle(img,(int(x1),int(x2)),(int(x3),int(x4)),(255,0,0),2)    
    #    print(boundary_vertices)
        
        
        # Reference Image
        with io.open(ref_path,"rb") as image_file:
            content = image_file.read()
            
        image = vision.types.Image(content = content)
        img = cv2.imread(ref_path)
        img_height_ref,img_width_ref,img_channel_ref = img.shape
    #    print("The ref image dims are: ", img_width_ref,img_height_ref)
        
        response = client.text_detection(image = image)
        texts = response.text_annotations
        
        
        boundary_vertices_ref = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in texts[0].bounding_poly.vertices])
        
        box_width_ref = int(boundary_vertices_ref[2].replace("(","").replace(")","").split(",")[0]) - int(boundary_vertices_ref[0].replace("(","").replace(")","").split(",")[0])
        box_height_ref =  int(boundary_vertices_ref[2].replace("(","").replace(")","").split(",")[1]) - int(boundary_vertices_ref[0].replace("(","").replace(")","").split(",")[1])
        
        width_coeff = box_width/box_width_ref
        height_coeff = box_height/box_height_ref
        
        new_width = img_width*width_coeff
        new_height = img_height*height_coeff
        
    #    print(new_width, new_height)
    #    cv2.imwrite("my_3.png",img)
    #    cv2.imshow("lalala", img)
    
    # =============================================================================
    # # Cropping a rectangle in the image
    #     image_cropped = img[347:398,500:1000]
    #     cv2.imwrite("cropped.png",image_cropped)
    #     
    #     
    #     with io.open("C:/Users/Wilsy/.spyder-py3/cropped.png","rb") as image_file:
    #         content = image_file.read()
    #         
    #     image = vision.types.Image(content = content)
    #     response = client.text_detection(image = image)
    #     texts = response.text_annotations
    # #    for text in texts:
    # #        print('\n"{}"'.format(text.description))
    # 
    #     for text in texts:
    #         print('\n"{}"'.format(text.description))
    # 
    #         vertices = (['({},{})'.format(vertex.x, vertex.y)
    #                     for vertex in text.bounding_poly.vertices])
    # 
    #         print('bounds: {}'.format(','.join(vertices)))
    # 
    # =============================================================================
    
    #   def image_resize()
        new_img = cv2.resize(img,(math.floor(new_width),math.floor(new_height)))    
        cv2.imwrite("new_image_3.png",new_img)
        return {"code":200,"message":"Request Successful. Image processed"}


input_image = detect_text("C:/Users/Wilsy/Documents/Aadhar Card_1.jpg",2)
print(input_image)


