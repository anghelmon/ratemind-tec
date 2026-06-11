import streamlit as st
import time
import matplotlib.pyplot as plt
import numpy as np

# =========================================================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# =========================================================================
st.set_page_config(page_title="RateMind - Razones de Cambio", layout="wide")

st.title("📐 RateMind: Mediador de Razones de Cambio con IA")
st.write("Desarrollado para el curso MA1102 - Cálculo Diferencial e Integral | TEC")

# =========================================================================
# 2. BARRA LATERAL DE NAVEGACIÓN
# =========================================================================
seccion = st.sidebar.radio(
    "Menú de Navegación:",
    ["1. Fundamento Teórico", "2. Tutor con IA", "3. Reto final"]
)

# =========================================================================
# SECCIÓN 1: FUNDAMENTO TEÓRICO
# =========================================================================
if seccion == "1. Fundamento Teórico":
    st.header("1. Concepto de Razón de Cambio Relacionada")
    st.write("""
    En el mundo real, muchas variables están ligadas por relaciones geométricas o físicas. 
    Cuando estas variables cambian con respecto al tiempo, sus **razones de cambio** también están relacionadas.
    """)
    
    st.info("""
    **Definición Matemática:** Si dos variables $x$ e $y$ dependen del tiempo $t$ y están relacionadas por una ecuación, 
    podemos encontrar la relación entre sus derivadas $\\frac{dx}{dt}$ y $\\frac{dy}{dt}$ utilizando la **derivación implícita** y la regla de la cadena.
    """)
    
    st.latex(r"\frac{dy}{dt} = \frac{dy}{dx} \cdot \frac{dx}{dt}")
    
    st.subheader("Pasos generales para resolver estos problemas:")
    st.markdown("""
    1. **Identificar las variables:** Asignar símbolos a todas las magnitudes que funciones con respecto al tiempo.
    2. **Escribir datos conocidos:** Identificar qué tasas de cambio nos da el enunciado.
    3. **Encontrar la ecuación ligadura:** Una fórmula geométrica o física que relacione las variables.
    4. **Derivar implícitamente:** Derivar ambos lados de la ecuación respecto al tiempo ($t$).
    5. **Sustituir y despejar:** Introducir los valores numéricos *después* de haber derivado y despejar la incógnita.
    """)

# =========================================================================
# SECCIÓN 2: SIMULADOR E IA (Gráfico Nativo de Python + Tutor Gemini)
# =========================================================================
elif seccion == "2. Tutor con IA":
    st.header("Resolución de Problemas con Mediación Pedagógica")
    
    modalidad = st.radio(
        "Elige la modalidad de trabajo:",
        ["A. Problema Guiado (Tanque Cónico Interactivo)", "B. Resolver mi propio problema de Razón de Cambio"]
    )
    
    st.write("---")
    col1, col2 = st.columns([1, 1])
    
    # CONFIGURACIÓN DEL CASO A: EL CONO CON GRÁFICO NATIVO
    if modalidad == "A. Problema Guiado (Tanque Cónico Interactivo)":
        with col1:
            st.subheader("Visualización y Enunciado")
            st.write("""
            Un tanque de agua tiene la forma de un cono invertido. La altura del tanque es de **10 metros** y el radio de la base superior es de **4 metros**. Si se bombea agua al tanque a razón constante 
            de $2\\text{ m}^3/\\text{min}$, ¿con qué rapidez sube el nivel del agua cuando el líquido tiene 
            una profundidad de **5 metros**?
            """)
            
            st.write("---")
            # Control interactivo del nivel del agua
            altura_actual = st.slider("Ajusta la profundidad del agua ($h$ en metros):", 1.0, 10.0, 5.0)
            
            # GENERACIÓN DEL GRÁFICO INTERACTIVO NATIVO EN PYTHON
            fig, ax = plt.subplots(figsize=(5, 5))
            
            # Dibujar el contorno del cono invertido (paredes del tanque)
            ax.plot([-4, 0, 4], [10, 0, 10], color="black", linewidth=2, label="Paredes del Tanque")
            ax.plot([-4, 4], [10, 10], color="black", linestyle="--") # Tapa superior
            
            # Calcular el radio actual del agua por semejanza de triángulos (r = 0.4 * h)
            radio_agua = 0.4 * altura_actual
            
            # Dibujar el agua como un trapecio coloreado de azul
            y_agua = np.linspace(0, altura_actual, 100)
            x_izq = -0.4 * y_agua
            x_der = 0.4 * y_agua
            ax.fill_betweenx(y_agua, x_izq, x_der, color="skyblue", alpha=0.7, label="Agua en el tanque")
            
            # Configuración estética del gráfico
            ax.set_xlim(-5, 5)
            ax.set_ylim(-0.5, 11)
            ax.set_xlabel("Radio (metros)")
            ax.set_ylabel("Altura / Profundidad (metros)")
            ax.set_title("Estado Dinámico del Tanque")
            ax.grid(True, linestyle=":", alpha=0.6)
            ax.legend(loc="upper right")
            
            # Mostrar el gráfico directamente en la interfaz de Streamlit
            st.pyplot(fig)
            
            # Cálculos de validación matemática en tiempo real
            dv_dt = 2.0
            velocidad_real = (25 * dv_dt) / (4 * 3.141592 * (altura_actual**2))
            
            st.metric(label="Rapidez instantánea calculada teóricamente (dh/dt)", value=f"{velocidad_real:.4f} m/min")
            st.caption("💡 *Observación matemática:* Nota en el gráfico que a menor altura el cono es más estrecho, por lo que el nivel sube rápido. Conforme se llena, se ensancha y el agua sube más lento.")

        instrucciones_tutor = (
            "Eres un profesor y tutor experto en cálculo del Instituto Tecnológico de Costa Rica (TEC). "
            "Estás ayudando a un estudiante a resolver un problema específico de razones de cambio relacionadas de un cono invertido "
            "(Altura = 10m, Radio = 4m, dV/dt = 2 m^3/min). "
            "REGLA DE ORO ABSOLUTA: Nunca, bajo ninguna circunstancia, le des la respuesta numérica final ni resuelvas las derivadas por él. "
            "Debes usar estrictamente el método socrático: hazle preguntas cortas, evalúa si sus planteamientos son correctos y dale pistas conceptuales muy breves."
        )
        mensaje_inicial = "¡Hola! Analicemos el problema del cono invertido juntos junto al simulador visual. ¿Qué datos o variables logras identificar primero en el enunciado?"

    # CONFIGURACIÓN DEL CASO B: PROBLEMA LIBRE
    else:
        with col1:
            st.subheader("📥 Introduce tu propio problema")
            st.write("""
            Escribe en el cuadro de abajo el enunciado de cualquier problema de razones de cambio relacionadas que quieras estudiar.
            """)
            problema_usuario = st.text_area(
                "Escribe aquí el enunciado completo:",
                placeholder="Ejemplo: Una escalera de 5 metros está apoyada contra una pared..."
            )
            if problema_usuario:
                st.success("📝 Problema registrado. Ahora ve al chat de la derecha para empezar la tutoría.")
            else:
                st.info("💡 Por favor, digita un problema para que el tutor de IA tenga el contexto de qué ayudarte a analizar.")

        instrucciones_tutor = (
            "Eres un profesor y tutor experto en cálculo del Instituto Tecnológico de Costa Rica (TEC). "
            f"El estudiante quiere que lo guíes a resolver el siguiente problema que él mismo propuso: '{problema_usuario}'. "
            "REGLA DE ORO ABSOLUTA: Nunca, bajo ninguna circunstancia, resuelvas el problema por él ni le des el resultado numérico final. "
            "Tu labor es guiarlo paso a paso de forma socrática sin resolver nada."
        )
        mensaje_inicial = "¡Hola! He leído el problema que registraste. Comencemos con el primer paso del análisis matemático: ¿cuáles son las variables involucradas y qué tasas de cambio nos da directamente el texto?"

    # COLUMNA 2: Chatbot Tutor con API de Gemini
    with col2:
        st.subheader("🤖 Tu Tutor IA de Cálculo (En Vivo)")
        st.write("Usa este chat para interactuar con la IA. Ella se adaptará a la opción de la izquierda.")

        import google.genai as genai
        from google.genai import types

        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=GEMINI_API_KEY)

        historial_key = f"history_{modalidad}"

        if historial_key not in st.session_state:
            st.session_state[historial_key] = [{"role": "model", "text": mensaje_inicial}]

        for msg in st.session_state[historial_key]:
            role_display = "user" if msg["role"] == "user" else "assistant"
            with st.chat_message(role_display):
                st.write(msg["text"])

        if user_input := st.chat_input("Escribe tu duda o tu paso aquí...", key=f"input_{modalidad}"):
            st.session_state[historial_key].append({"role": "user", "text": user_input})
            with st.chat_message("user"):
                st.write(user_input)

            if modalidad == "B. Resolver mi propio problema de Razón de Cambio" and not problema_usuario:
                with st.chat_message("assistant"):
                    aviso_error = "⚠️ Por favor, escribe primero el enunciado de tu problema en el cuadro de la izquierda."
                    st.error(aviso_error)
                    st.session_state[historial_key].append({"role": "model", "text": aviso_error})
            else:
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    contents_api = []
                    for m in st.session_state[historial_key]:
                        contents_api.append(
                            types.Content(role=m["role"], parts=[types.Part.from_text(text=m["text"])])
                        )

                    try:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=contents_api,
                            config=types.GenerateContentConfig(
                                system_instruction=instrucciones_tutor,
                                temperature=0.4
                            )
                        )
                        reply = response.text
                        message_placeholder.write(reply)
                        st.session_state[historial_key].append({"role": "model", "text": reply})
                    except Exception as e:
                        st.error("Hubo un problema de comunicación con los servidores de la IA. Revisa tu conexión.")

# =========================================================================
# SECCIÓN 3: RETO final
# =========================================================================
elif seccion == "3. Reto final":
    st.header("🎯 Demuestra tu Autonomía Matemática")
    st.subheader("Problema Avanzado: El auto en la intersección")
    st.write("""
    Un automóvil viaja hacia el norte a $60\\text{ km/h}$ y otro hacia el este a $80\\text{ km/h}$. 
    Ambos parten del mismo punto de la intersección. ¿Con qué rapidez aumenta la distancia entre ellos 
    exactamente **2 horas** después de que iniciaron su viaje?
    """)
    
    st.warning("⚠️ **Retiro de apoyo de IA:** En esta sección el chatbot está desactivado. Resuélvelo por tu cuenta.")
    
    st.write("---")
    respuesta_usuario = st.number_input("Ingresa tu respuesta numérica final para la razón de cambio (en km/h):", min_value=0.0, step=1.0)
    
    if st.button("Verificar y Validar Respuesta"):
        if abs(respuesta_usuario - 100.0) < 0.1:
            st.success("🎉 ¡Excelente! Tu respuesta es correcta y matemáticamente exacta. La distancia aumenta a razón de **100 km/h**.")
        else:
            st.error("❌ La respuesta no es correcta. Te doy una pista: usa Pitágoras e intenta de nuevo.")