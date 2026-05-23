# Plan de Implementación: Sistema Inteligente de Optimización Operacional (NexusCore Systems)

Este documento detalla la planificación arquitectónica, la estructura de módulos, las metodologías algorítmicas y la hoja de ruta para el desarrollo de la plataforma web interna de toma de decisiones de **NexusCore Systems**.

El proyecto consiste en una aplicación web interactiva que resolverá algoritmos cuantitativos de optimización por medio de programación dinámica y optimización no lineal (desarrollados de forma nativa sin librerías externas), se conectará asíncronamente con la API de Groq para obtener un análisis cualitativo y estratégico tipo CTO, y generará reportes profesionales consolidados en formato PDF.

---

## 📋 Estructura de Módulos Propuesta (Arquitectura del Proyecto)

Para cumplir con el requerimiento de programación orientada a objetos (POO), modularidad y separación de responsabilidades, estructuraremos el proyecto en un backend con **Python (FastAPI)** y un frontend moderno con **HTML5, CSS3 (Vanilla con diseño premium) y JavaScript**.

La estructura de directorios y archivos dentro de `c:\Users\Valentina\Desktop\NEXUSCORE SYSTEMS` será la siguiente:

```
NEXUSCORE SYSTEMS/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # Punto de entrada de FastAPI y configuración de CORS
│   │   ├── config.py                # Variables de entorno y llaves de API (Groq)
│   │   │
│   │   ├── algorithms/              # Motor Algorítmico (Lógica de optimización pura en POO)
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # Clase base abstracta de optimización
│   │   │   ├── knapsack.py          # Sub-problema A: Mochila (Carga de Servidores)
│   │   │   ├── stage_coach.py       # Sub-problema B: Grafo por Etapas (Ruta Crítica)
│   │   │   └── non_linear.py        # Parte II: Optimización No Lineal (Marketing)
│   │   │
│   │   ├── services/                # Servicios de integración externa
│   │   │   ├── __init__.py
│   │   │   ├── groq_service.py      # Cliente HTTP asíncrono para la API de Groq
│   │   │   └── pdf_service.py       # Generador nativo de reportes PDF formales
│   │   │
│   │   └── routers/                 # Controladores de la API (End-points)
│   │       ├── __init__.py
│   │       ├── optimization.py      # Endpoints para ejecutar los tres algoritmos
│   │       └── ai.py                # Endpoints para invocar el análisis de Groq
│   │
│   ├── requirements.txt             # Dependencias (fastapi, uvicorn, httpx, reportlab, etc.)
│   └── run.py                       # Script de arranque del servidor backend
│
├── frontend/
│   ├── index.html                   # Interfaz de usuario unificada (Dashboard premium)
│   ├── css/
│   │   └── style.css                # Estilos modernos (Glow, cristalografía, animaciones, dark mode)
│   └── js/
│       ├── api.js                   # Módulo de comunicación con el backend (Fetch API)
│       ├── ui.js                    # Manipulación del DOM, renderizado de grafos y tablas dinámicas
│       └── app.js                   # Orquestador del flujo del cliente
│
└── Proyecto Metodos Cuantitativos.pdf
```

---

## 🛠️ Detalle de Componentes y Funcionalidades

### 1. Motor Algorítmico (Backend - POO Puro)

Cada algoritmo heredará de una clase base abstracta `BaseOptimizer` para mantener una arquitectura orientada a objetos consistente y limpia.

#### A. Módulo de Carga de Servidores (`knapsack.py`)
- **Problema**: Knapsack (Mochila) 0/1 para maximizar la estabilidad de microservicios con un límite de 16 GB de RAM (configurable).
- **Entradas**: Arreglo de objetos `Microservicio` (Nombre, RAM, Valor de Prioridad) y capacidad máxima del servidor.
- **Lógica**: Tabla de programación dinámica bidimensional.
- **Salida**: Estabilidad total máxima, lista de microservicios seleccionados para el despliegue y la matriz paso a paso para el reporte.

#### B. Módulo de Grafo por Etapas (`stage_coach.py`)
- **Problema**: Encontrar la ruta de menor latencia acumulada desde el nodo inicial (A) al final (J) mediante programación dinámica hacia atrás (Backward).
- **Entradas**: Lista de etapas, nodos de cada etapa y latencias de conexión (aristas con costos).
- **Lógica**: Algoritmo recursivo backward estructurado por etapas.
- **Salida**: Ruta crítica óptima (ej. `A -> C -> E -> H -> J`), costo mínimo acumulado de latencia y la tabla de decisiones de cada etapa con $f_n(s)$ y $d_n^*(s)$.

#### C. Módulo de Optimización de Marketing No Lineal (`non_linear.py`)
- **Problema**: Maximizar $f(x_1, x_2) = c_1 x_1 + c_2 x_2 - a_1 x_1^2 - a_2 x_2^2$ sujeto a $x_1 + x_2 \le B$ y $x_1, x_2 \ge 0$.
- **Entradas**: Presupuesto límite $B$ (default 10, que representa $10,000) y coeficientes de la función.
- **Lógica**: Como no se permiten optimizadores externos, implementaremos un resolvedor de **Búsqueda por Bisección / Búsqueda de Sección Áurea** o una **Búsqueda Fina en Malla** en el intervalo $[0, B]$ para encontrar la distribución óptima exacta de $x_1$ y $x_2 = B - x_1$. Este método es 100% robusto y no depende de librerías externas de optimización.
- **Salida**: Asignación óptima de presupuesto para $x_1$ (Creadores de Contenido) y $x_2$ (Anuncios Programáticos), junto con el retorno estimado (número de usuarios adquiridos).

---

### 2. Módulo de Integración con IA (Groq API) (`groq_service.py`)

- **Objetivo**: Conexión asíncrona mediante un cliente HTTP para enviar los resultados matemáticos y recibir conclusiones estratégicas de negocio.
- **Configuración**: Conexión al endpoint de Groq usando el modelo rápido `llama3-8b-8192`.
- **Estructura del Prompt (CTO Persona)**:
  ```
  Actúa como el Chief Technology Officer (CTO) de NexusCore Systems.
  Analiza críticamente la viabilidad de negocio de los siguientes resultados de optimización cuantitativa:
  
  1. CARGA DE SERVIDORES (PROGRAMACIÓN DINÁMICA):
     - Microservicios seleccionados: [Lista]
     - RAM consumida: [Valor] GB / [Límite] GB
     - Estabilidad obtenida: [Valor]
     
  2. RED DE DISTRIBUCIÓN (RUTA MÍNIMA):
     - Ruta crítica: [Ruta]
     - Latencia total: [Valor] ms
     
  3. PRESUPUESTO DE MARKETING (OPTIMIZACIÓN NO LINEAL):
     - Presupuesto Creadores (x1): $[Valor]
     - Presupuesto Anuncios (x2): $[Valor]
     - Retorno estimado: [Valor] miles de usuarios
     
  Evalúa de forma profesional:
  - Si la latencia obtenida es competitiva en la industria de desarrollo de software actual.
  - El riesgo técnico del esquema de memoria y estabilidad de los servidores seleccionado.
  - La eficiencia del retorno de inversión en marketing digital ante los rendimientos decrecientes y saturación del mercado.
  ```

---

### 3. Módulo de Exportación a PDF (`pdf_service.py`)

- **Objetivo**: Generar de forma nativa en el backend un documento PDF con un formato altamente profesional, formal y listo para presentación corporativa.
- **Librería sugerida**: `reportlab` (biblioteca estándar y poderosa de Python para generar archivos PDF estructurados directamente desde código binario).
- **Contenido del PDF**:
  - Encabezado institucional de **NexusCore Systems**.
  - Resumen ejecutivo de los tres problemas de optimización.
  - Tablas completas y detalladas de los cálculos matemáticos (incluyendo las matrices de decisión paso a paso para programación dinámica).
  - Sección formal para las "Conclusiones Estratégicas del Asistente de IA (CTO)".

---

### 4. Interfaz de Usuario (Frontend Premium)

Para impresionar visualmente al usuario y cumplir con la directiva de diseño web moderno de alta gama, crearemos una SPA (Single Page Application) con estética de panel tecnológico o **dashboard financiero premium**:
- **Estilo Visual**: Modo oscuro profundo con acentos de color vibrantes (azul eléctrico `#00e5ff`, verde esmeralda `#00e676` y púrpura neón `#d500f9`), bordes suavizados con efecto de vidrio (*glassmorphism*), tipografía limpia (`Outfit` o `Inter` de Google Fonts) y sombras difuminadas con brillo.
- **Sección de Entrada interactiva**: Formularios interactivos para configurar los parámetros (capacidad RAM, coeficientes de marketing, pesos/prioridades de servidores, aristas de la red) con valores cargados por defecto para facilitar pruebas rápidas.
- **Sección de Resultados Visuales**:
  - Tarjetas de resumen con indicadores de rendimiento (KPIs) clave.
  - Renderizado dinámico e interactivo del grafo de la red y la ruta crítica resaltada con colores vivos.
  - Visualización ordenada de las matrices de decisión paso a paso de programación dinámica.
- **Sección de IA**: Un contenedor destacado con efectos de carga modernos para presentar las "Conclusiones Estratégicas del Asistente de IA".
- **Botón de Exportación**: Botón premium flotante o de acción principal para gatillar la descarga directa del reporte PDF.

---

## 🎯 Plan de Verificación

### Pruebas Automatizadas
1. **Pruebas Unitarias de Algoritmos**: Archivos de prueba `test_algorithms.py` ejecutados con `pytest` para verificar que:
   - El algoritmo Knapsack retorne exactamente la selección óptima y el valor máximo para el ejemplo del PDF (RAM 16 GB, microservicios dados).
   - El algoritmo de ruta crítica en el grafo por etapas devuelva exactamente la ruta de latencia mínima para la red del ejemplo (Ruta óptima teórica y latencia acumulada).
   - El algoritmo no lineal calcule correctamente el máximo exacto para el presupuesto de marketing dado.
2. **Validación de Datos**: Pruebas de borde para asegurar que las entradas negativas, capacidades nulas o parámetros no numéricos en la API sean rechazados de forma elegante mediante códigos HTTP 422.

### Pruebas Manuales y Visuales
1. **Verificación de la Interfaz**: Validar la responsividad y las transiciones suaves en diferentes tamaños de pantalla.
2. **Generación del Reporte**: Ejecutar el flujo completo de resolución e inteligencia artificial, exportar el PDF y abrirlo para asegurar la legibilidad, alineación y correcta inclusión de los datos paso a paso y el texto del CTO.

---

## 🚦 Estado Actual: ¿Qué falta por construir?

Dado que la carpeta del proyecto está vacía a excepción de las especificaciones en PDF, falta construir la totalidad de los módulos propuestos:

- [ ] **Estructura del Proyecto**: Crear las carpetas `backend/` y `frontend/`.
- [ ] **Configuración del Backend**: Inicializar `requirements.txt` e instalar dependencias.
- [ ] **Codificación Algorítmica**: Desarrollar en POO `knapsack.py`, `stage_coach.py` y `non_linear.py` con sus respectivas matrices paso a paso.
- [ ] **Controladores API**: Crear los endpoints de FastAPI en `main.py` y los enrutadores.
- [ ] **Integración de Servicios**: Implementar el servicio de API de Groq en `groq_service.py` y el generador de reportes en `pdf_service.py`.
- [ ] **Diseño del Frontend**: Crear `index.html`, `style.css` y los scripts JavaScript en la carpeta `frontend/`.
- [ ] **Integración del Sistema**: Conectar el frontend con el backend, probar el flujo completo de extremo a extremo, configurar valores de prueba por defecto y habilitar la exportación nativa a PDF.

---

## ❓ Preguntas Abiertas para el Usuario

> [!IMPORTANT]
> Agradecemos su retroalimentación sobre los siguientes puntos para ajustar el diseño antes de proceder a la fase de construcción:
>
> 1. **Tecnología del Backend**: ¿Le parece adecuada la propuesta de usar **FastAPI (Python)** para el backend? Dado que el backend de algoritmos requiere programación orientada a objetos pura y manejo matemático, Python es ideal, y FastAPI nos permite interactuar fluidamente mediante una API asíncrona.
> 2. **Librería de PDF**: ¿Está de acuerdo con generar el PDF en el backend utilizando `reportlab`? Esto garantiza un reporte muy formal y estructurado de manera nativa.
> 3. **API Key de Groq**: Para habilitar la IA, necesitaremos configurar una variable de entorno `GROQ_API_KEY`. ¿Cuenta ya con una clave de API de Groq o prefiere que le dejemos las instrucciones para obtener una gratuita?
