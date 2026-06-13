from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

# Importamos las rutas de inicio (las crearemos en el siguiente paso)
# from routers import inicio 

app = FastAPI(
    title="Kiosco Inteligente",
    version="1.0"
)

# Configuración vital: Monta la carpeta 'static' para que el CSS no se rompa
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuramos las plantillas HTML
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def inicio(request: Request):
    # Esto renderiza tu archivo templates/index.html
    return templates.TemplateResponse("index.html", {"request": request})

# Aquí irán tus futuras APIs de reconocimiento
@app.get("/reconocimiento")
async def reconocimiento():
    return {"mensaje": "Iniciando cámara para reconocimiento..."}
