import cv2
from pyzbar.pyzbar import decode

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        continue

    
    decoded_objs = decode(frame)
    
    for obj in decoded_objs:
        print('QR Kod içeriği: ', obj.data)

    cv2.imshow('QR Kod Okuyucu', frame)

   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
