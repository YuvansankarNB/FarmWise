import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Group

# Register Tamil and English fonts
pdfmetrics.registerFont(TTFont('Latha', 'C:/Windows/Fonts/latha.ttf'))
pdfmetrics.registerFont(TTFont('LathaBold', 'C:/Windows/Fonts/lathab.ttf'))

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#64748b'))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 804, 'FarmWise AI — Technical & Agronomic Master Guide')
            self.setStrokeColor(colors.HexColor('#e2e8f0'))
            self.setLineWidth(0.6)
            self.line(54, 796, 541, 796)
            
        # Footer
        text = f'Page {self._pageNumber} of {page_count}'
        self.drawRightString(541, 35, text)
        self.drawString(54, 35, 'FARMWISE AI PLATFORM ARCHITECTURE • TASK 1 CAMPUS CHALLENGE')
        self.setStrokeColor(colors.HexColor('#e2e8f0'))
        self.setLineWidth(0.6)
        self.line(54, 46, 541, 46)
        self.restoreState()

def create_flowchart_soil():
    d = Drawing(480, 230)
    bg = Rect(0, 0, 480, 230, fillColor=colors.HexColor('#0f172a'), strokeColor=None, rx=8, ry=8)
    d.add(bg)

    def box(x, y, w, h, title, subtitle="", stroke='#38bdf8', fill='#1e293b'):
        g = Group()
        r = Rect(x, y, w, h, fillColor=colors.HexColor(fill), strokeColor=colors.HexColor(stroke), strokeWidth=1, rx=4, ry=4)
        g.add(r)
        t = String(x + w/2, y + h/2 + (4 if subtitle else -3), title, fontName='Helvetica-Bold', fontSize=8.5, fillColor=colors.white, textAnchor='middle')
        g.add(t)
        if subtitle:
            s = String(x + w/2, y + h/2 - 7, subtitle, fontName='Helvetica', fontSize=7, fillColor=colors.HexColor('#94a3b8'), textAnchor='middle')
            g.add(s)
        return g

    def down_arrow(x, y1, y2):
        g = Group()
        l = Line(x, y1, x, y2, strokeColor=colors.HexColor('#38bdf8'), strokeWidth=1)
        g.add(l)
        arr = String(x, y2 - 4, "v", fontName='Helvetica-Bold', fontSize=8, fillColor=colors.HexColor('#38bdf8'), textAnchor='middle')
        g.add(arr)
        return g

    d.add(box(160, 185, 160, 26, "Survey Number", "Cadastral Geo-Reference", stroke='#38bdf8'))
    d.add(down_arrow(240, 185, 165))
    d.add(box(140, 138, 200, 26, "Deterministic Soil Registry", "(SHA-256 Hash + TNAU Agro-Zones)", stroke='#10b981'))
    d.add(down_arrow(240, 138, 118))
    d.add(box(90, 80, 300, 36, "Chemical Soil Profile Generated", "pH: 8.2 (Alkaline) | OC: 0.42% (Low) | NPK: 170 / 12 / 260 kg/ha", stroke='#e2e8f0', fill='#090d16'))
    
    # Left & Right arrows
    d.add(down_arrow(160, 80, 52))
    d.add(down_arrow(320, 80, 52))
    d.add(box(50, 15, 190, 34, "Fertilizer Uptake Efficiency", "pH Penalty + OC Boost -> 62% Uptake", stroke='#f59e0b'))
    d.add(box(250, 15, 190, 34, "Soil Amendment Engine", "Gypsum 100 kg/ac + ZnSO4 10 kg/ac", stroke='#10b981'))
    return d

def create_flowchart_advisory():
    d = Drawing(480, 250)
    bg = Rect(0, 0, 480, 250, fillColor=colors.HexColor('#0f172a'), strokeColor=None, rx=8, ry=8)
    d.add(bg)

    def box(x, y, w, h, title, subtitle="", stroke='#38bdf8', fill='#1e293b'):
        g = Group()
        r = Rect(x, y, w, h, fillColor=colors.HexColor(fill), strokeColor=colors.HexColor(stroke), strokeWidth=1, rx=4, ry=4)
        g.add(r)
        t = String(x + w/2, y + h/2 + (4 if subtitle else -3), title, fontName='Helvetica-Bold', fontSize=8.5, fillColor=colors.white, textAnchor='middle')
        g.add(t)
        if subtitle:
            s = String(x + w/2, y + h/2 - 7, subtitle, fontName='Helvetica', fontSize=7, fillColor=colors.HexColor('#94a3b8'), textAnchor='middle')
            g.add(s)
        return g

    def down_arrow(x, y1, y2):
        g = Group()
        l = Line(x, y1, x, y2, strokeColor=colors.HexColor('#38bdf8'), strokeWidth=1)
        g.add(l)
        arr = String(x, y2 - 4, "v", fontName='Helvetica-Bold', fontSize=8, fillColor=colors.HexColor('#38bdf8'), textAnchor='middle')
        g.add(arr)
        return g

    d.add(box(60, 205, 160, 28, "Crop Phenotype (Img)", "Paddy - Active Tillering", stroke='#10b981'))
    d.add(box(260, 205, 160, 28, "Micro-Climate Forecast", "35mm Rain Forecast in 24 hrs", stroke='#0ea5e9'))
    
    # Merge down
    l1 = Line(140, 205, 140, 185, strokeColor=colors.HexColor('#38bdf8'), strokeWidth=1)
    l2 = Line(340, 205, 340, 185, strokeColor=colors.HexColor('#38bdf8'), strokeWidth=1)
    l3 = Line(140, 185, 340, 185, strokeColor=colors.HexColor('#38bdf8'), strokeWidth=1)
    d.add(l1); d.add(l2); d.add(l3)
    d.add(down_arrow(240, 185, 168))

    d.add(box(120, 140, 240, 26, "Agricultural Knowledge Agent", "TNAU Crop Guide + ICAR RAG Manuals", stroke='#38bdf8'))
    
    # Split to interlocks
    d.add(down_arrow(160, 140, 116))
    d.add(down_arrow(320, 140, 116))
    d.add(box(50, 80, 180, 32, "Soil Profile Interlock", "High P -> Reduce DAP by 20%", stroke='#eab308'))
    d.add(box(250, 80, 180, 32, "Weather Conflict Interlock", "Heavy Rain -> Postpone Top-Dressing", stroke='#ef4444'))

    # Merge to Verifier
    l4 = Line(140, 80, 140, 64, strokeColor=colors.HexColor('#38bdf8'), strokeWidth=1)
    l5 = Line(340, 80, 340, 64, strokeColor=colors.HexColor('#38bdf8'), strokeWidth=1)
    l6 = Line(140, 64, 340, 64, strokeColor=colors.HexColor('#38bdf8'), strokeWidth=1)
    d.add(l4); d.add(l5); d.add(l6)
    d.add(down_arrow(240, 64, 48))

    d.add(box(130, 10, 220, 34, "Claude 3.5 Sonnet Verifier", "Hallucination Check & Safety Sign-off", stroke='#8b5cf6'))
    return d

def generate_exact_format_pdf(filename="docs/FarmWise_AI_System_Documentation.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # English Typography Matching User Template Exactly
    style_badge_top = ParagraphStyle('BadgeTop', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.HexColor('#059669'))
    style_badge_h1 = ParagraphStyle('BadgeH1', fontName='Helvetica-Bold', fontSize=14, leading=17, textColor=colors.HexColor('#065f46'))
    style_badge_sub = ParagraphStyle('BadgeSub', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor('#047857'))
    
    style_doc_title = ParagraphStyle('DocTitle', fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor('#065f46'), spaceBefore=12, spaceAfter=4)
    style_doc_sub_ta = ParagraphStyle('DocSubTa', fontName='Latha', fontSize=10, leading=14, textColor=colors.HexColor('#475569'), spaceAfter=8)

    style_part_h1 = ParagraphStyle('PartH1', fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=colors.HexColor('#065f46'), spaceBefore=8, spaceAfter=4)
    style_part_h1_ta = ParagraphStyle('PartH1Ta', fontName='LathaBold', fontSize=12, leading=17, textColor=colors.HexColor('#065f46'), spaceBefore=8, spaceAfter=4)

    style_feature_h2 = ParagraphStyle('FeatH2', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#065f46'), spaceBefore=12, spaceAfter=4, keepWithNext=True)
    style_feature_h2_ta = ParagraphStyle('FeatH2Ta', fontName='LathaBold', fontSize=11, leading=16, textColor=colors.HexColor('#065f46'), spaceBefore=12, spaceAfter=4, keepWithNext=True)

    style_sub_h3 = ParagraphStyle('SubH3', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=colors.HexColor('#0f766e'), spaceBefore=7, spaceAfter=3, keepWithNext=True)
    style_sub_h3_ta = ParagraphStyle('SubH3Ta', fontName='LathaBold', fontSize=9.5, leading=14, textColor=colors.HexColor('#0f766e'), spaceBefore=7, spaceAfter=3, keepWithNext=True)

    style_body = ParagraphStyle('Body', fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=colors.HexColor('#334155'), spaceAfter=4)
    style_body_ta = ParagraphStyle('BodyTa', fontName='Latha', fontSize=8.5, leading=13.5, textColor=colors.HexColor('#334155'), spaceAfter=4)

    style_bullet = ParagraphStyle('Bullet', fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=colors.HexColor('#334155'), leftIndent=12, spaceAfter=3)
    style_bullet_ta = ParagraphStyle('BulletTa', fontName='Latha', fontSize=8.5, leading=13.5, textColor=colors.HexColor('#334155'), leftIndent=12, spaceAfter=3)

    style_code_badge = ParagraphStyle('CodeBadge', fontName='Courier', fontSize=8, leading=11, textColor=colors.HexColor('#0f766e'))

    story = []

    # ==================== CALLOUT HEADER CARD ====================
    header_content = [
        [Paragraph("FARMWISE AI PLATFORM ARCHITECTURE", style_badge_top)],
        [Paragraph("FarmWise AI — Technical & Agronomic Master Guide", style_badge_h1)],
        [Paragraph("Bilingual Implementation Reference (English & தமிழ்) • Task 1 Campus Challenge", style_badge_sub)]
    ]
    t_header = Table(header_content, colWidths=[487])
    t_header.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0fdf4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#a7f3d0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_header)
    story.append(Spacer(1, 8))

    story.append(Paragraph("FarmWise AI — Comprehensive Engineering & Agronomy Guide", style_doc_title))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#059669'), spaceBefore=2, spaceAfter=4))
    story.append(Paragraph("(முழுமையான தொழில்நுட்ப மற்றும் வேளாண்மை வழிகாட்டி ஆவணம்)", style_doc_sub_ta))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=10))

    # ==================== PART 1: ENGLISH ====================
    story.append(Paragraph("PART 1: COMPLETE ENGLISH DOCUMENTATION", style_part_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#059669'), spaceBefore=2, spaceAfter=8))

    # 1. FarmWise AI Advisor
    story.append(Paragraph("1. FarmWise AI Advisor (Core Orchestrator & Conversational Agent)", style_feature_h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    story.append(Paragraph("Feature Overview", style_sub_h3))
    story.append(Paragraph("The <b>FarmWise AI Advisor</b> is the central coordinating engine of the platform. It functions as an agricultural expert system and conversational assistant that handles farmer inquiries via text, voice, or parcel selection. Rather than relying on a single AI model, it uses a multi-agent orchestrator that breaks down incoming requests, delegates tasks to specialized sub-agents, cross-verifies facts, and returns actionable advisories.", style_body))
    
    story.append(Paragraph("Tech Stack Used & Why", style_sub_h3))
    story.append(Paragraph("• <b>FastAPI (Python 3.11):</b> Async REST API server chosen for non-blocking I/O, rapid JSON serialization, and native OpenAPI/Pydantic validation.", style_bullet))
    story.append(Paragraph("• <b>LangGraph / Multi-Agent StateGraph:</b> Manages multi-agent execution loops using a strongly-typed shared state (<font face='Courier' color='#0f766e'>AgentState</font>). It allows agents to run sequentially or in parallel.", style_bullet))
    story.append(Paragraph("• <b>Multi-Model Routing Architecture:</b>", style_bullet))
    story.append(Paragraph("  - <b>Ministral 8B / 3B (Amazon Bedrock):</b> Low-latency, cost-effective models used for query classification, intent extraction, and light translation.", style_bullet))
    story.append(Paragraph("  - <b>Gemini 1.5 Flash (Google Cloud / Vertex AI):</b> High-speed multimodal model with a large context window for image diagnostics and audio transcription.", style_bullet))
    story.append(Paragraph("  - <b>Claude 3.5 Sonnet:</b> Operates as the \"Verifier and Critic Agent\" to conduct hallucination checks and safety audits on agricultural recommendations.", style_bullet))
    story.append(Paragraph("• <b>RAG System (Amazon Titan Text Embeddings V2 + FAISS/Chroma):</b> Provides semantic search over official agronomic manuals (TNAU Crop Production Guide, ICAR manuals).", style_bullet))
    story.append(Paragraph("• <b>Frontend:</b> React + Vite + Tailwind CSS + Web Speech API for real-time Tamil and English voice synthesis.", style_bullet))

    story.append(Paragraph("What the Feature Actually Did", style_sub_h3))
    story.append(Paragraph("1. Ingests user input (survey numbers, field photos, voice recordings, or conversational questions).", style_bullet))
    story.append(Paragraph("2. Maintains session memory (<font face='Courier' color='#0f766e'>chat_history</font>) to support conversational context.", style_bullet))
    story.append(Paragraph("3. Coordinates specialized sub-agents (Geo, Image, Weather, Soil, Knowledge, Verifier).", style_bullet))
    story.append(Paragraph("4. Records live telemetry for each step: model selected, input/output tokens, latency in milliseconds, tool outputs, and scientific citations.", style_bullet))

    story.append(Paragraph("How It Works (Step-by-Step)", style_sub_h3))
    story.append(Paragraph("1. <b>Request Intake:</b> The user submits a query (e.g., <i>\"When should I apply urea to my paddy field?\"</i> or selects survey number <font face='Courier' color='#0f766e'>124/2A</font>).", style_bullet))
    story.append(Paragraph("2. <b>Intent Analysis & Planning:</b> <font face='Courier' color='#0f766e'>planner.py</font> breaks the request into execution steps.", style_bullet))
    story.append(Paragraph("3. <b>State Hydration:</b> Shared state is initialized with parcel information, recent weather data, and soil health metrics.", style_bullet))
    story.append(Paragraph("4. <b>Agent Graph Execution:</b> If a field photo is present, the Image Agent classifies crop variety and stage; concurrently Weather and Soil Agents fetch microclimate forecasts and soil data.", style_bullet))
    story.append(Paragraph("5. <b>Safety & Hallucination Verification:</b> The Verifier Agent audits advice (e.g., ensuring chemical concentrations do not exceed recommended safety limits).", style_bullet))
    story.append(Paragraph("6. <b>Streaming & Delivery:</b> Finalized advice is delivered to the frontend with interactive UI cards, decision traces, and voice synthesis support.", style_bullet))

    # 2. Cadastral Parcel & FMB Boundary
    story.append(Paragraph("2. Cadastral Parcel & FMB Boundary", style_feature_h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    story.append(Paragraph("Feature Overview", style_sub_h3))
    story.append(Paragraph("The <b>Cadastral Parcel & FMB Boundary</b> feature bridges physical land ownership records with interactive digital maps. It uses official Tamil Nadu Land Records and Field Measurement Book (FMB) survey data to identify, calculate, and display land boundaries.", style_body))
    story.append(Paragraph("Tech Stack Used & Why", style_sub_h3))
    story.append(Paragraph("• <b>Turf.js & GeoJSON:</b> Geospatial analysis library for point-in-polygon queries, area computations, and centroid calculations directly without requiring an enterprise GIS server.", style_bullet))
    story.append(Paragraph("• <b>React Leaflet + OSM & Esri Satellite Layers:</b> High-performance, mobile-responsive mapping with vector overlays and high-resolution satellite views.", style_bullet))
    story.append(Paragraph("• <b>Cadastral Repository:</b> GeoJSON repository containing coordinates, sub-division boundaries, and land-use records for surveyed villages (Tenkasi & Thoothukudi).", style_bullet))
    story.append(Paragraph("What the Feature Actually Did", style_sub_h3))
    story.append(Paragraph("1. Translates government survey numbers (e.g., <font face='Courier' color='#0f766e'>124/2A</font>, <font face='Courier' color='#0f766e'>1476</font>) into geospatial boundary polygons.", style_bullet))
    story.append(Paragraph("2. Calculates parcel area in Hectares and Acres.", style_bullet))
    story.append(Paragraph("3. Determines geographic centroid [<font face='Courier' color='#0f766e'>latitude, longitude</font>] to anchor micro-climate weather forecasts and satellite layers.", style_bullet))
    story.append(Paragraph("4. Masks personal identifiable information (PII) of landowners by default to ensure privacy compliance.", style_bullet))

    # 3. Ground-Truth Field Photo
    story.append(Paragraph("3. Ground-Truth Field Photo", style_feature_h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    story.append(Paragraph("Feature Overview", style_sub_h3))
    story.append(Paragraph("The <b>Ground-Truth Field Photo</b> pipeline manages the capture, verification, and preprocessing of real field images taken by farmers or village extension workers.", style_body))
    story.append(Paragraph("Tech Stack Used & Why", style_sub_h3))
    story.append(Paragraph("• <b>Python PIL / Pillow & ExifRead:</b> Extracts EXIF metadata (GPS latitude/longitude, date/time, camera hardware, orientation).", style_bullet))
    story.append(Paragraph("• <b>Private AWS S3 Storage (ap-south-1 Mumbai):</b> Secure object storage where images remain private without public URL exposure.", style_bullet))
    story.append(Paragraph("• <b>FastAPI UploadFile (Streaming Ingestion):</b> Processes binary multipart payloads with client-side compression to accommodate rural cellular networks.", style_bullet))
    story.append(Paragraph("What the Feature Actually Did", style_sub_h3))
    story.append(Paragraph("1. Ingests smartphone photographs of standing crops, soil, and diseased foliage.", style_bullet))
    story.append(Paragraph("2. Extracts embedded GPS coordinates and timestamps from image metadata.", style_bullet))
    story.append(Paragraph("3. Validates whether the photo was taken within reasonable distance of the claimed cadastral parcel boundary.", style_bullet))
    story.append(Paragraph("4. Normalizes, resizes, and stores the image safely for downstream computer vision models.", style_bullet))

    # 4. Crop Phenotype & Health
    story.append(Paragraph("4. Crop Phenotype & Health", style_feature_h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    story.append(Paragraph("Feature Overview", style_sub_h3))
    story.append(Paragraph("The <b>Crop Phenotype & Health</b> engine serves as an automated diagnostic tool. It visually inspects crop canopies and leaves to detect crop species, phenological growth stages, and visible symptoms of pest infestations or nutrient deficiencies.", style_body))
    story.append(Paragraph("Tech Stack Used & Why", style_sub_h3))
    story.append(Paragraph("• <b>Gemini 1.5 Flash Multimodal Vision:</b> Chosen for fast multimodal reasoning, low per-image cost, and ability to parse agricultural details accurately.", style_bullet))
    story.append(Paragraph("• <b>Amazon Bedrock Titan Multimodal Embeddings (Fallback):</b> Vector-based visual matching fallback to compare inputs against verified disease libraries.", style_bullet))
    story.append(Paragraph("• <b>Pydantic Schemas (<font face='Courier' color='#0f766e'>CropAnalysis</font>):</b> Enforces strict structured JSON output to feed downstream decision logic.", style_bullet))
    story.append(Paragraph("What the Feature Actually Did", style_sub_h3))
    story.append(Paragraph("1. Identifies crop variety (e.g., Rice/Paddy, Banana, Coconut, Maize).", style_bullet))
    story.append(Paragraph("2. Determines exact phenological growth stage (e.g., Nursery, Active Tillering, Panicle Initiation, Flowering, Maturity).", style_bullet))
    story.append(Paragraph("3. Identifies pests and fungal/bacterial diseases (e.g., Brown Plant Hopper, Bacterial Leaf Blight, Rice Blast).", style_bullet))
    story.append(Paragraph("4. Assigns an overall crop health score (0–100%) and a diagnostic confidence rating.", style_bullet))

    # 5. Micro-Climate & Agro-Met
    story.append(Paragraph("5. Micro-Climate & Agro-Met", style_feature_h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    story.append(Paragraph("Feature Overview", style_sub_h3))
    story.append(Paragraph("The <b>Micro-Climate & Agro-Met</b> service provides parcel-level weather intelligence. It translates raw meteorological variables into operational farming advisories and risk warnings.", style_body))
    story.append(Paragraph("Tech Stack Used & Why", style_sub_h3))
    story.append(Paragraph("• <b>Open-Meteo Weather API:</b> Provides open, non-commercial weather data without API key restrictions or rate-limit throttles.", style_bullet))
    story.append(Paragraph("• <b>Agro-Meteorological Rule Engine (<font face='Courier' color='#0f766e'>weather_service.py</font>):</b> Translates weather data into specific field advisories (spray safety windows, rainfall warnings, disease-risk indices).", style_bullet))
    story.append(Paragraph("What the Feature Actually Did", style_sub_h3))
    story.append(Paragraph("1. Fetches a 7-day hourly forecast and 14-day rainfall history based on parcel centroid coordinates.", style_bullet))
    story.append(Paragraph("2. <b>Rain Leaching Risk:</b> Forecast Rainfall (48h) > 15 mm -> Trigger Rain Leaching Warning (delay nitrogen application).", style_bullet))
    story.append(Paragraph("3. <b>Foliar Spray Window:</b> Wind Speed < 15 km/h & Rain Probability < 30% -> Safe Spraying Window.", style_bullet))
    story.append(Paragraph("4. <b>Fungal Pathogen Risk:</b> Relative Humidity > 85% & 24°C <= Temp <= 28°C -> High Blast / Blight Risk alert.", style_bullet))

    # 6. Soil Health & Chemical Profile (With Architecture Flowchart)
    story.append(Paragraph("6. Soil Health & Chemical Profile (In-Depth Technical Breakdown)", style_feature_h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    story.append(Paragraph("Feature Overview", style_sub_h3))
    story.append(Paragraph("The <b>Soil Health & Chemical Profile</b> engine calculates chemical, biological, and physical properties of the soil at the parcel level. It replicates the functionality of the National Soil Health Card (SHC) scheme, grounding chemical evaluations in Tamil Nadu Agricultural University (TNAU) Soil Survey standards.", style_body))
    story.append(Paragraph("Tech Stack Used & Why", style_sub_h3))
    story.append(Paragraph("• <b>TNAU Soil Survey & Fertility Classification Guidelines:</b> Encodes empirical benchmarks for Tamil Nadu agro-climatic zones.", style_bullet))
    story.append(Paragraph("• <b>National Soil Health Card (SHC) Standard:</b> Standardizes macronutrients (N, P, K in kg/ha), Organic Carbon (%), Soil Reaction (pH), and Electrical Conductivity (EC in dS/m).", style_bullet))
    story.append(Paragraph("• <b>Deterministic Cryptographic Simulation (<font face='Courier' color='#0f766e'>soil_service.py</font>):</b> Uses SHA-256 hashing on survey numbers so that test parcels yield consistent, realistic, and unvarying soil data across reloads.", style_bullet))
    
    story.append(Paragraph("In-Depth Scientific & Algorithmic Mechanics", style_sub_h3))
    story.append(create_flowchart_soil())
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>1. Fertilizer Uptake Efficiency Formula:</b>", style_body))
    story.append(Paragraph("Applied chemical fertilizer does not have 100% bioavailability. Nutrient fixation depends heavily on soil pH and organic carbon:", style_body))
    story.append(Paragraph("• <b>pH Penalty:</b> |pH - 7.0| × 12.0", style_bullet))
    story.append(Paragraph("• <b>OC Boost:</b> (Organic Carbon - 0.5) × 15.0", style_bullet))
    story.append(Paragraph("• <b>Efficiency Score:</b> Clamp(85 - pH Penalty + OC Boost, 52%, 92%)", style_bullet))
    story.append(Paragraph("<i>Scientific Basis: In neutral soil (pH 6.8–7.2) with high OC (>0.75%), fertilizer uptake reaches ~88%. Above pH 8.0, phosphorus binds with calcium ions forming insoluble calcium phosphate, dropping uptake efficiency to 55%–62%.</i>", style_body))
    
    story.append(Paragraph("<b>2. Soil Amendment Decision Logic:</b>", style_body))
    story.append(Paragraph("• <b>Alkaline Soils (pH > 7.8):</b> Apply Agricultural Gypsum (CaSO4·2H2O) @ 100 kg/acre to displace exchangeable sodium. Grow green manure crops (Daincha @ 20 kg/acre). Use Neem-Coated Urea in split doses + Zinc Sulphate (21%) @ 10 kg/acre.", style_bullet))
    story.append(Paragraph("• <b>Acidic Soils (pH < 6.3):</b> Apply Agricultural Lime (Dolomite / CaCO3) @ 120 kg/acre. Use Rock Phosphate as basal phosphorus source.", style_bullet))

    # 7. Personalised Agronomic Advisory (With Architecture Flowchart)
    story.append(Paragraph("7. Personalised Agronomic Advisory (In-Depth Technical Breakdown)", style_feature_h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    story.append(Paragraph("Feature Overview", style_sub_h3))
    story.append(Paragraph("The <b>Personalised Agronomic Advisory</b> engine synthesizes crop growth stage, soil chemistry, and micro-climate forecasts into a verified, field-specific action plan.", style_body))
    story.append(Paragraph("Tech Stack Used & Why", style_sub_h3))
    story.append(Paragraph("• <b>TNAU Crop Production Guide:</b> Verified agronomic standards for Tamil Nadu crops (Rice, Banana, Coconut, Maize).", style_bullet))
    story.append(Paragraph("• <b>Multi-Agent Synthesis Engine (<font face='Courier' color='#0f766e'>knowledge_agent.py</font>):</b> Merges data from Image, Weather, and Soil agents into a unified schedule.", style_bullet))
    story.append(Paragraph("• <b>Claude 3.5 Sonnet Verifier (<font face='Courier' color='#0f766e'>verifier_agent.py</font>):</b> Reviews advisory drafts to ensure dosage safety, detect chemical conflicts, and eliminate hallucinations.", style_bullet))
    story.append(Paragraph("• <b>Bilingual Speech Synthesis (<font face='Courier' color='#0f766e'>TTSButton.jsx</font>):</b> Converts advisory cards into spoken Tamil (ta-IN) and English (en-IN).", style_bullet))

    story.append(Paragraph("In-Depth Scientific & Algorithmic Mechanics", style_sub_h3))
    story.append(create_flowchart_advisory())
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>1. Dynamic Dosage Compensation Algorithm:</b>", style_body))
    story.append(Paragraph("• <b>Phosphorus Compensation:</b> If soil test reveals High Available P (> 22 kg/ha), the system automatically reduces chemical DAP dosage by 20%, cutting costs and avoiding toxicity.", style_bullet))
    story.append(Paragraph("• <b>Bio-Fertilizer Integration:</b> Adds Azospirillum (N-fixing) + Phosphobacteria (P-solubilizing) @ 2 kg/acre with 50 kg FYM, cutting synthetic chemical Nitrogen needs by 25%.", style_bullet))
    story.append(Paragraph("• <b>Weather-Conflict Interlock:</b> If Forecast Rainfall (48h) > 15 mm, nitrogen top-dressing is delayed by 24–48 hours until standing water drains to prevent leaching runoff.", style_bullet))

    # 8. Additional Platform Features Table
    story.append(Paragraph("8. Additional Platform Features", style_feature_h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    table_features_en = [
        [Paragraph("<b>Feature</b>", style_sub_h3), Paragraph("<b>Tech Stack</b>", style_sub_h3), Paragraph("<b>What It Does & How It Works</b>", style_sub_h3)],
        [
            Paragraph("<b>Bilingual Voice Assistant (Tamil & English)</b>", style_body),
            Paragraph("Web Speech API + Gemini Audio Fallback", style_code_badge),
            Paragraph("Farmers tap microphone and speak in Tamil (<i>\"என் நிலத்துக்கு என்ன உரம் போடணும்?\"</i>). System transcribes audio, runs agent pipeline, and reads answer aloud.", style_body)
        ],
        [
            Paragraph("<b>Government-Format Printable Report</b>", style_body),
            Paragraph("React Print CSS / @media print", style_code_badge),
            Paragraph("Compiles parcel maps, landowner details, soil cards, and advisories into an official Tamil Nadu Agriculture Department / Kisan Credit Card format for bank loans or crop insurance.", style_body)
        ],
        [
            Paragraph("<b>Real-Time APMC Mandi Market Prices</b>", style_body),
            Paragraph("Agmarknet / e-NAM RAG Engine", style_code_badge),
            Paragraph("Retrieves real-time prices (Min, Max, Modal in ₹/Quintal) from nearby local markets (Tenkasi, Tirunelveli, Madurai) so farmers can plan harvest sales.", style_body)
        ],
        [
            Paragraph("<b>Hallucination Verifier & Decision Trace</b>", style_body),
            Paragraph("Claude 3.5 Sonnet / Bedrock Verifier", style_code_badge),
            Paragraph("Displays a step-by-step trace of every tool call, latency, token count, model selected, and scientific citation behind every recommendation.", style_body)
        ],
        [
            Paragraph("<b>Farmer Data Privacy Masking</b>", style_body),
            Paragraph("PII Masking Engine (<font face='Courier'>privacy_service.py</font>)", style_code_badge),
            Paragraph("Automatically masks landowner names and sensitive survey records (e.g., Murugan S. -> M****** S.) in public views, displaying full records only in authorized officer views.", style_body)
        ]
    ]
    t_feat_en = Table(table_features_en, colWidths=[120, 120, 247])
    t_feat_en.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#065f46')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_feat_en)
    story.append(Spacer(1, 14))

    # ==================== PART 2: TAMIL ====================
    story.append(PageBreak())
    story.append(Paragraph("PART 2: TAMIL TRANSLATION & EXPLANATION", style_part_h1))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#059669'), spaceBefore=2, spaceAfter=4))
    story.append(Paragraph("(பகுதி 2: விரிவான தமிழ் விளக்கக் கையேடு)", style_doc_sub_ta))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=8))

    # 1. FarmWise AI Advisor
    story.append(Paragraph("1. FarmWise AI Advisor (முதன்மை ஒருங்கிணைப்பாளர் & உரையாடல் உதவியாளர்)", style_feature_h2_ta))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    story.append(Paragraph("இந்த அம்சம் என்ன செய்கிறது?", style_sub_h3_ta))
    story.append(Paragraph("FarmWise AI Advisor என்பது இந்த தளத்தின் <b>\"மைய மூளை\" (Central Brain)</b> ஆகும். ஒரு விவசாயி தனது சர்வே எண், நிலத்தின் புகைப்படம் அல்லது குரல் மூலம் கேள்வி கேட்கும்போது, இந்த ஆலோசகர் பல்வேறு துணை ஏஜென்ட்டுகளை (Sub-Agents) இயக்கி, துல்லியமான மற்றும் பாதுகாப்பான வேளாண் ஆலோசனைகளை வழங்குகிறது.", style_body_ta))
    story.append(Paragraph("பயன்படுத்தப்பட்ட தொழில்நுட்பங்கள் & காரணங்கள்:", style_sub_h3_ta))
    story.append(Paragraph("• <b>FastAPI (Python 3.11):</b> அதிவேகமான மற்றும் தடையற்ற API பரிமாற்றத்திற்கு பயன்படுகிறது.", style_bullet_ta))
    story.append(Paragraph("• <b>LangGraph / Multi-Agent StateGraph:</b> பல AI ஏஜென்ட்டுகள் ஒன்றுக்கொன்று தகவல்களைப் பகிர்ந்து செயல்பட உதவுகிறது.", style_bullet_ta))
    story.append(Paragraph("• <b>Multi-Model Routing Architecture:</b>", style_bullet_ta))
    story.append(Paragraph("  - <b>Ministral 8B / 3B (Amazon Bedrock):</b> குறைந்த செலவில் விரைவான திட்டமிடல் மற்றும் மொழிபெயர்ப்பு பணிகளுக்கு.", style_bullet_ta))
    story.append(Paragraph("  - <b>Gemini 1.5 Flash (Google Cloud):</b> புகைப்படங்களை ஆராயவும் மற்றும் தமிழ் குரல் பதிவுகளை உரையாக மாற்றவும்.", style_bullet_ta))
    story.append(Paragraph("  - <b>Claude 3.5 Sonnet:</b> வழங்கப்பட்ட ஆலோசனைகளில் தவறுகள் உள்ளதா என சரிபார்க்கும் தணிக்கையாளராக (Verifier/Critic).", style_bullet_ta))
    story.append(Paragraph("• <b>Vector RAG (Titan Text Embeddings + FAISS):</b> தமிழ்நாடு வேளாண்மைப் பல்கலைக்கழகம் (TNAU) மற்றும் ICAR வழிகாட்டி கையேடுகளில் இருந்து அறிவியல் பூர்வமான தகவல்களைத் தேடி எடுக்கிறது.", style_bullet_ta))
    story.append(Paragraph("இது எவ்வாறு செயல்படுகிறது?", style_sub_h3_ta))
    story.append(Paragraph("1. விவசாயி சர்வே எண்ணை உள்ளிடுகிறார் அல்லது கேள்வி கேட்கிறார்.", style_bullet_ta))
    story.append(Paragraph("2. Planner எந்தெந்த ஏஜென்ட்டுகள் செயல்பட வேண்டும் என்பதைத் திட்டமிடுகிறது.", style_bullet_ta))
    story.append(Paragraph("3. பயிர் புகைப்படம், மண் வளம் மற்றும் வானிலை தகவல்கள் திரட்டப்படுகின்றன.", style_bullet_ta))
    story.append(Paragraph("4. Knowledge Agent பல்கலைக்கழக வழிகாட்டுதல்களின்படி உரம் மற்றும் பூச்சி மேலாண்மை அட்டவணையை உருவாக்குகிறது.", style_bullet_ta))
    story.append(Paragraph("5. Verifier Agent இந்த பரிந்துரைகளில் ஏதேனும் ஆபத்தான தவறுகள் உள்ளதா என சரிபார்த்து உறுதி செய்கிறது.", style_bullet_ta))
    story.append(Paragraph("6. முடிவுகள் எளிய திரையிலும், தமிழ் குரல் வாசிப்பாகவும் (Voice Readout) விவசாயிக்கு வழங்கப்படுகின்றன.", style_bullet_ta))

    # 2. Cadastral Parcel & FMB Boundary
    story.append(Paragraph("2. Cadastral Parcel & FMB Boundary (நில அளவை மற்றும் FMB எல்லை வரைபடம்)", style_feature_h2_ta))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    story.append(Paragraph("இந்த அம்சம் என்ன செய்கிறது?", style_sub_h3_ta))
    story.append(Paragraph("விவசாயியின் பட்டா மற்றும் சிட்டா சர்வே எண்களைக் கொண்டு (எ.கா: 124/2A), அவர்களின் நிலத்தின் துல்லியமான எல்லைகளை வரைபடத்தில் காட்டுகிறது. நிலத்தின் மொத்த பரப்பளவு (ஹெக்டேர் மற்றும் ஏக்கர்) கணக்கிடப்படுகிறது.", style_body_ta))
    story.append(Paragraph("பயன்படுத்தப்பட்ட தொழில்நுட்பங்கள் & காரணங்கள்:", style_sub_h3_ta))
    story.append(Paragraph("• <b>Turf.js & GeoJSON:</b> நிலத்தின் பரப்பளவு, சுற்றளவு மற்றும் மையப்புள்ளியை விரைவாகக் கணக்கிடும் வரைபட கணிதக் கருவி.", style_bullet_ta))
    story.append(Paragraph("• <b>React Leaflet + OSM & Esri Satellite Layers:</b> குறைந்த இணைய வேகத்திலும் மொபைலில் தெளிவாக இயங்கும் செயற்கைக்கோள் வரைபடம்.", style_bullet_ta))
    story.append(Paragraph("• <b>Tamil Nadu Land Records Dataset:</b> தமிழ்நாடு அரசின் FMB (புல வரைபடம்) எல்லைத் தரவுகள்.", style_bullet_ta))
    story.append(Paragraph("இது எவ்வாறு செயல்படுகிறது?", style_sub_h3_ta))
    story.append(Paragraph("1. விவசாயி சர்வே எண்ணைத் தேர்ந்தெடுத்ததும், வரைபடத் தரவுத்தளத்தில் இருந்து எல்லைக் கோடுகள் எடுக்கப்படுகின்றன.", style_bullet_ta))
    story.append(Paragraph("2. Turf.js நிலத்தின் பரப்பளவு மற்றும் மையப்புள்ளியைத் தீர்மானிக்கிறது.", style_bullet_ta))
    story.append(Paragraph("3. செயற்கைக்கோள் வரைபடம் அந்த இடத்திற்கு நகர்ந்து நிலத்தின் எல்லையைக் கோடிட்டுக் காட்டுகிறது.", style_bullet_ta))
    story.append(Paragraph("4. விவசாயியின் தனிப்பட்ட தகவல்கள் பாதுகாக்கப்பட்டு, பெயர் மறைக்கப்பட்டு காட்டப்படும் (எ.கா: M****** S.).", style_bullet_ta))

    # 3. Ground-Truth Field Photo
    story.append(Paragraph("3. Ground-Truth Field Photo (நேரடி களப் புகைப்படம்)", style_feature_h2_ta))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    story.append(Paragraph("இந்த அம்சம் என்ன செய்கிறது?", style_sub_h3_ta))
    story.append(Paragraph("விவசாயிகள் தங்கள் வயலில் எடுக்கும் பயிர் அல்லது இலைகளின் புகைப்படங்களைச் சேகரித்து சரிபார்க்கிறது. புகைப்படத்தில் உள்ள GPS தகவலைக் கொண்டு, படம் உண்மையில் அந்த சர்வே எண் நிலத்தில்தான் எடுக்கப்பட்டதா என்பதை உறுதி செய்கிறது.", style_body_ta))
    story.append(Paragraph("பயன்படுத்தப்பட்ட தொழில்நுட்பங்கள் & காரணங்கள்:", style_sub_h3_ta))
    story.append(Paragraph("• <b>Python PIL / Pillow & ExifRead:</b> புகைப்படத்தின் தரம், நேரம் மற்றும் GPS இருப்பிடத்தை ஆராய்கிறது.", style_bullet_ta))
    story.append(Paragraph("• <b>Private AWS S3 (Mumbai ap-south-1):</b> புகைப்படங்கள் பொது இணையத்தில் கசியாமல் பாதுகாப்பாகச் சேமிக்கப்படுகின்றன.", style_bullet_ta))
    story.append(Paragraph("• <b>FastAPI Streaming Upload:</b> கிராமப்புறங்களில் இணைய வேகம் குறைவாக இருந்தாலும் புகைப்படங்களை எளிதாகப் பதிவேற்றுகிறது.", style_bullet_ta))

    # 4. Crop Phenotype & Health
    story.append(Paragraph("4. Crop Phenotype & Health (பயிர் வகை & ஆரோக்கியக் கண்காணிப்பு)", style_feature_h2_ta))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    story.append(Paragraph("இந்த அம்சம் என்ன செய்கிறது?", style_sub_h3_ta))
    story.append(Paragraph("வயல் புகைப்படத்தைப் பார்த்து: 1. என்ன பயிர் சாகுபடி செய்யப்பட்டுள்ளது (நெல், வாழை, சோளம், தென்னை)? 2. பயிர் எந்த வளர்ச்சிப் பருவத்தில் உள்ளது (நாற்றுப் பருவம், தூர் கட்டும் பருவம், கதிர் உருவாகும் பருவம், முதிர்ச்சிப் பருவம்)? 3. பூச்சி அல்லது பூஞ்சாண நோய்களின் தாக்குதல் உள்ளதா (எ.கா: புகையான் பூச்சி, பாக்டீரியா இலைக்கருகல், இலைப்புள்ளி நோய்)? 4. பயிரின் ஆரோக்கிய மதிப்பீடு (Health Score: 0-100%) ஆகியவற்றைத் துல்லியமாகக் கண்டறிகிறது.", style_body_ta))
    story.append(Paragraph("பயன்படுத்தப்பட்ட தொழில்நுட்பங்கள் & காரணங்கள்:", style_sub_h3_ta))
    story.append(Paragraph("• <b>Gemini 1.5 Flash Multimodal Vision:</b> புகைப்படத்தில் உள்ள பயிர் அறிகுறிகளைத் துல்லியமாகவும் குறைந்த செலவிலும் கண்டறியும் திறன் கொண்டது.", style_bullet_ta))
    story.append(Paragraph("• <b>Bedrock Titan Multimodal Embeddings (மாற்று வழி):</b> இணையத் தடங்கல் ஏற்பட்டால் நோய் மாதிரிகளை ஒப்பிட்டுப் பார்க்க உதவும் மாதிரித் தொகுப்பு.", style_bullet_ta))
    story.append(Paragraph("• <b>Pydantic Schemas:</b> தகவல்கள் குழப்பமின்றி முறையான தரவுகளாக (JSON) மாற்றப்படுவதை உறுதி செய்கிறது.", style_bullet_ta))

    # 5. Micro-Climate & Agro-Met
    story.append(Paragraph("5. Micro-Climate & Agro-Met (நுண் வானிலை & வேளாண் எச்சரிக்கைகள்)", style_feature_h2_ta))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    story.append(Paragraph("இந்த அம்சம் என்ன செய்கிறது?", style_sub_h3_ta))
    story.append(Paragraph("விவசாயியின் நிலத்திற்குரிய நேரடி 7-நாள் வானிலை முன்னறிவிப்பைப் பெறுகிறது. மழைப்பொழிவு, ஈரப்பதம், காற்றின் வேகம் ஆகியவற்றை அடிப்படையாகக் கொண்டு விவசாயிகளுக்கு முன்கூட்டியே எச்சரிக்கைகளை வழங்குகிறது.", style_body_ta))
    story.append(Paragraph("பயன்படுத்தப்பட்ட தொழில்நுட்பங்கள் & காரணங்கள்:", style_sub_h3_ta))
    story.append(Paragraph("• <b>Open-Meteo Weather API:</b> கட்டணமில்லாத மற்றும் தடையற்ற வானிலை முன்னறிவிப்பு சேவை.", style_bullet_ta))
    story.append(Paragraph("• <b>Agro-Meteorological Rule Engine (weather_service.py):</b> வானிலை எண்களை நடைமுறை விவசாய எச்சரிக்கைகளாக மாற்றும் விதிகளின் தொகுப்பு.", style_bullet_ta))
    story.append(Paragraph("• <b>மழை உரம் இழப்பு எச்சரிக்கை:</b> அடுத்த 48 மணி நேரத்தில் 15 மி.மீ-க்கு மேல் மழை பெய்யும் வாய்ப்பிருந்தால், யூரியா போன்ற மேலுரமிடுவதைத் தள்ளிப்போட எச்சரிக்கிறது.", style_bullet_ta))
    story.append(Paragraph("• <b>பூஞ்சாண நோய் எச்சரிக்கை:</b> காற்றின் ஈரப்பதம் 85%-க்கு அதிகமாகவும், வெப்பநிலை 24–28°C ஆகவும் இருந்தால், குலைநோய் (Blast) தாக்குதல் வர வாய்ப்புள்ளதாக எச்சரிக்கிறது.", style_bullet_ta))

    # 6. Soil Health & Chemical Profile (Tamil)
    story.append(Paragraph("6. Soil Health & Chemical Profile (மண்வளம் மற்றும் ஊட்டச்சத்து பகுப்பாய்வு — ஆழமான விளக்கம்)", style_feature_h2_ta))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    story.append(Paragraph("இந்த அம்சம் என்ன செய்கிறது?", style_sub_h3_ta))
    story.append(Paragraph("விவசாயியின் நிலத்திற்கான விரிவான மண்வள அட்டை (Soil Health Card) அறிக்கையை உருவாக்குகிறது. மண்ணின் வகை, கார-அமிலத்தன்மை (pH), கரிமக் கரிமம் (Organic Carbon), முதன்மை சத்துக்களான தழைச்சத்து (N), மணிச்சத்து (P), சாம்பல்சத்து (K) மற்றும் உவர்-அமில நிலையை ஆராய்கிறது.", style_body_ta))
    story.append(Paragraph("பயன்படுத்தப்பட்ட தொழில்நுட்பங்கள் & காரணங்கள்:", style_sub_h3_ta))
    story.append(Paragraph("• <b>TNAU மண் ஆய்வு நெறிமுறைகள்:</b> தமிழ்நாட்டின் வேளாண் மண்டலங்களுக்கான (காவிரி டெல்டா, மேற்கு மண்டலம், தென் மண்டலம்) அதிகாரப்பூர்வ மண் வள அளவுகோல்கள்.", style_bullet_ta))
    story.append(Paragraph("• <b>தேசிய மண்வள அட்டைத் திட்டம் (SHC):</b> ஊட்டச்சத்துக்களின் அளவை முறைப்படுத்துகிறது (கிலோ/ஹெக்டேர்).", style_bullet_ta))
    story.append(Paragraph("• <b>Deterministic Cryptographic Simulation (soil_service.py):</b> மாதிரி சர்வே எண்களை SHA-256 முறையில் குறியாக்கம் செய்வதன் மூலம் எப்போதும் நம்பகமான மண் பண்புகள் மாறாமல் காட்டப்படுகின்றன.", style_bullet_ta))
    story.append(Paragraph("ஆழமான அறிவியல் மற்றும் செயல்பாட்டுக் கோட்பாடுகள்:", style_sub_h3_ta))
    story.append(Paragraph("<b>1. உர பயன்பாட்டுத் திறன் கணக்கீடு (Fertilizer Uptake Efficiency Formula):</b>", style_body_ta))
    story.append(Paragraph("மண்ணில் இடப்படும் ரசாயன உரங்கள் அனைத்தையும் பயிர்களால் உடனடியாக உறிஞ்சிவிட முடியாது. நடுநிலையான மண்ணில் (pH 6.8–7.2) உர பயன்பாட்டுத் திறன் 88% வரை இருக்கும். ஆனால் மண் காரத்தன்மையுடன் (pH 8.2) இருக்கும்போது, மணிச்சத்து சுண்ணாம்புடன் பிணைக்கப்பட்டு பயிர்களுக்குக் கிடைக்காமல் போகிறது; மேலும் யூரியா வாயுவாக வீணாகிறது. இதனால் பயன்பாட்டுத் திறன் 62% ஆகக் குறைகிறது.", style_body_ta))
    story.append(Paragraph("<b>2. மண் சீர்திருத்தப் பரிந்துரைகள் (Soil Amendments):</b>", style_body_ta))
    story.append(Paragraph("• <b>மண் காரத்தன்மை அதிகமாக இருந்தால் (pH > 7.8):</b> ஏக்கருக்கு 100 கிலோ வேளாண் ஜிப்சம் (CaSO4·2H2O) இடப் பரிந்துரைக்கப்படுகிறது. தக்கைப்பூண்டு (Daincha) அல்லது சணப்பை ஏக்கருக்கு 20 கிலோ விதைத்து மடக்கி உழ வேண்டும். சாதாரண யூரியாவைத் தவிர்த்து வேப்பம்பூசப்பட்ட யூரியாவைப் பிரித்து இட வேண்டும். துத்தநாக சல்பேட் ஏக்கருக்கு 10 கிலோ இட வேண்டும்.", style_bullet_ta))
    story.append(Paragraph("• <b>மண் அமிலத்தன்மை அதிகமாக இருந்தால் (pH < 6.3):</b> ஏக்கருக்கு 120 கிலோ வேளாண் சுண்ணாம்பு (டாலமைட்) இட வேண்டும். ராக் பாஸ்பேட் உரத்தைப் பயன்படுத்த வேண்டும்.", style_bullet_ta))

    # 7. Personalised Agronomic Advisory (Tamil)
    story.append(Paragraph("7. Personalised Agronomic Advisory (தனிப்பயனாக்கப்பட்ட வேளாண் ஆலோசனை — ஆழமான விளக்கம்)", style_feature_h2_ta))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    story.append(Paragraph("இந்த அம்சம் என்ன செய்கிறது?", style_sub_h3_ta))
    story.append(Paragraph("விவசாயியின் பயிர் நிலை, மண் பரிசோதனை முடிவுகள் மற்றும் வானிலை முன்னறிவிப்பு ஆகிய மூன்றையும் ஒருங்கிணைத்து, அந்த நிலத்திற்கேற்ற பிரத்யேக வேளாண் செயல் திட்டத்தை உருவாக்குகிறது.", style_body_ta))
    story.append(Paragraph("பயன்படுத்தப்பட்ட தொழில்நுட்பங்கள் & காரணங்கள்:", style_sub_h3_ta))
    story.append(Paragraph("• <b>TNAU பயிர் சாகுபடி வழிகாட்டித் தரவு:</b> நெல், வாழை, சோளம், தென்னை பயிர்களுக்கான சாகுபடி கையேடு.", style_bullet_ta))
    story.append(Paragraph("• <b>LangGraph Multi-Agent Synthesis (knowledge_agent.py):</b> அனைத்து துணை ஏஜென்ட்டுகளின் தரவுகளையும் ஒருங்கிணைக்கும் அறிவு இயந்திரம்.", style_bullet_ta))
    story.append(Paragraph("• <b>Claude 3.5 Sonnet Verifier (verifier_agent.py):</b> பரிந்துரைக்கப்பட்ட மருந்துகளின் அளவுகள் பாதுகாப்பானதா என்பதை தணிக்கை செய்து உறுதி செய்கிறது.", style_bullet_ta))
    story.append(Paragraph("• <b>தமிழ் குரல் வாசிப்பு வசதி (TTSButton.jsx):</b> விவசாயிகள் வாசிக்க சிரமப்பட்டால், ஆலோசனைகளைத் தூய தமிழில் குரல் வடிவில் வாசித்துக் காட்டுகிறது.", style_bullet_ta))
    story.append(Paragraph("ஆழமான அறிவியல் மற்றும் செயல்பாட்டுக் கோட்பாடுகள்:", style_sub_h3_ta))
    story.append(Paragraph("<b>1. மண் நிலைக்கு ஏற்ப உர அளவை மாற்றியமைக்கும் முறை (Dynamic Dosage Adjustment):</b> பொதுவான வேளாண் அட்டவணைகள் அனைவருக்கும் ஒரே அளவிலான உரத்தையே பரிந்துரைக்கும் (எ.கா: நெல்லுக்கு ஏக்கருக்கு 120:38:38 கிலோ NPK). ஆனால் FarmWise AI மண்ணின் தரத்திற்கேற்ப உர அளவை மாற்றியமைக்கிறது:", style_body_ta))
    story.append(Paragraph("• <b>மணிச்சத்து குறைப்பு:</b> மண்ணில் மணிச்சத்து அதிகமாக இருந்தால் (>22.0 கிலோ/ஹெக்டேர்), இரசாயன DAP உரத்தின் அளவை 20% குறைத்து செலவை மிச்சப்படுத்துகிறது.", style_bullet_ta))
    story.append(Paragraph("• <b>உயிர் உரங்கள் சேர்த்தல்:</b> அசோஸ்பைரில்லம் மற்றும் பாஸ்போபாக்டீரியா தலா 2 கிலோவை 50 கிலோ தொழுவுரத்துடன் கலந்து இடப் பரிந்துரைப்பதன் மூலம், இரசாயன தழைச்சத்துத் தேவையை 25% குறைக்கிறது.", style_bullet_ta))
    story.append(Paragraph("• <b>வானிலை முரண்பாடு சரிபார்ப்பு:</b> அடுத்த 48 மணி நேரத்தில் 15 மி.மீ-க்கு மேல் மழை பெய்யும் வாய்ப்பிருந்து, அதே நேரத்தில் யூரியா மேலுரமிட வேண்டிய நிலை இருந்தால்: உரமிடும் காலம் உடனடியாக \"மழைக்குப் பின் இடவும் (மழை நீர் வடிந்த பிறகு 24–48 மணி நேரம் கழித்து இடவும்)\" என மாற்றப்படும்.", style_bullet_ta))

    # 8. Additional Platform Features (Tamil Table)
    story.append(Paragraph("8. அமைப்பில் உள்ள பிற முக்கிய அம்சங்கள்", style_feature_h2_ta))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=5))
    table_features_ta = [
        [Paragraph("<b>கூடுதல் அம்சம்</b>", style_sub_h3_ta), Paragraph("<b>பயன்படுத்தப்பட்ட தொழில்நுட்பம்</b>", style_sub_h3_ta), Paragraph("<b>என்ன செய்கிறது & எவ்வாறு இயங்குகிறது?</b>", style_sub_h3_ta)],
        [
            Paragraph("<b>இருமொழி குரல் உதவியாளர் (தமிழ் & ஆங்கிலம்)</b>", style_body_ta),
            Paragraph("Web Speech API + Gemini Audio", style_code_badge),
            Paragraph("விவசாயிகள் மைக்ரோஃபோன் பொத்தானை அழுத்தி தமிழில் பேசலாம் (<i>\"என் நிலத்திற்கு எப்போது உரம் போட வேண்டும்?\"</i>). AI அதனைப் புரிந்துகொண்டு தமிழிலேயே பதிலளிக்கிறது.", style_body_ta)
        ],
        [
            Paragraph("<b>அரசு மாதிரி அச்சு அறிக்கை (Printable Report)</b>", style_body_ta),
            Paragraph("React Print CSS / @media print", style_code_badge),
            Paragraph("நில வரைபடம், பயிர் நிலை, மண் அட்டை மற்றும் ஆலோசனைகளை அரசு அதிகாரிகள், பயிர் காப்பீடு மற்றும் வங்கி கடன் பெறுவதற்கு ஏற்ற ஆவணமாக அச்சிட்டுத் தருகிறது.", style_body_ta)
        ],
        [
            Paragraph("<b>நேரடி ஒழுங்குமுறை விற்பனைக்கூட (APMC Mandi) விலை நிலவரம்</b>", style_body_ta),
            Paragraph("e-NAM / Agmarknet RAG Engine", style_code_badge),
            Paragraph("அருகிலுள்ள சந்தைகளில் (தென்காசி, திருநெல்வேலி, மதுரை) தற்போதைய விளைபொருட்களின் விற்பனை விலையைக் (குறைந்தபட்ச, அதிகபட்ச விலை ₹/குவிண்டால்) காட்டுகிறது.", style_body_ta)
        ],
        [
            Paragraph("<b>தவறுகளைத் தணிக்கை செய்யும் முறை (Decision Trace)</b>", style_body_ta),
            Paragraph("Claude 3.5 Sonnet / Bedrock Verifier", style_code_badge),
            Paragraph("AI ஒவ்வொரு முடிவையும் எவ்வாறு எடுத்தது, எந்தப் பல்கலைக்கழகப் புத்தகத்திலிருந்து மேற்கோள் காட்டியது என்பதை வெளிப்படையாகத் திரையில் காட்டுகிறது.", style_body_ta)
        ],
        [
            Paragraph("<b>விவசாயி தரவுப் பாதுகாப்பு (PII Masking)</b>", style_body_ta),
            Paragraph("Privacy Engine (privacy_service.py)", style_code_badge),
            Paragraph("பட்டாதாரரின் தனிப்பட்ட விவரங்களை மறைத்து (எ.கா: M****** S.) பொதுப்பார்வைக்கு பாதுகாப்பாக வைக்கிறது; அதிகாரிகள் உள்நுழையும் போது மட்டுமே முழு விவரமும் தெரியும்.", style_body_ta)
        ]
    ]
    t_feat_ta = Table(table_features_ta, colWidths=[120, 120, 247])
    t_feat_ta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#065f46')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_feat_ta)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated exact-replica PDF: {filename} (Size: {os.path.getsize(filename)} bytes)")

if __name__ == "__main__":
    generate_exact_format_pdf()
