# FarmWise AI - Complete System Architecture, Modules, APIs & Technical Documentation
## முழுமையான கணினி கட்டமைப்பு, தொகுதிகள், ஏபிஐ விவரங்கள் மற்றும் தொழில்நுட்ப ஆவணம்

---

# SECTION 1: ENGLISH DOCUMENTATION

## 1. Executive Summary & Platform Overview

**FarmWise AI** is an enterprise-grade, agentic multi-model agricultural intelligence platform developed for the **FarmwiseAI Campus Product Challenge (Task 1: Multi-Model, Multimodal, and Agentic AI System)**. It transforms fragmented, heterogeneous agricultural data—including satellite cadastral land maps (FMB), soil health card metrics, real-time meteorological feeds, computer vision field photos, agricultural research corpora (TNAU / ICAR), and commodity market rates (e-NAM / Agmarknet)—into verifiable, actionable agricultural advisories and spatial intelligence.

The system is designed for two primary user personas:
1. **Farmers**: Provided with a simple, voice-first (Tamil and English), touch-friendly mobile interface for parcel advisory, disease diagnosis, crop recommendation, and conversational guidance.
2. **Agricultural & Administrative Officers**: Provided with a GIS-powered state-wide dashboard featuring cadastral boundary overlays, smart priority alerts, audit logging, manual ground verification workflows, and formal government-format advisory reports.

---

## 2. System Architecture & Multi-Model Orchestration

```
+---------------------------------------------------------------------------------------------------+
|                                  USER INTERFACE LAYER (React + Vite)                              |
|   +-----------------------+   +----------------------+   +------------------------------------+   |
|   | Farmer Mobile Portal  |   | Voice Assistant (TA) |   | Admin GIS & Smart Alerts Dashboard |   |
|   +-----------+-----------+   +----------+-----------+   +-----------------+------------------+   |
+---------------|--------------------------|---------------------------------|----------------------+
                |                          |                                 |
                +--------------------------+---------------------------------+
                                           | HTTPS / REST / SSE
                                           v
+---------------------------------------------------------------------------------------------------+
|                                 FASTAPI & AGENT ORCHESTRATOR LAYER                                |
|  FastAPI Router (app/main.py) <---> LangGraph Workflow State Machine (app/agents/graph.py)       |
+---------------------------------------------------------------------------------------------------+
       |                    |                    |                   |                   |
       v                    v                    v                   v                   v
+--------------+   +----------------+   +---------------+   +----------------+   +------------------+
| Planner Agent|   | Geo & Cadastre |   | Weather Agent |   | Vision / Image |   | Agri Knowledge   |
| (Ministral-8B|   | (Turf.js / GIS |   | (Open-Meteo   |   | (Gemini-Flash/ |   | (TNAU / ICAR RAG |
| / Bedrock)   |   | Cadastral FMB) |   | 7-Day Forecast|   | Phenotype DL)  |   | Titan Embeddings)|
+--------------+   +----------------+   +---------------+   +----------------+   +------------------+
       |                    |                    |                   |                   |
       +--------------------+--------------------+-------------------+-------------------+
                                           |
                                           v
                       +---------------------------------------+
                       |   Critic / Verifier Agent             |
                       |   (Claude 3.5 Sonnet / Multi-Check)   |
                       +---------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------------------+
|                                   DATA & STORAGE ADAPTERS                                         |
|  - S3 / Local Private Vault: Cadastral GeoJSON, Field Photos, Generated Advisory Artifacts        |
|  - In-Memory & DynamoDB Repository: 14,643 Ground Truth Parcels, Audit Logs, SHC Soil Profiles    |
+---------------------------------------------------------------------------------------------------+
```

### Multi-Model Justification & Routing Strategy
In strict adherence to Task 1 specifications, FarmWise AI employs at least 3 distinct models with differentiated architectural roles:
1. **Ministral 8B / 3B Instruct (AWS Bedrock)**: Low-latency, cost-effective open-weight model utilized for high-throughput initial task planning, structured schema extraction, query intent classification, and query rewriting.
2. **Gemini 1.5 Flash / Pro (Google API)**: High-speed multimodal vision analysis for field plant photograph inspection, disease detection, phenotyping, and speech-to-text audio transcription fallback.
3. **Claude 3.5 Sonnet (Anthropic API)**: Premier cognitive engine acting as the autonomous **Critic and Verifier Agent**, inspecting agronomic recommendations, validating fertilizer dosages against soil pH thresholds, and halting hallucinations before reports are issued.
4. **Amazon Titan Text Embeddings V2 & Titan Multimodal Embeddings**: Dense vector representations for semantic RAG search across TNAU / ICAR manuals.

---

## 3. Detailed Module Specifications

### Module 1: Geospatial Cadastral Mapping & Parcel Identification
- **Purpose**: Correlates survey numbers with physical cadastral boundaries and verifies geo-coordinates against authentic Tamil Nadu land records (Tenkasi & Thoothukudi districts).
- **APIs Used**:
  - `GET /api/parcels/search?q={query}`: Searches registered cadastral survey numbers.
  - `GET /api/parcels/{survey_number}`: Retrieves complete parcel attributes, soil profile, and geo-polygon.
  - `GET /api/admin/crop-monitoring/cadastral-boundaries`: Returns GeoJSON polygons for Leaflet overlay.
- **How It Works**:
  1. The user inputs or speaks a survey number (e.g., `1476`, `386`).
  2. The service queries `Ground_truth_Points.csv` and GeoJSON files (`Cadastral_Map_Final.geojson` and `FMB_sample.geojson`).
  3. It validates if the coordinates reside inside authorized village boundaries using point-in-polygon calculations.
  4. The frontend renders the land parcel geometry directly on Esri Satellite and OpenStreetMap base layers.

### Module 2: Soil Health Card (SHC) & Chemical Reclamation Analysis
- **Purpose**: Computes nutrient deficiencies, soil reaction (pH), electrical conductivity (EC), and organic carbon (OC) to generate precise chemical and bio-fertilizer reclamation guidelines.
- **APIs Used**:
  - Integrated within `/api/parcels/{survey_number}` and `/api/advisory/run`.
- **How It Works**:
  1. Retrieves registered NPK, pH, EC, and OC values for the parcel.
  2. Evaluates ratings against scientific agronomical thresholds:
     - Alkaline ($pH > 7.8$): Recommends agricultural gypsum ($\text{CaSO}_4\cdot 2\text{H}_2\text{O}$) and zinc sulphate ($\text{ZnSO}_4$).
     - Acidic ($pH < 6.5$): Recommends agricultural lime ($\text{CaCO}_3$) or dolomite.
     - Optimal ($6.5 \le pH \le 7.5$): Recommends organic matter maintenance (composted coir pith, FYM).
  3. Tailors split nitrogen fertilizer strategies (e.g., Neem-Coated Urea in 3 splits) to minimize volatilization.

### Module 3: Agro-Meteorological Weather Intelligence
- **Purpose**: Provides hyper-local meteorological observations and 7-day predictive forecasts to guide sowing, spraying, and irrigation operations.
- **APIs Used**:
  - `GET /api/weather/parcel/{survey_number}`: Resolves parcel coordinates and calls the Open-Meteo REST API.
  - External API: `https://api.open-meteo.com/v1/forecast` (Free, keyless, global meteorological reanalysis).
- **How It Works**:
  1. Extracts latitude and longitude from the selected cadastral parcel.
  2. Fetches real-time temperature, relative humidity, wind speed, precipitation probability, and 7-day forecast.
  3. Computes spray suitability windows (e.g., alerts if wind speed exceeds 15 km/h or rain probability > 60%).

### Module 4: Multimodal Field Computer Vision & Crop Phenotyping
- **Purpose**: Diagnoses plant diseases, identifies growth stages, and validates crop health from field photographs.
- **APIs Used**:
  - `POST /api/upload`: Uploads and validates field imagery.
  - Multimodal Vision API via `gemini-1.5-flash` or Titan Multimodal Embeddings.
- **How It Works**:
  1. Farmer uploads a field photo via mobile camera or file selector.
  2. The image is passed to `image_agent.py` along with parcel context (crop name, planting date).
  3. The vision model analyzes morphological symptoms (e.g., yellowing leaves, leaf blast lesions, stem borer holes).
  4. Outputs a structured verdict: crop identification, phenological stage (vegetative, flowering, harvesting), health score (0–100%), and detected pathogens.

### Module 5: LangGraph Multi-Agent Advisory Orchestrator
- **Purpose**: Coordinates specialized agents to formulate a unified, verified agricultural advisory.
- **APIs Used**:
  - `POST /api/advisory/run`: Initiates the end-to-end multi-agent graph execution.
- **How It Works**:
  1. **Planner Agent** parses inputs and constructs a directed dependency graph.
  2. Parallel execution invokes **GeoAgent**, **WeatherAgent**, **ImageAgent**, and **SoilAgent**.
  3. **AgriKnowledgeAgent** queries the RAG vector index of TNAU Agritech Portal and ICAR packages of practices.
  4. **Synthesizer** compiles the preliminary advisory.
  5. **Critic / Verifier Agent (Claude 3.5 Sonnet)** reviews the output for agronomic contradictions, excessive chemical dosages, or hallucinated facts before final sign-off.

### Module 6: AI-Powered Seasonal Crop Recommendation & Profit Prediction
- **Purpose**: Recommends the top 5 alternative crops ranked by agro-ecological suitability, cost of cultivation, market demand, and expected net profit per acre.
- **APIs Used**:
  - `GET /api/crop-recommendations?district={...}&taluk={...}&village={...}&survey_number={...}`
  - `GET /api/crop-recommendations/{survey_number}/profit-analysis`
  - `GET /api/crop-recommendations/{survey_number}/market-trends`
  - `GET /api/admin/crop-recommendations/analytics`
- **How It Works**:
  1. Evaluates parcel soil profile, current season (Kharif, Rabi, Zaid), water availability, and historical weather.
  2. Scores all candidate regional crops across 4 weighted dimensions:
     $$\text{Score} = (0.35 \times \text{Soil}) + (0.25 \times \text{Weather}) + (0.25 \times \text{Economics}) + (0.15 \times \text{TNAU Suitability})$$
  3. Calculates detailed financial forecasts:
     - Cultivation cost per acre (seeds, fertilizers, labor, irrigation).
     - Expected yield per acre (Quintals / MT).
     - Forecasted selling price via Agmarknet/e-NAM modal price trends.
     - Net Profit = $\text{Gross Revenue} - \text{Cultivation Cost}$.
  4. Returns Ranked Top 5 recommendations with plain-language explanations.

### Module 7: Admin Smart Alerts & Priority Crop Monitoring GIS
- **Purpose**: Provides administrative officers with real-time surveillance across 14,643 parcels, featuring multi-crop status icons, smart priority filtering, and verification workflows.
- **APIs Used**:
  - `GET /api/admin/crop-monitoring/filters`: Returns cascading dropdown options.
  - `GET /api/admin/crop-monitoring/overview`: Aggregates state-wide statistics and alert counts.
  - `GET /api/admin/crop-monitoring/markers`: Returns stratified geo-referenced markers with crop emojis and color codes.
  - `GET /api/admin/crop-monitoring/records`: Returns paginated tabular registry.
  - `GET /api/admin/crop-monitoring/records/{record_id}`: Fetches complete parcel dossier.
  - `PUT /api/admin/crop-monitoring/records/{record_id}`: Verifies or rejects crop records with audit logging.
  - `GET /api/admin/crop-monitoring/audit-log`: Retrieves tamper-evident officer audit trails.
- **How It Works**:
  1. Classifies each parcel into **HIGH**, **MEDIUM**, or **LOW** priority based on transparent criteria:
     - **HIGH**: Critical crop health ($< 50\%$), confirmed active disease/pest infestation.
     - **MEDIUM**: Moderate health ($50\text{--}79\%$), missing health telemetry, unverified cadastral boundary.
     - **LOW**: Verified healthy crops ($80\text{--}100\%$) without alerts.
  2. Renders dynamic Leaflet markers with crop emojis (`🌾`, `🥥`, `🍌`, `🌽`, `🎋`, etc.) and priority color rings.
  3. Implements **stratified sampling** to guarantee that rare and dominant crops alike remain visible simultaneously on the GIS map.
  4. Features a direct **"Map"** button in table rows that auto-focuses and pins specific parcels.

### Module 8: Agricultural-Only AI Chatbot & Voice Assistant
- **Purpose**: Voice-enabled conversational assistant restricted strictly to agricultural domains in English and Tamil.
- **APIs Used**:
  - `POST /api/chat`: Sends user query, language preference, and parcel context.
  - `POST /api/voice/transcribe`: Converts uploaded speech audio to text using Gemini Flash.
  - `POST /api/advisory/translate`: Translates advisories between English and Tamil.
- **How It Works**:
  1. **Intent Gatekeeper**: Before answering, an automated classifier determines if the question is agricultural. Unrelated questions (e.g., politics, coding, entertainment) are politely declined and redirected.
  2. **Context Enrichment**: Injects the active farmer's soil metrics, current parcel weather, and crop history into the prompt.
  3. **RAG Knowledge Retrieval**: Vector search extracts factual TNAU/ICAR agronomic recommendations.
  4. **Speech-to-Text & Text-to-Speech**: Integrates Web Speech API natively in the browser with Gemini Audio transcription fallback.

---

# SECTION 2: TAMIL DOCUMENTATION (தமிழ் ஆவணமாக்கம்)

## 1. திட்டத்தின் முக்கிய நோக்கம் மற்றும் கண்ணோட்டம்

**ஃபார்ம்வைஸ் AI (FarmWise AI)** என்பது விவசாயிகளுக்காகவும், வேளாண்மைத்துறை அதிகாரிகளுக்காகவும் உருவாக்கப்பட்ட அதிநவீன மல்டி-மாடல் (Multi-Model) முகவர் அடிப்படையிலான செயற்கை நுண்ணறிவு தளமாகும். இது தமிழ்நாட்டின் தென்காசி மற்றும் தூத்துக்குடி மாவட்டங்களின் உண்மையான நில அளவை பதிவேடுகள் (FMB Cadastral Maps), மண் வள அட்டை (Soil Health Card), நேரடி வானிலை தகவல், பயிர் புகைப்படங்கள், தமிழ்நாடு வேளாண்மைப் பல்கலைக்கழகம் (TNAU) மற்றும் ICAR வழிகாட்டுதல்கள் மற்றும் வேளாண் சந்தை விலைகளை (e-NAM / Agmarknet) ஒருங்கிணைத்து செயல்படுகிறது.

இத்தளம் இரு முக்கிய பயனர்களுக்காக வடிவமைக்கப்பட்டுள்ளது:
1. **விவசாயிகள்**: எளிய தமிழில் குரல் வழி (Voice Assistant) மற்றும் தொடுதிரை வாயிலாக பயிர் ஆலோசனை, நோய் கண்டறிதல், மற்றும் மாற்றுப் பயிர் பரிந்துரைகளைப் பெறலாம்.
2. **அரசு அதிகாரிகள்**: செயற்கைக்கோள் வரைபடம் (GIS Map), அவசர முன்னுரிமை எச்சரிக்கைகள் (Smart Alerts), நில சரிபார்ப்பு வசதிகள் மற்றும் அதிகாரப்பூர்வ அரசு அறிக்கைகளைப் பெறலாம்.

---

## 2. செயற்கை நுண்ணறிவு கட்டமைப்பு (Multi-Model Architecture)

இத்தளத்தில் 3 வெவ்வேறு AI மாடல்கள் அவற்றின் தனித்துவமான பயன்பாடுகளுக்காக பயன்படுத்தப்படுகின்றன:
1. **Ministral 8B / 3B Instruct (AWS Bedrock)**: திட்டமிடல் (Planning), தரவு பிரித்தெடுத்தல் மற்றும் விவசாயம் தொடர்பான கேள்விகளை வகைப்படுத்துதல்.
2. **Gemini 1.5 Flash (Google AI)**: பயிர் புகைப்படங்களை ஆய்வு செய்து நோய் கண்டறிதல் மற்றும் தமிழ் குரல் பதிவுகளை உரையாக மாற்றுதல்.
3. **Claude 3.5 Sonnet (Anthropic)**: முதன்மை சரிபார்ப்பாளர் (Verifier/Critic Agent) - பரிந்துரைகளில் உர அளவுகள் மற்றும் அறிவியல் உண்மைகள் சரியாக உள்ளதா என்பதை உறுதிசெய்து பிழைகளைத் தடுத்தல்.
4. **Amazon Titan Embeddings**: TNAU வேளாண் நூலகத்திலிருந்து துல்லியமான தகவல்களை மீட்டெடுக்கும் RAG கட்டமைப்பு.

---

## 3. முக்கிய தொகுதிகளின் விரிவான விவரங்கள்

### தொகுதி 1: நில அளவை வரைபடம் & சர்வே எண் அடையாளம் (Geospatial Cadastral GIS)
- **பயன்பாடு**: விவசாயியின் நில சர்வே எண் (Survey Number) மற்றும் உட்பிரிவை தமிழ்நாட்டின் உண்மையான நில வரைபடங்களுடன் (FMB) ஒப்பிட்டு துல்லியமாக காட்டுகிறது.
- **பயன்படுத்தப்பட்ட APIகள்**:
  - `GET /api/parcels/search`: சர்வே எண்களை தேட உதவுகிறது.
  - `GET /api/parcels/{survey_number}`: குறிப்பிட்ட சர்வே எண்ணின் பரப்பளவு, எல்லைகள் மற்றும் மண் வள விவரங்களை வழங்குகிறது.
  - `GET /api/admin/crop-monitoring/cadastral-boundaries`: வரைபடத்தில் நில எல்லைக் கோடுகளை வரைகிறது.
- **செயல்படும் விதம்**:
  1. விவசாயி தனது சர்வே எண்ணை உள்ளிடும்போது அல்லது பேசும்போது கணினி நில ஆவணங்களை சரிபார்க்கிறது.
  2. செயற்கைக்கோள் வரைபடத்தில் அவரது நிலத்தின் அமைவிடம் மற்றும் பரப்பளவு நேரடியாக காட்டப்படுகிறது.

### தொகுதி 2: மண் வள அட்டை & ஊட்டச்சத்து மேலாண்மை (Soil Health Card Analysis)
- **பயன்பாடு**: மண்ணின் கார அமிலத்தன்மை (pH), மின்கடத்துதிறன் (EC), கரிம கார்பன் (OC) மற்றும் தழை, மணி, சாம்பல் சத்துக்களை (NPK) ஆய்வு செய்கிறது.
- **பயன்படுத்தப்பட்ட APIகள்**: `/api/parcels/{survey_number}` மற்றும் `/api/advisory/run`.
- **செயல்படும் விதம்**:
  1. கார மண் ($pH > 7.8$) என்றால் ஜிப்சம் மற்றும் துத்தநாக சல்பேட் பரிந்துரைக்கப்படுகிறது.
  2. அமில மண் ($pH < 6.5$) என்றால் விவசாய சுண்ணாம்பு பரிந்துரைக்கப்படுகிறது.
  3. நடுநிலை மண் ($6.5 - 7.5$) என்றால் மண்புழு உரம் மற்றும் இயற்கை எரு பரிந்துரைக்கப்படுகிறது.
  4. யூரியாவை பிரித்து இடுவதற்கான வழிமுறைகளை வழங்குகிறது.

### தொகுதி 3: துல்லிய வானிலை முன்னறிவிப்பு (Weather Intelligence)
- **பயன்பாடு**: நில அமைவிடத்திற்கான 7 நாள் வானிலை முன்னறிவிப்பு மற்றும் மழை வாய்ப்பை தெரிவிக்கிறது.
- **பயன்படுத்தப்பட்ட APIகள்**:
  - `GET /api/weather/parcel/{survey_number}`
  - வெளி API: `Open-Meteo REST API` (இலவச, துல்லிய வானிலை சேவை).
- **செயல்படும் விதம்**:
  1. சர்வே எண்ணின் அட்சரேகை மற்றும் தீர்க்கரேகையைப் பெறுகிறது.
  2. வெப்பநிலை, காற்றின் வேகம், ஈரப்பதம் மற்றும் மழை வாய்ப்பை கணக்கிடுகிறது.
  3. பூச்சிக்கொல்லி தெளிப்பதற்கும் பாசனம் செய்வதற்கும் உகந்த நேரத்தை வழிகாட்டுகிறது.

### தொகுதி 4: பயிர் புகைப்பட நோய் கண்டறிதல் (Computer Vision Disease Diagnosis)
- **பயன்பாடு**: பயிரின் இலையையோ அல்லது செடியையோ புகைப்படம் எடுத்து பதிவேற்றினால், பயிரின் வகையையும் தாக்கியுள்ள நோயையும் உடனடியாக கண்டறிகிறது.
- **பயன்படுத்தப்பட்ட APIகள்**:
  - `POST /api/upload`: புகைப்படத்தை பதிவேற்றுகிறது.
  - `Gemini 1.5 Flash Vision API`: படங்களை ஆய்வு செய்கிறது.
- **செயல்படும் விதம்**:
  1. விவசாயி மொபைல் கேமரா மூலம் பயிர் படத்தை பதிவேற்றுகிறார்.
  2. AI மாதிரி இலைப்புள்ளி, கருகல் நோய், தண்டு துளைப்பான் போன்ற அறிகுறிகளை ஆய்வு செய்கிறது.
  3. பயிரின் ஆரோக்கிய சதவீதம் (0-100%) மற்றும் நோயைக் கட்டுப்படுத்தும் TNAU அங்கீகரித்த இயற்கை மற்றும் இரசாயன மருந்துகளை பரிந்துரைக்கிறது.

### தொகுதி 5: ஒருங்கிணைந்த முகவர் ஆலோசனை இயந்திரம் (LangGraph Multi-Agent Orchestrator)
- **பயன்பாடு**: மண், வானிலை, பயிர் ஆரோக்கியம் ஆகிய அனைத்தையும் ஒருங்கிணைத்து முழுமையான விரிவான வேளாண் ஆலோசனையை உருவாக்குகிறது.
- **பயன்படுத்தப்பட்ட APIகள்**:
  - `POST /api/advisory/run`
- **செயல்படும் விதம்**:
  1. திட்டமிடல் முகவர் (Planner) அனைத்து பணிகளையும் ஒழுங்கமைக்கிறது.
  2. மண், வானிலை, படம் மற்றும் அறிவு முகவர்கள் ஒரே நேரத்தில் தகவல்களை திரட்டுகின்றன.
  3. சரிபார்ப்பு முகவர் (Claude Verifier) எந்த ஒரு தவறான பரிந்துரையும் செல்லாமல் உறுதிசெய்து விவசாயிக்கு வழங்குகிறது.

### தொகுதி 6: பருவகால பயிர் பரிந்துரை & லாப கணிப்பு (Crop Recommendation & Profit Engine)
- **பயன்பாடு**: விவசாயியின் நிலத்திற்கு தற்போதைய பருவத்தில் அதிக மகசூல் மற்றும் அதிக லாபம் தரக்கூடிய சிறந்த 5 மாற்றுப் பயிர்களை பரிந்துரைக்கிறது.
- **பயன்படுத்தப்பட்ட APIகள்**:
  - `GET /api/crop-recommendations`: சிறந்த 5 பயிர்களை வரிசைப்படுத்துகிறது.
  - `GET /api/crop-recommendations/{survey_number}/profit-analysis`: ஒரு ஏக்கருக்கான செலவு மற்றும் லாபத்தை கணக்கிடுகிறது.
  - `GET /api/crop-recommendations/{survey_number}/market-trends`: சந்தை விலை போக்குகளை காட்டுகிறது.
  - `GET /api/admin/crop-recommendations/analytics`: வட்டார அளவிலான பயிர் புள்ளிவிவரங்களை வழங்குகிறது.
- **செயல்படும் விதம்**:
  1. மண்ணின் தன்மை, நீர் வசதி, தற்போதைய பருவம் (கார், குருவை, நவரை) மற்றும் சந்தை விலையை மதிப்பீடு செய்கிறது.
  2. ஒவ்வொரு பயிருக்கும்:
     - பரிந்துரைக்கப்பட்ட விதைப்பு காலம் மற்றும் அறுவடை காலம்.
     - ஏக்கருக்கான சாகுபடி செலவு (விதை, உரம், உழவு, ஆட்கள்).
     - எதிர்பார்க்கப்படும் விளைச்சல் மற்றும் சந்தை விற்பனை விலை.
     - எதிர்பார்க்கப்படும் நிகர லாபம் (Net Profit).
  3. வெறும் விலை உயர்வை மட்டும் பார்க்காமல், உற்பத்தி செலவையும் மண்ணின் பொருத்தத்தையும் கணக்கிட்டு பரிந்துரைக்கிறது.

### தொகுதி 7: அரசு அதிகாரிகள் கண்காணிப்பு வரைபடம் & ஸ்மார்ட் எச்சரிக்கைகள் (Admin Smart Alerts GIS)
- **பயன்பாடு**: 14,643 நில ஆவணங்களை மாவட்ட மற்றும் கிராம அளவில் அதிகாரிகள் கண்காணிக்கவும், கள ஆய்வு செய்து சரிபார்க்கவும் உதவுகிறது.
- **பயன்படுத்தப்பட்ட APIகள்**:
  - `GET /api/admin/crop-monitoring/filters`: வடிகட்டிகளை வழங்குகிறது.
  - `GET /api/admin/crop-monitoring/overview`: புள்ளிவிவரங்கள் மற்றும் எச்சரிக்கை எண்ணிக்கைகளை கணக்கிடுகிறது.
  - `GET /api/admin/crop-monitoring/markers`: பயிர் சின்னங்களுடன் கூடிய வரைபட புள்ளிகளை வழங்குகிறது.
  - `GET /api/admin/crop-monitoring/records`: பதிவேடு அட்டவணையை வழங்குகிறது.
  - `PUT /api/admin/crop-monitoring/records/{record_id}`: நிலத்தை அங்கீகரிக்க அல்லது நிராகரிக்க உதவுகிறது.
  - `GET /api/admin/crop-monitoring/audit-log`: அதிகாரிகளின் ஆய்வு பதிவேட்டை பாதுகாக்கிறது.
- **செயல்படும் விதம்**:
  1. நிலங்களை **உயர் முன்னுரிமை (HIGH)**, **நடுத்தர முன்னுரிமை (MEDIUM)**, மற்றும் **குறைந்த முன்னுரிமை (LOW)** என பிரிக்கிறது:
     - **HIGH**: பயிர் உடல்நிலை மோசம் ($< 50\%$) அல்லது தீவிர பூச்சி தாக்குதல் உள்ளவை.
     - **MEDIUM**: நடுத்தர நிலை ($50\text{--}79\%$) அல்லது ஆய்வு செய்யப்படாத நிலங்கள்.
     - **LOW**: ஆரோக்கியமான மற்றும் சரிபார்க்கப்பட்ட நிலங்கள்.
  2. வரைபடத்தில் பயிர் சின்னங்களுடன் (`🌾` நெல், `🥥` தென்னை, `🍌` வாழை, `🌽` மக்காச்சோளம், `🎋` கரும்பு) வண்ண வளையங்களுடன் காட்சியளிக்கிறது.
  3. அட்டவணையில் உள்ள **"Map"** பொத்தானை அழுத்தினால் குறிப்பிட்ட நிலத்தின் பயிர் சின்னம் வரைபடத்தில் உடனடியாக பெரிதாக்கப்பட்டு காட்டப்படுகிறது.

### தொகுதி 8: விவசாய AI உரையாடல் & குரல் உதவியாளர் (Agricultural Voice Chatbot)
- **பயன்பாடு**: விவசாய கேள்விகளுக்கு மட்டும் பிரத்யேகமாக பதிலளிக்கும் தமிழ்க் குரல் உதவியாளர்.
- **பயன்படுத்தப்பட்ட APIகள்**:
  - `POST /api/chat`: விவசாய உரையாடல்.
  - `POST /api/voice/transcribe`: குரல் பதிவை உரையாக மாற்றுதல்.
  - `POST /api/advisory/translate`: ஆங்கிலம் மற்றும் தமிழ் மொழிபெயர்ப்பு.
- **செயல்படும் விதம்**:
  1. **Domain Classifier**: விவசாயம் அல்லாத சினிமா, அரசியல், மென்பொருள் கேள்விகளை நாசூக்காக தவிர்த்து, விவசாய வினாக்களுக்கு மட்டுமே பதிலளிக்கிறது.
  2. விவசாயியின் நில மண் வளம் மற்றும் வானிலையை நினைவில் வைத்து தகுந்த ஆலோசனையை தமிழில் குரலாகவும் உரையாகவும் வழங்குகிறது.

---
*FarmWise AI Technical Documentation - Generated for FarmWise AI Agricultural Intelligence Platform.*
