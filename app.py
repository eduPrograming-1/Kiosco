from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse

from registro import router as registro_router

import cv2
import datetime
import time
import os

app = FastAPI()

# ==========================================
# IMPORTAR MODULO REGISTRO
# ==========================================

app.include_router(registro_router)

# ==========================================
# CARPETA DE FOTOS
# ==========================================

os.makedirs("fotos", exist_ok=True)

# ==========================================
# CAMARA
# ==========================================

camara = cv2.VideoCapture(0)

camara.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camara.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# ==========================================
# DETECTOR FACIAL
# ==========================================

detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# ==========================================
# VARIABLES DE ACCESO
# ==========================================

usuario_detectado = False
nombre_usuario = ""

# ==========================================
# VIDEO STREAM
# ==========================================

def generar_video():

    global usuario_detectado
    global nombre_usuario

    while True:

        success, frame = camara.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        gris = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        rostros = detector.detectMultiScale(
            gris,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100,100)
        )

        usuario_detectado = False

        for (x, y, w, h) in rostros:

            rostro_actual = frame[y:y+h, x:x+w]

            for archivo in os.listdir("fotos"):

                ruta = os.path.join(
                    "fotos",
                    archivo
                )

                foto_registrada = cv2.imread(ruta)

                if foto_registrada is None:
                    continue

                try:

                    rostro_gris = cv2.cvtColor(
                        rostro_actual,
                        cv2.COLOR_BGR2GRAY
                    )

                    registrado_gris = cv2.cvtColor(
                        foto_registrada,
                        cv2.COLOR_BGR2GRAY
                    )

                    rostro_gris = cv2.resize(
                        rostro_gris,
                        (200,200)
                    )

                    registrado_gris = cv2.resize(
                        registrado_gris,
                        (200,200)
                    )

                    diferencia = cv2.absdiff(
                        rostro_gris,
                        registrado_gris
                    )

                    resultado = diferencia.mean()

                    if resultado < 55:

                        usuario_detectado = True

                        nombre_usuario = archivo.replace(
                            ".jpg",
                            ""
                        )

                        cv2.putText(
                            frame,
                            "ACCESO AUTORIZADO",
                            (x, y-40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0,255,0),
                            2
                        )

                        break

                except:
                    pass

            # ======================================
            # RECTANGULO VERDE
            # ======================================

            cv2.rectangle(
                frame,
                (x,y),
                (x+w,y+h),
                (0,255,0),
                3
            )

            if datetime.datetime.now().microsecond % 2 == 0:

                cv2.rectangle(
                    frame,
                    (x,y),
                    (x+w,y+h),
                    (0,255,0),
                    6
                )

            if usuario_detectado:

                texto = "ROSTRO VALIDADO"

                color = (0,255,0)

            else:

                texto = "ROSTRO DETECTADO"

                color = (0,255,255)

            cv2.putText(
                frame,
                texto,
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

        ret, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )

# ==========================================
# PAGINA PRINCIPAL
# ==========================================

@app.get("/")
async def inicio():

    global usuario_detectado
    global nombre_usuario

    fecha = datetime.datetime.now().strftime("%d/%m/%Y")
    hora = datetime.datetime.now().strftime("%I:%M %p")

    html = f"""

<!DOCTYPE html>
<html lang="es">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Kiosco IA</title>

<link rel="stylesheet"
href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<style>

*{{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:Arial;
}}

body{{

    width:100%;
    height:100vh;

    display:flex;
    justify-content:center;
    align-items:center;

    background:
    linear-gradient(
        135deg,
        #0f172a,
        #1e3a8a,
        #312e81
    );
}}

.kiosco{{

    width:100%;
    max-width:520px;

    height:100vh;

    overflow:auto;

    background:#f8fafc;

    display:flex;
    flex-direction:column;
}}

.header{{

    background:
    linear-gradient(
        90deg,
        #001b4b,
        #0f172a
    );

    color:white;

    padding:20px;

    display:flex;
    justify-content:space-between;
    align-items:center;
}}

.logo{{

    display:flex;
    align-items:center;

    gap:12px;
}}

.logo i{{

    font-size:32px;
}}

.logo h2{{

    font-size:16px;
}}

.fecha{{

    text-align:right;

    font-size:12px;
}}

.contenido{{

    flex:1;

    padding:30px;

    text-align:center;
}}

h1{{

    color:#0f172a;

    font-size:42px;

    margin-bottom:10px;
}}

.subtitulo{{

    color:#64748b;

    margin-bottom:35px;

    font-size:17px;
}}

.camara-container{{

    position:relative;

    width:320px;
    height:320px;

    margin:auto;
}}

.camara{{

    width:320px;
    height:320px;

    border-radius:50%;

    overflow:hidden;

    border:5px solid #dbeafe;

    box-shadow:
    0px 0px 20px rgba(0,0,0,0.1);
}}

.camara img{{

    width:100%;
    height:100%;

    object-fit:cover;
}}

.esquina{{

    width:35px;
    height:35px;

    border:4px solid #22c55e;

    position:absolute;

    z-index:10;

    animation:pulse 1s infinite;
}}

@keyframes pulse{{

    0%{{ opacity:1; }}
    50%{{ opacity:0.2; }}
    100%{{ opacity:1; }}
}}

.e1{{

    top:65px;
    left:65px;

    border-right:none;
    border-bottom:none;
}}

.e2{{

    top:65px;
    right:65px;

    border-left:none;
    border-bottom:none;
}}

.e3{{

    bottom:65px;
    left:65px;

    border-right:none;
    border-top:none;
}}

.e4{{

    bottom:65px;
    right:65px;

    border-left:none;
    border-top:none;
}}

.titulo-inst{{

    margin-top:35px;

    font-size:22px;

    font-weight:bold;

    color:#0f172a;
}}

.instrucciones{{

    margin-top:25px;

    display:flex;

    justify-content:space-between;

    gap:15px;
}}

.item{{

    flex:1;
}}

.item i{{

    font-size:35px;

    color:#64748b;

    margin-bottom:12px;
}}

.item p{{

    font-size:13px;

    color:#334155;
}}

.seguridad{{

    margin-top:35px;

    background:#e2e8f0;

    border-radius:20px;

    padding:20px;

    display:flex;

    gap:15px;

    align-items:center;

    text-align:left;
}}

.seguridad i{{

    font-size:35px;

    color:#0f172a;
}}

.seguridad h3{{

    font-size:14px;

    margin-bottom:5px;

    color:#0f172a;
}}

.seguridad p{{

    font-size:12px;

    color:#334155;
}}

.footer{{

    height:80px;

    background:
    linear-gradient(
        90deg,
        #001b4b,
        #0f172a
    );

    display:flex;
    justify-content:center;
    align-items:center;
}}

.footer button{{

    background:none;

    border:none;

    color:white;

    font-size:15px;

    cursor:pointer;
}}

.menu{{

    margin-top:25px;
}}

.menu a{{

    text-decoration:none;

    background:#2563eb;

    color:white;

    padding:15px 30px;

    border-radius:12px;
}}

.acceso{{

    margin-top:30px;

    background:#dcfce7;

    padding:25px;

    border-radius:20px;

    color:#166534;
}}

.acceso h1{{

    color:#166534;

    margin-top:10px;
}}

</style>

</head>

<body>

<div class="kiosco">

    <div class="header">

        <div class="logo">

            <i class="fa-solid fa-graduation-cap"></i>

            <div>

                <h3 style="font-size:12px; color:#cbd5e1;">

                    Instituto Tecnológico de Zitácuaro

                </h3>

                <h2>

                    KIOSCO DE SERVICIOS ESCOLARES

                </h2>

            </div>

        </div>

        <div class="fecha">

            <p>{fecha}</p>
            <p>{hora}</p>

        </div>

    </div>

    <div class="contenido">

        <h1>

            Bienvenido

        </h1>

        <p class="subtitulo">

            Para ingresar, realiza el reconocimiento facial

        </p>

        <div class="camara-container">

            <div class="camara">

                <img src="/video">

            </div>

            <div class="esquina e1"></div>
            <div class="esquina e2"></div>
            <div class="esquina e3"></div>
            <div class="esquina e4"></div>

        </div>

        <script>

        setInterval(() => {{

            fetch('/validar-acceso')
            .then(response => response.json())
            .then(data => {{

                if(data.acceso){{

                    window.location.href="/servicios";

                }}

            }});

        }}, 2000);

        </script>

        <div class="titulo-inst">

            Instrucciones:

        </div>

        <div class="instrucciones">

            <div class="item">

                <i class="fa-regular fa-user"></i>

                <p>

                    Colócate frente
                    a la cámara

                </p>

            </div>

            <div class="item">

                <i class="fa-regular fa-sun"></i>

                <p>

                    Asegúrate de tener
                    buena iluminación

                </p>

            </div>

            <div class="item">

                <i class="fa-regular fa-face-smile"></i>

                <p>

                    Mantén tu rostro
                    dentro del marco

                </p>

            </div>

        </div>

        <div class="seguridad">

            <i class="fa-solid fa-lock"></i>

            <div>

                <h3>

                    Tus datos están protegidos.

                </h3>

                <p>

                    Este sistema garantiza
                    la seguridad y privacidad
                    de tu información.

                </p>

            </div>

        </div>

        {f'''

        <div class="acceso">

            <h2>

                ACCESO AUTORIZADO

            </h2>

            <h1>

                {nombre_usuario}

            </h1>

            <p>

                Bienvenido al sistema

            </p>

        </div>

        ''' if usuario_detectado else '''

        <div class="menu">

            <a href="/registro">

                REGISTRAR ESTUDIANTE

            </a>

        </div>

        '''}

    </div>

    <div class="footer">

        <button onclick="salirSistema()">

            CANCELAR ✕

        </button>

    </div>

</div>

<script>

function salirSistema(){{

    alert("Es un placer atenderlo");

    window.location.href = "about:blank";

}}

</script>

</body>
</html>

    """

    return HTMLResponse(content=html)

# ==========================================
# VALIDAR ACCESO
# ==========================================

@app.get("/validar-acceso")
async def validar_acceso():

    global usuario_detectado

    return {
        "acceso": usuario_detectado
    }

# ==========================================
# SERVICIOS ESCOLARES
# ==========================================

@app.get("/servicios")
async def servicios():

    html = """

<!DOCTYPE html>
<html lang="es">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Servicios Escolares</title>

<link rel="stylesheet"
href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:Arial;
}

body{

    background:
    linear-gradient(
        135deg,
        #0f172a,
        #1e3a8a,
        #312e81
    );

    min-height:100vh;

    display:flex;
    justify-content:center;
    align-items:center;

    padding:20px;
}

.panel{

    width:100%;
    max-width:900px;

    background:white;

    border-radius:25px;

    overflow:hidden;

    box-shadow:
    0px 0px 40px rgba(0,0,0,0.4);
}

.header{

    background:
    linear-gradient(
        90deg,
        #001b4b,
        #0f172a
    );

    color:white;

    padding:30px;

    text-align:center;
}

.contenido{

    padding:40px;
}

.grid{

    display:grid;

    grid-template-columns:1fr 1fr;

    gap:30px;
}

.tarjeta{

    background:#f8fafc;

    border-radius:20px;

    padding:35px;

    text-align:center;

    border:2px solid #e2e8f0;
}

.tarjeta i{

    font-size:70px;

    color:#2563eb;

    margin-bottom:20px;
}

.tarjeta button{

    background:#2563eb;

    color:white;

    border:none;

    padding:15px 25px;

    border-radius:12px;

    cursor:pointer;
}

.footer{

    padding:25px;

    text-align:center;
}

.footer button{

    background:#ef4444;

    color:white;

    border:none;

    padding:15px 30px;

    border-radius:12px;

    cursor:pointer;
}

</style>

</head>

<body>

<div class="panel">

    <div class="header">

        <i class="fa-solid fa-graduation-cap fa-3x"></i>

        <h1>

            Servicios Escolares

        </h1>

        <p>

            Instituto Tecnológico de Zitácuaro

        </p>

    </div>

    <div class="contenido">

        <div class="grid">

            <div class="tarjeta">

                <i class="fa-solid fa-file-lines"></i>

                <h2>

                    Constancia con Calificaciones

                </h2>

                <p>

                    Genera una constancia oficial
                    con historial académico.

                </p>

                <button>

                    GENERAR

                </button>

            </div>

            <div class="tarjeta">

                <i class="fa-solid fa-file"></i>

                <h2>

                    Constancia sin Calificaciones

                </h2>

                <p>

                    Genera constancia oficial
                    sin historial académico.

                </p>

                <button>

                    GENERAR

                </button>

            </div>

        </div>

    </div>

    <div class="footer">

        <button onclick="window.location.href='/'">

            CERRAR SESIÓN

        </button>

    </div>

</div>

</body>
</html>

    """

    return HTMLResponse(content=html)

# ==========================================
# VIDEO
# ==========================================

@app.get("/video")
def video():

    return StreamingResponse(
        generar_video(),
        media_type=
        "multipart/x-mixed-replace; boundary=frame"
    )