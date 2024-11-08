import streamlit as st
import requests
import time

# Función para obtener datos de ThingSpeak
def get_data():
    url = 'https://api.thingspeak.com/channels/2733960/feeds.json?results=1'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['feeds'][0]  # Regresa los datos de la primera entrada
    else:
        st.error("Error al acceder a la API.")
        return None

# Función para verificar datos críticos
def check_critical_data(data):
    alerts = []
    
    # Verificar los valores críticos y agregar alertas
    if int(data['field1']) > 100:
        alerts.append("La temperatura está muy alta. Enviando mensaje de alerta.")
    if int(data['field2']) < 5.5:
        alerts.append("El pH está muy bajo. Enviando mensaje de alerta.")
    if float(data['field3']) < 50:
        alerts.append("La concentración de nutrientes está muy baja. Enviando mensaje de alerta.")
    if int(data['field4']) < 30:
        alerts.append("La humedad está muy baja. Enviando mensaje de alerta.")
    
    return alerts

# Configuración de la interfaz Streamlit
st.title("Monitoreo en Tiempo Real de Sensores")
st.write("Visualización de datos en tiempo real desde ThingSpeak")

# Contenedor vacío para actualizar datos sin recargar toda la página
data_placeholder = st.empty()
alert_placeholder = st.empty()

# Bucle para mostrar datos en tiempo real
while True:
    # Obtener los datos de la API
    data = get_data()
    
    if data:
        # Mostrar los datos en la interfaz
        with data_placeholder.container():
            st.subheader("Últimos Datos Recibidos")
            st.write(f"Temperatura: {data['field1']} °C")
            st.write(f"pH: {data['field2']}")
            st.write(f"Concentración de Nutrientes: {data['field3']} %")
            st.write(f"Humedad: {data['field4']} %")
        
        # Verificar si hay alertas
        alerts = check_critical_data(data)
        
        # Actualizar los mensajes de alerta
        with alert_placeholder.container():
            if alerts:
                for alert in alerts:
                    st.warning(alert)
            else:
                # Aquí solo mostramos un mensaje cuando no hay alertas
                st.success("Todos los valores están dentro de los rangos seguros.")
        

    # Esperar 15 segundos antes de la próxima actualización
    time.sleep(5)

