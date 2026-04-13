import requests
import json
from bs4 import BeautifulSoup

def obtener_html_carta():
    url = "https://www.vips.es/carta"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Haciendo petición a: {url}...")
    try:
        respuesta = requests.get(url, headers=headers)
        respuesta.raise_for_status() 
        print("¡Conexión exitosa!\n")
        return BeautifulSoup(respuesta.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la web: {e}")
        return None

def extraer_datos_platos(sopa):
    # Creamos una lista vacía para guardar todos nuestros platos
    menu_vips = []
    
    # 1. Buscamos TODOS los contenedores con la clase "product"
    # No nos importa si son divs, articles o lis, solo que tengan esa clase
    productos = sopa.find_all(class_="product")
    
    print(f"Se han encontrado {len(productos)} productos en la página.\n")
    
    # 2. Iteramos sobre cada "caja" de producto
    for producto in productos:
        # Buscamos el h2 dentro de esta caja específica
        etiqueta_titulo = producto.find('h2')
        # Buscamos el p dentro de esta caja específica
        etiqueta_desc = producto.find('p')
        
        # 3. Extraemos el texto solo si la etiqueta existe (nuestra regla de oro)
        # Usamos .strip() para limpiar espacios en blanco extra o saltos de línea molestos
        titulo = etiqueta_titulo.text.strip() if etiqueta_titulo else "Sin nombre"
        descripcion = etiqueta_desc.text.strip() if etiqueta_desc else "Sin descripción"
        
        # 4. Guardamos la información estructurada en un diccionario
        datos_plato = {
            "plato": titulo,
            "descripcion": descripcion
        }
        
        menu_vips.append(datos_plato)
        
    return menu_vips

# Punto de entrada del script
if __name__ == "__main__":
    sopa = obtener_html_carta()
    
    if sopa:
        # Ejecutamos nuestra función de extracción
        mi_carta = extraer_datos_platos(sopa)
        
        # --- NUEVO: GUARDAR EN JSON ---
        print("\nGuardando los datos en menu_vips.json...")
        
        # Abrimos (o creamos) un archivo llamado 'menu_vips.json' en modo escritura ('w')
        # Usamos utf-8 para que los acentos y las eñes se guarden perfectamente
        with open('menu_vips.json', 'w', encoding='utf-8') as archivo:
            # Volcamos nuestra lista de diccionarios al archivo
            # indent=4 lo formatea bonito para que sea fácil de leer por un humano
            json.dump(mi_carta, archivo, ensure_ascii=False, indent=4)
            
        print("¡Proceso terminado con éxito! Revisa tu carpeta del proyecto.")