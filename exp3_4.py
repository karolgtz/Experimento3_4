import numpy as np
import PySimpleGUI as sg
import serial
import pandas as pd

# Crear el objeto de conexión serial
arduino = serial.Serial('COM3', 115200)

# Inicialización de parámetros del Instrumento Virtual
dist=0.0
xcoor=0
yant=0
xant= 0
Tespera = 20 # En milisegundos
datos = np.array([])
SaveData = False
v1=0
v2=0
v3=0
v4=0
v5=0
vprom=0
a=0
b=0

# Crear un método o función para borrar la gráfica y dibujar los ejes
def dibujo():
    # Draw axis    
    graph.erase()
    graph.DrawLine((0,0), (100,0))    
    graph.DrawLine((0,0), (0,100))    

    for x in range(0, 101, 20):    
        graph.DrawLine((x,-3), (x,3))    
        if x != 0:    
            graph.DrawText( x, (x,-10), color='green')    

    for y in range(0, 101, 20):    
        graph.DrawLine((-3,y), (3,y))    
        if y != 0:    
            graph.DrawText( y/10, (-10,y), color='blue')

# Configuración de elementos de la ventana
layout = [  [sg.InputText(default_text=v1,size=(8, 10),justification='center',background_color='gray', text_color='black', font='Arial 50 bold', key='Cajav1'), sg.Text('cm/s')], 
            [sg.InputText(default_text=v2,size=(8, 10),justification='center',background_color='gray', text_color='black', font='Arial 50 bold', key='Cajav2'), sg.Text('cm/s')],
            [sg.InputText(default_text=v3,size=(8, 10),justification='center',background_color='gray', text_color='black', font='Arial 50 bold', key='Cajav3'), sg.Text('cm/s')],
            [sg.InputText(default_text=v4,size=(8, 10),justification='center',background_color='gray', text_color='black', font='Arial 50 bold', key='Cajav4'), sg.Text('cm/s')],
            [sg.InputText(default_text=v5,size=(8, 10),justification='center',background_color='gray', text_color='black', font='Arial 50 bold', key='Cajav5'), sg.Text('cm/s')],
            [sg.InputText(default_text=vprom,size=(8, 10),justification='center',background_color='gray', text_color='black', font='Arial 50 bold', key='Cajav6'), sg.Text('cm/s')],
            [sg.HorizontalSeparator()],
            [sg.Checkbox('Gráfica', key='grafON'),sg.Checkbox('Datos', key='dataON')],
            [sg.HorizontalSeparator()],
            [sg.Graph(canvas_size=(400, 400),visible=False, graph_bottom_left=(-15,-15), graph_top_right=(105,105), background_color='white', key='graph')]]

# Crear la ventana
window = sg.Window('Medidor de distancia por ultrasonido', layout).Finalize()
graph = window['graph'] 

# Dibujar los ejes
dibujo()
arduino.write(b'a')
v1=float(arduino.readline().strip())
print (v1)
arduino.write(b'b')
v2=float(arduino.readline().strip())
print (v2)
arduino.write(b'c')
v3=float(arduino.readline().strip())
print (v3)
arduino.write(b'd')
v4=float(arduino.readline().strip())
print (v4)
arduino.write(b'e')
v5=float(arduino.readline().strip())
print (v5)

vprom=(v1+v2+v3+v4+v5)/5
# Ciclo infinito para atender eventos
while True:             
    
    # Capturar eventos y valores de elementos de la ventana
    event, values = window.read(timeout=Tespera)

    # Interrumpir el ciclo con el evento Cerrar ventana
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    
    # Si hay eventos, procesar 
    if event:
        
        # Almacenar Volt
        if values['dataON']==True: 
            SaveData = True
            datos=np.append(datos,dist)

        # Actualizar resultados
        window['Cajav1'].update("{:.{}f}".format( v1, 1))
        window['Cajav2'].update("{:.{}f}".format( v2, 1))
        window['Cajav3'].update("{:.{}f}".format( v3, 1))
        window['Cajav4'].update("{:.{}f}".format( v4, 1))
        window['Cajav5'].update("{:.{}f}".format( v5, 1))
        window['Cajav6'].update("{:.{}f}".format( vprom, 1))

        # Dibujar trazo 
        if values['grafON']==True: 
            graph.update(visible=True)
            graph.DrawLine((xant,yant),(xcoor,dist) ,color="red",width=1)
            yant=dist
            xant = xcoor 
            xcoor = xcoor + 1
            if(xcoor==100): 
                xcoor=0
                xant= 0            
                dibujo()
        else:
            graph.update(visible=False)

# Guardar datos en archivo .CSV
if SaveData==True:
    df = pd.DataFrame(datos)
    df.to_csv('MisDatos.csv', header=False)

window.close()
arduino.close()
