import streamlit as st
import requests
import plotly.graph_objects as go
import time

# Inicialización de listas para almacenar los datos de cada sensor en tiempo real
temp_data = []
ph_data = []
nutrients_data = []
hum_data = []
timestamps = []

# Función para obtener datos de ThingSpeak
def get_data():
    url = 'https://thingspeak.mathworks.com/channels/2735925/feeds.json?results=1'
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
    if int(data['field1']) > 22:
        alerts.append("Temperatura muy alta. Enviando mensaje de alerta.")
    elif int(data['field1']) < 16:
        alerts.append("Temperatura muy baja. Enviando mensaje de alerta.")
        
    if float(data['field2']) > 6:
        alerts.append("El pH está alto. Enviando mensaje de alerta.")
    elif float(data['field2']) < 5.5:
        alerts.append("El pH está bajo. Enviando mensaje de alerta.")
        
    if int(data['field3']) < 500:
        alerts.append("La concentración de nutrientes es baja. Enviando mensaje de alerta.")
    elif int(data['field3']) > 700:
        alerts.append("La concentración de nutrientes está saturada. Enviando mensaje de alerta.")
        
    if int(data['field4']) < 50:
        alerts.append("La humedad está baja. Enviando mensaje de alerta.")
    elif int(data['field4']) > 70:
        alerts.append("La humedad está alta. Enviando mensaje de alerta.")
    
    return alerts

# Configuración de la interfaz Streamlit
st.title("Monitoreo en Tiempo Real de Sensores")
st.write("Visualización de datos en tiempo real desde ThingSpeak")

# Contenedores para los datos y alertas
data_placeholder = st.empty()
alert_placeholder = st.empty()

# Configurar contenedores para gráficos
col1, col2 = st.columns(2)
temp_chart = col1.empty()
ph_chart = col2.empty()
nutrients_chart = col1.empty()
hum_chart = col2.empty()

# Bucle para mostrar datos en tiempo real
while True:
    # Obtener los datos de la API
    data = get_data()
    
    if data:
        # Agregar los datos actuales a las listas correspondientes
        temp_data.append(int(data['field1']))
        ph_data.append(float(data['field2']))
        nutrients_data.append(int(data['field3']))
        hum_data.append(int(data['field4']))
        timestamps.append(data['created_at'])

        # Mostrar los datos en la interfaz
        with data_placeholder.container():
            st.subheader("Últimos Datos Recibidos")
            st.write(f"Temperatura: {data['field1']} °C")
            st.write(f"pH: {data['field2']}")
            st.write(f"Concentración de Nutrientes: {data['field3']} ppm")
            st.write(f"Humedad: {data['field4']} %")

        # Verificar si hay alertas
        alerts = check_critical_data(data)
        with alert_placeholder.container():
            if alerts:
                for alert in alerts:
                    st.warning(alert)
            else:
                st.success("Todos los valores están dentro de los rangos seguros.")
        
        # Crear y actualizar gráficos individuales para cada sensor
        temp_fig = go.Figure(data=[go.Scatter(x=timestamps, y=temp_data, mode='lines+markers', name="Temperatura")])
        temp_fig.update_layout(title="Temperatura (°C)", xaxis_title="Tiempo", yaxis_title="Temperatura (°C)", height=300)
        temp_chart.plotly_chart(temp_fig, use_container_width=True)

        ph_fig = go.Figure(data=[go.Scatter(x=timestamps, y=ph_data, mode='lines+markers', name="pH")])
        ph_fig.update_layout(title="pH", xaxis_title="Tiempo", yaxis_title="pH", height=300)
        ph_chart.plotly_chart(ph_fig, use_container_width=True)
        
        nutrients_fig = go.Figure(data=[go.Scatter(x=timestamps, y=nutrients_data, mode='lines+markers', name="Nutrientes")])
        nutrients_fig.update_layout(title="Concentración de Nutrientes (ppm)", xaxis_title="Tiempo", yaxis_title="Nutrientes (%)", height=300)
        nutrients_chart.plotly_chart(nutrients_fig, use_container_width=True)
        
        hum_fig = go.Figure(data=[go.Scatter(x=timestamps, y=hum_data, mode='lines+markers', name="Humedad")])
        hum_fig.update_layout(title="Humedad (%)", xaxis_title="Tiempo", yaxis_title="Humedad (%)", height=300)
        hum_chart.plotly_chart(hum_fig, use_container_width=True)
    
    # Esperar antes de la próxima actualización
    time.sleep(15)
