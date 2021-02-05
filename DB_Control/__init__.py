from datetime import datetime

import firebase_admin
from firebase_admin import firestore

# Inicializar Firebase con Variables ENV, consultar configuración de entorno de desarrollo
print("Inicializando módulo Firestore...")
app = firebase_admin.initialize_app()

print("Credenciales validadas, inicializando cliente...")
db = firestore.client()

# Inicialización terminada con éxito
print("Cliente inicializado satisfactoriamente, conexión a Firebase exitosa!")
