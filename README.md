```markdown
# Sistema de Información para la Gestión del Aprovisionamiento — Florería Sarai

## Propósito
Automatizar y optimizar la planificación de compras para arreglos florales personalizados bajo el modelo de pedidos anticipados en Florería Sarai, eliminando los cálculos manuales, reduciendo compras urgentes y minimizando las mermas de productos perecibles.

## Características principales
* **Lenguaje y lógica:** Desarrollado en Python 3.x (con manejo de fechas mediante `datetime`).
* **Interfaz interactiva local:** Aplicación web desarrollada con Streamlit, accesible desde un navegador web.
* **Procesamiento y agrupación:** Organización, consolidación de requerimientos y preparación de datos analíticos con Pandas.
* **Almacenamiento local (Edge Computing):** Persistencia en archivos JSON locales (`pedidos.json` para los pedidos y `fournisseur.json` para proveedores, recetas, *lead time* y vida útil en tienda / *shelf life*).

## Funcionamiento de la aplicación
1. **Pestaña 1 — Registro y Pedidos:** Permite registrar pedidos de clientes (nombre, fecha requerida de entrega, bouquet predefinido o composición ajustable) y validar la viabilidad de los plazos antes de guardar en `pedidos.json`.
2. **Pestaña 2 — Órdenes de Compra Consolidadas:** Aplica planificación retroactiva (*backward scheduling*) considerando la fecha de preparación, la vida útil en tienda (*shelf life*) y el tiempo de entrega del proveedor (*lead time*), consolidando compras por proveedor y fecha con alertas visuales.
3. **Pestaña 3 — Analítica BI:** Muestra gráficos de demanda total consolidada por variedad floral y distribución de compras por proveedor para apoyar la toma de decisiones.

## Cómo descargar y ejecutar el proyecto

### 1. Descargar los archivos
* En la página principal del repositorio en GitHub, hagan clic en el botón verde **`<> Code`** y seleccionen **`Download ZIP`**.
* Descompriman el archivo ZIP en una carpeta de su computadora (por ejemplo, en el Escritorio o en `Documentos\Floreria-Sarai`).
* Verifiquen que el script principal de Python (`app.py`) y los archivos JSON (`pedidos.json`, `fournisseur.json`) estén en la misma carpeta.

### 2. Abrir la terminal e instalar dependencias
* **En Windows:** Abran el **Símbolo del sistema** (*CMD*) o **PowerShell** y naveguen hasta la carpeta del proyecto usando `cd`:
  ```bash
  cd "C:\ruta\a\su\carpeta\Floreria-Sarai"

```

* **En macOS / Linux:** Abran la **Terminal** y entren en la carpeta del proyecto:
```bash
cd /ruta/a/su/carpeta/Floreria-Sarai

```


* Instalen las librerías requeridas (`streamlit` y `pandas`):
```bash
pip install streamlit pandas

```


*(Si el repositorio incluye un archivo `requirements.txt`, también pueden ejecutar `pip install -r requirements.txt`.)*

### 3. Ejecutar la aplicación

Desde la misma terminal (ubicada dentro de la carpeta del proyecto), ejecuten:

```bash
streamlit run app.py

```


* Al ejecutarse, se abrirá automáticamente su navegador web en la dirección local (por lo general `http://localhost:8501`).
* Para detener el servidor local, vuelvan a la terminal y presionen **`Ctrl + C`**.

```

```
