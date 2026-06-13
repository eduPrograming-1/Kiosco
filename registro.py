from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, StreamingResponse

import cv2
import os

router = APIRouter()

# ==========================================
# CREAR CARPETA
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
# VIDEO STREAM
# ==========================================

def generar_video():

    while True:

        success, frame = camara.read()

        if not success:
            break

        # espejo
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

        # ======================================
        # RECTANGULO FACIAL
        # ======================================

        for (x, y, w, h) in rostros:

            cv2.rectangle(
                frame,
                (x,y),
                (x+w,y+h),
                (0,255,0),
                3
            )

            cv2.putText(
                frame,
                "ROSTRO DETECTADO",
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,0),
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
# VIDEO REGISTRO
# ==========================================

@router.get("/video_registro")
def video_registro():

    return StreamingResponse(
        generar_video(),
        media_type=
        "multipart/x-mixed-replace; boundary=frame"
    )

# ==========================================
# FORMULARIO
# ==========================================

@router.get("/registro")
async def formulario_registro():

    html = """

<!DOCTYPE html>
<html lang="es">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Registro de Estudiantes</title>

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

.formulario{

    width:100%;
    max-width:750px;

    background:white;

    border-radius:25px;

    overflow:hidden;

    box-shadow:
    0px 0px 35px rgba(0,0,0,0.4);
}

.header{

    background:
    linear-gradient(
        90deg,
        #001b4b,
        #0f172a
    );

    color:white;

    padding:25px;

    text-align:center;
}

.header i{

    font-size:55px;

    margin-bottom:10px;
}

.header h1{

    margin-bottom:10px;
}

.contenido{

    padding:30px;
}

/* CAMARA */

.camara{

    width:320px;
    height:320px;

    margin:auto;

    border-radius:20px;

    overflow:hidden;

    border:5px solid #2563eb;

    margin-bottom:30px;

    box-shadow:
    0px 0px 25px rgba(37,99,235,0.3);
}

.camara img{

    width:100%;
    height:100%;

    object-fit:cover;
}

/* GRID */

.grid{

    display:grid;

    grid-template-columns:1fr 1fr;

    gap:20px;
}

.campo{

    display:flex;
    flex-direction:column;
}

.campo label{

    margin-bottom:8px;

    font-weight:bold;

    color:#0f172a;
}

.campo input,
.campo select{

    padding:14px;

    border-radius:12px;

    border:1px solid #cbd5e1;

    outline:none;

    transition:0.3s;
}

.campo input:focus,
.campo select:focus{

    border-color:#2563eb;

    box-shadow:
    0px 0px 10px rgba(37,99,235,0.3);
}

.full{

    grid-column:1/3;
}

/* BOTONES */

.botones{

    margin-top:30px;

    display:flex;

    gap:20px;
}

.btn{

    flex:1;

    padding:16px;

    border:none;

    border-radius:14px;

    cursor:pointer;

    font-size:16px;

    transition:0.3s;
}

.guardar{

    background:#2563eb;

    color:white;
}

.guardar:hover{

    background:#1d4ed8;
}

.cancelar{

    background:#e2e8f0;

    color:#0f172a;
}

.cancelar:hover{

    background:#cbd5e1;
}

/* RESPONSIVE */

@media(max-width:768px){

    .grid{

        grid-template-columns:1fr;
    }

    .full{

        grid-column:auto;
    }

    .botones{

        flex-direction:column;
    }

    .camara{

        width:100%;
        height:280px;
    }
}

</style>

</head>

<body>

<div class="formulario">

    <div class="header">

        <i class="fa-solid fa-user-plus"></i>

        <h1>

            Registro de Estudiante

        </h1>

        <p>

            Instituto Tecnológico de Zitácuaro

        </p>

    </div>

    <div class="contenido">

        <!-- CAMARA -->

        <div class="camara">

            <img src="/video_registro">

        </div>

        <!-- FORMULARIO -->

        <form action="/guardar-registro"
        method="post">

            <div class="grid">

                <div class="campo">

                    <label>
                        Apellido Paterno
                    </label>

                    <input type="text"
                    name="apellido_paterno"
                    required>

                </div>

                <div class="campo">

                    <label>
                        Apellido Materno
                    </label>

                    <input type="text"
                    name="apellido_materno"
                    required>

                </div>

                <div class="campo full">

                    <label>
                        Nombre
                    </label>

                    <input type="text"
                    name="nombre"
                    required>

                </div>

                <div class="campo">

                    <label>
                        Número de Control
                    </label>

                    <input type="text"
                    name="control"
                    required>

                </div>

                <div class="campo">

                    <label>
                        Carrera
                    </label>

                    <input type="text"
                    name="carrera"
                    required>

                </div>

                <div class="campo">

                    <label>
                        Semestre
                    </label>

                    <select name="semestre">

                        <option>1</option>
                        <option>2</option>
                        <option>3</option>
                        <option>4</option>
                        <option>5</option>
                        <option>6</option>
                        <option>7</option>
                        <option>8</option>
                        <option>9</option>

                    </select>

                </div>

                <div class="campo">

                    <label>
                        Teléfono
                    </label>

                    <input type="text"
                    name="telefono"
                    required>

                </div>

                <div class="campo full">

                    <label>
                        Correo Electrónico
                    </label>

                    <input type="email"
                    name="correo"
                    required>

                </div>

            </div>

            <div class="botones">

                <button class="btn guardar">

                    CAPTURAR Y GUARDAR

                </button>

                <button type="button"
                class="btn cancelar"
                onclick="window.location.href='/'">

                    CANCELAR

                </button>

            </div>

        </form>

    </div>

</div>

</body>
</html>

    """

    return HTMLResponse(content=html)

# ==========================================
# GUARDAR REGISTRO
# ==========================================

@router.post("/guardar-registro")
async def guardar_registro(

    apellido_paterno:str = Form(...),
    apellido_materno:str = Form(...),
    nombre:str = Form(...),
    control:str = Form(...),
    carrera:str = Form(...),
    semestre:str = Form(...),
    correo:str = Form(...),
    telefono:str = Form(...)

):

    # ======================================
    # CAPTURAR FOTO
    # ======================================

    success, frame = camara.read()

    if success:

        frame = cv2.flip(frame, 1)

        nombre_imagen = f"fotos/{control}.jpg"

        cv2.imwrite(
            nombre_imagen,
            frame
        )

    # ======================================
    # MOSTRAR DATOS
    # ======================================

    print("===== ESTUDIANTE REGISTRADO =====")

    print(apellido_paterno)
    print(apellido_materno)
    print(nombre)
    print(control)
    print(carrera)
    print(semestre)
    print(correo)
    print(telefono)

    return HTMLResponse("""

    <script>

        alert("Estudiante registrado correctamente");

        window.location.href="/";

    </script>

    """)