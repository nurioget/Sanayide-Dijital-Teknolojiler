import cv2
import numpy as np

def detect_squares(image, min_size_cm, max_size_cm):
    # Kamera çözünürlüğü ve fiziksel boyutları belirle (cm)

    frame_height_cm = 30  # Kameranın görebildiği yükseklik (cm)

    # Grayscale ve blur işlemi
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Kenar tespiti (Canny)
    edges = cv2.Canny(blurred, 50, 150)

    # Kontur bulma
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Konturları dolaş ve kareleri bul
    for contour in contours:
        # Çokgen oluştur ve kenar sayısını al
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Eğer 4 kenarlı ve kapalı bir şekilse
        if len(approx) == 4 and cv2.isContourConvex(approx):
            # Bounding box boyutlarını al
            (x, y, w, h) = cv2.boundingRect(approx)

            # Boyutu pikselden cm'ye çevir
            frame_width_pixels = image.shape[1]
            frame_height_pixels = image.shape[0]
            height_cm = (h / frame_height_pixels) * frame_height_cm

            # Eğer genişlik ve yükseklik belirtilen aralıktaysa, kare olarak işaretle
            if min_size_cm  <= max_size_cm and min_size_cm <= height_cm <= max_size_cm:
                cv2.drawContours(image, [approx], -1, (0, 255, 0), 3)
                # Kare koordinatları ve boyutunu yazdır
                print(f"Kare bulundu:cm x {height_cm:.2f} cm")

    return image

# Kameradan görüntü al
cap = cv2.VideoCapture(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Kare algılama fonksiyonunu çağır
    detected_frame = detect_squares(frame, min_size_cm=1.2, max_size_cm=2.7)

    
    # Sonuç görüntüsünü göster
    cv2.imshow('Squares Detection', detected_frame)

    # 'q' tuşuna basılana kadar bekle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
