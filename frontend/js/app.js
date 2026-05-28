/**
 * Orquestador principal y gestor de estado para el Frontend de NexusCore Systems.
 */

// ESTADO GLOBAL DE LA APLICACIÓN
const ESTADO = {
    // Sub-problema A: Servidores (Mochila)
    mochila: {
        capacidad: 16,
        elementos: []
    },
    // Sub-problema B: Enrutamiento (Ruta por Etapas)
    enrutamiento: {
        etapas: [],
        conexiones: {}
    },
    // Parte II: Mercadeo (No Lineal)
    marketing: {
        presupuesto: 10.0,
        c1: 4.0,
        c2: 5.0,
        a1: 0.2,
        a2: 0.3
    },
    // Resultados calculados guardados para IA y PDF
    resultados: {
        mochila: null,
        enrutamiento: null,
        marketing: null,
        conclusionesIA: null
    }
};

// VALORES ACADÉMICOS PREESTABLECIDOS POR EL PDF (DATOS POR DEFECTO)
const VALORES_DEFECTO = {
    mochila: {
        capacidad: 16,
        elementos: [
            { id: 1, nombre: "Autenticación y Seguridad", peso: 3, valor: 5 },
            { id: 2, nombre: "Matchmaking (Emparejamiento)", peso: 4, valor: 7 },
            { id: 3, nombre: "Sincronización de Estado (Física)", peso: 7, valor: 11 },
            { id: 4, nombre: "Base de Datos Caché", peso: 5, valor: 8 }
        ]
    },
    enrutamiento: {
        etapas: [
            ["A"],
            ["B", "C", "D"],
            ["E", "F", "G"],
            ["H", "I"],
            ["J"]
        ],
        conexiones: {
            "A": { "B": 4.0, "C": 6.0, "D": 3.0 },
            "B": { "E": 7.0, "F": 5.0 },
            "C": { "E": 3.0, "F": 8.0, "G": 4.0 },
            "D": { "F": 6.0, "G": 9.0 },
            "E": { "H": 5.0, "I": 6.0 },
            "F": { "H": 3.0, "I": 5.0 },
            "G": { "H": 8.0, "I": 2.0 },
            "H": { "J": 4.0 },
            "I": { "J": 7.0 }
        }
    },
    marketing: {
        presupuesto: 10.0,
        c1: 4.0,
        c2: 5.0,
        a1: 0.2,
        a2: 0.3
    }
};

// INICIALIZACIÓN
document.addEventListener("DOMContentLoaded", () => {
    iniciarApp();
    configurarEventos();
    verificarSaludBackend();

    // Iniciar chequeo periódico cada 6 segundos
    setInterval(verificarSaludBackend, 6000);
});

function iniciarApp() {
    // Cargar valores por defecto
    restaurarValoresDefecto();

    // Mostrar sección inicial (Dashboard)
    UI.mostrarSeccion("dashboard-section");

    // Renderizar inputs iniciales
    UI.renderizarInputsMochila(ESTADO.mochila.elementos);
    UI.renderizarInputsEnrutamiento(ESTADO.enrutamiento.etapas, ESTADO.enrutamiento.conexiones);

    // Rellenar inputs de marketing en el HTML
    document.getElementById("mkt-budget").value = ESTADO.marketing.presupuesto;
    document.getElementById("mkt-c1").value = ESTADO.marketing.c1;
    document.getElementById("mkt-a1").value = ESTADO.marketing.a1;
    document.getElementById("mkt-c2").value = ESTADO.marketing.c2;
    document.getElementById("mkt-a2").value = ESTADO.marketing.a2;

    // Inicializar íconos de Lucide
    lucide.createIcons();
}

function restaurarValoresDefecto() {
    ESTADO.mochila = JSON.parse(JSON.stringify(VALORES_DEFECTO.mochila));
    ESTADO.enrutamiento = JSON.parse(JSON.stringify(VALORES_DEFECTO.enrutamiento));
    ESTADO.marketing = JSON.parse(JSON.stringify(VALORES_DEFECTO.marketing));
}

// CONFIGURACIÓN DE EVENT LISTENERS
function configurarEventos() {
    // Navegación Sidebar
    document.querySelectorAll(".nav-item").forEach(btn => {
        btn.addEventListener("click", (e) => {
            const target = btn.getAttribute("data-target");
            UI.mostrarSeccion(target);

            // Si entramos a la sección de enrutamiento, redibujamos el canvas para evitar distorsiones
            if (target === "routing-section" && ESTADO.resultados.enrutamiento) {
                setTimeout(() => {
                    UI.dibujarGrafoEnrutamiento(
                        ESTADO.resultados.enrutamiento.etapas_datos,
                        ESTADO.resultados.enrutamiento.conexiones_datos,
                        ESTADO.resultados.enrutamiento.ruta_optima
                    );
                }, 50);
            }
            // Si entramos a la sección de mercadeo, redibujamos el canvas del gráfico
            if (target === "marketing-section" && ESTADO.resultados.marketing) {
                setTimeout(() => {
                    UI.dibujarGraficoMarketing(
                        ESTADO.resultados.marketing.puntos_grafica,
                        ESTADO.resultados.marketing.optimo_restringido
                    );
                }, 50);
            }
        });
    });

    // Acción Global "Optimizar Todo"
    document.getElementById("btn-global-optimize").addEventListener("click", async () => {
        try {
            // Mostrar efectos visuales
            const btn = document.getElementById("btn-global-optimize");
            btn.innerHTML = `<div class="spinner" style="width:14px; height:14px; margin:0"></div> Procesando...`;
            btn.setAttribute("disabled", "true");

            // 1. Optimizar Carga de Servidores
            await ejecutarOptimizacionMochila();

            // 2. Optimizar Enrutamiento
            await ejecutarOptimizacionEnrutamiento();

            // 3. Optimizar Presupuesto
            await ejecutarOptimizacionMarketing();

            // Ir a la pestaña de reportes
            UI.mostrarSeccion("report-section");

            // 4. Solicitar IA automáticamente
            await ejecutarAnalisisIA();

            btn.innerHTML = `<i data-lucide="zap"></i> Optimizar Todo`;
            btn.removeAttribute("disabled");
            lucide.createIcons();

        } catch (error) {
            UI.mostrarNotificacion(`Error en optimización global: ${error.message}`, "error");
            console.error(error);
            const btn = document.getElementById("btn-global-optimize");
            btn.innerHTML = `<i data-lucide="zap"></i> Optimizar Todo`;
            btn.removeAttribute("disabled");
            lucide.createIcons();
        }
    });

    // Acción "Valores por Defecto"
    document.getElementById("btn-reset-defaults").addEventListener("click", () => {
        iniciarApp();
        UI.mostrarNotificacion("Se han restaurado los valores por defecto.", "success");
    });

    // --- SECCIÓN A: MOCHILA (SERVIDORES) ---
    // Botón Agregar Microservicio
    document.getElementById("btn-add-ms").addEventListener("click", () => {
        const nextId = ESTADO.mochila.elementos.length > 0
            ? Math.max(...ESTADO.mochila.elementos.map(item => item.id)) + 1
            : 1;

        ESTADO.mochila.elementos.push({
            id: nextId,
            nombre: `Microservicio Nuevo`,
            peso: 2,
            valor: 4
        });
        UI.renderizarInputsMochila(ESTADO.mochila.elementos);
    });

    // Escuchar cambios en los inputs de microservicios
    const msTable = document.getElementById("ms-inputs-table");
    msTable.addEventListener("change", (e) => {
        const index = parseInt(e.target.getAttribute("data-index"));
        if (isNaN(index)) return;

        if (e.target.classList.contains("ms-name-input")) {
            ESTADO.mochila.elementos[index].nombre = e.target.value;
        } else if (e.target.classList.contains("ms-weight-input")) {
            ESTADO.mochila.elementos[index].peso = parseInt(e.target.value) || 1;
        } else if (e.target.classList.contains("ms-value-input")) {
            ESTADO.mochila.elementos[index].valor = parseInt(e.target.value) || 0;
        }
    });

    // Botón eliminar microservicio
    msTable.addEventListener("click", (e) => {
        const btn = e.target.closest(".btn-remove-row");
        if (!btn) return;

        const index = parseInt(btn.getAttribute("data-index"));
        ESTADO.mochila.elementos.splice(index, 1);
        UI.renderizarInputsMochila(ESTADO.mochila.elementos);
    });

    // Botón Optimizar Mochila
    document.getElementById("btn-optimize-knap").addEventListener("click", async () => {
        const capInput = parseInt(document.getElementById("knap-capacity").value);
        ESTADO.mochila.capacidad = isNaN(capInput) ? 16 : capInput;

        try {
            await ejecutarOptimizacionMochila();
            UI.mostrarNotificacion("¡Optimización de servidores completada con éxito!", "success");
        } catch (error) {
            UI.mostrarNotificacion(`Error al optimizar: ${error.message}`, "error");
        }
    });

    // --- SECCIÓN B: ENRUTAMIENTO (ETAPAS) ---
    // Escuchar cambios en los inputs de nodos por etapa
    const stagesContainer = document.getElementById("routing-stages-inputs");
    stagesContainer.addEventListener("change", (e) => {
        if (e.target.classList.contains("stage-nodes-input")) {
            const index = parseInt(e.target.getAttribute("data-index"));
            const nodes = e.target.value.split(",").map(n => n.trim()).filter(n => n !== "");

            if (nodes.length === 0) {
                UI.mostrarNotificacion("Una etapa debe contener al menos un nodo.", "warning");
                UI.renderizarInputsEnrutamiento(ESTADO.enrutamiento.etapas, ESTADO.enrutamiento.conexiones);
                return;
            }

            ESTADO.enrutamiento.etapas[index] = nodes;

            // Re-sincronizar conexiones eliminando nodos que ya no existen
            sanearConexiones();
            UI.renderizarInputsEnrutamiento(ESTADO.enrutamiento.etapas, ESTADO.enrutamiento.conexiones);
        }
    });

    // Escuchar cambios en los inputs de latencia
    const connectionsContainer = document.getElementById("connections-editor-list");
    connectionsContainer.addEventListener("change", (e) => {
        if (e.target.classList.contains("latency-input")) {
            const fromNode = e.target.getAttribute("data-from");
            const toNode = e.target.getAttribute("data-to");
            const value = parseFloat(e.target.value);

            if (isNaN(value) || value < 0) {
                UI.mostrarNotificacion("La latencia debe ser un número positivo.", "warning");
                return;
            }

            if (!ESTADO.enrutamiento.conexiones[fromNode]) {
                ESTADO.enrutamiento.conexiones[fromNode] = {};
            }
            ESTADO.enrutamiento.conexiones[fromNode][toNode] = value;
        }
    });

    // Botón calcular Ruta Crítica
    document.getElementById("btn-optimize-routing").addEventListener("click", async () => {
        try {
            await ejecutarOptimizacionEnrutamiento();
            UI.mostrarNotificacion("¡Ruta crítica por etapas calculada correctamente!", "success");
        } catch (error) {
            UI.mostrarNotificacion(`Error en ruta crítica: ${error.message}`, "error");
        }
    });

    // --- SECCIÓN C: MERCADEO (NO LINEAL) ---
    document.getElementById("btn-optimize-marketing").addEventListener("click", async () => {
        try {
            // Leer valores del HTML
            ESTADO.marketing.presupuesto = parseFloat(document.getElementById("mkt-budget").value) || 10.0;
            ESTADO.marketing.c1 = parseFloat(document.getElementById("mkt-c1").value) || 4.0;
            ESTADO.marketing.a1 = parseFloat(document.getElementById("mkt-a1").value) || 0.2;
            ESTADO.marketing.c2 = parseFloat(document.getElementById("mkt-c2").value) || 5.0;
            ESTADO.marketing.a2 = parseFloat(document.getElementById("mkt-a2").value) || 0.3;

            await ejecutarOptimizacionMarketing();
            UI.mostrarNotificacion("¡Optimización de presupuesto no lineal completada!", "success");
        } catch (error) {
            UI.mostrarNotificacion(`Error al optimizar presupuesto: ${error.message}`, "error");
        }
    });

    // --- SECCIÓN E: REPORTE & IA ---
    // Generar Análisis de Groq
    document.getElementById("btn-request-ai").addEventListener("click", async () => {
        // Validar que tengamos los 3 resultados matemáticos
        if (!ESTADO.resultados.mochila || !ESTADO.resultados.enrutamiento || !ESTADO.resultados.marketing) {
            UI.mostrarNotificacion("Primero debe calcular los tres problemas matemáticos de optimización (puede presionar 'Optimizar Todo' en la cabecera).", "warning");
            return;
        }

        try {
            await ejecutarAnalisisIA();
        } catch (error) {
            UI.mostrarNotificacion(`Error en IA: ${error.message}`, "error");
        }
    });

    // Descargar Reporte PDF
    document.getElementById("btn-download-pdf").addEventListener("click", async () => {
        if (!ESTADO.resultados.mochila || !ESTADO.resultados.enrutamiento || !ESTADO.resultados.marketing || !ESTADO.resultados.conclusionesIA) {
            UI.mostrarNotificacion("Se requieren todos los resultados cuantitativos y cualitativos para generar el reporte PDF.", "warning");
            return;
        }

        try {
            const btn = document.getElementById("btn-download-pdf");
            btn.innerHTML = `<div class="spinner" style="width:12px; height:12px; margin:0"></div> Descargando...`;
            btn.setAttribute("disabled", "true");

            const pdfBlob = await API.descargarReportePdf(
                ESTADO.resultados.mochila,
                ESTADO.resultados.enrutamiento,
                ESTADO.resultados.marketing,
                ESTADO.resultados.conclusionesIA
            );

            // Disparar descarga en navegador
            const url = window.URL.createObjectURL(pdfBlob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "Reporte_Optimizacion_NexusCore.pdf";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            btn.innerHTML = `<i data-lucide="download"></i> Descargar Reporte Completo (PDF)`;
            btn.removeAttribute("disabled");
            lucide.createIcons();

        } catch (error) {
            UI.mostrarNotificacion(`Error al descargar el PDF: ${error.message}`, "error");
            const btn = document.getElementById("btn-download-pdf");
            btn.innerHTML = `<i data-lucide="download"></i> Descargar Reporte Completo (PDF)`;
            btn.removeAttribute("disabled");
            lucide.createIcons();
        }
    });
}

// SANEADOR DE CONEXIONES (Remueve destinos inexistentes)
function sanearConexiones() {
    const allNodes = new Set(ESTADO.enrutamiento.etapas.flat());
    const sanitized = {};

    for (const fromNode in ESTADO.enrutamiento.conexiones) {
        if (allNodes.has(fromNode)) {
            sanitized[fromNode] = {};
            for (const toNode in ESTADO.enrutamiento.conexiones[fromNode]) {
                if (allNodes.has(toNode)) {
                    sanitized[fromNode][toNode] = ESTADO.enrutamiento.conexiones[fromNode][toNode];
                }
            }
            if (Object.keys(sanitized[fromNode]).length === 0) {
                delete sanitized[fromNode];
            }
        }
    }

    // Si faltan aristas entre etapas contiguas, creamos aristas vacías (costo = 5.0 por defecto) para mantener conectividad
    for (let s = 0; s < ESTADO.enrutamiento.etapas.length - 1; s++) {
        const fromNodes = ESTADO.enrutamiento.etapas[s];
        const toNodes = ESTADO.enrutamiento.etapas[s + 1];

        fromNodes.forEach(fromNode => {
            toNodes.forEach(toNode => {
                if (!sanitized[fromNode]) sanitized[fromNode] = {};
                if (sanitized[fromNode][toNode] === undefined) {
                    sanitized[fromNode][toNode] = 5.0; // Valor default de conexión
                }
            });
        });
    }

    ESTADO.enrutamiento.conexiones = sanitized;
}

// FUNCIONES DE EJECUCIÓN (Llamadas API y actualización visual)

async function ejecutarOptimizacionMochila() {
    const res = await API.optimizarMochila(ESTADO.mochila.capacidad, ESTADO.mochila.elementos);
    ESTADO.resultados.mochila = res;
    UI.renderizarResultadosMochila(res);
    return res;
}

async function ejecutarOptimizacionEnrutamiento() {
    const res = await API.optimizarRutaEtapas(ESTADO.enrutamiento.etapas, ESTADO.enrutamiento.conexiones);
    ESTADO.resultados.enrutamiento = res;
    UI.renderizarResultadosEnrutamiento(res);
    return res;
}

async function ejecutarOptimizacionMarketing() {
    const res = await API.optimizarNoLineal(
        ESTADO.marketing.presupuesto,
        ESTADO.marketing.c1,
        ESTADO.marketing.c2,
        ESTADO.marketing.a1,
        ESTADO.marketing.a2
    );
    ESTADO.resultados.marketing = res;
    UI.renderizarResultadosMarketing(res);
    return res;
}

async function ejecutarAnalisisIA() {
    UI.renderizarCargaIA();
    try {
        const res = await API.obtenerAnalisisIA(
            ESTADO.resultados.mochila,
            ESTADO.resultados.enrutamiento,
            ESTADO.resultados.marketing
        );
        ESTADO.resultados.conclusionesIA = res.conclusiones;
        UI.renderizarResultadoIA(res.conclusiones);
        return res;
    } catch (error) {
        UI.renderizarErrorIA(error.message);
        throw error;
    }
}

// CONTROLADOR DE SALUD DEL BACKEND
async function verificarSaludBackend() {
    const enLinea = await API.comprobarEstado();
    UI.actualizarEstadoBackend(enLinea);
}
