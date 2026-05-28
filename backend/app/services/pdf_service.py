import io
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT


class ServicioPdf:
    """
    Servicio de generación de reportes PDF formales utilizando ReportLab.
    Construye el documento en memoria y lo retorna como bytes descargables.
    El reporte incluye: portada, tablas DP, resultados de marketing (con Lagrange),
    y el análisis cualitativo generado por la IA.
    """

    @staticmethod
    def generar_reporte(
        resultado_mochila:      Dict[str, Any],
        resultado_enrutamiento:  Dict[str, Any],
        resultado_marketing:    Dict[str, Any],
        conclusiones_ia:        str
    ) -> bytes:
        """
        Construye el PDF completo en memoria y retorna el contenido como bytes.
        Incluye todas las secciones del proyecto: DP, No Lineal, Lagrange, IA.
        """
        # Buffer en memoria donde se escribirá el PDF
        buffer = io.BytesIO()

        # Configurar el documento (tamaño carta, márgenes estándar)
        documento = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=54,
            leftMargin=54,
            topMargin=54,
            bottomMargin=54
        )

        # ----------------------------------------------------------------
        # PALETA DE COLORES INSTITUCIONALES
        # ----------------------------------------------------------------
        COLOR_PRIMARIO   = colors.HexColor("#0f172a")   # Azul oscuro corporativo
        COLOR_SECUNDARIO = colors.HexColor("#0284c7")   # Azul cielo para encabezados
        COLOR_ACENTO     = colors.HexColor("#0f766e")   # Verde teal para IA
        COLOR_TEXTO      = colors.HexColor("#334155")   # Gris de texto principal
        COLOR_FONDO_CLARO = colors.HexColor("#f8fafc")  # Fondo gris claro para tablas

        # ----------------------------------------------------------------
        # ESTILOS TIPOGRÁFICOS DEL DOCUMENTO
        # ----------------------------------------------------------------
        estilos_base = getSampleStyleSheet()

        estilo_titulo = ParagraphStyle(
            'TituloDocumento',
            parent=estilos_base['Normal'],
            fontName='Helvetica-Bold', fontSize=22, leading=26,
            textColor=COLOR_PRIMARIO, alignment=TA_CENTER
        )
        estilo_subtitulo = ParagraphStyle(
            'SubtituloDocumento',
            parent=estilos_base['Normal'],
            fontName='Helvetica', fontSize=12, leading=16,
            textColor=COLOR_SECUNDARIO, alignment=TA_CENTER
        )
        estilo_h1 = ParagraphStyle(
            'SeccionH1',
            parent=estilos_base['Heading1'],
            fontName='Helvetica-Bold', fontSize=16, leading=20,
            textColor=COLOR_PRIMARIO, spaceBefore=15, spaceAfter=8, keepWithNext=True
        )
        estilo_h2 = ParagraphStyle(
            'SeccionH2',
            parent=estilos_base['Heading2'],
            fontName='Helvetica-Bold', fontSize=12, leading=16,
            textColor=COLOR_SECUNDARIO, spaceBefore=10, spaceAfter=6, keepWithNext=True
        )
        estilo_cuerpo = ParagraphStyle(
            'CuerpoTexto',
            parent=estilos_base['BodyText'],
            fontName='Helvetica', fontSize=10, leading=14,
            textColor=COLOR_TEXTO, alignment=TA_JUSTIFY, spaceAfter=10
        )
        estilo_cuerpo_negrita = ParagraphStyle(
            'CuerpoNegrita', parent=estilo_cuerpo, fontName='Helvetica-Bold'
        )
        estilo_enc_tabla = ParagraphStyle(
            'EncabezadoTabla',
            parent=estilos_base['Normal'],
            fontName='Helvetica-Bold', fontSize=8, leading=10,
            textColor=colors.white, alignment=TA_CENTER
        )
        estilo_celda = ParagraphStyle(
            'CeldaTabla',
            parent=estilos_base['Normal'],
            fontName='Helvetica', fontSize=8, leading=10,
            textColor=COLOR_TEXTO, alignment=TA_CENTER
        )
        estilo_celda_izq = ParagraphStyle(
            'CeldaTablaIzquierda',
            parent=estilos_base['Normal'],
            fontName='Helvetica', fontSize=8, leading=10,
            textColor=COLOR_TEXTO, alignment=TA_LEFT
        )
        estilo_ia = ParagraphStyle(
            'EncabezadoIA',
            parent=estilos_base['Heading2'],
            fontName='Helvetica-Bold', fontSize=12, leading=16,
            textColor=COLOR_ACENTO, spaceBefore=12, spaceAfter=6, keepWithNext=True
        )

        # Lista de elementos del documento (contenido ordenado)
        contenido = []

        # ================================================================
        # SECCIÓN 0: PORTADA / ENCABEZADO
        # ================================================================
        contenido.append(Paragraph("NEXUSCORE SYSTEMS", estilo_subtitulo))
        contenido.append(Spacer(1, 10))
        contenido.append(Paragraph("INFORME TÉCNICO DE OPTIMIZACIÓN OPERACIONAL", estilo_titulo))
        contenido.append(Spacer(1, 5))
        contenido.append(Paragraph(
            "Plataforma Inteligente de Soporte a Decisiones en Infraestructura y Marketing",
            estilo_subtitulo
        ))
        contenido.append(Spacer(1, 20))

        # Línea decorativa
        linea_separadora = Table([[""]], colWidths=[504], rowHeights=[3])
        linea_separadora.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), COLOR_SECUNDARIO),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
        ]))
        contenido.append(linea_separadora)
        contenido.append(Spacer(1, 15))

        # Resumen ejecutivo
        contenido.append(Paragraph(
            "<b>Resumen Ejecutivo:</b> Este informe consolida los resultados cuantitativos y cualitativos "
            "de la plataforma de optimización de NexusCore Systems. Las secciones siguientes detallan: "
            "la asignación óptima de microservicios al servidor maestro (Programación Dinámica), "
            "la ruta de menor latencia en la red de distribución (DP Backward), "
            "la distribución óptima del presupuesto de marketing (Lagrange + Gradiente), "
            "y el análisis estratégico emitido por el asistente de IA en rol de CTO.",
            estilo_cuerpo
        ))

        # ================================================================
        # SECCIÓN I: PROGRAMACIÓN DINÁMICA
        # ================================================================
        contenido.append(Paragraph(
            "Parte I: Programación Dinámica y Enrutamiento Eficiente",
            estilo_h1
        ))

        # ---- Sub-problema A: Mochila ----
        contenido.append(Paragraph(
            "Sub-problema A: Carga de Servidores (Mochila 0/1)",
            estilo_h2
        ))
        capacidad_srv = resultado_mochila.get('capacidad', 0)
        val_maximo    = resultado_mochila.get('valor_maximo', 0)
        peso_usado    = resultado_mochila.get('peso_utilizado', 0)

        contenido.append(Paragraph(
            f"El algoritmo maximizó el Índice de Estabilidad del sistema desplegando microservicios "
            f"en un servidor con capacidad de <b>{capacidad_srv} GB</b>. "
            f"El valor de estabilidad máximo alcanzado es <b>{val_maximo}</b>, "
            f"consumiendo <b>{peso_usado} GB</b> de RAM.",
            estilo_cuerpo
        ))

        # Lista de microservicios seleccionados
        contenido.append(Paragraph("<b>Microservicios Seleccionados para el Despliegue:</b>", estilo_cuerpo))
        texto_servicios = ""
        for item in resultado_mochila.get('elementos_elegidos', []):
            texto_servicios += f"• <b>{item['nombre']}</b> (RAM: {item['peso']} GB | Prioridad: {item['valor']})<br/>"
        contenido.append(Paragraph(texto_servicios or "Ninguno.", estilo_cuerpo))
        contenido.append(Spacer(1, 10))

        # Tabla DP paso a paso
        contenido.append(Paragraph("<b>Matriz de Decisiones DP (Paso a Paso):</b>", estilo_cuerpo))

        tabla_dp_datos = resultado_mochila.get('tabla_paso_a_paso', {})
        encabezados_dp = tabla_dp_datos.get('encabezados', [])
        filas_dp       = tabla_dp_datos.get('filas', [])

        # Limitar columnas para evitar desbordamiento en el PDF
        max_cols = 11
        limite_cols = min(len(encabezados_dp), max_cols)

        enc_pdf = ([Paragraph("Microservicio / RAM", estilo_enc_tabla)]
                   + [Paragraph(encabezados_dp[c], estilo_enc_tabla) for c in range(limite_cols)])
        if len(encabezados_dp) > max_cols:
            enc_pdf += [Paragraph("...", estilo_enc_tabla), Paragraph(encabezados_dp[-1], estilo_enc_tabla)]

        filas_pdf = []
        for fila in filas_dp:
            etiqueta = fila["etiqueta_fila"]
            valores  = fila["valores"]
            fila_pdf = [Paragraph(etiqueta, estilo_celda_izq)]
            for c in range(limite_cols):
                fila_pdf.append(Paragraph(str(valores[c]), estilo_celda))
            if len(encabezados_dp) > max_cols:
                fila_pdf += [Paragraph("...", estilo_celda), Paragraph(str(valores[-1]), estilo_celda)]
            filas_pdf.append(fila_pdf)

        tabla_dp = Table([enc_pdf] + filas_pdf)
        tabla_dp.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARIO),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_FONDO_CLARO]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
        ]))
        contenido.append(tabla_dp)
        contenido.append(Spacer(1, 15))

        # ---- Sub-problema B: Grafo por Etapas ----
        contenido.append(Paragraph(
            "Sub-problema B: Red de Distribución de Datos (Grafos por Etapas)",
            estilo_h2
        ))
        nodo_ini     = resultado_enrutamiento.get('nodo_inicial', 'A')
        nodo_dst     = resultado_enrutamiento.get('nodo_destino', 'J')
        costo_min    = resultado_enrutamiento.get('costo_minimo', 0.0)
        ruta_optima  = resultado_enrutamiento.get('ruta_optima', [])

        contenido.append(Paragraph(
            f"Mediante DP Backward se calculó la ruta crítica desde el nodo "
            f"<b>{nodo_ini}</b> hasta el nodo <b>{nodo_dst}</b>. "
            f"La latencia mínima acumulada es de <b>{costo_min} ms</b>, "
            f"siguiendo la ruta: <b>{' → '.join(ruta_optima)}</b>.",
            estilo_cuerpo
        ))

        # Tablas de decisión por etapa
        contenido.append(Paragraph("<b>Tablas de Decisión DP Backward por Etapa:</b>", estilo_cuerpo))
        for tabla_etapa in resultado_enrutamiento.get('tablas_paso_a_paso', []):
            encabezados_et = [Paragraph(h, estilo_enc_tabla) for h in tabla_etapa["encabezados"]]
            filas_et = [
                [Paragraph(str(celda), estilo_celda) for celda in fila]
                for fila in tabla_etapa["filas"]
            ]
            tabla_obj = Table([encabezados_et] + filas_et)
            tabla_obj.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), COLOR_SECUNDARIO),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_FONDO_CLARO]),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
            ]))
            contenido.append(KeepTogether([
                Paragraph(f"<b>{tabla_etapa['descripcion']}</b>", estilo_cuerpo),
                tabla_obj,
                Spacer(1, 8)
            ]))

        contenido.append(PageBreak())

        # ================================================================
        # SECCIÓN II: OPTIMIZACIÓN NO LINEAL
        # ================================================================
        contenido.append(Paragraph(
            "Parte II: Optimización No Lineal (Presupuesto de Marketing)",
            estilo_h1
        ))

        opt_restringido = resultado_marketing.get('optimo_restringido', {})
        presupuesto_mkt = resultado_marketing.get('presupuesto', 0.0)
        x1_val  = opt_restringido.get('x1', 0.0)
        x2_val  = opt_restringido.get('x2', 0.0)
        val_mkt = opt_restringido.get('valor', 0.0)

        # Calcular porcentajes de inversión
        x1_pct = (x1_val / presupuesto_mkt * 100) if presupuesto_mkt > 0 else 0
        x2_pct = (x2_val / presupuesto_mkt * 100) if presupuesto_mkt > 0 else 0

        contenido.append(Paragraph(
            f"Para el lanzamiento estratégico, se distribuyó un presupuesto de "
            f"<b>${presupuesto_mkt * 1000:,.2f}</b> aplicando la función no lineal de "
            f"adquisición de usuarios con rendimientos marginales decrecientes.",
            estilo_cuerpo
        ))

        # Tabla resumen de la asignación óptima
        enc_mkt = [
            Paragraph("Variable publicitaria", estilo_enc_tabla),
            Paragraph("% de inversión", estilo_enc_tabla),
            Paragraph("Monto asignado", estilo_enc_tabla)
        ]
        filas_mkt = [
            [Paragraph("Campañas de Creadores de Contenido (x₁)", estilo_celda_izq),
             Paragraph(f"{x1_pct:.1f}%", estilo_celda),
             Paragraph(f"${x1_val * 1000:,.2f}", estilo_celda)],
            [Paragraph("Anuncios Programáticos (x₂)", estilo_celda_izq),
             Paragraph(f"{x2_pct:.1f}%", estilo_celda),
             Paragraph(f"${x2_val * 1000:,.2f}", estilo_celda)],
            [Paragraph("<b>Retorno Total Estimado</b>", estilo_celda_izq),
             Paragraph("-", estilo_celda),
             Paragraph(f"<b>{val_mkt * 1000:,.0f} usuarios/mes</b>", estilo_celda)]
        ]
        tabla_mkt = Table([enc_mkt] + filas_mkt, colWidths=[250, 110, 144])
        tabla_mkt.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLOR_PRIMARIO),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_FONDO_CLARO]),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]))
        contenido.append(tabla_mkt)
        contenido.append(Spacer(1, 12))

        # ---- Sub-sección: Método de Lagrange ----
        contenido.append(Paragraph("Método de Multiplicadores de Lagrange", estilo_h2))
        lagrange = resultado_marketing.get('metodo_lagrange', {})

        if "multiplicador_lambda" in lagrange:
            # Mostrar el planteamiento y resultado del método de Lagrange
            pasos = lagrange.get('pasos_detalle', {})
            contenido.append(Paragraph(
                f"Con la restricción presupuestaria activa (x₁ + x₂ = {presupuesto_mkt}), "
                f"se aplicó el Método de Lagrange obteniendo el multiplicador "
                f"<b>λ = {lagrange.get('multiplicador_lambda', 'N/A')}</b>.",
                estilo_cuerpo
            ))
            if pasos:
                for clave, valor_paso in pasos.items():
                    contenido.append(Paragraph(f"• {valor_paso}", estilo_cuerpo))
            interpretacion = lagrange.get('interpretacion', '')
            if interpretacion:
                contenido.append(Paragraph(f"<b>Interpretación:</b> {interpretacion}", estilo_cuerpo))
        elif "nota" in lagrange:
            contenido.append(Paragraph(lagrange["nota"], estilo_cuerpo))

        # ---- Sub-sección: Método de Gradiente ----
        contenido.append(Paragraph("Método de Ascenso de Gradiente Proyectado", estilo_h2))
        gradiente = resultado_marketing.get('metodo_gradiente', {})
        if gradiente:
            convergido    = gradiente.get('convergido', False)
            num_iters     = gradiente.get('iteraciones_totales', 0)
            x1_grad       = gradiente.get('x1_optimo', 0.0)
            x2_grad       = gradiente.get('x2_optimo', 0.0)
            valor_grad    = gradiente.get('valor_optimo', 0.0)
            tasa_apr      = gradiente.get('tasa_aprendizaje', 0.01)
            estado_conv   = "Sí (convergió)" if convergido else f"No (alcanzó el límite de {num_iters} iteraciones)"

            contenido.append(Paragraph(
                f"El algoritmo iterativo de Ascenso de Gradiente Proyectado ejecutó "
                f"<b>{num_iters} iteraciones</b> con tasa de aprendizaje α = {tasa_apr}. "
                f"Convergencia: <b>{estado_conv}</b>. "
                f"Solución obtenida: x₁ = {x1_grad}, x₂ = {x2_grad}, "
                f"f(x₁,x₂) = {valor_grad * 1000:.0f} usuarios.",
                estilo_cuerpo
            ))

        contenido.append(Spacer(1, 15))

        # ================================================================
        # SECCIÓN III: CONCLUSIONES DE IA (CTO)
        # ================================================================
        contenido.append(Paragraph(
            "Parte III: Conclusiones Estratégicas del Asistente de IA (CTO)",
            estilo_h1
        ))
        contenido.append(Paragraph(
            "La siguiente sección fue generada por el motor inteligente de Groq "
            "(modelo llama3-8b-8192), analizando los resultados desde la perspectiva "
            "de un Chief Technology Officer (CTO):",
            estilo_cuerpo
        ))

        # Procesar el texto Markdown de la IA y convertirlo a párrafos de ReportLab
        lineas = conclusiones_ia.split('\n')
        for linea in lineas:
            texto = linea.strip()
            if not texto:
                continue

            # Filtrar notas del sistema (avisos internos)
            if "⚠️ Nota del Sistema" in texto or "*Esta es una conclusión" in texto:
                continue

            # Título de nivel 1 (#)
            if texto.startswith("# "):
                contenido.append(Paragraph(texto[2:], estilo_ia))
            # Título de nivel 2 (##)
            elif texto.startswith("## "):
                contenido.append(Paragraph(texto[3:], estilo_h2))
            # Título de nivel 3 (###)
            elif texto.startswith("### "):
                contenido.append(Paragraph(f"<b>{texto[4:]}</b>", estilo_cuerpo_negrita))
            # Elemento de lista (viñeta * o -)
            elif texto.startswith("* ") or texto.startswith("- "):
                texto_item = texto[2:].replace("**", "<b>", 1).replace("**", "</b>", 1)
                contenido.append(Paragraph(f"• {texto_item}", estilo_cuerpo))
            # Lista numerada (1. , 2. , etc.)
            elif texto.split('.')[0].isdigit():
                partes = texto.split('.', 1)
                num    = partes[0]
                item   = partes[1].strip() if len(partes) > 1 else ""
                item   = item.replace("**", "<b>", 1).replace("**", "</b>", 1)
                contenido.append(Paragraph(f"<b>{num}.</b> {item}", estilo_cuerpo))
            # Párrafo normal
            else:
                texto = texto.replace("**", "<b>", 1).replace("**", "</b>", 1)
                contenido.append(Paragraph(texto, estilo_cuerpo))

        # ----------------------------------------------------------------
        # Construir el PDF con todo el contenido acumulado
        # ----------------------------------------------------------------
        documento.build(contenido)

        # Extraer los bytes del buffer y retornarlos
        bytes_pdf = buffer.getvalue()
        buffer.close()
        return bytes_pdf
