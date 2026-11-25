import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# 1. Register Fonts
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
            self.drawString(54, 800, 'FarmWise AI - System Architecture, APIs & Technical Specification')
            self.setStrokeColor(colors.HexColor('#cbd5e1'))
            self.setLineWidth(0.5)
            self.line(54, 792, 541, 792)
            
        # Footer
        text = f'Page {self._pageNumber} of {page_count}'
        self.drawRightString(541, 35, text)
        self.drawString(54, 35, 'FARMWISE AI AGENTIC INTELLIGENCE PLATFORM')
        self.setStrokeColor(colors.HexColor('#cbd5e1'))
        self.setLineWidth(0.5)
        self.line(54, 47, 541, 47)
        self.restoreState()

def build_pdf(filename="docs/FarmWise_AI_System_Documentation.pdf"):
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

    # English Styles
    style_en_title = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#065f46')
    )
    style_en_subtitle = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#047857')
    )
    style_en_h1 = ParagraphStyle(
        'Heading1_EN',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    style_en_h2 = ParagraphStyle(
        'Heading2_EN',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    style_en_body = ParagraphStyle(
        'Body_EN',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=5
    )
    style_en_code = ParagraphStyle(
        'Code_EN',
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#0f766e')
    )

    # Tamil Styles
    style_ta_h1 = ParagraphStyle(
        'Heading1_TA',
        fontName='LathaBold',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor('#065f46'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    style_ta_h2 = ParagraphStyle(
        'Heading2_TA',
        fontName='LathaBold',
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    style_ta_body = ParagraphStyle(
        'Body_TA',
        fontName='Latha',
        fontSize=9,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=5
    )

    story = []

    # ==================== COVER / HEADER ====================
    story.append(Paragraph("FarmWise AI Platform", style_en_title))
    story.append(Paragraph("Enterprise Multi-Model & Multimodal Agricultural Intelligence Platform", style_en_subtitle))
    story.append(Paragraph("System Architecture, Modules, APIs, & Functional Specifications", ParagraphStyle('Sub2', fontName='Helvetica-Oblique', fontSize=9.5, leading=13, textColor=colors.HexColor('#64748b'))))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#10b981'), spaceAfter=14))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Target System:</b> FarmWise AI (Task 1)", style_en_body), Paragraph("<b>Region & Base:</b> ap-south-1 (Mumbai) / Tamil Nadu", style_en_body)],
        [Paragraph("<b>Primary Datasets:</b> Tenkasi & Thoothukudi (14,643 parcels)", style_en_body), Paragraph("<b>Languages:</b> Bilingual (English & Tamil)", style_en_body)],
        [Paragraph("<b>Multi-Model Suite:</b> Ministral-8B, Gemini Flash, Claude 3.5", style_en_body), Paragraph("<b>Status:</b> Production Ready & Verified", style_en_body)]
    ]
    t_meta = Table(meta_data, colWidths=[240, 247])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # ==================== SECTION 1: ENGLISH ====================
    story.append(Paragraph("SECTION 1: SYSTEM ARCHITECTURE & MODULE TECHNICAL GUIDE (ENGLISH)", style_en_h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceAfter=10))

    # 1. Executive Summary
    story.append(Paragraph("1. Platform Mission & Multi-Model Justification", style_en_h2))
    p1 = ("FarmWise AI is an agentic agricultural decision-support engine engineered to empower farmers with parcel-level "
          "advisories and equip government officers with statewide crop surveillance. To eliminate single-model failure and hallucinations, "
          "the architecture enforces a differentiated multi-model routing pipeline:")
    story.append(Paragraph(p1, style_en_body))

    model_table_data = [
        [Paragraph("<b>AI Model / Service</b>", style_en_body), Paragraph("<b>Tier & Provider</b>", style_en_body), Paragraph("<b>Architectural Responsibility</b>", style_en_body)],
        [Paragraph("<b>Ministral 8B / 3B Instruct</b>", style_en_body), Paragraph("AWS Bedrock (Open-weight)", style_en_body), Paragraph("Rapid task planning, structured parameter extraction, query rewriting, and intent classification.", style_en_body)],
        [Paragraph("<b>Gemini 1.5 Flash / Pro</b>", style_en_body), Paragraph("Google Multimodal Vision", style_en_body), Paragraph("Plant field photograph phenotyping, leaf pathology diagnosis, and Tamil audio transcription fallback.", style_en_body)],
        [Paragraph("<b>Claude 3.5 Sonnet</b>", style_en_body), Paragraph("Anthropic (Proprietary)", style_en_body), Paragraph("Autonomous Verifier/Critic Agent: audits advisories, checks fertilizer limits, and prevents hallucinations.", style_en_body)],
        [Paragraph("<b>Amazon Titan Embeddings V2</b>", style_en_body), Paragraph("AWS Bedrock Vector Engine", style_en_body), Paragraph("Dense semantic RAG indexing across TNAU and ICAR agricultural practices manuals.", style_en_body)]
    ]
    t_models = Table(model_table_data, colWidths=[120, 110, 257])
    t_models.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#065f46')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_models)
    story.append(Spacer(1, 10))

    # Modules Breakdown (English)
    modules_en = [
        {
            "num": "2.1",
            "name": "Geospatial Cadastral GIS & Parcel Identification",
            "apis": [
                "GET /api/parcels/search?q={query}",
                "GET /api/parcels/{survey_number}",
                "GET /api/admin/crop-monitoring/cadastral-boundaries"
            ],
            "uses": "Matches survey numbers to cadastral boundaries (FMB) across Sivagiri (Tenkasi) and Thoothukudi villages. Validates land parcel polygons against revenue records.",
            "how": "Reads 14,643 ground truth points and cadastral GeoJSON. Uses point-in-polygon geometry (Turf.js) to confirm parcel bounds and displays the land parcel on Leaflet satellite imagery."
        },
        {
            "num": "2.2",
            "name": "Soil Health Card (SHC) & Reclamation Analysis",
            "apis": [
                "GET /api/parcels/{survey_number} (soil_profile)",
                "POST /api/advisory/run (SoilAgent sub-workflow)"
            ],
            "uses": "Evaluates soil reaction (pH), electrical conductivity (EC), organic carbon (OC), and NPK levels to prescribe bio-fertilizers and chemical amendments.",
            "how": "Applies agronomic threshold rules: Alkaline soil (pH > 7.8) receives Gypsum (100 kg/acre) and Zinc Sulphate; acidic soil receives Lime. Recommends split application of Neem-Coated Urea."
        },
        {
            "num": "2.3",
            "name": "Agro-Meteorological Weather Intelligence",
            "apis": [
                "GET /api/weather/parcel/{survey_number}",
                "External: Open-Meteo REST API (global 7-day forecast)"
            ],
            "uses": "Provides live weather, rainfall history, and a 7-day forecast for temperature, humidity, and wind speed to schedule irrigation and agrochemical spraying.",
            "how": "Resolves parcel latitude/longitude and queries Open-Meteo. Evaluates spray safety thresholds (e.g., wind speed < 15 km/h, precipitation probability < 40%)."
        },
        {
            "num": "2.4",
            "name": "Computer Vision Phenotyping & Disease Detection",
            "apis": [
                "POST /api/upload (Multipart image upload)",
                "Vision Model: gemini-1.5-flash / Titan Multimodal"
            ],
            "uses": "Identifies crop species, phenological stage (vegetative, flowering, harvest), and diagnoses foliar diseases (blast, blight, stem borer) directly from field photos.",
            "how": "The uploaded photograph is sent to Gemini Flash alongside agronomic prompts. The model inspects lesion morphology, estimates a health score (0-100%), and specifies pathogen controls."
        },
        {
            "num": "2.5",
            "name": "LangGraph Multi-Agent Advisory Orchestrator",
            "apis": [
                "POST /api/advisory/run (End-to-end multi-agent execution)"
            ],
            "uses": "Coordinates specialized agents to synthesize a comprehensive, hallucination-free agricultural advisory tailored to the farmer's specific land parcel.",
            "how": "PlannerAgent builds an execution graph. GeoAgent, WeatherAgent, SoilAgent, and ImageAgent execute in parallel. AgriKnowledgeAgent queries TNAU RAG vector data. VerifierAgent audits the final advisory before returning."
        },
        {
            "num": "2.6",
            "name": "Seasonal Crop Recommendation & Profit Engine",
            "apis": [
                "GET /api/crop-recommendations",
                "GET /api/crop-recommendations/{survey_number}/profit-analysis",
                "GET /api/crop-recommendations/{survey_number}/market-trends",
                "GET /api/admin/crop-recommendations/analytics"
            ],
            "uses": "Recommends top 5 alternative crops ranked by soil suitability, seasonal climate, water budget, cultivation expenses, and expected market profits per acre.",
            "how": "Evaluates 12 regional crops. Computes cost of cultivation (seeds, fertilizer, labor), projected yield, and market rates from e-NAM/Agmarknet. Yields net profit = gross revenue - total costs."
        },
        {
            "num": "2.7",
            "name": "Admin Smart Alerts & Priority GIS Monitoring",
            "apis": [
                "GET /api/admin/crop-monitoring/overview",
                "GET /api/admin/crop-monitoring/markers (Stratified GIS symbols)",
                "GET /api/admin/crop-monitoring/records (Paginated registry)",
                "PUT /api/admin/crop-monitoring/records/{id} (Verification & Audit)"
            ],
            "uses": "Allows officers to monitor 14,643 parcels, filter by health/disease/priority, inspect field images, approve/reject land claims, and view audit trails.",
            "how": "Classifies parcels into HIGH, MEDIUM, and LOW priority based on health thresholds (<50% = High). Employs stratified sampling so all 12 crops are visible as distinct emoji markers on Leaflet GIS."
        },
        {
            "num": "2.8",
            "name": "Agricultural-Only AI Chatbot & Voice Assistant",
            "apis": [
                "POST /api/chat (LangGraph conversational turn)",
                "POST /api/voice/transcribe (Audio to text via Gemini)",
                "POST /api/advisory/translate (Bilingual English-Tamil translation)"
            ],
            "uses": "Provides interactive voice and text advisory in Tamil and English strictly confined to farming, soils, diseases, weather, fertilizers, and market rates.",
            "how": "Features an Intent Gatekeeper that politely rejects non-agricultural questions. Injects live parcel soil/weather context and queries TNAU RAG embeddings to provide factual guidance."
        }
    ]

    for m in modules_en:
        story.append(Paragraph(f"<b>{m['num']} {m['name']}</b>", style_en_h2))
        
        # Details Table
        mod_table_data = [
            [Paragraph("<b>APIs Used:</b>", style_en_body), Paragraph("<br/>".join([f"<code>{a}</code>" for a in m['apis']]), style_en_body)],
            [Paragraph("<b>Primary Uses:</b>", style_en_body), Paragraph(m['uses'], style_en_body)],
            [Paragraph("<b>How It Works:</b>", style_en_body), Paragraph(m['how'], style_en_body)]
        ]
        t_mod = Table(mod_table_data, colWidths=[100, 387])
        t_mod.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f1f5f9')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t_mod)
        story.append(Spacer(1, 6))

    # ==================== SECTION 2: TAMIL ====================
    story.append(PageBreak())
    story.append(Paragraph("பிரிவு 2: முழுமையான அமைப்புக் கட்டமைப்பு & தொகுதிகளின் விளக்கம் (TAMIL)", style_ta_h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceAfter=10))

    intro_ta = ("ஃபார்ம்வைஸ் AI (FarmWise AI) என்பது தமிழ்நாட்டின் விவசாயிகளுக்காகவும், வேளாண் அதிகாரிகளுக்காகவும் உருவாக்கப்பட்ட "
                "அதிநவீன மல்டி-மாடல் (Multi-Model) மற்றும் பல-முகவர் (Multi-Agent) செயற்கை நுண்ணறிவு தளமாகும். இது மண் வளம், நேரடி வானிலை, "
                "பயிர் புகைப்பட நோய் ஆய்வு, TNAU/ICAR ஆராய்ச்சி வழிகாட்டல்கள் மற்றும் சந்தை விலைகளை ஒருங்கிணைத்து துல்லியமான ஆலோசனைகளை வழங்குகிறது.")
    story.append(Paragraph(intro_ta, style_ta_body))
    story.append(Spacer(1, 8))

    modules_ta = [
        {
            "num": "1.1",
            "name": "நில அளவை வரைபடம் & சர்வே எண் அடையாளம் (Geospatial Cadastral GIS)",
            "apis": "GET /api/parcels/search | GET /api/parcels/{survey_number} | GET /api/admin/crop-monitoring/cadastral-boundaries",
            "uses": "விவசாயியின் சர்வே எண் மற்றும் கிராமத்தை சரிபார்த்து, உண்மையான FMB நில வரைபட எல்லைகளுடன் இணைத்து காட்டுகிறது.",
            "how": "தென்காசி (சிவகிரி) மற்றும் தூத்துக்குடி மாவட்டங்களின் 14,643 நிலப் பதிவேடுகளை Turf.js மூலம் சரிபார்த்து, செயற்கைக்கோள் வரைபடத்தில் நிலப்பரப்பை காட்சிப்படுத்துகிறது."
        },
        {
            "num": "1.2",
            "name": "மண் வள அட்டை & ஊட்டச்சத்து மேலாண்மை (Soil Health Card Analysis)",
            "apis": "GET /api/parcels/{survey_number} (soil_profile) | POST /api/advisory/run (SoilAgent)",
            "uses": "மண்ணின் அமில/காரத்தன்மை (pH), கரிம கார்பன் மற்றும் NPK அளவுகளை ஆய்வு செய்து, ரசாயன மற்றும் இயற்கை உரங்களை பரிந்துரைக்கிறது.",
            "how": "கார மண் (pH > 7.8) என்றால் ஜிப்சம் (100 கிலோ/ஏக்கர்) மற்றும் துத்தநாக சல்பேட் பரிந்துரைக்கிறது. யூரியாவை 3 தவணைகளாக இடுவதற்கான அறிவியல் முறைகளை வழங்குகிறது."
        },
        {
            "num": "1.3",
            "name": "துல்லிய வானிலை முன்னறிவிப்பு (Weather Intelligence)",
            "apis": "GET /api/weather/parcel/{survey_number} | Open-Meteo REST API (7-day forecast)",
            "uses": "விவசாய நிலத்திற்கான நேரடி வானிலை, வெப்பநிலை, காற்றின் வேகம், ஈரப்பதம் மற்றும் 7 நாள் மழை வாய்ப்பை வழங்குகிறது.",
            "how": "சர்வே எண்ணின் அமைவிடத்தை எடுத்து Open-Meteo API மூலம் வானிலையை பெற்று, மருந்து தெளிப்பதற்கும் பாசனத்திற்கும் உகந்த நேரத்தை வழிகாட்டுகிறது."
        },
        {
            "num": "1.4",
            "name": "பயிர் புகைப்பட நோய் கண்டறிதல் (Computer Vision Disease Diagnosis)",
            "apis": "POST /api/upload (புகைப்பட பதிவேற்றம்) | Gemini 1.5 Flash Vision API",
            "uses": "விவசாயி தனது செல்போனில் எடுக்கும் பயிர் புகைப்படத்தை ஆய்வு செய்து, பயிரின் வகை, வளர்ச்சி நிலை மற்றும் தாக்கியுள்ள நோய்களை கண்டறிகிறது.",
            "how": "Gemini Flash AI மாதிரி பயிரின் இலைப்புள்ளி, கருகல், தண்டு துளைப்பான் போன்ற நோய்களை அடையாளம் கண்டு, ஆரோக்கிய மதிப்பெண் (0-100%) மற்றும் TNAU அங்கீகரித்த மருந்துகளை கூறுகிறது."
        },
        {
            "num": "1.5",
            "name": "ஒருங்கிணைந்த முகவர் ஆலோசனை இயந்திரம் (LangGraph Multi-Agent Orchestrator)",
            "apis": "POST /api/advisory/run (முழுமையான AI முகவர் செயலாக்கம்)",
            "uses": "மண், வானிலை, பயிர் ஆரோக்கியம் ஆகியவற்றை இணைத்து, பிழையற்ற, துல்லியமான இறுதி வேளாண் ஆலோசனையை உருவாக்குகிறது.",
            "how": "திட்டமிடல் முகவர் (Planner) பணிகளை பிரிக்கிறது. மண், வானிலை, பட முகவர்கள் தகவல்களை சேகரிக்கின்றன. Claude 3.5 Verifier முகவர் அனைத்து பரிந்துரைகளையும் அறிவியல் பூர்வமாக தணிக்கை செய்கிறது."
        },
        {
            "num": "1.6",
            "name": "பருவகால பயிர் பரிந்துரை & லாப கணிப்பு (Crop Recommendation & Profit Engine)",
            "apis": "GET /api/crop-recommendations | GET /api/crop-recommendations/{survey_number}/profit-analysis",
            "uses": "மண்ணின் தன்மை, பருவம், நீர் இருப்பு மற்றும் சந்தை விலையின் அடிப்படையில் அதிக லாபம் தரும் சிறந்த 5 மாற்றுப் பயிர்களை வரிசைப்படுத்துகிறது.",
            "how": "ஏக்கருக்கான சாகுபடி செலவு, எதிர்பார்க்கப்படும் மகசூல் மற்றும் e-NAM/Agmarknet சந்தை விலையை கணக்கிட்டு, விவசாயிக்கு கிடைக்கக்கூடிய நிகர லாபத்தை (Net Profit) முன்கூட்டியே காட்டுகிறது."
        },
        {
            "num": "1.7",
            "name": "அரசு அதிகாரிகள் கண்காணிப்பு வரைபடம் & ஸ்மார்ட் எச்சரிக்கைகள் (Admin Smart Alerts GIS)",
            "apis": "GET /api/admin/crop-monitoring/markers | PUT /api/admin/crop-monitoring/records/{id} | GET audit-log",
            "uses": "14,643 நிலங்களை அதிகாரிகள் கண்காணிக்கவும், நோய் தாக்கிய பயிர்களை உடனடியாக அடையாளம் கண்டு கள ஆய்வு செய்யவும் உதவுகிறது.",
            "how": "நிலங்களை உயர் (HIGH), நடுத்தர (MEDIUM), குறைந்த (LOW) முன்னுரிமையாக பிரிக்கிறது. வரைபடத்தில் அனைத்து 12 பயிர்களும் எமோஜி சின்னங்களாக (நெல், தென்னை, வாழை, மக்காச்சோளம்) தோன்றும் வகையில் Stratified Sampling பயன்படுத்தப்பட்டுள்ளது."
        },
        {
            "num": "1.8",
            "name": "விவசாய AI உரையாடல் & குரல் உதவியாளர் (Agricultural Voice Chatbot)",
            "apis": "POST /api/chat | POST /api/voice/transcribe | POST /api/advisory/translate",
            "uses": "விவசாய கேள்விகளுக்கு மட்டுமே பதிலளிக்கும் தமிழ்க் குரல் மற்றும் உரை உரையாடல் உதவியாளர்.",
            "how": "Domain Classifier மூலம் அரசியல், சினிமா, பொது தொழில்நுட்ப கேள்விகளை நாசூக்காக தவிர்த்து, விவசாய வினாக்களுக்கு மட்டும் TNAU நூலகம் மற்றும் விவசாயியின் நில விபரங்களின் அடிப்படையில் பதிலளிக்கிறது."
        }
    ]

    for m in modules_ta:
        story.append(Paragraph(f"<b>{m['num']} {m['name']}</b>", style_ta_h2))
        mod_table_ta = [
            [Paragraph("<b>பயன்படுத்தப்பட்ட API:</b>", style_ta_body), Paragraph(f"<code>{m['apis']}</code>", style_en_body)],
            [Paragraph("<b>முக்கிய பயன்பாடு:</b>", style_ta_body), Paragraph(m['uses'], style_ta_body)],
            [Paragraph("<b>செயல்படும் விதம்:</b>", style_ta_body), Paragraph(m['how'], style_ta_body)]
        ]
        t_ta = Table(mod_table_ta, colWidths=[110, 377])
        t_ta.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f0fdf4')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#86efac')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dcfce7')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t_ta)
        story.append(Spacer(1, 6))

    # Build PDF with custom NumberedCanvas for professional page numbering
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated bilingual PDF at: {filename} (Size: {os.path.getsize(filename)} bytes)")

if __name__ == "__main__":
    build_pdf()
