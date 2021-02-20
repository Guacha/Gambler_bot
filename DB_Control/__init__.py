import firebase_admin
from firebase_admin import firestore
from google.cloud.firestore_v1.client import Client

# Variable que contiene la instancia de Firestore, siempre retorna esto si ya existe
__db = None


def initialise_database() -> Client:
    """Obtener un cliente de la aplicación de Google Cloud que le permite al bot interactuar con
    Firebase, en caso de que el cliente ya haya sido creado, retornará la misma instancia del cliente,
    sin inicializar una nueva.

    Returns:
        google.cloud.firestore_v1.client.Client: El cliente Google Cloud de Firestore
    """    
    global __db
    if __db is None:
        # Inicializar Firebase con Variables ENV, consultar configuración de entorno de desarrollo
        print("Inicializando módulo Firestore...")
        app = firebase_admin.initialize_app()
        __db = firestore.client()
        print("Credenciales validadas, inicializando cliente...")
    
        # Inicialización terminada con éxito
        print("Cliente inicializado satisfactoriamente, conexión a Firebase exitosa!")
        return __db
    
    else:
        return __db
