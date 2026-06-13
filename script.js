*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    font-family:Arial, Helvetica, sans-serif;
    background:#0f172a;
    color:white;
    min-height:100vh;
}

.contenedor{
    display:flex;
    min-height:100vh;
}

/* PANEL IZQUIERDO */

.panel-izquierdo{

    width:300px;

    background:#111827;

    padding:30px;

    display:flex;

    flex-direction:column;

    gap:20px;

    justify-content:center;
}

.panel-izquierdo h1{

    text-align:center;

    margin-bottom:30px;

    font-size:2rem;
}

/* PANEL DERECHO */

.panel-derecho{

    flex:1;

    display:flex;

    flex-direction:column;

    justify-content:center;

    align-items:center;

    padding:20px;
}

.panel-derecho h2{

    margin-bottom:20px;

    text-align:center;
}

/* BOTONES */

button{

    width:100%;

    padding:15px;

    border:none;

    border-radius:12px;

    background:#2563eb;

    color:white;

    font-size:18px;

    cursor:pointer;

    transition:0.3s;
}

button:hover{

    background:#1d4ed8;

    transform:translateY(-2px);
}

/* CAMARA */

.camara{

    width:100%;

    max-width:800px;

    display:flex;

    justify-content:center;

    align-items:center;
}

.camara img{

    width:100%;

    height:auto;

    border-radius:20px;

    border:5px solid white;

    display:block;
}

/* TABLETS */

@media (max-width:1024px){

    .panel-izquierdo{

        width:250px;
    }

    button{

        font-size:16px;
    }
}

/* CELULARES */

@media (max-width:768px){

    .contenedor{

        flex-direction:column;
    }

    .panel-izquierdo{

        width:100%;

        padding:20px;
    }

    .panel-derecho{

        padding:15px;
    }

    .panel-izquierdo h1{

        font-size:1.8rem;
    }

    button{

        font-size:16px;

        padding:14px;
    }
}

/* CELULARES PEQUEÑOS */

@media (max-width:480px){

    .panel-izquierdo h1{

        font-size:1.5rem;
    }

    .panel-derecho h2{

        font-size:1.2rem;
    }

    button{

        font-size:14px;

        padding:12px;
    }
}