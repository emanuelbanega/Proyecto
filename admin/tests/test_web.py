from http import client
from web import create_app

app = create_app()
app.testing = True
client = app.test_client()

def test_home():
    response = client.get("/")
    assert b"<h1>Inicio</h1>" in response.data

# def test_perfil():
#     response = client.get("/perfil")
#     assert b"<h1>perfil</h1>" in response.data

# def test_estado_societario():
#     response = client.get("/estado_societario")
#     assert b"<h1>Estado Societario</h1>" in response.data