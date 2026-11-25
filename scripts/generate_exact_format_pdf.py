import os
import subprocess
import sys

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>FarmWise AI — Technical &amp; Agronomic Master Guide</title>
<style>
  @page {
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
  }

  * {
    box-sizing: border-box;
  }

  body {
    font-family: 'Segoe UI', 'Nirmala UI', 'Latha', Arial, sans-serif;
    color: #334155;
    font-size: 9.5pt;
    line-height: 1.55;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* Top Callout Card */
  .hero-card {
    background-color: #f0fdf4;
    border: 1.2px solid #a7f3d0;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 14px;
  }
  .hero-badge {
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: #059669;
    text-transform: uppercase;
    margin-bottom: 4px;
  }
  .hero-title {
    font-size: 16pt;
    font-weight: 800;
    color: #064e3b;
    margin: 0 0 4px 0;
  }
  .hero-sub {
    font-size: 9pt;
    color: #047857;
    margin: 0;
  }

  .main-title {
    font-size: 16pt;
    font-weight: 800;
    color: #065f46;
    margin: 10px 0 6px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid #059669;
  }
  .main-sub-ta {
    font-family: 'Nirmala UI', 'Latha', sans-serif;
    font-size: 10pt;
    font-style: italic;
    color: #475569;
    margin: 4px 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #e2e8f0;
  }

  .part-header {
    font-size: 13pt;
    font-weight: 800;
    color: #065f46;
    text-transform: uppercase;
    margin: 16px 0 10px 0;
    padding-bottom: 5px;
    border-bottom: 2px solid #10b981;
    page-break-after: avoid;
  }

  .module-section {
    margin-bottom: 14px;
  }

  h2.module-title {
    font-size: 11.5pt;
    font-weight: 700;
    color: #065f46;
    margin: 14px 0 6px 0;
    padding-bottom: 4px;
    border-bottom: 1px solid #cbd5e1;
    page-break-after: avoid;
  }

  h3.sub-title {
    font-size: 9.5pt;
    font-weight: 700;
    color: #0f766e;
    margin: 8px 0 3px 0;
    page-break-after: avoid;
  }

  p {
    margin: 0 0 6px 0;
  }

  ul, ol {
    margin: 2px 0 8px 0;
    padding-left: 18px;
  }

  li {
    margin-bottom: 3px;
  }

  code {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    background-color: #f1f5f9;
    color: #0f766e;
    padding: 1px 4px;
    border-radius: 3px;
  }

  .formula-box {
    background-color: #f8fafc;
    border-left: 3px solid #10b981;
    padding: 7px 11px;
    margin: 6px 0 8px 0;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    color: #0f172a;
    page-break-inside: avoid;
  }

  .diagram-box {
    background-color: #0f172a;
    border-radius: 8px;
    padding: 12px;
    margin: 8px 0 10px 0;
    text-align: center;
    page-break-inside: avoid;
  }

  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 12px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }
  table.data-table th {
    background-color: #065f46;
    color: #ffffff;
    text-align: left;
    padding: 7px 9px;
    font-weight: 700;
    border: 1px solid #065f46;
  }
  table.data-table td {
    padding: 7px 9px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
  }
  table.data-table tr:nth-child(even) td {
    background-color: #f8fafc;
  }

  .page-break {
    page-break-before: always;
  }

  .tamil-text {
    font-family: 'Nirmala UI', 'Latha', sans-serif;
  }
</style>
</head>
<body>

  <!-- HERO CALLOUT -->
  <div class="hero-card">
    <div class="hero-badge">FARMWISE AI PLATFORM ARCHITECTURE</div>
    <h1 class="hero-title">FarmWise AI — Technical &amp; Agronomic Master Guide</h1>
    <p class="hero-sub">Bilingual Implementation Reference (English &amp; தமிழ்) &bull; Task 1 Campus Challenge</p>
  </div>

  <div class="main-title">FarmWise AI — Comprehensive Engineering &amp; Agronomy Guide</div>
  <div class="main-sub-ta">(முழுமையான தொழில்நுட்ப மற்றும் வேளாண்மை வழிகாட்டி ஆவணம்)</div>

  <!-- ==================== PART 1: ENGLISH ==================== -->
  <div class="part-header">PART 1: COMPLETE ENGLISH DOCUMENTATION</div>

  <!-- 1 -->
  <div class="module-section">
    <h2 class="module-title">1. FarmWise AI Advisor (Core Orchestrator &amp; Conversational Agent)</h2>
    <h3 class="sub-title">Feature Overview</h3>
    <p>The <strong>FarmWise AI Advisor</strong> is the central coordinating engine of the platform. It functions as an agricultural expert system and conversational assistant that handles farmer inquiries via text, voice, or parcel selection. Rather than relying on a single AI model, it uses a multi-agent orchestrator that breaks down incoming requests, delegates tasks to specialized sub-agents, cross-verifies facts, and returns actionable advisories.</p>

    <h3 class="sub-title">Tech Stack &amp; APIs Used</h3>
    <ul>
      <li><strong>FastAPI (Python 3.11):</strong> Async REST API server (<code>POST /api/advisory/run</code>, <code>POST /api/chat</code>) chosen for non-blocking I/O, rapid JSON serialization, and native Pydantic validation.</li>
      <li><strong>LangGraph / Multi-Agent StateGraph:</strong> Manages multi-agent execution loops using a strongly-typed shared state (<code>AgentState</code>), enabling sequential and parallel agent execution.</li>
      <li><strong>Multi-Model Routing Architecture:</strong>
        <ul>
          <li><strong>Ministral 8B / 3B (AWS Bedrock):</strong> Low-latency, cost-effective open-weight model used for query classification, intent extraction, and light translation.</li>
          <li><strong>Gemini 1.5 Flash (Google API):</strong> High-speed multimodal model for plant image diagnostics and Tamil audio transcription fallback.</li>
          <li><strong>Claude 3.5 Sonnet (Anthropic):</strong> Operates as the <em>Verifier &amp; Critic Agent</em> to conduct hallucination checks and safety audits on agricultural recommendations.</li>
        </ul>
      </li>
      <li><strong>RAG System (Amazon Titan Text Embeddings V2 + Vector Store):</strong> Semantic search over official TNAU Crop Production Guide &amp; ICAR manuals.</li>
    </ul>

    <h3 class="sub-title">What It Does &amp; How It Works</h3>
    <ol>
      <li><strong>Request Intake:</strong> Farmer submits a query, survey number (e.g., <code>1476</code>), field photo, or Tamil voice recording.</li>
      <li><strong>Intent Gatekeeper &amp; Planning:</strong> <code>planner.py</code> classifies agricultural intent (politely refusing non-agricultural queries) and builds the agent execution graph.</li>
      <li><strong>Parallel Agent Execution:</strong> Geo, Weather, Soil, and Image agents hydrate the shared <code>AgentState</code> concurrently.</li>
      <li><strong>Knowledge &amp; Verifier Audit:</strong> <code>knowledge_agent.py</code> pulls TNAU guidelines; <code>verifier_agent.py</code> (Claude 3.5) audits fertilizer dosages and weather conflicts before delivery.</li>
    </ol>
  </div>

  <!-- 2 -->
  <div class="module-section">
    <h2 class="module-title">2. Cadastral Parcel &amp; FMB Boundary</h2>
    <h3 class="sub-title">Feature Overview</h3>
    <p>Bridges physical land ownership records with interactive digital maps using Tamil Nadu Land Records and Field Measurement Book (FMB) survey data across Tenkasi (Sivagiri) and Thoothukudi districts (14,643 registered records).</p>

    <h3 class="sub-title">Tech Stack &amp; APIs Used</h3>
    <ul>
      <li><strong>APIs:</strong> <code>GET /api/parcels/search</code>, <code>GET /api/parcels/{survey_number}</code>, <code>GET /api/admin/crop-monitoring/cadastral-boundaries</code>.</li>
      <li><strong>Turf.js &amp; GeoJSON:</strong> Point-in-polygon validation, area calculation (Acres/Hectares), and geographic centroid computation.</li>
      <li><strong>React Leaflet + Esri Satellite &amp; OpenStreetMap:</strong> Interactive map rendering with cadastral polygon overlays.</li>
    </ul>

    <h3 class="sub-title">How It Works</h3>
    <ol>
      <li>User enters or speaks a survey number; <code>geo_agent.py</code> queries <code>Ground_truth_Points.csv</code> and FMB GeoJSON files.</li>
      <li>Computes parcel area, centroid <code>[lat, lng]</code>, and masks PII landowner names by default (e.g., <code>R. K****</code>) for public privacy compliance.</li>
    </ol>
  </div>

  <!-- 3 & 4 -->
  <div class="module-section">
    <h2 class="module-title">3. Ground-Truth Field Photo &amp; 4. Crop Phenotype &amp; Health</h2>
    <h3 class="sub-title">Feature Overview</h3>
    <p>Manages field photograph ingestion, EXIF GPS verification, and multimodal computer vision diagnostics to detect crop species, growth stage, pests, and foliar diseases.</p>

    <h3 class="sub-title">Tech Stack &amp; APIs Used</h3>
    <ul>
      <li><strong>APIs:</strong> <code>POST /api/upload</code> (streaming multipart upload).</li>
      <li><strong>Python PIL / Pillow &amp; ExifRead:</strong> Extracts GPS coordinates &amp; timestamps to verify photo proximity to the claimed parcel.</li>
      <li><strong>Private AWS S3 (ap-south-1 Mumbai):</strong> Secure private object storage.</li>
      <li><strong>Gemini 1.5 Flash Multimodal Vision + Titan Multimodal Embeddings (Fallback):</strong> Returns structured JSON (<code>CropAnalysis</code>) with crop name, growth stage, health score (0–100%), and detected pathology.</li>
    </ul>
  </div>

  <!-- 5 -->
  <div class="module-section">
    <h2 class="module-title">5. Micro-Climate &amp; Agro-Met Intelligence</h2>
    <h3 class="sub-title">Feature Overview &amp; APIs</h3>
    <p>Provides parcel-level 7-day weather forecasts and 14-day rainfall history via <code>GET /api/weather/parcel/{survey_number}</code> backed by the keyless <strong>Open-Meteo REST API</strong>.</p>
    <div class="formula-box">
      Rule 1 (Rain Leaching): Forecast Rainfall (48h) &gt; 15 mm &rArr; Trigger Rain Leaching Warning (Delay Urea)<br/>
      Rule 2 (Spray Safety): Wind Speed &lt; 15 km/h AND Rain Prob &lt; 30% &rArr; Safe Foliar Spraying Window<br/>
      Rule 3 (Pathogen Risk): Humidity &gt; 85% AND 24&deg;C &le; Temp &le; 28&deg;C &rArr; High Blast / Blight Risk
    </div>
  </div>

  <!-- 6 -->
  <div class="module-section">
    <h2 class="module-title">6. Soil Health &amp; Chemical Profile (In-Depth Technical Breakdown)</h2>
    <h3 class="sub-title">Feature Overview</h3>
    <p>Evaluates parcel-level soil chemical properties (pH, EC, Organic Carbon, NPK) grounded in Tamil Nadu Agricultural University (TNAU) Soil Survey &amp; National Soil Health Card (SHC) standards.</p>

    <div class="diagram-box">
      <svg width="480" height="175" viewBox="0 0 480 175" xmlns="http://www.w3.org/2000/svg">
        <rect x="160" y="6" width="160" height="24" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
        <text x="240" y="21" fill="#ffffff" font-size="9.5" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">Survey Number (Cadastral ID)</text>
        <line x1="240" y1="30" x2="240" y2="45" stroke="#38bdf8" stroke-width="1.2"/>
        <polygon points="236,42 244,42 240,48" fill="#38bdf8"/>

        <rect x="130" y="48" width="220" height="24" rx="4" fill="#1e293b" stroke="#10b981" stroke-width="1.2"/>
        <text x="240" y="63" fill="#ffffff" font-size="9.5" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">Deterministic Soil Registry (SHA-256 + TNAU)</text>
        <line x1="240" y1="72" x2="240" y2="86" stroke="#38bdf8" stroke-width="1.2"/>
        <polygon points="236,83 244,83 240,89" fill="#38bdf8"/>

        <rect x="75" y="89" width="330" height="30" rx="4" fill="#090d16" stroke="#cbd5e1" stroke-width="1"/>
        <text x="240" y="102" fill="#e2e8f0" font-size="8.5" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">Chemical Soil Profile: pH 8.2 (Alkaline) | OC: 0.42% (Low)</text>
        <text x="240" y="114" fill="#94a3b8" font-size="8" text-anchor="middle" font-family="Segoe UI, sans-serif">Available NPK: N = 170 kg/ha | P = 12 kg/ha | K = 260 kg/ha</text>

        <line x1="155" y1="119" x2="155" y2="134" stroke="#38bdf8" stroke-width="1.2"/>
        <polygon points="151,131 159,131 155,137" fill="#38bdf8"/>
        <line x1="325" y1="119" x2="325" y2="134" stroke="#38bdf8" stroke-width="1.2"/>
        <polygon points="321,131 329,131 325,137" fill="#38bdf8"/>

        <rect x="35" y="137" width="205" height="30" rx="4" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
        <text x="137" y="150" fill="#fbbf24" font-size="8.5" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">Efficiency Score Engine</text>
        <text x="137" y="162" fill="#cbd5e1" font-size="7.5" text-anchor="middle" font-family="Segoe UI, sans-serif">pH Penalty + OC Boost &rarr; 62% Uptake</text>

        <rect x="250" y="137" width="205" height="30" rx="4" fill="#1e293b" stroke="#10b981" stroke-width="1.2"/>
        <text x="352" y="150" fill="#34d399" font-size="8.5" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">Soil Amendment Engine</text>
        <text x="352" y="162" fill="#cbd5e1" font-size="7.5" text-anchor="middle" font-family="Segoe UI, sans-serif">Gypsum 100 kg/ac + ZnSO4 10 kg/ac</text>
      </svg>
    </div>

    <div class="formula-box">
      pH Penalty = |pH - 7.0| &times; 12.0 &nbsp;|&nbsp; OC Boost = (Organic Carbon - 0.5) &times; 15.0<br/>
      Fertilizer Uptake Efficiency Score = Clamp(85 - pH Penalty + OC Boost, 52%, 92%)
    </div>
    <ul>
      <li><strong>Alkaline Soils (pH &gt; 7.8):</strong> Apply Agricultural Gypsum (100 kg/acre), green manure (Daincha @ 20 kg/acre), Neem-Coated Urea in splits, and Zinc Sulphate (10 kg/acre).</li>
      <li><strong>Acidic Soils (pH &lt; 6.3):</strong> Apply Agricultural Lime / Dolomite (120 kg/acre) and Rock Phosphate.</li>
    </ul>
  </div>

  <!-- 7 -->
  <div class="module-section">
    <h2 class="module-title">7. Personalised Agronomic Advisory &amp; Multi-Agent Interlocks</h2>
    <p>Synthesizes crop phenotype, soil profile, and weather forecast into a verified action plan with dynamic dosage compensation (e.g., reducing DAP by 20% when soil Phosphorus &gt; 22 kg/ha, adding Azospirillum + Phosphobacteria bio-fertilizers, and postponing Urea top-dressing if 48h rainfall &gt; 15 mm).</p>
    <div class="diagram-box">
      <svg width="480" height="175" viewBox="0 0 480 175" xmlns="http://www.w3.org/2000/svg">
        <rect x="45" y="6" width="175" height="24" rx="4" fill="#1e293b" stroke="#10b981" stroke-width="1.2"/>
        <text x="132" y="21" fill="#ffffff" font-size="8.5" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">Crop Phenotype (Paddy - Tillering)</text>
        <rect x="260" y="6" width="175" height="24" rx="4" fill="#1e293b" stroke="#0ea5e9" stroke-width="1.2"/>
        <text x="347" y="21" fill="#ffffff" font-size="8.5" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">Weather (35mm Rain in 24 hrs)</text>

        <line x1="132" y1="30" x2="132" y2="39" stroke="#38bdf8" stroke-width="1.2"/>
        <line x1="347" y1="30" x2="347" y2="39" stroke="#38bdf8" stroke-width="1.2"/>
        <line x1="132" y1="39" x2="347" y2="39" stroke="#38bdf8" stroke-width="1.2"/>
        <line x1="240" y1="39" x2="240" y2="49" stroke="#38bdf8" stroke-width="1.2"/>
        <polygon points="236,46 244,46 240,52" fill="#38bdf8"/>

        <rect x="120" y="52" width="240" height="24" rx="4" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
        <text x="240" y="67" fill="#ffffff" font-size="9" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">Agricultural Knowledge Agent (TNAU RAG)</text>

        <line x1="150" y1="76" x2="150" y2="88" stroke="#38bdf8" stroke-width="1.2"/>
        <line x1="330" y1="76" x2="330" y2="88" stroke="#38bdf8" stroke-width="1.2"/>

        <rect x="40" y="88" width="190" height="28" rx="4" fill="#1e293b" stroke="#eab308" stroke-width="1.2"/>
        <text x="135" y="100" fill="#fde047" font-size="8" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">Soil Profile Interlock</text>
        <text x="135" y="111" fill="#cbd5e1" font-size="7.5" text-anchor="middle" font-family="Segoe UI, sans-serif">High P &rarr; Reduce DAP by 20%</text>

        <rect x="250" y="88" width="190" height="28" rx="4" fill="#1e293b" stroke="#ef4444" stroke-width="1.2"/>
        <text x="345" y="100" fill="#fca5a5" font-size="8" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">Weather Conflict Interlock</text>
        <text x="345" y="111" fill="#cbd5e1" font-size="7.5" text-anchor="middle" font-family="Segoe UI, sans-serif">Heavy Rain &rarr; Postpone Urea</text>

        <line x1="135" y1="116" x2="135" y2="126" stroke="#38bdf8" stroke-width="1.2"/>
        <line x1="345" y1="116" x2="345" y2="126" stroke="#38bdf8" stroke-width="1.2"/>
        <line x1="135" y1="126" x2="345" y2="126" stroke="#38bdf8" stroke-width="1.2"/>
        <line x1="240" y1="126" x2="240" y2="136" stroke="#38bdf8" stroke-width="1.2"/>
        <polygon points="236,133 244,133 240,139" fill="#38bdf8"/>

        <rect x="115" y="139" width="250" height="28" rx="4" fill="#1e293b" stroke="#a855f7" stroke-width="1.2"/>
        <text x="240" y="151" fill="#d8b4fe" font-size="8.5" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">Claude 3.5 Sonnet Verifier</text>
        <text x="240" y="162" fill="#cbd5e1" font-size="7.5" text-anchor="middle" font-family="Segoe UI, sans-serif">Safety Audit &rarr; Final Bilingual Advisory Card</text>
      </svg>
    </div>
  </div>

  <!-- 8 & 9 -->
  <div class="module-section">
    <h2 class="module-title">8. Seasonal Crop Recommendation &amp; Profit Prediction + Admin GIS Monitoring</h2>
    <ul>
      <li><strong>Crop Recommendation Engine (<code>GET /api/crop-recommendations</code>, <code>/profit-analysis</code>, <code>/market-trends</code>):</strong> Ranks Top 5 seasonal crops using Soil (35%), Weather (25%), Economics (25%), and TNAU Suitability (15%), displaying cultivation cost, expected yield, Agmarknet/e-NAM selling price, and Net Profit per acre.</li>
      <li><strong>Admin Priority GIS Monitoring (<code>GET /api/admin/crop-monitoring/markers</code>, <code>/records</code>, <code>PUT /records/{id}</code>):</strong> Monitors 14,643 parcels with cascading filters (District, Taluk, Village, Crop, Health, Disease, Verification: <em>Verified, Verification Required, Rejected, Not Verified</em>, Priority: <em>HIGH, MEDIUM, LOW</em>). Uses <strong>stratified multi-crop sampling</strong> so all 12 crops render simultaneously on Leaflet satellite maps, synced with the verification registry table and audit log.</li>
    </ul>

    <h3 class="sub-title">Additional Platform Capabilities Summary</h3>
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 24%;">Feature</th>
          <th style="width: 26%;">Tech Stack / APIs</th>
          <th style="width: 50%;">What It Does &amp; How It Works</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Bilingual Voice Assistant</strong></td>
          <td>Web Speech API + <code>POST /api/voice/transcribe</code></td>
          <td>Farmers speak in Tamil or English; audio is transcribed via Gemini Flash fallback, processed by the agricultural-only chatbot, and read aloud via TTS.</td>
        </tr>
        <tr>
          <td><strong>Government-Format Report</strong></td>
          <td>HTML Print CSS + QR Verification</td>
          <td>Compiles parcel boundaries, soil cards, and advisories into an official bilingual Tamil Nadu Agriculture Dept format with SHA-256 verification.</td>
        </tr>
        <tr>
          <td><strong>APMC Mandi Market Prices</strong></td>
          <td><code>GET /api/market/prices</code> (e-NAM / Agmarknet)</td>
          <td>Retrieves live modal prices (&#8377;/Quintal) from nearby regional markets (Tenkasi, Tirunelveli, Madurai) to inform harvest timing.</td>
        </tr>
        <tr>
          <td><strong>Farmer Data Privacy Masking</strong></td>
          <td><code>privacy_service.py</code></td>
          <td>Automatically masks landowner names (e.g., <code>Murugan S. &rarr; M****** S.</code>) in public views while exposing full records only to authenticated officers.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- ==================== PART 2: TAMIL ==================== -->
  <div class="page-break"></div>
  <div class="part-header tamil-text">PART 2: TAMIL TRANSLATION &amp; EXPLANATION (பகுதி 2: விரிவான தமிழ் விளக்கக் கையேடு)</div>

  <!-- TA 1 -->
  <div class="module-section tamil-text">
    <h2 class="module-title">1. FarmWise AI Advisor (முதன்மை ஒருங்கிணைப்பாளர் &amp; உரையாடல் உதவியாளர்)</h2>
    <h3 class="sub-title">இந்த அம்சம் என்ன செய்கிறது?</h3>
    <p><strong>FarmWise AI Advisor</strong> என்பது இந்த தளத்தின் <strong>"மைய மூளை" (Central Brain)</strong> ஆகும். ஒரு விவசாயி தனது சர்வே எண், நிலத்தின் புகைப்படம் அல்லது தமிழ் குரல் மூலம் கேள்வி கேட்கும்போது, இந்த ஆலோசகர் பல்வேறு துணை ஏஜென்ட்டுகளை (Sub-Agents) இயக்கி, துல்லியமான மற்றும் பாதுகாப்பான வேளாண் ஆலோசனைகளை வழங்குகிறது.</p>

    <h3 class="sub-title">பயன்படுத்தப்பட்ட தொழில்நுட்பங்கள் &amp; APIகள்:</h3>
    <ul>
      <li><strong>FastAPI (Python 3.11):</strong> அதிவேகமான மற்றும் தடையற்ற API (<code>POST /api/advisory/run</code>, <code>POST /api/chat</code>) பரிமாற்றத்திற்கு பயன்படுகிறது.</li>
      <li><strong>LangGraph / Multi-Agent StateGraph:</strong> பல AI ஏஜென்ட்டுகள் ஒன்றுக்கொன்று தகவல்களைப் பகிர்ந்து செயல்பட உதவுகிறது.</li>
      <li><strong>Multi-Model Routing:</strong>
        <ul>
          <li><strong>Ministral 8B / 3B (AWS Bedrock):</strong> குறைந்த செலவில் விரைவான திட்டமிடல் மற்றும் விவசாயக் கேள்விகளை வகைப்படுத்தல்.</li>
          <li><strong>Gemini 1.5 Flash (Google Cloud):</strong> பயிர் புகைப்படங்களை ஆராயவும் மற்றும் தமிழ் குரல் பதிவுகளை உரையாக மாற்றவும்.</li>
          <li><strong>Claude 3.5 Sonnet:</strong> வழங்கப்பட்ட ஆலோசனைகளில் தவறுகள் உள்ளதா என சரிபார்க்கும் தணிக்கையாளராக (Verifier/Critic).</li>
        </ul>
      </li>
      <li><strong>Vector RAG (Amazon Titan Embeddings):</strong> தமிழ்நாடு வேளாண்மைப் பல்கலைக்கழகம் (TNAU) மற்றும் ICAR வழிகாட்டி கையேடுகளில் இருந்து அறிவியல் பூர்வமான தகவல்களைத் தேடி எடுக்கிறது.</li>
    </ul>

    <h3 class="sub-title">இது எவ்வாறு செயல்படுகிறது?</h3>
    <ol>
      <li>விவசாயி சர்வே எண்ணை உள்ளிடுகிறார் அல்லது தமிழ் குரலில் கேள்வி கேட்கிறார் (விவசாயம் அல்லாத கேள்விகள் நாசூக்காக தவிர்க்கப்படும்).</li>
      <li><code>planner.py</code> எந்தெந்த ஏஜென்ட்டுகள் செயல்பட வேண்டும் என்பதைத் திட்டமிடுகிறது.</li>
      <li>பயிர் புகைப்படம், மண் வளம் மற்றும் வானிலை தகவல்கள் ஒரே நேரத்தில் திரட்டப்படுகின்றன.</li>
      <li><strong>Knowledge Agent</strong> பல்கலைக்கழக வழிகாட்டுதல்களின்படி உரம் மற்றும் பூச்சி மேலாண்மை அட்டவணையை உருவாக்குகிறது.</li>
      <li><strong>Verifier Agent (Claude 3.5)</strong> இந்த பரிந்துரைகளில் ஆபத்தான தவறுகள் உள்ளதா என சரிபார்த்து உறுதி செய்கிறது.</li>
    </ol>
  </div>

  <!-- TA 2 -->
  <div class="module-section tamil-text">
    <h2 class="module-title">2. Cadastral Parcel &amp; FMB Boundary (நில அளவை மற்றும் FMB எல்லை வரைபடம்)</h2>
    <h3 class="sub-title">இந்த அம்சம் என்ன செய்கிறது?</h3>
    <p>விவசாயியின் பட்டா மற்றும் சிட்டா சர்வே எண்களைக் கொண்டு (எ.கா: <code>1476</code>, <code>386</code>), தென்காசி (சிவகிரி) மற்றும் தூத்துக்குடி மாவட்டங்களின் 14,643 நிலப் பதிவேடுகளில் இருந்து நிலத்தின் துல்லியமான எல்லைகளையும் பரப்பளவையும் (ஏக்கர்/ஹெக்டேர்) செயற்கைக்கோள் வரைபடத்தில் காட்டுகிறது.</p>
    <ul>
      <li><strong>APIகள்:</strong> <code>GET /api/parcels/search</code>, <code>GET /api/parcels/{survey_number}</code>, <code>GET /api/admin/crop-monitoring/cadastral-boundaries</code>.</li>
      <li><strong>தொழில்நுட்பம்:</strong> Turf.js, GeoJSON, React Leaflet + Esri Satellite. விவசாயியின் தனிப்பட்ட பெயர்கள் பாதுகாக்கப்பட்டு மறைக்கப்படும் (எ.கா: <code>R. K****</code>).</li>
    </ul>
  </div>

  <!-- TA 3 & 4 -->
  <div class="module-section tamil-text">
    <h2 class="module-title">3. Ground-Truth Field Photo &amp; 4. Crop Phenotype &amp; Health (களப் புகைப்படம் &amp; பயிர் நோய் ஆய்வு)</h2>
    <p>விவசாயிகள் வயலில் எடுக்கும் பயிர் புகைப்படங்களை <code>POST /api/upload</code> மூலம் பதிவேற்றும்போது, <strong>PIL / ExifRead</strong> மூலம் GPS இருப்பிடம் சரிபார்க்கப்பட்டு <strong>Private AWS S3 (Mumbai)</strong>-ல் சேமிக்கப்படுகிறது. பின்னர் <strong>Gemini 1.5 Flash Vision</strong> படத்தை ஆய்வு செய்து பயிர் வகை, வளர்ச்சிப் பருவம், ஆரோக்கிய மதிப்பெண் (0–100%) மற்றும் பூச்சி/நோய்களைத் துல்லியமாகக் கண்டறிகிறது.</p>
  </div>

  <!-- TA 5 -->
  <div class="module-section tamil-text">
    <h2 class="module-title">5. Micro-Climate &amp; Agro-Met (நுண் வானிலை &amp; வேளாண் எச்சரிக்கைகள்)</h2>
    <p><code>GET /api/weather/parcel/{survey_number}</code> மற்றும் <strong>Open-Meteo Weather API</strong> மூலம் நிலத்திற்குரிய நேரடி 7-நாள் வானிலை முன்னறிவிப்பைப் பெறுகிறது.</p>
    <div class="formula-box tamil-text">
      1. மழை உரம் இழப்பு எச்சரிக்கை: அடுத்த 48 மணி நேரத்தில் 15 மி.மீ-க்கு மேல் மழை பெய்தால் யூரியா இடுவதைத் தள்ளிப்போட எச்சரிக்கும்.<br/>
      2. மருந்து தெளிக்கும் நேரம்: காற்றின் வேகம் 15 கி.மீ/மணிக்கு குறைவாகவும் மழை வாய்ப்பின்றியும் இருந்தால் பாதுகாப்பான நேரம் எனக் காட்டும்.<br/>
      3. பூஞ்சாண நோய் எச்சரிக்கை: ஈரப்பதம் 85%-க்கு மேலும் வெப்பநிலை 24–28&deg;C ஆகவும் இருந்தால் குலைநோய் (Blast) எச்சரிக்கை வழங்கும்.
    </div>
  </div>

  <!-- TA 6 -->
  <div class="module-section tamil-text">
    <h2 class="module-title">6. Soil Health &amp; Chemical Profile (மண்வளம் மற்றும் ஊட்டச்சத்து பகுப்பாய்வு)</h2>
    <p>TNAU மற்றும் தேசிய மண்வள அட்டைத் திட்டத்தின் (SHC) கீழ் மண்ணின் கார-அமிலத்தன்மை (pH), கரிமக் கரிமம் (OC), தழை, மணி, சாம்பல் சத்துக்கள் (NPK) மற்றும் உவர் தன்மையை (EC) ஆய்வு செய்கிறது.</p>
    <ul>
      <li><strong>மண் காரத்தன்மை (pH &gt; 7.8):</strong> ஏக்கருக்கு 100 கிலோ வேளாண் ஜிப்சம், தக்கைப்பூண்டு பசுந்தாள் உரம் (20 கிலோ/ஏக்கர்), வேப்பம்பூசப்பட்ட யூரியா மற்றும் துத்தநாக சல்பேட் (10 கிலோ/ஏக்கர்) பரிந்துரைக்கப்படுகிறது.</li>
      <li><strong>மண் அமிலத்தன்மை (pH &lt; 6.3):</strong> ஏக்கருக்கு 120 கிலோ வேளாண் சுண்ணாம்பு (டாலமைட்) மற்றும் ராக் பாஸ்பேட் பரிந்துரைக்கப்படுகிறது.</li>
      <li><strong>உர பயன்பாட்டுத் திறன்:</strong> நடுநிலையான மண்ணில் (pH 6.8–7.2) உர ஏற்புத்திறன் 88% வரை இருக்கும்; கார மண்ணில் (pH 8.2) இது 62% ஆகக் குறையும்.</li>
    </ul>
  </div>

  <!-- TA 7 -->
  <div class="module-section tamil-text">
    <h2 class="module-title">7. Personalised Agronomic Advisory (தனிப்பயனாக்கப்பட்ட வேளாண் ஆலோசனை)</h2>
    <p><code>knowledge_agent.py</code> மற்றும் <code>verifier_agent.py</code> (Claude 3.5) இணைந்து மண்ணில் மணிச்சத்து அதிகமாக இருந்தால் DAP உரத்தை 20% குறைத்து செலவை மிச்சப்படுத்துகிறது. அசோஸ்பைரில்லம் மற்றும் பாஸ்போபாக்டீரியா உயிர் உரங்களை இணைத்து இரசாயன உரத் தேவையை 25% குறைக்கிறது. மழை முன்னறிவிப்பு இருந்தால் உரமிடும் தேதியைத் தானாகவே மாற்றியமைத்துத் தமிழ் குரல் வடிவிலும் (TTS) வழங்குகிறது.</p>
  </div>

  <!-- TA 8 -->
  <div class="module-section tamil-text">
    <h2 class="module-title">8. பருவகால பயிர் பரிந்துரை, லாப கணிப்பு &amp; அரசு அதிகாரி GIS கண்காணிப்பு</h2>
    <ul>
      <li><strong>பயிர் பரிந்துரை &amp; லாப கணிப்பு (<code>GET /api/crop-recommendations</code>):</strong> மண் தன்மை, பருவம், நீர் வசதி மற்றும் e-NAM/Agmarknet சந்தை விலையின் அடிப்படையில் அதிக லாபம் தரும் சிறந்த 5 மாற்றுப் பயிர்களை சாகுபடி செலவு மற்றும் நிகர லாபத்துடன் (Net Profit) காட்டுகிறது.</li>
      <li><strong>அரசு அதிகாரி GIS கண்காணிப்பு (<code>GET /api/admin/crop-monitoring/markers</code>):</strong> 14,643 நிலப் பதிவேடுகளை மாவட்டம், வட்டம், கிராமம், பயிர், ஆரோக்கியம், நோய், சரிபார்ப்பு நிலை (<em>Verified, Verification Required, Rejected, Not Verified</em>) மற்றும் முன்னுரிமை (<em>HIGH, MEDIUM, LOW</em>) அடிப்படையில் வடிகட்டி, 12 பயிர்களின் எமோஜி சின்னங்களையும் செயற்கைக்கோள் வரைபடத்திலும் கீழேயுள்ள அட்டவணையிலும் துல்லியமாகக் காட்டுகிறது.</li>
    </ul>

    <table class="data-table tamil-text">
      <thead>
        <tr>
          <th style="width: 24%;">கூடுதல் அம்சம்</th>
          <th style="width: 26%;">பயன்படுத்தப்பட்ட தொழில்நுட்பம்</th>
          <th style="width: 50%;">என்ன செய்கிறது &amp; எவ்வாறு இயங்குகிறது?</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>இருமொழி குரல் உதவியாளர் (தமிழ் &amp; ஆங்கிலம்)</strong></td>
          <td>Web Speech API + Gemini Audio</td>
          <td>விவசாயிகள் மைக்ரோஃபோன் பொத்தானை அழுத்தி தமிழில் பேசலாம். AI அதனைப் புரிந்துகொண்டு தமிழிலேயே பதிலளித்து குரலாக வாசிக்கும்.</td>
        </tr>
        <tr>
          <td><strong>அரசு மாதிரி அச்சு அறிக்கை (Printable Report)</strong></td>
          <td>HTML Print CSS + QR Code</td>
          <td>நில வரைபடம், பயிர் நிலை, மண் அட்டை மற்றும் ஆலோசனைகளை அரசு அதிகாரிகள் மற்றும் வங்கி கடன் பெறுவதற்கு ஏற்ற ஆவணமாக அச்சிட்டுத் தருகிறது.</td>
        </tr>
        <tr>
          <td><strong>நேரடி சந்தை (APMC Mandi) விலை நிலவரம்</strong></td>
          <td>e-NAM / Agmarknet API</td>
          <td>அருகிலுள்ள சந்தைகளில் (தென்காசி, திருநெல்வேலி, மதுரை) விளைபொருட்களின் இன்றைய விற்பனை விலையைக் (&#8377;/குவிண்டால்) காட்டுகிறது.</td>
        </tr>
        <tr>
          <td><strong>விவசாயி தரவுப் பாதுகாப்பு (PII Masking)</strong></td>
          <td><code>privacy_service.py</code></td>
          <td>பட்டாதாரரின் தனிப்பட்ட பெயர்களை மறைத்து (எ.கா: <code>M****** S.</code>) பாதுகாப்பாக வைக்கிறது; அதிகாரிகள் உள்நுழையும் போது மட்டுமே முழு விவரமும் தெரியும்.</td>
        </tr>
      </tbody>
    </table>
  </div>

</body>
</html>
"""

def generate_pdf_via_chrome():
    os.makedirs("docs", exist_ok=True)
    html_path = os.path.abspath("docs/FarmWise_AI_System_Documentation.html")
    pdf_path = os.path.abspath("docs/FarmWise_AI_System_Documentation.pdf")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_CONTENT)

    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    browser = next((p for p in chrome_candidates if os.path.exists(p)), None)
    if not browser:
        print("Error: Neither Chrome nor Edge was found for HTML-to-PDF rendering.", file=sys.stderr)
        sys.exit(1)

    file_url = "file:///" + html_path.replace("\\", "/")
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        file_url
    ]
    print(f"Rendering PDF using {os.path.basename(browser)} (full HarfBuzz Tamil shaping)...")
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if res.returncode != 0:
        print("Browser error:", res.stderr, file=sys.stderr)
        sys.exit(res.returncode)

    if os.path.exists(pdf_path):
        print(f"Successfully generated readable bilingual PDF: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
    else:
        print("Error: PDF file was not created.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    generate_pdf_via_chrome()
