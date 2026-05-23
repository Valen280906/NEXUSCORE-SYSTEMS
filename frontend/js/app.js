/**
 * Orquestador principal y gestor de estado para el Frontend de NexusCore Systems.
 */

// ESTADO GLOBAL DE LA APLICACIÓN
const STATE = {
    // Sub-problema A: Servidores (Mochila)
    knapsack: {
        capacity: 16,
        items: []
    },
    // Sub-problema B: Enrutamiento (Ruta por Etapas)
    routing: {
        stages: [],
        connections: {}
    },
    // Parte II: Mercadeo (No Lineal)
    marketing: {
        budget: 10.0,
        c1: 4.0,
        c2: 5.0,
        a1: 0.2,
        a2: 0.3
    },
    // Resultados calculados guardados para IA y PDF
    results: {
        knapsack: null,
        routing: null,
        marketing: null,
        aiConclusions: null
    }
};

// VALORES ACADÉMICOS PREESTABLECIDOS POR EL PDF (DATOS POR DEFECTO)
const DEFAULT_VALUES = {
    knapsack: {
        capacity: 16,
        items: [
            { id: 1, name: "Autenticación y Seguridad", weight: 3, value: 5 },
            { id: 2, name: "Matchmaking (Emparejamiento)", weight: 4, value: 7 },
            { id: 3, name: "Sincronización de Estado (Física)", weight: 7, value: 11 },
            { id: 4, name: "Base de Datos Caché", weight: 5, value: 8 }
        ]
    },
    routing: {
        stages: [
            ["A"],
            ["B", "C", "D"],
            ["E", "F", "G"],
            ["H", "I"],
            ["J"]
        ],
        connections: {
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
        budget: 10.0,
        c1: 4.0,
        c2: 5.0,
        a1: 0.2,
        a2: 0.3
    }
};

// INICIALIZACIÓN
document.addEventListener("DOMContentLoaded", () => {
    initApp();
    setupEventListeners();
    checkBackendHealth();
    
    // Iniciar chequeo periódico cada 6 segundos
    setInterval(checkBackendHealth, 6000);
});

function initApp() {
    // Cargar valores por defecto
    restoreDefaults();
    
    // Mostrar sección inicial (Dashboard)
    UI.showSection("dashboard-section");
    
    // Renderizar inputs iniciales
    UI.renderKnapsackInputs(STATE.knapsack.items);
    UI.renderRoutingInputs(STATE.routing.stages, STATE.routing.connections);
    
    // Rellenar inputs de marketing en el HTML
    document.getElementById("mkt-budget").value = STATE.marketing.budget;
    document.getElementById("mkt-c1").value = STATE.marketing.c1;
    document.getElementById("mkt-a1").value = STATE.marketing.a1;
    document.getElementById("mkt-c2").value = STATE.marketing.c2;
    document.getElementById("mkt-a2").value = STATE.marketing.a2;

    // Inicializar íconos de Lucide
    lucide.createIcons();
}

function restoreDefaults() {
    STATE.knapsack = JSON.parse(JSON.stringify(DEFAULT_VALUES.knapsack));
    STATE.routing = JSON.parse(JSON.stringify(DEFAULT_VALUES.routing));
    STATE.marketing = JSON.parse(JSON.stringify(DEFAULT_VALUES.marketing));
}

// CONFIGURACIÓN DE EVENT LISTENERS
function setupEventListeners() {
    // Navegación Sidebar
    document.querySelectorAll(".nav-item").forEach(btn => {
        btn.addEventListener("click", (e) => {
            const target = btn.getAttribute("data-target");
            UI.showSection(target);
            
            // Si entramos a la sección de enrutamiento, redibujamos el canvas para evitar distorsiones
            if (target === "routing-section" && STATE.results.routing) {
                setTimeout(() => {
                    UI.drawRoutingGraph(
                        STATE.results.routing.stages_data,
                        STATE.results.routing.connections_data,
                        STATE.results.routing.optimal_path
                    );
                }, 50);
            }
            // Si entramos a la sección de mercadeo, redibujamos el canvas del gráfico
            if (target === "marketing-section" && STATE.results.marketing) {
                setTimeout(() => {
                    UI.drawMarketingChart(
                        STATE.results.marketing.chart_points,
                        STATE.results.marketing.constrained_optimum
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
            await runKnapsackOptimization();
            
            // 2. Optimizar Enrutamiento
            await runRoutingOptimization();
            
            // 3. Optimizar Presupuesto
            await runMarketingOptimization();
            
            // Ir a la pestaña de reportes
            UI.showSection("report-section");
            
            // 4. Solicitar IA automáticamente
            await runAIAnalysis();

            btn.innerHTML = `<i data-lucide="zap"></i> Optimizar Todo`;
            btn.removeAttribute("disabled");
            lucide.createIcons();
            
        } catch (error) {
            alert(`Error en optimización global: ${error.message}`);
            console.error(error);
            const btn = document.getElementById("btn-global-optimize");
            btn.innerHTML = `<i data-lucide="zap"></i> Optimizar Todo`;
            btn.removeAttribute("disabled");
            lucide.createIcons();
        }
    });

    // Acción "Valores por Defecto"
    document.getElementById("btn-reset-defaults").addEventListener("click", () => {
        initApp();
        alert("Se han restaurado los valores académicos por defecto de NexusCore Systems.");
    });

    // --- SECCIÓN A: MOCHILA (SERVIDORES) ---
    // Botón Agregar Microservicio
    document.getElementById("btn-add-ms").addEventListener("click", () => {
        const nextId = STATE.knapsack.items.length > 0 
            ? Math.max(...STATE.knapsack.items.map(item => item.id)) + 1 
            : 1;
        
        STATE.knapsack.items.push({
            id: nextId,
            name: `Microservicio Nuevo`,
            weight: 2,
            value: 4
        });
        UI.renderKnapsackInputs(STATE.knapsack.items);
    });

    // Escuchar cambios en los inputs de microservicios
    const msTable = document.getElementById("ms-inputs-table");
    msTable.addEventListener("change", (e) => {
        const index = parseInt(e.target.getAttribute("data-index"));
        if (isNaN(index)) return;
        
        if (e.target.classList.contains("ms-name-input")) {
            STATE.knapsack.items[index].name = e.target.value;
        } else if (e.target.classList.contains("ms-weight-input")) {
            STATE.knapsack.items[index].weight = parseInt(e.target.value) || 1;
        } else if (e.target.classList.contains("ms-value-input")) {
            STATE.knapsack.items[index].value = parseInt(e.target.value) || 0;
        }
    });

    // Botón eliminar microservicio
    msTable.addEventListener("click", (e) => {
        const btn = e.target.closest(".btn-remove-row");
        if (!btn) return;
        
        const index = parseInt(btn.getAttribute("data-index"));
        STATE.knapsack.items.splice(index, 1);
        UI.renderKnapsackInputs(STATE.knapsack.items);
    });

    // Botón Optimizar Mochila
    document.getElementById("btn-optimize-knap").addEventListener("click", async () => {
        const capInput = parseInt(document.getElementById("knap-capacity").value);
        STATE.knapsack.capacity = isNaN(capInput) ? 16 : capInput;
        
        try {
            await runKnapsackOptimization();
            alert("¡Optimización de servidores completada con éxito!");
        } catch (error) {
            alert(`Error al optimizar: ${error.message}`);
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
                alert("Una etapa debe contener al menos un nodo.");
                UI.renderRoutingInputs(STATE.routing.stages, STATE.routing.connections);
                return;
            }
            
            STATE.routing.stages[index] = nodes;
            
            // Re-sincronizar conexiones eliminando nodos que ya no existen
            sanitizeConnections();
            UI.renderRoutingInputs(STATE.routing.stages, STATE.routing.connections);
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
                alert("La latencia debe ser un número positivo.");
                return;
            }
            
            if (!STATE.routing.connections[fromNode]) {
                STATE.routing.connections[fromNode] = {};
            }
            STATE.routing.connections[fromNode][toNode] = value;
        }
    });

    // Botón calcular Ruta Crítica
    document.getElementById("btn-optimize-routing").addEventListener("click", async () => {
        try {
            await runRoutingOptimization();
            alert("¡Ruta crítica por etapas calculada correctamente!");
        } catch (error) {
            alert(`Error en ruta crítica: ${error.message}`);
        }
    });

    // --- SECCIÓN C: MERCADEO (NO LINEAL) ---
    document.getElementById("btn-optimize-marketing").addEventListener("click", async () => {
        try {
            // Leer valores del HTML
            STATE.marketing.budget = parseFloat(document.getElementById("mkt-budget").value) || 10.0;
            STATE.marketing.c1 = parseFloat(document.getElementById("mkt-c1").value) || 4.0;
            STATE.marketing.a1 = parseFloat(document.getElementById("mkt-a1").value) || 0.2;
            STATE.marketing.c2 = parseFloat(document.getElementById("mkt-c2").value) || 5.0;
            STATE.marketing.a2 = parseFloat(document.getElementById("mkt-a2").value) || 0.3;
            
            await runMarketingOptimization();
            alert("¡Optimización de presupuesto no lineal completada!");
        } catch (error) {
            alert(`Error al optimizar presupuesto: ${error.message}`);
        }
    });

    // --- SECCIÓN E: REPORTE & IA ---
    // Generar Análisis de Groq
    document.getElementById("btn-request-ai").addEventListener("click", async () => {
        // Validar que tengamos los 3 resultados matemáticos
        if (!STATE.results.knapsack || !STATE.results.routing || !STATE.results.marketing) {
            alert("Primero debe calcular los tres problemas matemáticos de optimización (puede presionar 'Optimizar Todo' en la cabecera).");
            return;
        }
        
        try {
            await runAIAnalysis();
        } catch (error) {
            alert(`Error en IA: ${error.message}`);
        }
    });

    // Descargar Reporte PDF
    document.getElementById("btn-download-pdf").addEventListener("click", async () => {
        if (!STATE.results.knapsack || !STATE.results.routing || !STATE.results.marketing || !STATE.results.aiConclusions) {
            alert("Se requieren todos los resultados cuantitativos y cualitativos para generar el reporte PDF consolidado.");
            return;
        }
        
        try {
            const btn = document.getElementById("btn-download-pdf");
            btn.innerHTML = `<div class="spinner" style="width:12px; height:12px; margin:0"></div> Descargando...`;
            btn.setAttribute("disabled", "true");
            
            const pdfBlob = await API.downloadPdfReport(
                STATE.results.knapsack,
                STATE.results.routing,
                STATE.results.marketing,
                STATE.results.aiConclusions
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
            alert(`Error al descargar el PDF: ${error.message}`);
            const btn = document.getElementById("btn-download-pdf");
            btn.innerHTML = `<i data-lucide="download"></i> Descargar Reporte Completo (PDF)`;
            btn.removeAttribute("disabled");
            lucide.createIcons();
        }
    });
}

// SANEADOR DE CONEXIONES (Remueve destinos inexistentes)
function sanitizeConnections() {
    const allNodes = new Set(STATE.routing.stages.flat());
    const sanitized = {};
    
    for (const fromNode in STATE.routing.connections) {
        if (allNodes.has(fromNode)) {
            sanitized[fromNode] = {};
            for (const toNode in STATE.routing.connections[fromNode]) {
                if (allNodes.has(toNode)) {
                    sanitized[fromNode][toNode] = STATE.routing.connections[fromNode][toNode];
                }
            }
            if (Object.keys(sanitized[fromNode]).length === 0) {
                delete sanitized[fromNode];
            }
        }
    }
    
    // Si faltan aristas entre etapas contiguas, creamos aristas vacías (costo = 5.0 por defecto) para mantener conectividad
    for (let s = 0; s < STATE.routing.stages.length - 1; s++) {
        const fromNodes = STATE.routing.stages[s];
        const toNodes = STATE.routing.stages[s+1];
        
        fromNodes.forEach(fromNode => {
            toNodes.forEach(toNode => {
                if (!sanitized[fromNode]) sanitized[fromNode] = {};
                if (sanitized[fromNode][toNode] === undefined) {
                    sanitized[fromNode][toNode] = 5.0; // Valor default de conexión
                }
            });
        });
    }
    
    STATE.routing.connections = sanitized;
}

// FUNCIONES DE EJECUCIÓN (Llamadas API y actualización visual)

async function runKnapsackOptimization() {
    const res = await API.optimizeKnapsack(STATE.knapsack.capacity, STATE.knapsack.items);
    STATE.results.knapsack = res;
    UI.renderKnapsackResults(res);
    return res;
}

async function runRoutingOptimization() {
    const res = await API.optimizeStagecoach(STATE.routing.stages, STATE.routing.connections);
    STATE.results.routing = res;
    UI.renderRoutingResults(res);
    return res;
}

async function runMarketingOptimization() {
    const res = await API.optimizeNonLinear(
        STATE.marketing.budget,
        STATE.marketing.c1,
        STATE.marketing.c2,
        STATE.marketing.a1,
        STATE.marketing.a2
    );
    STATE.results.marketing = res;
    UI.renderMarketingResults(res);
    return res;
}

async function runAIAnalysis() {
    UI.renderAiLoading();
    try {
        const res = await API.getAIAnalysis(
            STATE.results.knapsack,
            STATE.results.routing,
            STATE.results.marketing
        );
        STATE.results.aiConclusions = res.conclusions;
        UI.renderAiResult(res.conclusions);
        return res;
    } catch (error) {
        UI.renderAiError(error.message);
        throw error;
    }
}

// CONTROLADOR DE SALUD DEL BACKEND
async function checkBackendHealth() {
    const isOnline = await API.checkStatus();
    UI.updateBackendStatus(isOnline);
}
