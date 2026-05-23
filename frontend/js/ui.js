/**
 * Módulo de Interfaz de Usuario (UI) para NexusCore Systems.
 * Gestiona el dibujo de tablas dinámicas, matrices DP, gráficos de canvas y renderizado de la red.
 */

const UI = {
    // ----------------------------------------------------
    // MÓDULO GENERAL / MENÚS
    // ----------------------------------------------------
    showSection(sectionId) {
        document.querySelectorAll(".content-section").forEach(sec => {
            sec.classList.remove("active");
        });
        document.querySelectorAll(".nav-item").forEach(btn => {
            btn.classList.remove("active");
        });
        
        const targetSection = document.getElementById(sectionId);
        if (targetSection) targetSection.classList.add("active");
        
        // Resaltar botón de navegación
        const navBtn = document.querySelector(`.nav-item[data-target="${sectionId}"]`);
        if (navBtn) navBtn.classList.add("active");

        // Actualizar títulos de cabecera
        const title = document.getElementById("page-title");
        const subtitle = document.getElementById("page-subtitle");
        
        if (sectionId === "dashboard-section") {
            title.textContent = "Panel de Control General";
            subtitle.textContent = "Monitoreo de parámetros y optimización cuantitativa en tiempo real.";
        } else if (sectionId === "knapsack-section") {
            title.textContent = "Carga de Servidores Maestros";
            subtitle.textContent = "Programación dinámica para resolver la mochila de recursos críticos.";
        } else if (sectionId === "routing-section") {
            title.textContent = "Enrutamiento Regional de Baja Latencia";
            subtitle.textContent = "Programación dinámica backward por etapas en topología de red.";
        } else if (sectionId === "marketing-section") {
            title.textContent = "Optimización de Presupuesto Publicitario";
            subtitle.textContent = "Maximización de usuarios mediante resolvedor de rendimientos marginales no lineales.";
        } else if (sectionId === "report-section") {
            title.textContent = "Dictamen del CTO & Exportación";
            subtitle.textContent = "Conclusiones analíticas del asistente de IA y descarga de reporte corporativo en PDF.";
        }
    },

    updateBackendStatus(isOnline) {
        const dot = document.querySelector(".pulse-dot");
        const text = document.querySelector(".status-text");
        if (isOnline) {
            dot.className = "pulse-dot online";
            text.textContent = "Backend: Conectado";
        } else {
            dot.className = "pulse-dot offline";
            text.textContent = "Backend: Desconectado";
        }
    },

    // ----------------------------------------------------
    // DIBUJAR FORMULARIO E INGRESO DE MOCHILA (Servidores)
    // ----------------------------------------------------
    renderKnapsackInputs(items) {
        const tbody = document.getElementById("ms-inputs-body");
        tbody.innerHTML = "";
        
        items.forEach((item, index) => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td><span style="font-family: var(--font-mono); color: var(--color-primary)">${item.id}</span></td>
                <td><input type="text" value="${item.name}" class="ms-name-input" data-index="${index}"></td>
                <td><input type="number" value="${item.weight}" min="1" max="128" class="ms-weight-input" data-index="${index}"></td>
                <td><input type="number" value="${item.value}" min="0" class="ms-value-input" data-index="${index}"></td>
                <td>
                    <button class="btn-remove-row" data-index="${index}">
                        <i data-lucide="trash-2"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });
        
        // Re-iniciar íconos de Lucide
        lucide.createIcons();
    },

    renderKnapsackResults(result) {
        document.getElementById("knap-max-value").textContent = result.max_value;
        document.getElementById("knap-used-weight").textContent = `${result.used_weight} / ${result.capacity} GB`;
        
        // Actualizar dashboard
        document.getElementById("dash-stability-val").textContent = `Estabilidad: ${result.max_value}`;
        document.getElementById("dash-stability-lbl").textContent = `${result.used_weight}GB RAM utilizados`;
        document.getElementById("mini-ram-cap").textContent = `${result.capacity} GB`;
        document.getElementById("mini-ms-count").textContent = result.total_items;

        // Renderizar lista de seleccionados
        const selectedList = document.getElementById("knap-selected-list");
        selectedList.innerHTML = "";
        
        if (result.selected_items.length === 0) {
            selectedList.innerHTML = `<p class="placeholder-text">Ninguno seleccionado (RAM insuficiente para estabilidad).</p>`;
        } else {
            result.selected_items.forEach(item => {
                const div = document.createElement("div");
                div.className = "selected-item-pill";
                div.innerHTML = `
                    <span><b>${item.name}</b></span>
                    <span>RAM: <strong>${item.weight} GB</strong> | Estabilidad: <strong>+${item.value}</strong></span>
                `;
                selectedList.appendChild(div);
            });
        }

        // Renderizar la Matriz DP Paso a Paso
        const headersTr = document.getElementById("knap-matrix-headers");
        const bodyTbody = document.getElementById("knap-matrix-body");
        
        headersTr.innerHTML = "";
        bodyTbody.innerHTML = "";
        
        // Headers (Capacidades de 0 a capacity)
        const thLabel = document.createElement("th");
        thLabel.textContent = "Microservicio incorporado";
        headersTr.appendChild(thLabel);
        
        result.step_by_step_table.headers.forEach(h => {
            const th = document.createElement("th");
            th.textContent = h;
            headersTr.appendChild(th);
        });

        // Filas de datos
        result.step_by_step_table.rows.forEach((row, rIdx) => {
            const tr = document.createElement("tr");
            
            const tdLabel = document.createElement("td");
            tdLabel.className = "row-header";
            tdLabel.textContent = row.row_label;
            tr.appendChild(tdLabel);
            
            row.values.forEach((val, cIdx) => {
                const td = document.createElement("td");
                td.textContent = val;
                
                // Resaltar la última celda óptima
                if (rIdx === result.step_by_step_table.rows.length - 1 && cIdx === row.values.length - 1) {
                    td.style.backgroundColor = "var(--color-primary-glow)";
                    td.style.color = "var(--color-primary)";
                    td.style.fontWeight = "700";
                    td.style.border = "1px solid var(--color-primary)";
                }
                tr.appendChild(td);
            });
            
            bodyTbody.appendChild(tr);
        });
    },

    // ----------------------------------------------------
    // INGRESO Y DISEÑO DE ENRUTAMIENTO (Ruta de Latencia)
    // ----------------------------------------------------
    renderRoutingInputs(stages, connections) {
        // 1. Mostrar etapas e inputs
        const stagesContainer = document.getElementById("routing-stages-inputs");
        stagesContainer.innerHTML = "";
        
        stages.forEach((stageNodes, sIdx) => {
            const div = document.createElement("div");
            div.className = "stage-input-row";
            div.style.marginBottom = "8px";
            div.innerHTML = `
                <span>Etapa ${sIdx + 1}:</span>
                <input type="text" value="${stageNodes.join(', ')}" class="stage-nodes-input" data-index="${sIdx}">
            `;
            stagesContainer.appendChild(div);
        });

        // Actualizar indicadores del Dashboard
        document.getElementById("mini-nodes-count").textContent = `${stages.flat().length} (${stages[0][0]} - ${stages[stages.length - 1][0]})`;

        // 2. Editor de latencias de conexiones
        const connectionsContainer = document.getElementById("connections-editor-list");
        connectionsContainer.innerHTML = "";
        
        // Iteramos de manera ordenada por las etapas
        for (let s = 0; s < stages.length - 1; s++) {
            const fromNodes = stages[s];
            const toNodes = stages[s+1];
            
            fromNodes.forEach(fromNode => {
                toNodes.forEach(toNode => {
                    const latVal = connections[fromNode] ? connections[fromNode][toNode] : null;
                    if (latVal !== null && latVal !== undefined) {
                        const row = document.createElement("div");
                        row.className = "connection-edit-row";
                        row.innerHTML = `
                            <span>Nodo <b>${fromNode}</b> → Nodo <b>${toNode}</b>:</span>
                            <input type="number" value="${latVal}" min="1" step="0.5" class="latency-input" data-from="${fromNode}" data-to="${toNode}">
                            <span>ms</span>
                        `;
                        connectionsContainer.appendChild(row);
                    }
                });
            });
        }
    },

    renderRoutingResults(result) {
        document.getElementById("routing-min-cost").textContent = `${result.min_cost.toFixed(1)} ms`;
        document.getElementById("routing-optimal-path").textContent = result.optimal_path.join(" → ");
        
        // Actualizar dashboard
        document.getElementById("dash-latency-val").textContent = `${result.min_cost.toFixed(1)} ms`;
        document.getElementById("dash-latency-lbl").textContent = `Ruta: ${result.optimal_path.join("→")}`;

        // Renderizar Tablas Paso a Paso de las Etapas
        const tablesContainer = document.getElementById("routing-stage-tables-container");
        tablesContainer.innerHTML = "";
        
        result.step_by_step_tables.forEach(table => {
            const tableDiv = document.createElement("div");
            tableDiv.style.marginBottom = "24px";
            
            const title = document.createElement("h4");
            title.innerHTML = `<i data-lucide="table"></i> ${table.descripcion}`;
            title.style.fontSize = "0.9rem";
            title.style.color = "var(--color-primary)";
            title.style.marginBottom = "8px";
            tableDiv.appendChild(title);
            
            const scrollDiv = document.createElement("div");
            scrollDiv.className = "table-scroll-container";
            
            const htmlTable = document.createElement("table");
            htmlTable.className = "matrix-table";
            
            // Header
            const thead = document.createElement("thead");
            const headerTr = document.createElement("tr");
            table.headers.forEach(h => {
                const th = document.createElement("th");
                th.textContent = h;
                headerTr.appendChild(th);
            });
            thead.appendChild(headerTr);
            htmlTable.appendChild(thead);
            
            // Body
            const tbody = document.createElement("tbody");
            table.rows.forEach(row => {
                const tr = document.createElement("tr");
                row.forEach((cell, cellIdx) => {
                    const td = document.createElement("td");
                    td.textContent = cell;
                    
                    // Si es la columna de estado, poner estilo
                    if (cellIdx === 0) {
                        td.className = "row-header";
                    }
                    
                    // Si el valor coincide con la mejor decisión o mejor costo, resaltar levemente
                    if (cellIdx === row.length - 1 && cell !== "None") {
                        // Columna d*(s)
                        td.style.color = "var(--color-accent)";
                        td.style.fontWeight = "600";
                    }
                    if (cellIdx === row.length - 2) {
                        // Columna f*(s)
                        td.style.color = "var(--color-primary)";
                        td.style.fontWeight = "600";
                    }
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            });
            htmlTable.appendChild(tbody);
            scrollDiv.appendChild(htmlTable);
            tableDiv.appendChild(scrollDiv);
            tablesContainer.appendChild(tableDiv);
        });

        // Dibujar el Grafo Interactivo
        this.drawRoutingGraph(result.stages_data, result.connections_data, result.optimal_path);
        
        lucide.createIcons();
    },

    drawRoutingGraph(stages, connections, optimalPath) {
        const canvas = document.getElementById("routing-canvas");
        if (!canvas) return;
        
        const ctx = canvas.getContext("2d");
        
        // Ajustar ancho real del canvas al tamaño del contenedor
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * window.devicePixelRatio;
        canvas.height = rect.height * window.devicePixelRatio;
        ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
        
        const width = rect.width;
        const height = rect.height;
        
        // Limpiar
        ctx.clearRect(0, 0, width, height);
        
        // Calcular coordenadas físicas para cada nodo
        const nodeCoords = {};
        const stageSpacing = width / (stages.length + 1);
        
        stages.forEach((stageNodes, sIdx) => {
            const x = stageSpacing * (sIdx + 1);
            const numNodes = stageNodes.length;
            const nodeSpacing = height / (numNodes + 1);
            
            stageNodes.forEach((node, nIdx) => {
                const y = nodeSpacing * (nIdx + 1);
                nodeCoords[node] = { x, y, stage: sIdx };
            });
        });

        // 1. Dibujar conexiones (Aristas)
        for (const fromNode in connections) {
            const fromCoord = nodeCoords[fromNode];
            if (!fromCoord) continue;
            
            for (const toNode in connections[fromNode]) {
                const toCoord = nodeCoords[toNode];
                if (!toCoord) continue;
                
                const latency = connections[fromNode][toNode];
                
                // Determinar si la conexión es parte de la ruta óptima
                const isOptimalConnection = this.isConnectionInPath(fromNode, toNode, optimalPath);
                
                // Estilo de arista
                ctx.beginPath();
                ctx.moveTo(fromCoord.x, fromCoord.y);
                ctx.lineTo(toCoord.x, toCoord.y);
                
                if (isOptimalConnection) {
                    ctx.strokeStyle = "rgba(56, 189, 248, 0.9)";
                    ctx.lineWidth = 3.5;
                    ctx.shadowColor = "#38bdf8";
                    ctx.shadowBlur = 10;
                } else {
                    ctx.strokeStyle = "rgba(255, 255, 255, 0.12)";
                    ctx.lineWidth = 1;
                    ctx.shadowBlur = 0;
                }
                ctx.stroke();
                
                // Dibujar el costo de latencia (Texto) sobre la línea
                const midX = (fromCoord.x + toCoord.x) / 2;
                const midY = (fromCoord.y + toCoord.y) / 2 - 6;
                ctx.shadowBlur = 0;
                ctx.fillStyle = isOptimalConnection ? "#38bdf8" : "rgba(255, 255, 255, 0.4)";
                ctx.font = isOptimalConnection ? "bold 10px var(--font-mono)" : "9px var(--font-mono)";
                ctx.textAlign = "center";
                ctx.fillText(`${latency}ms`, midX, midY);
            }
        }

        // 2. Dibujar nodos
        ctx.shadowBlur = 0;
        for (const nodeName in nodeCoords) {
            const coord = nodeCoords[nodeName];
            const isOptimalNode = optimalPath.includes(nodeName);
            
            // Dibujar círculo exterior
            ctx.beginPath();
            ctx.arc(coord.x, coord.y, 16, 0, Math.PI * 2);
            
            if (isOptimalNode) {
                ctx.fillStyle = "rgba(56, 189, 248, 0.2)";
                ctx.strokeStyle = "#38bdf8";
                ctx.lineWidth = 2.5;
                ctx.shadowColor = "#38bdf8";
                ctx.shadowBlur = 8;
            } else {
                ctx.fillStyle = "rgba(11, 19, 41, 0.9)";
                ctx.strokeStyle = "rgba(255, 255, 255, 0.25)";
                ctx.lineWidth = 1.5;
                ctx.shadowBlur = 0;
            }
            ctx.fill();
            ctx.stroke();
            ctx.shadowBlur = 0;
            
            // Texto del Nodo
            ctx.fillStyle = isOptimalNode ? "#ffffff" : "#94a3b8";
            ctx.font = "bold 11px var(--font-sans)";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(nodeName, coord.x, coord.y);
        }
    },

    isConnectionInPath(fromNode, toNode, path) {
        for (let i = 0; i < path.length - 1; i++) {
            if (path[i] === fromNode && path[i + 1] === toNode) {
                return true;
            }
        }
        return false;
    },

    // ----------------------------------------------------
    // MÓDULO DE MARKETING (Optimización No Lineal)
    // ----------------------------------------------------
    renderMarketingResults(result) {
        const opt = result.constrained_optimum;
        const budget = result.budget;
        
        // Usuarios estimados y estado
        document.getElementById("mkt-max-acquisition").textContent = `${(opt.value * 1000).toLocaleString('es-ES', {maximumFractionDigits:0})} nuevos jugadores`;
        document.getElementById("mini-mkt-budget").textContent = `$${(budget * 1000).toLocaleString('es-ES', {minimumFractionDigits:2, maximumFractionDigits:2})}`;
        
        // Dashboard principal
        document.getElementById("dash-users-val").textContent = `${(opt.value * 1000).toLocaleString('es-ES', {maximumFractionDigits:0})} usuarios`;
        document.getElementById("dash-users-lbl").textContent = `Retorno máximo asignado`;

        const isBudgetActive = result.is_budget_active;
        const statusEl = document.getElementById("mkt-constraint-status");
        if (isBudgetActive) {
            statusEl.textContent = "Presupuesto Agotado ($100% Utilizado)";
            statusEl.style.color = "var(--color-primary)";
        } else {
            statusEl.textContent = "Presupuesto Libre (Máximo Irrestricto alcanzado)";
            statusEl.style.color = "var(--color-success)";
        }

        // Montos e indicadores de barra
        const x1Val = opt.x1;
        const x2Val = opt.x2;
        
        const x1Pct = budget > 0 ? (x1Val / budget) * 100 : 0;
        const x2Pct = budget > 0 ? (x2Val / budget) * 100 : 0;
        
        document.getElementById("mkt-x1-val").textContent = `$${(x1Val * 1000).toLocaleString('es-ES', {minimumFractionDigits:2, maximumFractionDigits:2})} (${x1Pct.toFixed(1)}%)`;
        document.getElementById("mkt-x2-val").textContent = `$${(x2Val * 1000).toLocaleString('es-ES', {minimumFractionDigits:2, maximumFractionDigits:2})} (${x2Pct.toFixed(1)}%)`;
        
        document.getElementById("mkt-x1-fill").style.width = `${x1Pct}%`;
        document.getElementById("mkt-x2-fill").style.width = `${x2Pct}%`;

        // Datos del Máximo Teórico Irrestricto
        const unconstrained = result.unconstrained_optimum;
        const descBox = document.getElementById("mkt-unconstrained-desc");
        if (unconstrained.x1 === "inf") {
            descBox.textContent = "No existe un máximo global cerrado (coeficientes nulos o divergentes).";
        } else {
            descBox.innerHTML = `El punto de saturación absoluto ocurre en:<br/>
            • Creadores ($x_1$): <b>$${(unconstrained.x1 * 1000).toLocaleString('es-ES', {maximumFractionDigits:2})} USD</b><br/>
            • Anuncios ($x_2$): <b>$${(unconstrained.x2 * 1000).toLocaleString('es-ES', {maximumFractionDigits:2})} USD</b><br/>
            • Presupuesto requerido: <b>$${((unconstrained.x1 + unconstrained.x2) * 1000).toLocaleString('es-ES', {maximumFractionDigits:2})} USD</b>.`;
        }

        // Dibujar curva no lineal en Canvas
        this.drawMarketingChart(result.chart_points, opt);
    },

    drawMarketingChart(points, optimal) {
        const canvas = document.getElementById("marketing-canvas");
        if (!canvas) return;
        
        const ctx = canvas.getContext("2d");
        
        const rect = canvas.getBoundingClientRect();
        canvas.width = rect.width * window.devicePixelRatio;
        canvas.height = rect.height * window.devicePixelRatio;
        ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
        
        const w = rect.width;
        const h = rect.height;
        
        ctx.clearRect(0, 0, w, h);
        
        // Márgenes del gráfico
        const padding = { top: 20, right: 30, bottom: 40, left: 50 };
        const chartW = w - padding.left - padding.right;
        const chartH = h - padding.top - padding.bottom;
        
        // Encontrar escalas
        const maxValY = Math.max(...points.map(p => p.acquisition)) * 1.15;
        const maxValX = Math.max(...points.map(p => p.x1));
        
        const getX = (x1) => padding.left + (x1 / maxValX) * chartW;
        const getY = (acq) => padding.top + chartH - (acq / maxValY) * chartH;

        // 1. Dibujar cuadrícula de fondo
        ctx.strokeStyle = "rgba(255, 255, 255, 0.05)";
        ctx.lineWidth = 1;
        
        // Grid vertical
        for (let i = 0; i <= 5; i++) {
            const x1Val = (maxValX / 5) * i;
            const xPos = getX(x1Val);
            ctx.beginPath();
            ctx.moveTo(xPos, padding.top);
            ctx.lineTo(xPos, padding.top + chartH);
            ctx.stroke();
            
            // Etiquetas del eje X
            ctx.fillStyle = "rgba(255,255,255,0.4)";
            ctx.font = "9px var(--font-sans)";
            ctx.textAlign = "center";
            ctx.fillText(`$${x1Val.toFixed(1)}k`, xPos, padding.top + chartH + 15);
        }

        // Grid horizontal
        for (let i = 0; i <= 4; i++) {
            const acqVal = (maxValY / 4) * i;
            const yPos = getY(acqVal);
            ctx.beginPath();
            ctx.moveTo(padding.left, yPos);
            ctx.lineTo(padding.left + chartW, yPos);
            ctx.stroke();
            
            // Etiquetas del eje Y
            ctx.fillStyle = "rgba(255,255,255,0.4)";
            ctx.font = "9px var(--font-sans)";
            ctx.textAlign = "right";
            ctx.fillText(`${(acqVal * 1000).toFixed(0)}`, padding.left - 10, yPos + 3);
        }

        // Ejes principales
        ctx.strokeStyle = "rgba(255, 255, 255, 0.25)";
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(padding.left, padding.top);
        ctx.lineTo(padding.left, padding.top + chartH);
        ctx.lineTo(padding.left + chartW, padding.top + chartH);
        ctx.stroke();

        // 2. Dibujar la curva no lineal g(x1) frente al presupuesto total active
        ctx.beginPath();
        points.forEach((p, idx) => {
            const px = getX(p.x1);
            const py = getY(p.acquisition);
            if (idx === 0) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
        });
        
        ctx.strokeStyle = "var(--color-secondary)";
        ctx.lineWidth = 3;
        ctx.stroke();
        
        // Relleno degradado bajo la curva
        const grad = ctx.createLinearGradient(0, padding.top, 0, padding.top + chartH);
        grad.addColorStop(0, "rgba(192, 132, 252, 0.18)");
        grad.addColorStop(1, "rgba(192, 132, 252, 0)");
        
        ctx.lineTo(getX(points[points.length-1].x1), padding.top + chartH);
        ctx.lineTo(getX(points[0].x1), padding.top + chartH);
        ctx.closePath();
        ctx.fillStyle = grad;
        ctx.fill();

        // 3. Resaltar el Punto Óptimo Máximo Calculado
        const optX = getX(optimal.x1);
        const optY = getY(optimal.value);
        
        // Líneas punteadas hacia los ejes
        ctx.strokeStyle = "rgba(56, 189, 248, 0.5)";
        ctx.lineWidth = 1.5;
        ctx.setLineDash([4, 4]);
        
        ctx.beginPath();
        ctx.moveTo(optX, optY);
        ctx.lineTo(optX, padding.top + chartH);
        ctx.moveTo(optX, optY);
        ctx.lineTo(padding.left, optY);
        ctx.stroke();
        ctx.setLineDash([]); // Reset
        
        // Círculo óptimo
        ctx.beginPath();
        ctx.arc(optX, optY, 6, 0, Math.PI * 2);
        ctx.fillStyle = "#38bdf8";
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = 2;
        ctx.shadowColor = "#38bdf8";
        ctx.shadowBlur = 8;
        ctx.fill();
        ctx.stroke();
        ctx.shadowBlur = 0;
        
        // Etiqueta del valor óptimo
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 10px var(--font-sans)";
        ctx.textAlign = "left";
        ctx.fillText(`Óptimo: ${(optimal.value * 1000).toFixed(0)} usuarios (x1=$${optimal.x1.toFixed(1)}k, x2=$${optimal.x2.toFixed(1)}k)`, optX + 10, optY - 8);
    },

    // ----------------------------------------------------
    // MÓDULO DE IA Y REPORTE (Groq & PDF)
    // ----------------------------------------------------
    renderAiLoading() {
        const body = document.getElementById("ai-content-body");
        body.innerHTML = `
            <div class="ai-loading-box">
                <div class="spinner"></div>
                <p>Estableciendo conexión asíncrona con Groq...</p>
                <p style="font-size: 0.8rem; color: var(--text-dark); margin-top: 5px">Calculando dictamen del CTO a través de llama3-8b-8192...</p>
            </div>
        `;
    },

    renderAiResult(markdownText) {
        const body = document.getElementById("ai-content-body");
        
        // Traductor sencillo de markdown a HTML para renderizar el texto enriquecido de Groq
        let html = markdownText
            .replace(/\r\n/g, "\n")
            // Título 1 (#)
            .replace(/^#\s+(.+)$/gm, "<h1>$1</h1>")
            // Título 2 (##)
            .replace(/^##\s+(.+)$/gm, "<h2>$1</h2>")
            // Título 3 (###)
            .replace(/^###\s+(.+)$/gm, "<h3>$1</h3>")
            // Negritas
            .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>")
            // Listas desordenadas (* o -)
            .replace(/^\*\s+(.+)$/gm, "<li>$1</li>")
            .replace(/^-\s+(.+)$/gm, "<li>$1</li>")
            // Listas numeradas (ej: 1.)
            .replace(/^\d+\.\s+(.+)$/gm, "<li>$1</li>");
            
        // Envolver grupos de <li> secuenciales en un <ul>
        // Este es un wrapper simple de render
        html = html.replace(/(<li>.+?<\/li>)/gs, "<ul>$1<\/ul>");
        // Reemplazar saltos de línea repetidos por párrafos para evitar que quede pegado
        html = html.split("\n\n").map(p => {
            if (!p.trim().startsWith("<h") && !p.trim().startsWith("<u") && p.trim()) {
                return `<p>${p.trim()}</p>`;
            }
            return p.trim();
        }).join("");

        body.innerHTML = html;
        
        // Habilitar botón de PDF
        const btnPdf = document.getElementById("btn-download-pdf");
        if (btnPdf) btnPdf.removeAttribute("disabled");
    },

    renderAiError(errorMessage) {
        const body = document.getElementById("ai-content-body");
        body.innerHTML = `
            <div class="empty-ai-message" style="color: var(--color-error)">
                <i data-lucide="alert-triangle"></i>
                <p><b>Error al procesar el análisis de la IA:</b></p>
                <p style="font-size: 0.8rem; margin-top: 5px">${errorMessage}</p>
            </div>
        `;
        lucide.createIcons();
    }
};
