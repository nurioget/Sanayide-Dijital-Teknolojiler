import cv2
import numpy as np

def detect_direction(lines, angle_threshold=40):
    if lines is None:
        return "Çizgi yok"
    
    angles = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            angle = np.arctan2((y2 - y1), (x2 - x1)) * 180 / np.pi
            angles.append(angle)
    
    mean_angle = np.mean(angles)
    
    if mean_angle < -angle_threshold:
        return "Sola dön"
    elif mean_angle > angle_threshold:
        return "Sağa dön"
    else:
        return "Düz git"

# Kamerayı başlat
cap = cv2.VideoCapture(1)

while True:
    # Kameradan bir kare yakalayın
    ret, frame = cap.read()

    if not ret:
        break

    # Görüntüyü gri tonlamaya çevir
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Görüntüyü bulanıklaştır (gürültüyü azaltmak için)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Siyah çizgiyi algılamak için threshold uygula
    _, threshold = cv2.threshold(blurred, 50, 255, cv2.THRESH_BINARY_INV)

    # Kenar algılama
    edges = cv2.Canny(threshold, 50, 150)

    # Hough Dönüşümü ile çizgileri algıla
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=10)

    # Çizgileri çiz ve yönünü belirle
    direction = detect_direction(lines, angle_threshold=15)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Yönü ekrana yazdır
    cv2.putText(frame, direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Sonuçları göster
    cv2.imshow('Frame', frame)
    cv2.imshow('Edges', edges)

    # 'q' tuşuna basarak döngüyü sonlandır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
