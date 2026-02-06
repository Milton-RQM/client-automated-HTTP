# Proyecto – Pipeline de Ingestión HTTP, KPIs y ETL con Pentaho

## Resumen general del proyecto

Este proyecto implementa un **pipeline de datos completo** que simula un escenario real de **ingestión de datos vía HTTP**, **procesamiento de métricas (KPIs)** y **carga mediante procesos ETL**, utilizando herramientas y patrones comunes en proyectos de **Data Engineering**.

El objetivo principal es demostrar la capacidad de:
- Consumir endpoints HTTP y APIs
- Simular comportamientos típicos de web scraping
- Generar datos técnicos de forma controlada
- Procesar métricas operativas
- Cargar información mediante Pentaho Data Integration
- Mantener una estructura modular, clara y reproducible

El proyecto está dividido en **módulos independientes**, cada uno con una responsabilidad clara dentro del flujo de datos.

---

## Índice de contenidos

1. [Arquitectura general del proyecto](#arquitectura-general-del-proyecto)
2. [Módulo 01 – Ingestión HTTP](#módulo-01--ingestión-http-simulación-de-api-y-web-scraping)
3. Módulo 02 – Simulación de logs técnicos
4. Módulo 03 – Procesamiento de KPIs
5. Módulo 04 – ETL con Pentaho y SQLite
6. Módulo 05 – Reportes y visualización
7. Tecnologías utilizadas
8. Ejecución del proyecto

---

## Arquitectura general del proyecto

El pipeline sigue una arquitectura secuencial y modular:

1. **Ingestión HTTP**  
   Simulación de consumo de APIs y escenarios de web scraping.
2. **Simulación de logs técnicos**  
   Generación de datos sintéticos representando llamadas HTTP.
3. **Procesamiento de KPIs**  
   Cálculo de métricas operativas por endpoint y día.
4. **ETL con Pentaho**  
   Carga de datos procesados en una base de datos SQLite.
5. **Reporte final**  
   Visualización de métricas en formato HTML.

Cada módulo puede ejecutarse de manera independiente, facilitando pruebas, mantenimiento y extensión del proyecto.

---

## Módulo 01 – Ingestión HTTP (Simulación de API y Web Scraping)

### Descripción general

Este módulo simula escenarios comunes de **ingestión de datos vía HTTP**, típicos en procesos de **web scraping** y **consumo de APIs**.  
El objetivo **no es extraer datos de un sitio web real**, sino validar el manejo de diferentes comportamientos HTTP utilizando una API de pruebas controlada.

Para este fin se utiliza **httpbin.org**, un servicio diseñado para probar clientes HTTP y simular respuestas reales como autenticación, manejo de sesiones, redirecciones, errores y respuestas en múltiples formatos.

---

### Objetivos del módulo

- Simular procesos de ingesta de datos vía HTTP
- Validar autenticación y manejo de sesiones
- Extraer datos en distintos formatos (JSON, XML y HTML)
- Manejar errores HTTP comunes (403)
- Seguir redirecciones correctamente
- Mantener cada escenario desacoplado y fácil de probar

---

### Escenarios implementados

| Escenario | Descripción |
|---------|------------|
| Autenticación básica | Simulación de HTTP Basic Authentication |
| Cookies y sesiones | Persistencia de sesión entre peticiones |
| Extracción JSON | Consumo y almacenamiento de respuestas JSON |
| Extracción XML | Parseo y almacenamiento de respuestas XML |
| Extracción HTML | Extracción de contenido desde HTML |
| Envío de formularios | Simulación de peticiones POST |
| Manejo de error 403 | Detección de accesos denegados |
| Manejo de redirecciones | Seguimiento correcto de redirecciones HTTP |

---

### Estructura del módulo

```text
01_ingestion_http/
│
├─ common/
│   ├─ __init__.py
│   └─ http_session.py
│
├─ auth/
│   ├─ __init__.py
│   └─ basic_auth.py
│
├─ cookies/
│   ├─ __init__.py
│   └─ cookies_session.py
│
├─ extraction/
│   ├─ __init__.py
│   ├─ get_json.py
│   ├─ get_xml.py
│   └─ get_html.py
│
├─ forms/
│   ├─ __init__.py
│   └─ post_form.py
│
├─ errors/
│   ├─ __init__.py
│   └─ handle_403.py
│
├─ redirects/
│   ├─ __init__.py
│   └─ follow_redirect.py
│
├─ outputs/
│   ├─ json/
│   ├─ xml/
│   └─ html/
│
└─ run_all.py
