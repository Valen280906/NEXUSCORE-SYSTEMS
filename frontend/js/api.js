/**
 * Cliente API para comunicarse con el servidor backend FastAPI de NexusCore Systems.
 */
const BASE_URL = "http://127.0.0.1:8000/api/v1";

const API = {
    /**
     * Comprueba el estado de la API.
     */
    async checkStatus() {
        try {
            const response = await fetch("http://127.0.0.1:8000/");
            if (response.ok) {
                return true;
            }
            return false;
        } catch (error) {
            console.error("Error al conectar con la raíz del backend:", error);
            return false;
        }
    },

    /**
     * Resuelve el problema de la mochila para servidores.
     */
    async optimizeKnapsack(capacity, items) {
        const response = await fetch(`${BASE_URL}/optimize/knapsack`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ capacity, items })
        });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Error en optimización de servidores.");
        }
        return await response.json();
    },

    /**
     * Resuelve el problema del camino mínimo Backward por etapas.
     */
    async optimizeStagecoach(stages, connections) {
        const response = await fetch(`${BASE_URL}/optimize/stagecoach`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ stages, connections })
        });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Error en enrutamiento por etapas.");
        }
        return await response.json();
    },

    /**
     * Resuelve la optimización no lineal de mercadeo.
     */
    async optimizeNonLinear(budget, c1, c2, a1, a2) {
        const response = await fetch(`${BASE_URL}/optimize/non-linear`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ budget, c1, c2, a1, a2 })
        });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Error en optimización no lineal.");
        }
        return await response.json();
    },

    /**
     * Genera conclusiones cualitativas de negocio mediante la API de Groq.
     */
    async getAIAnalysis(knapsackResult, routingResult, marketingResult) {
        const response = await fetch(`${BASE_URL}/ai/analyze`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                knapsack_result: knapsackResult,
                routing_result: routingResult,
                marketing_result: marketingResult
            })
        });
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Error al solicitar análisis de IA.");
        }
        return await response.json();
    },

    /**
     * Exporta el PDF combinando los resultados numéricos y el reporte cualitativo.
     */
    async downloadPdfReport(knapsackResult, routingResult, marketingResult, aiConclusions) {
        const response = await fetch(`${BASE_URL}/ai/export-pdf`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                knapsack_result: knapsackResult,
                routing_result: routingResult,
                marketing_result: marketingResult,
                ai_conclusions: aiConclusions
            })
        });
        if (!response.ok) {
            throw new Error("No se pudo descargar el reporte PDF.");
        }
        return await response.blob();
    }
};
