# Plataforma Inteligente de Optimización Operacional - NexusCore Systems

Este proyecto consiste en una aplicación web interactiva desarrollada para la toma de decisiones estratégicas de infraestructura y mercadeo en la empresa **NexusCore Systems**.

La plataforma permite resolver complejos problemas de optimización cuantitativa mediante el uso de algoritmos basados en **Programación Dinámica** y **Optimización No Lineal** desarrollados desde cero en el backend (sin librerías externas de optimización). Adicionalmente, cuenta con un análisis cualitativo y estratégico generado por la inteligencia artificial de **Groq** (simulando el rol de un Director de Tecnología - CTO) y permite la exportación nativa de un reporte técnico formal en formato **PDF**.

---

## 📁 Estructura del Proyecto

El sistema está estructurado bajo una arquitectura cliente-servidor moderna que separa el backend y el frontend, manteniendo el paradigma de **Programación Orientada a Objetos (POO)** en todas las capas del backend:

```
NEXUSCORE SYSTEMS/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # Punto de entrada de FastAPI y configuración de CORS
│   │   ├── config.py                # Carga de variables de entorno y llaves de API (Groq)
│   │   │
│   │   ├── algorithms/              # Motor Algorítmico (Lógica de optimización pura en POO)
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # Clase base abstracta de optimización (BaseOptimizer)
│   │   │   ├── knapsack.py          # Sub-problema A: Mochila (Carga de Servidores)
│   │   │   ├── stage_coach.py       # Sub-problema B: Grafo por Etapas (Ruta Crítica)
│   │   │   └── non_linear.py        # Parte II: Optimización No Lineal (Marketing)
│   │   │
│   │   ├── services/                # Servicios de integración externa
│   │   │   ├── __init__.py
│   │   │   ├── groq_service.py      # Cliente HTTP asíncrono para la API de Groq
│   │   │   └── pdf_service.py       # Generador de reportes PDF formales (usando ReportLab)
│   │   │
│   │   └── routers/                 # Enrutadores de la API (End-points)
│   │       ├── __init__.py
│   │       ├── optimization.py      # Endpoints para ejecutar los algoritmos matemáticos
│   │       └── ai.py                # Endpoints para solicitar análisis estratégico de Groq
│   │
│   ├── requirements.txt             # Dependencias del backend (FastAPI, ReportLab, etc.)
│   └── run.py                       # Script de arranque del servidor Uvicorn
│
├── frontend/
│   ├── index.html                   # Interfaz de usuario SPA (Dashboard premium)
│   ├── css/
│   │   └── style.css                # Estilos personalizados (Modo oscuro, cristales y glows)
│   └── js/
│       ├── api.js                   # Cliente Fetch para consumir la API de FastAPI
│       ├── ui.js                    # Manipulación dinámica del DOM y dibujo de grafos
│       └── app.js                   # Orquestador general del cliente y datos por defecto
│
└── Proyecto Metodos Cuantitativos.pdf
```

---

## ⚙️ Funcionalidades de cada Módulo

### 1. Motor Algorítmico (`backend/app/algorithms/`)
Cada algoritmo de resolución está encapsulado en una clase orientada a objetos que hereda de una clase abstracta común `BaseOptimizer` en `base.py`.
- **Carga de Servidores (`knapsack.py`)**: Utiliza programación dinámica unidimensional/bidimensional para resolver el problema de la mochila 0/1. Su fin es maximizar el valor de estabilidad acumulado desplegando un conjunto de microservicios críticos en un servidor maestro con capacidad de RAM limitada (por defecto 16 GB). Genera la matriz paso a paso completa.
- **Distribución de Datos (`stage_coach.py`)**: Resuelve el problema de la ruta crítica de menor latencia (en milisegundos) desde un servidor principal (Nodo A) hasta los servidores de respaldo regionales (Nodo J). Aplica programación dinámica hacia atrás (Backward) estructurada por etapas, devolviendo las tablas de decisión $f_n(s)$ y decisiones óptimas de cada paso.
- **Optimización de Marketing No Lineal (`non_linear.py`)**: Resuelve la asignación del presupuesto mensual de marketing ($B$, máximo $10,000) distribuido entre Campañas de Creadores de Contenido ($x_1$) y Anuncios Programáticos ($x_2$). La función no lineal es:
  $$\text{Maximizar } f(x_1, x_2) = c_1 x_1 + c_2 x_2 - a_1 x_1^2 - a_2 x_2^2$$
  Sujeto a:
  $$x_1 + x_2 \le B, \quad x_1, x_2 \ge 0$$
  Implementa un algoritmo de **Búsqueda por Bisección / Sección Áurea** y **Búsqueda de Malla Fina** sin requerir optimizadores externos.

### 2. Módulo de Integración con IA (`backend/app/services/groq_service.py`)
- Se conecta de forma asíncrona a la API de Groq usando el modelo de alta velocidad `llama3-8b-8192`.
- Formatea un prompt estructurado para que el LLM adopte el rol de un **Chief Technology Officer (CTO)** y evalúe la viabilidad de los resultados cuantitativos: latencia competitiva, riesgos técnicos de la memoria y el ROI de marketing digital frente a retornos decrecientes.
- Retorna las conclusiones estructuradas y formateadas en Markdown bajo el título "Conclusiones Estratégicas del Asistente de IA".

### 3. Módulo de Exportación (`backend/app/services/pdf_service.py`)
- Genera de manera nativa en el servidor un archivo PDF estructurado utilizando la librería **ReportLab**.
- Incorpora encabezados profesionales de NexusCore Systems, resúmenes matemáticos, las tablas paso a paso detalladas de programación dinámica y el análisis estratégico del CTO de IA.

### 4. Interfaz de Usuario (`frontend/`)
- Panel de control de una sola página (SPA) responsivo con estética de lujo (diseño oscuro, sombras de neón, tarjetas de cristal con difuminado).
- Entrada de datos interactiva: formularios en tiempo real precargados con los datos del problema académico para realizar pruebas de forma inmediata.
- Renderizado interactivo: visualiza tablas completas de cálculos paso a paso y dibuja el grafo de etapas de la red marcando de forma clara la ruta crítica de menor latencia.
- Descarga directa de reportes a PDF en un clic.

---

## 🚦 Guía para Puesta en Marcha

### Prerrequisitos
- Python 3.8 o superior instalado en el equipo.

### Pasos de Instalación y Ejecución

1. **Instalar Dependencias del Backend**:
   Desde la carpeta `backend/`, instale los paquetes de Python:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configurar la Llave de API de Groq**:
   Cree un archivo `.env` en la carpeta `backend/` con el siguiente contenido:
   ```env
   GROQ_API_KEY=tu_clave_de_api_aqui
   ```

3. **Iniciar el Servidor Backend**:
   Ejecute el script de arranque en la raíz del backend:
   ```bash
   python run.py
   ```
   El backend se levantará en `http://127.0.0.1:8000`. Puede abrir `http://127.0.0.1:8000/docs` para ver la interfaz interactiva de Swagger UI.

4. **Abrir el Frontend**:
   Simplemente abra el archivo `frontend/index.html` en su navegador web favorito. La interfaz se conectará automáticamente con el backend local.

---

## 🧪 Pruebas Unitarias

Para comprobar que los motores matemáticos funcionan correctamente, ejecute el conjunto de pruebas unitarias con:
```bash
pytest backend/tests/
```
