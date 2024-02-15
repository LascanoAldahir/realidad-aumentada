import cv2
import numpy as np
import cv2.aruco as aruco

import requests
#reemplaza tu token y vi  con tu token de autenticacion y numero de pin virtual
token="t7uA3ukcFNl6AaoKLN2h5HpA3CB-lJ-5"
pin_virtual="V0"
blynk_api_url= f'https://blynk.cloud/external/api/get?token={token}&{pin_virtual}'


# Crear un objeto detector de marcadores
parametros = cv2.aruco.DetectorParameters()

# Crear un diccionario de marcadores ArUco
aruco_diccionario = aruco.getPredefinedDictionary(aruco.DICT_6X6_100)

# Inicializar la cámara (asegúrate de tener una cámara conectada)
captura = cv2.VideoCapture(0)

#asi se quiere utilizar la camara del celular
ip="http://172.29.17.97:4747/video"
captura.open(ip)

# Cargar la imagen que deseas superponer 
nueva_imagen = cv2.imread("C:/Users/DESARROLLO IOT/Desktop/Lascano/Trabajos en clase/61.jpg")  

while True:
    # Capturar un fotograma o cuadro (frame) de la cámara
    lectura, frame = captura.read()
    
    # Convertir el fotograma a escala de grises
    cuadro_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Crear un objeto de detector ArUco
    detector = aruco.ArucoDetector(aruco_diccionario, parametros)

    # Detectar marcadores ArUco
    esquinas, identificador, puntosRechazados = detector.detectMarkers(cuadro_gris)


    #BLYNK
    valor_sensor = requests.get(blynk_api_url)
    valor=valor_sensor.text


    if identificador is not None:
        # Dibujar los marcadores detectados
        aruco.drawDetectedMarkers(frame, esquinas, identificador)
        
       
        for i in range(len(identificador)):
            # Obtener las esquinas del marcador actual
                marker_corners = esquinas[i][0]
                
                # Definir la posición y el tamaño de la superposición
                x, y, w, h = cv2.boundingRect(marker_corners)
                #escalar la imagen superpuesta para que se ajuste 
                imagen_sobrepuesta= cv2.resize(nueva_imagen,(w,h))
                #superponer la imagen en el marco
                frame[y:y+h, x:x+w]= imagen_sobrepuesta
                #superponer texto 
    
                cv2.putText(frame,valor,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
                #cv2.putText(frame,"Sensor 2",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
                
    # Mostrar el resultado en una ventana cv2.imshow(nombre_ventana, imagen)
    cv2.imshow('Aruco', frame)
    
    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar la ventana
captura.release()
cv2.destroyAllWindows()