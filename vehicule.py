import cv2
import numpy as np

# on va decouper le video on des frames utilisant la methode VideoCapture
# we can also use the index 0, -1 , 1 if we want to work on the video 
# provided by the camera 
cap = cv2.VideoCapture('video.mp4')
#initialiser le substructeur 
algo=cv2.createBackgroundSubtractorMOG2()

min_w=75
min_h=90

# conteur
count_line_position = 550

def center(x,y,w,h):
    x1=int(w/2)
    y1=int(h/2)
    cx= x+x1
    cy= y+y1
    return cx,cy

offset = 6
countr = 0

detect = []


while True :
  # if frame is read correctly ret is True
  #  if the video ends the ret = false
  ret,frame1 = cap.read()
  #cv2.imshow('fe',frame1)
  #cv2.waitKey(50000)

#   if not ret:
#     break


  #mog2_FGMask = algo.apply(frame1)
  #cv2.imshow('jjj', mog2_FGMask)

  #grey = cv2.cvtColor(frame1, cv2.COLOR_BAYER_BG2BGR)
  #blur = cv2.GaussianBlur(grey, (3,3), 5)

  img_sub = algo.apply(frame1)
#   dilate = cv2.dilate(img_sub,np.ones((5,5)))
#   kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
#   dilatada = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
#   dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
# counter,h = cv2.findContours(img_sub, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  thresh, _ = cv2.threshold(img_sub, 50, 255, cv2.THRESH_BINARY)

  cv2.line(thresh,(25,count_line_position),(1200,count_line_position),(255,127,0),2)
  # cv2.line(thresh,(25,count_line_position+50),(1200,count_line_position+50),(0,110,255),1)
  # cv2.line(thresh,(25,count_line_position-50),(1200,count_line_position-50),(0,110,255),1)

  counter,h = cv2.findContours(img_sub, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

  for (i,c) in enumerate(counter):
    (x,y,w,h) = cv2.boundingRect(c)
    validate_conter=(w>=min_w) and (h>=min_h) and ((h+w)>2*min(h,w)) 
    if not validate_conter:
      continue
    
    cv2.rectangle(frame1, (x,y), (x+w,y+h),(0,255,0),2)
    cv2.putText(frame1, "Vehicule"+ str(countr), (x,y-20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255,244,0))
    cntr= center(x,y,w,h)
    detect.append(cntr)
    cv2.circle(frame1,cntr, 5, (0,0,255),5)
    for (x,y) in detect:
      if y<(count_line_position+offset) and y>(count_line_position-offset):
        countr+=1
    cv2.line(frame1,(25,count_line_position),(1200,count_line_position),(255,127,0),3)
    detect.remove((x,y))
    print("vehicule conter:" + str(countr))
  cv2.putText(frame1, "VEHICULE COUNTER"+ str(countr), (450,70), cv2.FONT_HERSHEY_DUPLEX, 2, (0,0,255))


  cv2.imshow('detector',img_sub)
  cv2.imshow('video',frame1)
  

  if cv2.waitKey(13) == ord('q') :
    break


cv2.destroyAllWindows()
cap.release()