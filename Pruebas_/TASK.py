import sounddevice as sd
import numpy as np
import soundfile as sf

# ASK
fs = 18000  # Frecuencia de muestreo en Hz
duracion_tono = 0.3  # Duración del tono en segundos
f0 = 2000  # Frecuencia de la señal portadora para el bit 0
f1 = 3000  # Frecuencia de la señal portadora para el bit 1
amplitud = 0.5  # Amplitud de la señal portadora

def files_to_binary_representation(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()

    # Convertir datos binarios en una cadena de dígitos binarios
    binary_string = ''.join(format(byte, '08b') for byte in binary_data)
    print(binary_string)

    return binary_string

def modular_bit(bit):
    if bit == 0:
        señal_portadora = np.zeros(int(fs * duracion_tono))
    else:
        tiempo = np.linspace(0, duracion_tono, int(fs * duracion_tono), endpoint=False)
        señal_portadora = amplitud * np.sin(2 * np.pi * f1 * tiempo)
    
    return señal_portadora

def modular_cadena(cadena):
    señal_modulada = np.array([], dtype=np.float32)
    
    for caracter in cadena:
        bits = np.unpackbits(np.array([ord(caracter)], dtype=np.uint8))
        
        for bit in bits:
            señal_modulada = np.concatenate((señal_modulada, modular_bit(bit)))
       
    return señal_modulada

mensaje = "A"
señal_modulada = modular_cadena(mensaje)

sd.play(señal_modulada, fs)
sf.write('ASK.wav', señal_modulada, fs)
sd.wait()