import io
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

class PdfService:
    """
    Servicio de generación de reportes PDF formales utilizando ReportLab.
    Genera un informe técnico corporativo completo con tablas y análisis de negocio.
    """
    
    @staticmethod
    def generate_report(
        knapsack_res: Dict[str, Any],
        routing_res: Dict[str, Any],
        marketing_res: Dict[str, Any],
        ai_conclusions: str
    ) -> bytes:
        """
        Crea un PDF en memoria y devuelve los bytes del archivo generado.
        """
        buffer = io.BytesIO()
        
        # Configurar el documento
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=54,
            leftMargin=54,
            topMargin=54,
            bottomMargin=54
        )
        
        story = []
        
        # Paleta de colores institucionales
        PRIMARY_COLOR = colors.HexColor("#0f172a")    # Azul Oscuro (Deep slate)
        SECONDARY_COLOR = colors.HexColor("#0284c7")  # Azul Claro (Sky blue)
        ACCENT_COLOR = colors.HexColor("#0f766e")     # Verde Teal
        TEXT_COLOR = colors.HexColor("#334155")       # Gris de Texto
        LIGHT_BG = colors.HexColor("#f8fafc")         # Fondo gris claro para tablas
        
        # Hojas de estilo
        styles = getSampleStyleSheet()
        
        # Modificar y agregar estilos personalizados
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=PRIMARY_COLOR,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'DocSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            leading=16,
            textColor=SECONDARY_COLOR,
            alignment=TA_CENTER
        )
        
        h1_style = ParagraphStyle(
            'SectionH1',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=16,
            leading=20,
            textColor=PRIMARY_COLOR,
            spaceBefore=15,
            spaceAfter=8,
            keepWithNext=True
        )

        h2_style = ParagraphStyle(
            'SectionH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            textColor=SECONDARY_COLOR,
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True
        )

        body_style = ParagraphStyle(
            'DocBody',
            parent=styles['BodyText'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=TEXT_COLOR,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        )
        
        bold_body_style = ParagraphStyle(
            'DocBodyBold',
            parent=body_style,
            fontName='Helvetica-Bold'
        )

        table_header_style = ParagraphStyle(
            'TableHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=10,
            textColor=colors.white,
            alignment=TA_CENTER
        )

        table_cell_style = ParagraphStyle(
            'TableCell',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=10,
            textColor=TEXT_COLOR,
            alignment=TA_CENTER
        )

        table_cell_left_style = ParagraphStyle(
            'TableCellLeft',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            leading=10,
            textColor=TEXT_COLOR,
            alignment=TA_LEFT
        )

        ai_header_style = ParagraphStyle(
            'AiHeader',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            textColor=ACCENT_COLOR,
            spaceBefore=12,
            spaceAfter=6,
            keepWithNext=True
        )

        # ----------------------------------------------------
        # 1. ENCABEZADO / TÍTULO DE PORTADA
        # ----------------------------------------------------
        story.append(Paragraph("NEXUSCORE SYSTEMS", subtitle_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph("INFORME TÉCNICO DE OPTIMIZACIÓN OPERACIONAL", title_style))
        story.append(Spacer(1, 5))
        story.append(Paragraph("Plataforma Inteligente de Soporte a Decisiones en Infraestructura y Marketing", subtitle_style))
        story.append(Spacer(1, 20))
        
        # Línea divisoria decorativa
        line_table = Table([[""]], colWidths=[504], rowHeights=[3])
        line_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), SECONDARY_COLOR),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(line_table)
        story.append(Spacer(1, 15))
        
        # Resumen ejecutivo
        story.append(Paragraph(
            "<b>Resumen Ejecutivo:</b> Este informe consolida los resultados cuantitativos y cualitativos "
            "obtenidos para la toma de decisiones estratégicas. En las secciones siguientes, se detallan las "
            "soluciones óptimas a los problemas de carga de servidores (mediante Programación Dinámica), "
            "enrutamiento en red de baja latencia (Programación Dinámica Backward), asignación de presupuesto "
            "publicitario no lineal y, finalmente, un dictamen experto emitido por nuestro asistente de IA (CTO).",
            body_style
        ))
        
        # ----------------------------------------------------
        # 2. PARTE I: PROGRAMACIÓN DINÁMICA
        # ----------------------------------------------------
        story.append(Paragraph("Parte I: Programación Dinámica y Enrutamiento Eficiente", h1_style))
        
        # SUB-PROBLEMA A: Mochila (Carga de Servidores)
        story.append(Paragraph("Sub-problema A: El Problema de la Carga de Servidores (Volumen de Carga)", h2_style))
        story.append(Paragraph(
            f"El objetivo es maximizar la estabilidad total del sistema desplegando microservicios críticos en un "
            f"servidor maestro con capacidad de <b>{knapsack_res.get('capacity', 0)} GB</b>. "
            f"La optimización matemática dio como resultado un valor de estabilidad máximo de <b>{knapsack_res.get('max_value', 0)}</b> "
            f"utilizando un total de <b>{knapsack_res.get('used_weight', 0)} GB</b> de memoria RAM.",
            body_style
        ))
        
        # Lista de Microservicios Seleccionados
        story.append(Paragraph("<b>Microservicios Seleccionados para el Despliegue:</b>", body_style))
        selected_text = ""
        for item in knapsack_res.get('selected_items', []):
            selected_text += f"• <b>{item['name']}</b> (RAM: {item['weight']} GB | Prioridad: {item['value']})<br/>"
        story.append(Paragraph(selected_text if selected_text else "Ninguno.", body_style))
        story.append(Spacer(1, 10))

        # Tabla paso a paso de Mochila
        story.append(Paragraph("<b>Matriz de Decisiones Paso a Paso (Programación Dinámica):</b>", body_style))
        
        dp_table_data = knapsack_res.get('step_by_step_table', {})
        raw_headers = dp_table_data.get('headers', [])
        raw_rows = dp_table_data.get('rows', [])
        
        # Filtrar o adaptar las columnas si son demasiadas para que no se desborden de la página
        # La página de ancho utilizable tiene 504 ptos.
        max_cols_to_show = 11  # Mostrar capacidades hasta 10GB en PDF para legibilidad física
        cols_limit = min(len(raw_headers), max_cols_to_show)
        
        headers_pdf = [Paragraph("Microservicio / RAM", table_header_style)] + [Paragraph(raw_headers[c], table_header_style) for c in range(cols_limit)]
        if len(raw_headers) > max_cols_to_show:
            headers_pdf.append(Paragraph("...", table_header_style))
            headers_pdf.append(Paragraph(raw_headers[-1], table_header_style))
            
        rows_pdf = []
        for row in raw_rows:
            label = row["row_label"]
            vals = row["values"]
            pdf_row = [Paragraph(label, table_cell_left_style)]
            
            for c in range(cols_limit):
                pdf_row.append(Paragraph(str(vals[c]), table_cell_style))
                
            if len(raw_headers) > max_cols_to_show:
                pdf_row.append(Paragraph("...", table_cell_style))
                pdf_row.append(Paragraph(str(vals[-1]), table_cell_style))
                
            rows_pdf.append(pdf_row)
            
        knap_table = Table([headers_pdf] + rows_pdf)
        knap_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 4),
        ]))
        
        story.append(knap_table)
        story.append(Spacer(1, 15))
        
        # SUB-PROBLEMA B: Grafo por Etapas
        story.append(Paragraph("Sub-problema B: Red de Distribución de Datos (Grafos por Etapas)", h2_style))
        story.append(Paragraph(
            f"Se ha calculado la ruta crítica de menor latencia acumulada desde el servidor de origen (Nodo "
            f"<b>{routing_res.get('start_node', 'A')}</b>) hasta los servidores de respaldo regionales (Nodo "
            f"<b>{routing_res.get('end_node', 'J')}</b>) mediante programación dinámica Backward. "
            f"La latencia crítica mínima obtenida es de <b>{routing_res.get('min_cost', 0.0)} ms</b>, "
            f"siguiendo la ruta: <b>{' → '.join(routing_res.get('optimal_path', []))}</b>.",
            body_style
        ))
        
        # Tablas de decisión de cada etapa
        story.append(Paragraph("<b>Tablas de Decisión de Programación Dinámica Backward:</b>", body_style))
        for table in routing_res.get('step_by_step_tables', []):
            headers = [Paragraph(h, table_header_style) for h in table["headers"]]
            rows = []
            for row in table["rows"]:
                rows.append([Paragraph(str(cell), table_cell_style) for cell in row])
                
            etapa_table = Table([headers] + rows)
            etapa_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), SECONDARY_COLOR),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
            ]))
            
            # Encapsular cada etapa con su título
            story.append(KeepTogether([
                Paragraph(f"<b>{table['descripcion']}</b>", body_style),
                etapa_table,
                Spacer(1, 8)
            ]))
            
        story.append(PageBreak())  # Salto de página para el análisis estratégico e IA
        
        # ----------------------------------------------------
        # 3. PARTE II: OPTIMIZACIÓN NO LINEAL
        # ----------------------------------------------------
        story.append(Paragraph("Parte II: Optimización de Problemas No Lineales (Presupuesto de Marketing)", h1_style))
        
        marketing_opt = marketing_res.get('constrained_optimum', {})
        story.append(Paragraph(
            f"Para el lanzamiento estratégico, se distribuyó un presupuesto total de "
            f"<b>${marketing_res.get('budget', 0.0) * 1000:,.2f}</b> para maximizar la adquisición mensual de usuarios. "
            f"Utilizando bisección y refinamiento en malla fina sobre el modelo no lineal de rendimientos marginales, "
            f"la asignación óptima de recursos calculada es:",
            body_style
        ))
        
        # Tabla resumen marketing
        mkt_headers = [
            Paragraph("Variable publicitaria", table_header_style),
            Paragraph("Porcentaje de inversión", table_header_style),
            Paragraph("Monto asignado", table_header_style)
        ]
        
        x1_val = marketing_opt.get('x1', 0.0)
        x2_val = marketing_opt.get('x2', 0.0)
        budget_tot = marketing_res.get('budget', 1.0)
        
        x1_pct = (x1_val / budget_tot) * 100 if budget_tot > 0 else 0
        x2_pct = (x2_val / budget_tot) * 100 if budget_tot > 0 else 0
        
        mkt_rows = [
            [Paragraph("Campañas de Creadores de Contenido (x1)", table_cell_left_style), Paragraph(f"{x1_pct:.1f}%", table_cell_style), Paragraph(f"${x1_val * 1000:,.2f}", table_cell_style)],
            [Paragraph("Anuncios Programáticos (x2)", table_cell_left_style), Paragraph(f"{x2_pct:.1f}%", table_cell_style), Paragraph(f"${x2_val * 1000:,.2f}", table_cell_style)],
            [Paragraph("<b>Retorno Total Estimado</b>", table_cell_left_style), Paragraph("-", table_cell_style), Paragraph(f"<b>{marketing_opt.get('value', 0.0) * 1000:,.0f} usuarios/mes</b>", table_cell_style)]
        ]
        
        mkt_table = Table([mkt_headers] + mkt_rows, colWidths=[250, 110, 144])
        mkt_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
        ]))
        
        story.append(mkt_table)
        story.append(Spacer(1, 15))

        # ----------------------------------------------------
        # 4. PARTE III: CONCLUSIONES DE IA (CTO)
        # ----------------------------------------------------
        story.append(Paragraph("Parte III: Conclusiones Estratégicas del Asistente de IA (CTO)", h1_style))
        story.append(Paragraph(
            "La siguiente sección ha sido generada por el motor inteligente de Groq empleando modelos de "
            "alto rendimiento, proporcionando un análisis de viabilidad cualitativo sobre los resultados:",
            body_style
        ))
        
        # Procesar las conclusiones de IA de Markdown a párrafos de ReportLab
        # Haremos una traducción básica de Markdown a párrafos estilizados.
        lines = ai_conclusions.split('\n')
        in_list = False
        
        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue
            
            # Saltar notas informativas sobre la API Key si están presentes en la simulación
            if "⚠️ Nota del Sistema" in line_str or "*Esta es una conclusión" in line_str:
                continue
            
            # Título 1 (#)
            if line_str.startswith("# "):
                title_text = line_str[2:]
                story.append(Paragraph(title_text, ai_header_style))
                story.append(Spacer(1, 4))
            # Título 2 (##)
            elif line_str.startswith("## "):
                title_text = line_str[3:]
                story.append(Paragraph(title_text, h2_style))
                story.append(Spacer(1, 4))
            # Título 3 (###)
            elif line_str.startswith("### "):
                title_text = line_str[4:]
                story.append(Paragraph(f"<b>{title_text}</b>", bold_body_style))
                story.append(Spacer(1, 4))
            # Elementos de viñeta (lista)
            elif line_str.startswith("* ") or line_str.startswith("- "):
                list_text = line_str[2:]
                # Convertir negrita Markdown (**) a HTML (<b>)
                list_text = list_text.replace("**", "<b>", 1).replace("**", "</b>", 1)
                story.append(Paragraph(f"• {list_text}", body_style))
            # Elementos de lista numerada
            elif line_str.split('.')[0].isdigit():
                parts = line_str.split('.', 1)
                num = parts[0]
                text = parts[1].strip() if len(parts) > 1 else ""
                text = text.replace("**", "<b>", 1).replace("**", "</b>", 1)
                story.append(Paragraph(f"<b>{num}.</b> {text}", body_style))
            # Párrafo estándar
            else:
                text = line_str.replace("**", "<b>", 1).replace("**", "</b>", 1)
                story.append(Paragraph(text, body_style))
                
        # Construir el PDF
        doc.build(story)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
