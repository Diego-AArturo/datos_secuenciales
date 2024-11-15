**Proyecto de Asesoría Psicológica con Inteligencia Artificial**

Este proyecto integra modelos avanzados de inteligencia artificial, como Whisper, Gemini y ElevenLabs, para proporcionar una experiencia de asesoría psicológica asistida por IA. El flujo del programa es el siguiente:

Entrada de audio: el usuario proporciona una pregunta en formato de audio.
Conversión de audio a texto: el audio se transcribe a texto.
Generación de respuesta: la pregunta del usuario se analiza y se responde con un enfoque de asesoría psicológica.
Salida en audio: la respuesta se convierte nuevamente a audio y se reproduce para el usuario.
La interfaz gráfica (GUI) está desarrollada con Flet para Python.

Instrucciones para Ejecutar el Proyecto
Clona este repositorio:

```
Copiar código
git clone https://github.com/usuario/nombre-del-repositorio.git
```

Instala los requerimientos necesarios:

```
Copiar código
pip install -r requirements.txt

```

Ejecuta el programa:

```
Copiar código
python Bot_web.py
```

Al iniciar, la interfaz solicitará las API keys de Gemini y ElevenLabs (https://elevenlabs.io/app/speech-synthesis/text-to-speech). Ingresa cada clave en los campos correspondientes y presiona "Enter" para configurarlas en el sistema.

Una vez configuradas las claves, podrás comenzar a utilizar el chatbot haciendo preguntas en audio y recibiendo respuestas en formato de voz.

***Estructura del Código***

- *record_audio:* Graba el audio hasta detectar silencio, lo que indica el fin de la grabación.
- *save_audio:* Guarda el audio en un archivo temporal en formato MP3.
- *transcribe_audio:* Convierte el audio grabado a texto usando el modelo Whisper.
- *text_to_speech_stream:* Convierte el texto de respuesta a audio utilizando ElevenLabs.
- *main_logic:* Controla el flujo principal de la aplicación, incluyendo la grabación, transcripción, generación de respuesta y conversión de texto a voz.
- *main:* Configura la interfaz gráfica, incluyendo los campos de entrada de API y el botón para iniciar la grabación.

Uso del Botón de Grabación

Para hacer una pregunta, simplemente haz clic en el botón "Hacer pregunta" y permite que el sistema escuche, procese y responda en audio.

Notas

Este proyecto está configurado para funcionar con el modelo de Gemini y la voz de ElevenLabs "Mia - petite sounding".
La interfaz utiliza Flet para crear una experiencia visual intuitiva y amigable.

