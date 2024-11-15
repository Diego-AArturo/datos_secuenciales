import os
import math
import wave
import tempfile

import pyaudio
import whisper
from pydub import AudioSegment
from dotenv import load_dotenv
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
import flet as ft

# Cargar variables de entorno
load_dotenv()
api = None
api_elevenlabs = None
# Configurar APIs
# genai.configure(api_key=api)
# client = ElevenLabs(api_key=api_elevenlabs)

# Configuración de audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
SILENCE_THRESHOLD = 30.0
SILENCE_DURATION = 2  # en segundos
CHUNKS_TO_SILENCE = int(SILENCE_DURATION * RATE / CHUNK)

# Inicializa PyAudio y Whisper
audio = pyaudio.PyAudio()
model = whisper.load_model("base")

instruction = ('''
Responde como un asesor psicologico, experto en la salud mental
''')

# chat = genai.GenerativeModel(
#     "models/gemini-1.5-flash", system_instruction=instruction
# ).start_chat()

def record_audio():
    """Graba audio hasta detectar silencio prolongado."""
    stream_r = audio.open(format=FORMAT, channels=CHANNELS,
                          rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames, count = [], 0

    while True:
        data = stream_r.read(CHUNK)
        rms = sum(int.from_bytes(data[i:i+2], byteorder='little', signed=True)**2 
                  for i in range(0, len(data), 2))
        rms = math.sqrt(rms / (CHUNK // 2))
        if rms < SILENCE_THRESHOLD:
            count += 1
            if count >= CHUNKS_TO_SILENCE:
                break
        else:
            count = 0
        frames.append(data)

    stream_r.stop_stream()
    stream_r.close()
    return frames

def save_audio(frames):
    """Guarda el audio en un archivo WAV temporal y lo convierte a MP3."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav_file:
        with wave.open(temp_wav_file, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        temp_wav_file.close()  # Cierra el archivo WAV explícitamente

        temp_mp3_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        sound = AudioSegment.from_wav(temp_wav_file.name)
        sound.export(temp_mp3_file.name, format="mp3")

        os.remove(temp_wav_file.name)  # Eliminar el archivo WAV temporal
        return temp_mp3_file.name

def transcribe_audio(file_path):
    """Transcribe el archivo de audio usando Whisper."""
    return model.transcribe(file_path)["text"]

def text_to_speech_stream(text: str):
    """Convierte texto a voz utilizando ElevenLabs."""
    audio_stream = client.generate(
        text=text,
        voice="Mia - petite sounding",
        model="eleven_multilingual_v2",
        stream=True
    )
    return stream(audio_stream)

def main_logic(page, user_text, bot_text):
    try:
        # Mostrar mensaje de "Escuchando..."
        bot_text.value = "Escuchando..."
        bot_text.update()

        frames = record_audio()
        audio_path = save_audio(frames)
        transcript = transcribe_audio(audio_path)
        os.remove(audio_path)

        # Actualiza el campo de texto del usuario con la transcripción
        user_text.value = transcript
        user_text.update()

        # Generar respuesta con GenAI
        response = chat.send_message(transcript)

        # Mostrar la respuesta en el campo de texto del bot
        bot_text.value = response.text
        bot_text.update()

        # Convertir la respuesta en voz (esto solo genera el audio, no lo reproduce)
        text_to_speech_stream(response.text)

    except Exception as e:
        # En caso de error, muestra un mensaje de error en el bot
        
        bot_text.value = "Lo siento no te escuche"
        page.snack_bar.content = ft.Text("Error de configuracion")
        page.snack_bar.bgcolor = ft.colors.RED_200
        page.snack_bar.open = True
        page.update()
        



def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = True
    page.bgcolor = "#333333"
    PRIMARY_COLOR = "#A3C54B"
    TEXT_COLOR = ft.colors.WHITE


    def on_google_submit(e):
        global api, chat
        api = e.control.value 
        if api == '':
            page.snack_bar.content = ft.Text("Igrese la API de google")
            page.snack_bar.bgcolor = ft.colors.RED_200
            page.snack_bar.open = True

            page.update()
         # Actualiza la variable `api` con el valor del campo de texto
        else:
            genai.configure(api_key=api)
            
            chat = genai.GenerativeModel(
                "models/gemini-1.5-flash", system_instruction=instruction
            ).start_chat()

            # Actualizar y mostrar el snack_bar
            page.snack_bar.content = ft.Text("API key de Google configurada correctamente")
            page.snack_bar.open = True
            page.snack_bar.bgcolor = ft.colors.GREEN
            page.update()

    def on_elevenlabs_submit(e):
        global api_elevenlabs, client
        api_elevenlabs = e.control.value 
        if api == '':
            page.snack_bar.content = ft.Text("Ingrese la API de elevenlabs")
            page.snack_bar.bgcolor = ft.colors.RED_200
            page.snack_bar.open = True

            page.update()
        else: # Actualiza la variable `api` con el valor del campo de texto
            client = ElevenLabs(api_key=api_elevenlabs)
            
            # Actualizar y mostrar el snack_bar
            page.snack_bar.content = ft.Text("API key de elevenlabs configurada correctamente")
            page.snack_bar.open = True
            page.update()

    page.snack_bar = ft.SnackBar(
        content=ft.Text(""),
        bgcolor=ft.colors.GREEN
    )
    # Definir los campos de texto para el usuario y el bot
    # user_text = ft.TextField(label="User", col={"xs": 8, "md": 8}, bgcolor=ft.colors.GREY_900)
    #bot_text = ft.TextField(label="Bot", col={"xs": 8, "md": 8}, color=ft.colors.GREEN,multiline=True)
    user_text = ft.TextField(
    label="User",
    col={"xs": 8, "md": 8},
    bgcolor="#444444",  # Fondo gris oscuro para el usuario
    color=TEXT_COLOR,
    multiline=True,
    border_radius=ft.border_radius.all(10),  # Bordes redondeados
    
)

    bot_text = ft.TextField(
    label="Bot",
    col={"xs": 8, "md": 8},
    bgcolor=PRIMARY_COLOR,  # Verde para el bot
    color=TEXT_COLOR,
    multiline=True,
    border_radius=ft.border_radius.all(10),  # Bordes redondeados

)


    google = ft.ResponsiveRow(
    [
        ft.Text("key_google :", size=17, weight=ft.FontWeight.W_600, color=TEXT_COLOR, col={"xs": 4, "md": 4}),
        ft.TextField(
            label="Api_key",
            col={"xs": 8, "md": 8},
            bgcolor="#444444",  # Fondo ligeramente más claro
            color=TEXT_COLOR,
            password=True,
            can_reveal_password=True,
            on_submit=on_google_submit
        ),
    ],
    run_spacing={"xs": 10},
)

    elevenlabs = ft.ResponsiveRow(
        [
        ft.Text("key_elevenlabs :", size=17, weight=ft.FontWeight.W_600, color=TEXT_COLOR, col={"xs": 4, "md": 4}),
        ft.TextField(
            label="Api_key",
            col={"xs": 8, "md": 8},
            bgcolor="#444444",  # Fondo ligeramente más claro
            color=TEXT_COLOR,
            password=True,
            can_reveal_password=True,
            on_submit=on_elevenlabs_submit
        ),
    ],
    run_spacing={"xs": 10},
    )
    

    texts = [
        ft.Container(google, 
                     #border=ft.border.all(color=TEXT_COLOR),
                     col={"xs": 12, "md": 12}
                     ),
        ft.Container(elevenlabs,
                      #border=ft.border.all(),
                        col={"xs": 12, "md": 12}
                        ),
    ]

    historial_form = ft.Container(
    content=ft.Column(
        [
            ft.Container(content=ft.Text("Data Chat", size=32, weight=ft.FontWeight.W_600, color=ft.colors.WHITE, text_align='center')),  # Tamaño ajustado para jerarquía
            ft.Container(content=ft.Column(texts), border=ft.border.all(color=TEXT_COLOR, width=1),
                         border_radius=ft.border_radius.all(10), padding=15),  # Padding ajustado
        ],
        spacing=20,
    ),
    border=ft.border.all(color=TEXT_COLOR, width=2),
    border_radius=ft.border_radius.all(10),
    col={"xs": 12, "md": 5},
    padding=15,  # Padding en el contenedor general para más espacio
)

    
    chat_display = ft.Container(
    content=ft.Stack(
        [
            ft.Container(expand=True, bgcolor="#333333"),  # Fondo gris oscuro
            ft.Container(
                content=ft.Column([user_text, bot_text]),
                expand=True,
                bgcolor="#444444",
                padding=15,
                border=ft.border.all(color=TEXT_COLOR, width=1),
                border_radius=ft.border_radius.all(10),  # Bordes redondeados en todo el área de chat
            ),
        ]
    ),
    border=ft.border.all(color=TEXT_COLOR, width=1),
    border_radius=ft.border_radius.all(10),  # Bordes redondeados en todo el contenedor
    col={"xs": 12, "md": 7},
)

    items_center = ft.ResponsiveRow(
        [
            historial_form,
            chat_display,
        ],
        spacing=20,
        run_spacing={"xs": 20, "md": 20},
    )

    
    superior = ft.Container(
    content=ft.Text(
        "Chat voz ",
        size=48,  # Mantén este tamaño grande para destacar
        weight=ft.FontWeight.W_800,
        color=TEXT_COLOR,
        text_align='center',
        spans=[
            ft.TextSpan(
                "Charlabot",
                ft.TextStyle(color=PRIMARY_COLOR, size=48, weight=ft.FontWeight.W_800),
            )
        ]
    ),
    margin=ft.margin.only(top=20),
    padding=ft.padding.symmetric(horizontal=20),
    col={"xs": 12, "md": 12},
    alignment=ft.alignment.center_left
)

    centro = ft.Container(
    content=items_center,
    padding=ft.padding.all(20),  # Aplica un padding uniforme alrededor del contenido
    margin=ft.margin.symmetric(vertical=20),  # Margen uniforme en la parte superior e inferior
    col={"xs": 12, "md": 12},
)

    col = ft.Column(
        spacing=0,
        controls=[
            superior,
            centro,
        ],
    )

    container = ft.Container(col, bgcolor="#333333", alignment=ft.alignment.top_center)

    # Botón para iniciar la grabación y procesamiento
    
    
    start_button = ft.ElevatedButton(
    text = "Hacer pregunta",
    icon = ft.icons.MIC,
    on_click = lambda e: main_logic(page, user_text, bot_text),
    bgcolor = PRIMARY_COLOR,
    color = TEXT_COLOR,
    #border_radius=ft.border_radius.all(10),
    height = 60, 
     # Aumenta la altura para hacerlo más prominente
    on_hover = lambda e: (setattr(e.control, 'bgcolor', "#8BC34A" if e.data == "true" else PRIMARY_COLOR), e.control.update()),  # Cambia el color al pasar el mouse
)
    

    page.add(
        ft.Column(
            controls=[
                container,
                ft.Container(start_button,padding=ft.padding.only(left=25,top=0))
            ]
        )
    )

ft.app(main)
