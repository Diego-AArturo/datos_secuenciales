Proyecto de Asesoría Psicológica con Inteligencia Artificial
Este proyecto integra modelos avanzados de inteligencia artificial, como Whisper, Gemini y ElevenLabs, para proporcionar una experiencia de asesoría psicológica asistida por IA. El flujo del programa es el siguiente:

Entrada de audio: el usuario proporciona una pregunta en formato de audio.
Conversión de audio a texto: el audio se transcribe a texto.
Generación de respuesta: la pregunta del usuario se analiza y se responde con un enfoque de asesoría psicológica.
Salida en audio: la respuesta se convierte nuevamente a audio y se reproduce para el usuario.
La interfaz gráfica (GUI) está desarrollada con Flet para Python.

Instrucciones para Ejecutar el Proyecto
Clona este repositorio:

bash
Copiar código
git clone https://github.com/usuario/nombre-del-repositorio.git
Instala los requerimientos necesarios:

bash
Copiar código
pip install -r requirements.txt
Ejecuta el programa:

bash
Copiar código
python Bot_web.py
Al iniciar, la interfaz solicitará la API Key de Gemini y la API Key de ElevenLabs (puedes obtenerla en ElevenLabs). Ingresa cada clave y presiona "Enter" para que el sistema las registre.

Una vez configurado, podrás empezar a usar el programa para obtener respuestas de asesoría psicológica a través de audio.
