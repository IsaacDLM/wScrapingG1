import requests
import json
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def obtener_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        respuesta = requests.get(url, headers=headers)
        respuesta.raise_for_status() 
        return BeautifulSoup(respuesta.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con {url}: {e}")
        return None

def obtener_enlaces_categorias(sopa_principal):
    enlaces_categorias = []
    
    contenedor_menu = sopa_principal.find('ul', class_='menu-list') 
    
    if contenedor_menu:
        etiquetas_a = contenedor_menu.find_all('a', class_='category-link')
        
        for a in etiquetas_a:
            ruta_relativa = a.get('href')
            
            if ruta_relativa and ruta_relativa != "#":
                url_completa = urljoin("https://www.vips.es", ruta_relativa)
                
                if url_completa not in enlaces_categorias:
                    enlaces_categorias.append(url_completa)
                    
    return enlaces_categorias

def extraer_datos_platos(sopa, nombre_categoria):
    menu_categoria = []
    productos = sopa.find_all(class_="product")
    
    for producto in productos:
        etiqueta_titulo = producto.find('h2')
        etiqueta_desc = producto.find('p')
        
        titulo = etiqueta_titulo.text.strip() if etiqueta_titulo else "Sin nombre"
        descripcion = etiqueta_desc.text.strip() if etiqueta_desc else "Sin descripción"
        
        datos_plato = {
            "categoria": nombre_categoria,
            "plato": titulo,
            "descripcion": descripcion
        }
        menu_categoria.append(datos_plato)
        
    return menu_categoria

if __name__ == "__main__":
    url_base = "https://www.vips.es/carta"
    print("Iniciando el bot explorador...")
    
    sopa_inicio = obtener_html(url_base)
    
    if sopa_inicio:
        enlaces = obtener_enlaces_categorias(sopa_inicio)
        print(f"¡Se han encontrado {len(enlaces)} categorías para explorar!\n")
        
        carta_completa = []
        
        for enlace in enlaces:
            print(f"-> Explorando categoría: {enlace}")
            sopa_categoria = obtener_html(enlace)
            
            if sopa_categoria:
                nombre_cat = enlace.split('/')[-1].replace('-', ' ').capitalize()
                
                platos_extraidos = extraer_datos_platos(sopa_categoria, nombre_cat)
                carta_completa.extend(platos_extraidos)
                
                time.sleep(2)
        
        print("\nGuardando la carta completa en menu_vips.json...")
        with open('menu_vips.json', 'w', encoding='utf-8') as archivo:
            json.dump(carta_completa, archivo, ensure_ascii=False, indent=4)
            
        print(f"¡Éxito! Se han guardado un total de {len(carta_completa)} platos.")