/**
 * Cliente API para comunicarse con el servidor backend FastAPI de NexusCore Systems.
 * Todas las funciones y rutas están en español, siguiendo el estándar del proyecto.
 */
const URL_BASE = "http://127.0.0.1:8000/api/v1";

const API = {
    /**
     * Comprueba el estado de la API (Healthcheck).
     */
    async comprobarEstado() {
        try {
            const respuesta = await fetch("http://127.0.0.1:8000/");
            if (respuesta.ok) {
                return true;
            }
            return false;
        } catch (error) {
            console.error("Error al conectar con la raíz del backend:", error);
            return false;
        }
    },

    /**
     * Resuelve el Sub-problema A: Carga de Servidores (Mochila).
     */
    async optimizarMochila(capacidad, elementos) {
        const respuesta = await fetch(`${URL_BASE}/optimizar/mochila`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ capacidad, elementos })
        });
        if (!respuesta.ok) {
            const err = await respuesta.json();
            throw new Error(err.detail || "Error en optimización de servidores.");
        }
        return await respuesta.json();
    },

    /**
     * Resuelve el Sub-problema B: Enrutamiento por etapas (DP Backward).
     */
    async optimizarRutaEtapas(etapas, conexiones) {
        const respuesta = await fetch(`${URL_BASE}/optimizar/ruta-etapas`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ etapas, conexiones })
        });
        if (!respuesta.ok) {
            const err = await respuesta.json();
            throw new Error(err.detail || "Error en enrutamiento por etapas.");
        }
        return await respuesta.json();
    },

    /**
     * Resuelve la Parte II: Optimización no lineal de mercadeo.
     */
    async optimizarNoLineal(presupuesto, c1, c2, a1, a2) {
        const respuesta = await fetch(`${URL_BASE}/optimizar/no-lineal`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ presupuesto, c1, c2, a1, a2 })
        });
        if (!respuesta.ok) {
            const err = await respuesta.json();
            throw new Error(err.detail || "Error en optimización no lineal.");
        }
        return await respuesta.json();
    },

    /**
     * Parte III: Genera conclusiones cualitativas de negocio mediante la API de Groq.
     */
    async obtenerAnalisisIA(resultadoMochila, resultadoEnrutamiento, resultadoMarketing) {
        const respuesta = await fetch(`${URL_BASE}/ia/analizar`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                resultado_mochila:      resultadoMochila,
                resultado_enrutamiento:  resultadoEnrutamiento,
                resultado_marketing:    resultadoMarketing
            })
        });
        if (!respuesta.ok) {
            const err = await respuesta.json();
            throw new Error(err.detail || "Error al solicitar análisis de IA.");
        }
        return await respuesta.json();
    },

    /**
     * Parte III: Exporta el PDF combinando los resultados numéricos y el reporte cualitativo.
     */
    async descargarReportePdf(resultadoMochila, resultadoEnrutamiento, resultadoMarketing, conclusionesIA) {
        const respuesta = await fetch(`${URL_BASE}/ia/exportar-pdf`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                resultado_mochila:      resultadoMochila,
                resultado_enrutamiento:  resultadoEnrutamiento,
                resultado_marketing:    resultadoMarketing,
                conclusiones_ia:        conclusionesIA
            })
        });
        if (!respuesta.ok) {
            const err = await respuesta.json();
            throw new Error(err?.detail || "No se pudo descargar el reporte PDF.");
        }
        return await respuesta.blob();
    }
};
