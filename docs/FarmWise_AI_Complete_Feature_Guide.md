# FarmWise AI — Comprehensive Engineering & Agronomy Guide
*(முழுமையான தொழில்நுட்ப மற்றும் வேளாண்மை வழிகாட்டி ஆவணம்)*

---

# PART 1: COMPLETE ENGLISH DOCUMENTATION

---

## 1. FarmWise AI Advisor (Core Orchestrator & Conversational Agent)

### Feature Overview
The **FarmWise AI Advisor** is the central coordinating engine of the platform. It functions as an agricultural expert system and conversational assistant that handles farmer inquiries via text, voice, or parcel selection. Rather than relying on a single AI model, it uses a multi-agent orchestrator that breaks down incoming requests, delegates tasks to specialized sub-agents, cross-verifies facts, and returns actionable advisories.

### Tech Stack Used & Why
* **FastAPI (Python 3.11)**: Async REST API server chosen for non-blocking I/O, rapid JSON serialization, and native OpenAPI/Pydantic validation.
* **LangGraph / Multi-Agent StateGraph**: Manages multi-agent execution loops using a strongly-typed shared state (`AgentState`). It allows agents to run sequentially or in parallel.
* **Multi-Model Routing Architecture**:
  * **Ministral 8B / 3B (Amazon Bedrock)**: Low-latency, cost-effective models used for query classification, intent extraction, and light translation.
  * **Gemini 1.5 Flash (Google Cloud / Vertex AI)**: High-speed multimodal model with a large context window for image diagnostics and audio transcription.
  * **Claude 3.5 Sonnet**: Operates as the "Verifier and Critic Agent" to conduct hallucination checks and safety audits on agricultural recommendations.
* **RAG System (Amazon Titan Text Embeddings V2 + FAISS/Chroma)**: Provides semantic search over official agronomic manuals (TNAU Crop Production Guide, ICAR manuals).
* **Frontend**: React + Vite + Tailwind CSS + Web Speech API for real-time Tamil and English voice synthesis.

### What the Feature Actually Did
1. Ingests user input (survey numbers, field photos, voice recordings, or conversational questions).
2. Maintains session memory (`chat_history`) to support conversational context.
3. Coordinates specialized sub-agents (Geo, Image, Weather, Soil, Knowledge, Verifier).
4. Records live telemetry for each step: model selected, input/output tokens, latency in milliseconds, tool outputs, and scientific citations.

### How It Works (Step-by-Step)
1. **Request Intake**: The user submits a query (e.g., *"When should I apply urea to my paddy field?"* or selects survey number `124/2A`).
2. **Intent Analysis & Planning**: `planner.py` breaks the request into execution steps.
3. **State Hydration**: Shared state is initialized with parcel information, recent weather data, and soil health metrics.
4. **Agent Graph Execution**:
   * If a field photo is present, the **Image Agent** classifies the crop variety and stage.
   * Concurrently, the **Weather Agent** and **Soil Agent** fetch microclimate forecasts and soil test data.
   * The **Knowledge Agent** retrieves agronomic recommendations from the RAG knowledge base.
5. **Safety & Hallucination Verification**: The **Verifier Agent** audits the advice (e.g., ensuring chemical concentrations do not exceed recommended safety limits).
6. **Streaming & Delivery**: The finalized advice is delivered to the frontend with interactive UI cards, decision traces, and voice synthesis support.

---

## 2. Cadastral Parcel & FMB Boundary

### Feature Overview
The **Cadastral Parcel & FMB Boundary** feature bridges physical land ownership records with interactive digital maps. It uses official Tamil Nadu Land Records and Field Measurement Book (FMB) survey data to identify, calculate, and display land boundaries.

### Tech Stack Used & Why
* **Turf.js & GeoJSON**: Geospatial analysis library for point-in-polygon queries, area computations, and centroid calculations directly in Node.js/Python without requiring an enterprise GIS server.
* **React Leaflet + OpenStreetMap & Esri Satellite Layers**: High-performance, mobile-responsive mapping with vector overlays and high-resolution satellite views.
* **Cadastral Repository (`datasets/parcels/`)**: GeoJSON repository containing coordinates, sub-division boundaries, and land-use records for surveyed villages.

### What the Feature Actually Did
1. Translates government survey numbers (e.g., `124/2A`, `156/1`) into geospatial boundary polygons.
2. Calculates parcel area in Hectares and Acres.
3. Determines the geographic centroid `[latitude, longitude]` to anchor micro-climate weather forecasts and satellite layers.
4. Masks personal identifiable information (PII) of landowners by default to ensure privacy compliance.

### How It Works (Step-by-Step)
1. The user inputs a village name and survey number.
2. `geo_agent.py` queries the cadastral dataset for matching survey records.
3. Turf.js computes the polygon area, perimeter, and centroid.
4. The frontend map auto-pans and zooms to the parcel coordinates, drawing the boundaries with distinct borders.
5. If the user uploads a geotagged photo, the system calculates the distance from the parcel centroid to confirm if the photo was taken inside the parcel boundary.

---

## 3. Ground-Truth Field Photo

### Feature Overview
The **Ground-Truth Field Photo** pipeline manages the capture, verification, and preprocessing of real field images taken by farmers or village extension workers.

### Tech Stack Used & Why
* **Python PIL / Pillow & ExifRead**: Extracts EXIF metadata (GPS latitude/longitude, date/time, camera hardware, orientation).
* **Private AWS S3 Storage (`ap-south-1` Mumbai)**: Secure object storage where images remain private without public URL exposure.
* **FastAPI `UploadFile` (Streaming Ingestion)**: Processes binary multipart payloads with client-side compression to accommodate low-bandwidth rural cellular networks.

### What the Feature Actually Did
1. Ingests smartphone photographs of standing crops, soil, and diseased foliage.
2. Extracts embedded GPS coordinates and timestamps from image metadata.
3. Validates whether the photo was taken within a reasonable distance of the claimed cadastral parcel boundary.
4. Normalizes, resizes, and stores the image safely for downstream computer vision models.

### How It Works (Step-by-Step)
1. The user captures or uploads a photo through `ImageUploadModal.jsx`.
2. The browser generates a local thumbnail and uploads the raw image to `/api/v1/upload-field-photo`.
3. The server extracts EXIF tags. If GPS data is present, it compares the coordinates against the parcel polygon.
4. The image is stored in an S3 bucket with a tracked hash key.
5. The storage path is saved in the active `AgentState` for computer vision analysis.

---

## 4. Crop Phenotype & Health

### Feature Overview
The **Crop Phenotype & Health** engine serves as an automated diagnostic tool. It visually inspects crop canopies and leaves to detect crop species, phenological growth stages, and visible symptoms of pest infestations or nutrient deficiencies.

### Tech Stack Used & Why
* **Gemini 1.5 Flash Multimodal Vision**: Chosen for its fast multimodal reasoning, low per-image cost, and ability to parse agricultural details accurately.
* **Amazon Bedrock Titan Multimodal Embeddings (Fallback)**: Vector-based visual matching fallback to compare inputs against verified disease libraries if APIs become unreachable.
* **Pydantic Schemas (`CropAnalysis`)**: Enforces strict structured JSON output to feed downstream decision logic.

### What the Feature Actually Did
1. Identifies the crop variety (e.g., Rice/Paddy, Banana, Coconut, Maize).
2. Determines the exact phenological growth stage (e.g., Nursery, Active Tillering, Panicle Initiation, Flowering, Maturity).
3. Identifies pests and fungal/bacterial diseases (e.g., Brown Plant Hopper, Bacterial Leaf Blight, Rice Blast).
4. Assigns an overall crop health score (0–100%) and a diagnostic confidence rating.

### How It Works (Step-by-Step)
1. `image_agent.py` retrieves the image from storage.
2. It constructs a domain-specific visual diagnostic prompt with standard agronomic taxonomies.
3. Gemini 1.5 Flash processes the visual features and returns structured JSON:
   ```json
   {
     "crop_name": "Rice (Paddy)",
     "growth_stage": "Active Tillering",
     "health_score": 82,
     "stress_type": "Nutrient Deficiency",
     "detected_issue": "Early Nitrogen Chlorosis (Yellowing of lower leaves)",
     "confidence": 0.94
   }
   ```
4. The structured output is passed to the **Agricultural Knowledge Agent** to determine appropriate fertilizer and pesticide requirements.

---

## 5. Micro-Climate & Agro-Met

### Feature Overview
The **Micro-Climate & Agro-Met** service provides parcel-level weather intelligence. It translates raw meteorological variables into operational farming advisories and risk warnings.

### Tech Stack Used & Why
* **Open-Meteo Weather API**: Provides open, non-commercial weather data without API key restrictions or rate-limit throttles.
* **Agro-Meteorological Rule Engine (`weather_service.py`)**: Translates weather data into specific field advisories (spray safety windows, rainfall warnings, disease-risk indices).

### What the Feature Actually Did
1. Fetches a 7-day hourly forecast and 14-day rainfall history based on the parcel's centroid coordinates.
2. Computes the **Rain Leaching Risk**: Detects whether upcoming heavy rainfall could wash away applied fertilizers.
3. Computes the **Foliar Spray Window**: Determines whether wind speed and rain probability are suitable for pesticide or nutrient spraying.
4. Evaluates the **Pathogen Risk Index**: Flags combinations of high relative humidity and warm temperatures that foster fungal diseases.

### How It Works (Step-by-Step)
1. `weather_agent.py` extracts the parcel centroid `[latitude, longitude]`.
2. It calls the Open-Meteo endpoint to collect temperature, precipitation probability, humidity, and wind velocity.
3. The rule engine evaluates agronomic conditions:
   * **Rule 1 (Rain Leaching Alert)**:
     $$\text{Forecast Rainfall}_{48\text{h}} > 15\text{ mm} \implies \text{Trigger "Rain Leaching Warning"}$$
   * **Rule 2 (Foliar Spray Safety)**:
     $$\text{Wind Speed} < 15\text{ km/h} \text{ and } \text{Precipitation Probability} < 30\% \implies \text{"Safe Spraying Window"}$$
   * **Rule 3 (Fungal Pathogen Risk)**:
     $$\text{Relative Humidity} > 85\% \text{ and } 24^\circ\text{C} \le \text{Temp} \le 28^\circ\text{C} \implies \text{"High Blast / Blight Risk"}$$
4. The alerts are added to the shared state to adjust fertilizer timing in Feature 7.

---

## 6. Soil Health & Chemical Profile *(In-Depth Technical Breakdown)*

### Feature Overview
The **Soil Health & Chemical Profile** engine calculates chemical, biological, and physical properties of the soil at the parcel level. It replicates the functionality of the **National Soil Health Card (SHC)** scheme, grounding chemical evaluations in Tamil Nadu Agricultural University (TNAU) Soil Survey standards.

### Tech Stack Used & Why
* **TNAU Soil Survey & Fertility Classification Guidelines**: Encodes empirical benchmarks for Tamil Nadu agro-climatic zones.
* **National Soil Health Card (SHC) Standard**: Standardizes macronutrients (N, P, K in kg/ha), Organic Carbon (%), Soil Reaction (pH), and Electrical Conductivity (EC in dS/m).
* **Deterministic Cryptographic Simulation (`soil_service.py`)**: Uses SHA-256 hashing on survey numbers so that test parcels always yield consistent, realistic, and unvarying soil data across reloads.
* **Frontend UI (`SoilHealthCard.jsx`)**: Displays interactive visual indicators, including dynamic pH gradient meters, NPK progress bars, and nutrient status badges.

### What the Feature Actually Did
1. Identifies the soil order and mechanical texture (e.g., *Red Loamy Soil - Sandy Clay Loam*, *Deep Black Cotton Soil*, *Clayey Alluvium*).
2. Calculates primary chemical parameters:
   * **Soil Reaction (pH)**: Classifies the soil as Acidic (<6.3), Optimal Neutral (6.5–7.5), Slightly Alkaline (7.5–8.0), or Alkaline/Calcareous (>8.0).
   * **Organic Carbon (OC %)**: Measures humus content and biological health.
   * **Primary Macronutrients (NPK)**: Available Nitrogen (N), Phosphorus ($P_2O_5$), and Potassium ($K_2O$) in kg/ha categorized into Low, Medium, or High.
   * **Electrical Conductivity (EC)**: Measures soluble salt concentrations (dS/m) to flag salinity risks.
3. Computes the **Fertilizer Uptake Efficiency Score**: An index estimating the percentage of applied synthetic fertilizer the crop can absorb before nutrients are locked by soil chemistry.
4. Generates scientific **Soil Amendments**: Recommends chemical and biological amendments (e.g., Gypsum, Lime, Green Manure) to remediate degraded soils.

### In-Depth Scientific & Algorithmic Mechanics

```
   ┌────────────────────────────────────────────────────────┐
   │                  Survey Number                         │
   └───────────────────────────┬────────────────────────────┘
                               ▼
               ┌───────────────────────────────┐
               │  Deterministic Soil Registry  │
               │   (SHA-256 Hash + TNAU Zones) │
               └───────────────┬───────────────┘
                               ▼
        ┌──────────────────────────────────────────────┐
        │       Chemical Soil Profile Generated        │
        │ • pH: 8.2 (Alkaline)                         │
        │ • OC: 0.42% (Low)                            │
        │ • N: 170 kg/ha | P: 12 kg/ha | K: 260 kg/ha  │
        └───────┬──────────────────────────────┬───────┘
                │                              │
                ▼                              ▼
  ┌───────────────────────────┐  ┌───────────────────────────┐
  │  Efficiency Score Engine  │  │  Soil Amendment Engine    │
  │  pH Penalty + OC Boost    │  │ • Gypsum 100 kg/acre      │
  │  -> 62% Uptake Efficiency │  │ • Zinc Sulphate 10kg/acre │
  └───────────────────────────┘  └───────────────────────────┘
```

#### 1. Fertilizer Uptake Efficiency Formula
Applied chemical fertilizer does not have 100% bioavailability. Nutrient fixation depends heavily on soil pH and organic carbon:
$$\text{pH Penalty} = |\text{pH} - 7.0| \times 12.0$$
$$\text{OC Boost} = (\text{Organic Carbon} - 0.5) \times 15.0$$
$$\text{Efficiency Score} = \text{Clamp}(85 - \text{pH Penalty} + \text{OC Boost}, 52\%, 92\%)$$

* **Scientific Basis**: In neutral soil (pH 6.8–7.2) with high organic carbon (>0.75%), fertilizer uptake reaches ~88%. When soil pH climbs above 8.0, phosphorus binds with calcium ions to form insoluble calcium phosphate, and urea hydrolyzes into free ammonia gas, causing efficiency to drop to **55%–62%**.

#### 2. Soil Amendment Decision Logic
* **Case 1: Alkaline / Calcareous Soils ($\text{pH} > 7.8$)**:
  * **Chemical Remedy**: Apply **Agricultural Gypsum ($CaSO_4 \cdot 2H_2O$) @ 100 kg/acre**. Calcium ions displace exchangeable sodium from soil colloids, improving soil structure and water infiltration.
  * **Biological Remedy**: Cultivate and incorporate green manure crops (Daincha / Sunnhemp @ 20 kg/acre) 45 days prior to planting. Decomposing organic matter releases organic acids that lower soil pH.
  * **Fertilizer Modification**: Standard urea suffers from ammonia volatilization in alkaline conditions. The system recommends **Neem-Coated Urea in split doses** and adds **Zinc Sulphate (ZnSO4 21%) @ 10 kg/acre** to prevent zinc deficiency chlorosis.
* **Case 2: Acidic Soils ($\text{pH} < 6.3$)**:
  * **Chemical Remedy**: Apply **Agricultural Lime (Dolomite / $CaCO_3 + MgCO_3$) @ 120 kg/acre** during preparatory tillage to eliminate aluminum and iron toxicity.
  * **Fertilizer Modification**: Avoid acid-forming fertilizers like Ammonium Sulphate. Apply **Rock Phosphate** as a basal phosphorus source, which dissolves effectively in acidic environments.
* **Case 3: Low Organic Carbon ($\text{OC} < 0.50\%$)**:
  * Apply **5 Metric Tonnes/acre of well-decomposed Farmyard Manure (FYM)** or 2 MT/acre vermicompost to restore microbiological activity and cation exchange capacity (CEC).

---

## 7. Personalised Agronomic Advisory *(In-Depth Technical Breakdown)*

### Feature Overview
The **Personalised Agronomic Advisory** engine is the primary recommendation output of FarmWise AI. It synthesizes crop growth stage, soil chemistry, and micro-climate forecasts into a verified, field-specific action plan.

### Tech Stack Used & Why
* **TNAU Crop Production Guide & Knowledge Corpus**: Contains verified agronomic standards for Tamil Nadu crops (Rice, Banana, Coconut, Maize, Pulses).
* **Multi-Agent Synthesis Engine (`knowledge_agent.py`)**: Merges data from the Image, Weather, and Soil agents into a unified, actionable schedule.
* **Claude 3.5 Sonnet Verifier (`verifier_agent.py`)**: Reviews advisory drafts to ensure dosage safety, detect chemical conflicts, and eliminate hallucinations.
* **Bilingual Speech Synthesis (`TTSButton.jsx` & `translations.js`)**: Converts advisory cards into natural spoken Tamil (`ta-IN`) and English (`en-IN`) for farmers.

### What the Feature Actually Did
1. Builds a stage-by-stage nutrient and fertilizer schedule (basal, vegetative, panicle/flowering, grain fill).
2. Dynamically adjusts chemical quantities based on the parcel's specific soil test results.
3. Automatically updates fertilizer timing based on rainfall forecasts.
4. Prescribes targeted pest, weed, and disease treatments with exact dilution ratios.
5. Surfaces live local market (APMC Mandi) commodity prices to help farmers plan harvest logistics.

### In-Depth Scientific & Algorithmic Mechanics

```
       ┌────────────────────────┐      ┌────────────────────────┐
       │ Crop Phenotype (Img)   │      │ Micro-Climate Forecast │
       │ "Paddy - Tillering"    │      │ "35mm Rain in 24 hrs"  │
       └───────────┬────────────┘      └───────────┬────────────┘
                   │                               │
                   └───────────────┬───────────────┘
                                   ▼
                 ┌───────────────────────────────────┐
                 │    Agricultural Knowledge Agent   │
                 │      (RAG + TNAU Corpus Query)    │
                 └─────────────────┬─────────────────┘
                                   │
       ┌───────────────────────────┴───────────────────────────┐
       │                                                       │
       ▼                                                       ▼
┌───────────────────────────────┐               ┌───────────────────────────────┐
│ Soil Profile Interlock        │               │ Weather Conflict Interlock    │
│ Soil has High Phosphorus (P)  │               │ Forecast predicts heavy rain  │
│ ➔ Reduce DAP dosage by 20%    │               │ ➔ Postpone Urea top-dressing  │
└──────────────┬────────────────┘               └──────────────┬────────────────┘
               │                                               │
               └───────────────────────┬───────────────────────┘
                                       ▼
                     ┌───────────────────────────────────┐
                     │    Claude 3.5 Sonnet Verifier     │
                     │  (Hallucination & Safety Review)  │
                     └─────────────────┬─────────────────┘
                                       ▼
                     ┌───────────────────────────────────┐
                     │   Final Actionable Advisory Card  │
                     │   • Tamil/English TTS             │
                     │   • Exact Dosage & Split Timing   │
                     │   • APMC Mandi Real-time Rate     │
                     └───────────────────────────────────┘
```

#### 1. Dynamic Dosage Compensation Algorithm
Standard agricultural manuals publish flat, blanket fertilizer recommendations per hectare (e.g., Rice: 120:38:38 kg N:P:K). FarmWise AI replaces flat tables with dynamic, soil-compensated dosage adjustments:

* **Phosphorus ($P_2O_5$) Compensation**:
  * If soil test reveals **High Available Phosphorus ($P > 22.0\text{ kg/ha}$)**: The system automatically **reduces chemical DAP (Di-Ammonium Phosphate) dosage by 20%**, cutting input costs and preventing phosphorus saturation.
  * If soil test reveals **Low Phosphorus ($P < 12.0\text{ kg/ha}$)**: Prescribes full basal application of Single Super Phosphate (SSP @ 100 kg/acre) band-placed at 5 cm depth.
* **Soil Reclamation Stage Insertion**:
  * If soil pH is abnormal (<6.3 or >7.8), the agent injects a preliminary stage into the schedule: *"Stage 0: Soil Reclamation"*, requiring Lime or Gypsum application 15 days before planting.
* **Bio-Fertilizer Integration**:
  * Adds an inoculation schedule: *Azospirillum* (Nitrogen-fixing) + *Phosphobacteria* (Phosphate-solubilizing) @ 2 kg/acre mixed with 50 kg FYM. This safely cuts synthetic chemical Nitrogen needs by 25%.

#### 2. Weather-Conflict Verification Interlock
Before displaying the advisory, the agent cross-checks the fertilizer schedule against the 48-hour rainfall forecast:
* **Rule**:
  $$\text{If } \text{Forecast Rainfall}_{48\text{h}} > 15\text{ mm} \text{ and } \text{Schedule contains Top-Dress Nitrogen (Urea)}$$
  $$\implies \text{Update Timing: "Post-rain window (Delay application by 24-48 hours until standing water drains)"}$$
  $$\implies \text{Append Note: "Forecasted rain will cause nitrogen leaching and surface runoff."}$$

#### 3. Bilingual Voice Delivery
Smallholder farmers can read the advisory or click the speaker button to hear it read aloud in Tamil (`ta-IN`) with accurate pronunciation of agricultural terminology (e.g., *வேப்பம்பூசப்பட்ட யூரியா* for Neem-Coated Urea, *டி.ஏ.பி* for DAP).

---

## 8. Additional Platform Features

| Feature | Tech Stack | What It Does & How It Works |
| :--- | :--- | :--- |
| **Bilingual Voice Assistant (Tamil & English)** | Web Speech API + Gemini Audio Fallback | Farmers tap a microphone button and speak in Tamil (*"என் நிலத்துக்கு என்ன உரம் போடணும்?"*). The system transcribes the audio, runs the query through the agent pipeline, and reads the answer aloud. |
| **Government-Format Printable Report** | React Print CSS / `@media print` | Compiles parcel maps, landowner details, soil cards, and advisories into an official Tamil Nadu Agriculture Department / Kisan Credit Card format for bank loans or crop insurance claims. |
| **Real-Time APMC Mandi Market Prices** | Agmarknet / e-NAM RAG Engine | Retrieves real-time prices (Minimum, Maximum, Modal in ₹/Quintal) from nearby local markets (e.g., Tenkasi, Tirunelveli, Madurai) so farmers can plan their harvest sales. |
| **Hallucination Verifier & Decision Trace** | Claude 3.5 Sonnet / Bedrock Verifier | Displays a step-by-step trace of every tool call, latency, token count, model selected, and scientific citation behind every recommendation. |
| **Farmer Data Privacy Masking** | PII Masking Engine (`privacy_service.py`) | Automatically masks landowner names and sensitive survey records (e.g., `Murugan S.` $\rightarrow$ `M****** S.`) in public views, displaying full records only in authorized officer views. |

---
---

# PART 2: TAMIL TRANSLATION & EXPLANATION
*(பகுதி 2: விரிவான தமிழ் விளக்கக் கையேடு)*

---

## 1. FarmWise AI Advisor (முதன்மை ஒருங்கிணைப்பாளர் & உரையாடல் உதவியாளர்)

### இந்த அம்சம் என்ன செய்கிறது?
FarmWise AI Advisor என்பது இந்த தளத்தின் "மைய மூளை" (Central Brain) ஆகும். ஒரு விவசாயி தனது சர்வே எண், நிலத்தின் புகைப்படம் அல்லது குரல் மூலம் கேள்வி கேட்கும்போது, இந்த ஆலோசகர் பல்வேறு துணை ஏஜென்ட்டுகளை (Sub-Agents) இயக்கி, துல்லியமான மற்றும் பாதுகாப்பான வேளாண் ஆலோசனைகளை வழங்குகிறது.

### பயன்படுத்தப்பட்ட தொழில்நுட்பங்கள் & காரணங்கள்:
* **FastAPI (Python 3.11)**: அதிவேகமான மற்றும் தடையற்ற API பரிமாற்றத்திற்கு பயன்படுகிறது.
* **LangGraph / Multi-Agent StateGraph**: பல AI ஏஜென்ட்டுகள் ஒன்றுக்கொன்று தகவல்களைப் பகிர்ந்து செயல்பட உதவுகிறது.
* **Multi-Model Routing Architecture**:
  * **Ministral 8B / 3B (Amazon Bedrock)**: குறைந்த செலவில் விரைவான திட்டமிடல் மற்றும் மொழிபெயர்ப்பு பணிகளுக்கு.
  * **Gemini 1.5 Flash (Google Cloud)**: புகைப்படங்களை ஆராயவும் மற்றும் தமிழ் குரல் பதிவுகளை உரையாக மாற்றவும்.
  * **Claude 3.5 Sonnet**: வழங்கப்பட்ட ஆலோசனைகளில் தவறுகள் உள்ளதா என சரிபார்க்கும் தணிக்கையாளராக (Verifier/Critic).
* **Vector RAG (Titan Text Embeddings + FAISS)**: தமிழ்நாடு வேளாண்மைப் பல்கலைக்கழகம் (TNAU) மற்றும் ICAR வழிகாட்டி கையேடுகளில் இருந்து அறிவியல் பூர்வமான தகவல்களைத் தேடி எடுக்கிறது.

### இது எவ்வாறு செயல்படுகிறது?
1. விவசாயி சர்வே எண்ணை உள்ளிடுகிறார் அல்லது கேள்வி கேட்கிறார்.
2. `Planner` எந்தெந்த ஏஜென்ட்டுகள் செயல்பட வேண்டும் என்பதைத் திட்டமிடுகிறது.
3. பயிர் புகைப்படம், மண் வளம் மற்றும் வானிலை தகவல்கள் திரட்டப்படுகின்றன.
4. `Knowledge Agent` பல்கலைக்கழக வழிகாட்டுதல்களின்படி உரம் மற்றும் பூச்சி மேலாண்மை அட்டவணையை உருவாக்குகிறது.
5. `Verifier Agent` இந்த பரிந்துரைகளில் ஏதேனும் ஆபத்தான தவறுகள் உள்ளதா என சரிபார்த்து உறுதி செய்கிறது.
6. முடிவுகள் எளிய திரையிலும், தமிழ் குரல் வாசிப்பாகவும் (Voice Readout) விவசாயிக்கு வழங்கப்படுகின்றன.

---

## 2. Cadastral Parcel & FMB Boundary (நில அளவை மற்றும் FMB எல்லை வரைபடம்)

### இந்த அம்சம் என்ன செய்கிறது?
விவசாயியின் பட்டா மற்றும் சிட்டா சர்வே எண்களைக் கொண்டு (எ.கா: `124/2A`), அவர்களின் நிலத்தின் துல்லியமான எல்லைகளை வரைபடத்தில் காட்டுகிறது. நிலத்தின் மொத்த பரப்பளவு (ஹெக்டேர் மற்றும் ஏக்கர்) கணக்கிடப்படுகிறது.

### பயன்படுத்தப்பட்ட தொழில்நுட்பங்கள் & காரணங்கள்:
* **Turf.js & GeoJSON**: நிலத்தின் பரப்பளவு, சுற்றளவு மற்றும் மையப்புள்ளியை விரைவாகக் கணக்கிடும் வரைபட கணிதக் கருவி.
* **React Leaflet + OSM & Esri Satellite Layers**: குறைந்த இணைய வேகத்திலும் மொபைலில் தெளிவாக இயங்கும் செயற்கைக்கோள் வரைபடம்.
* **Tamil Nadu Land Records Dataset**: தமிழ்நாடு அரசின் FMB (புல வரைபடம்) எல்லைத் தரவுகள்.

### இது எவ்வாறு செயல்படுகிறது?
1. விவசாயி சர்வே எண்ணைத் தேர்ந்தெடுத்ததும், வரைபடத் தரவுத்தளத்தில் இருந்து எல்லைக் கோடுகள் எடுக்கப்படுகின்றன.
2. Turf.js நிலத்தின் பரப்பளவு மற்றும் மையப்புள்ளியைத் தீர்மானிக்கிறது.
3. செயற்கைக்கோள் வரைபடம் அந்த இடத்திற்கு நகர்ந்து நிலத்தின் எல்லையைக் கோடிட்டுக் காட்டுகிறது.
4. விவசாயியின் தனிப்பட்ட தகவல்கள் பாதுகாக்கப்பட்டு, பெயர் மறைக்கப்பட்டு காட்டப்படும் (எ.கா: `M****** S.`).

---

## 3. Ground-Truth Field Photo (நேரடி களப் புகைப்படம்)

### இந்த அம்சம் என்ன செய்கிறது?
விவசாயிகள் தங்கள் வயலில் எடுக்கும் பயிர் அல்லது இலைகளின் புகைப்படங்களைச் சேகரித்து சரிபார்க்கிறது. புகைப்படத்தில் உள்ள GPS தகவலைக் கொண்டு, படம் உண்மையில் அந்த சர்வே எண் நிலத்தில்தான் எடுக்கப்பட்டதா என்பதை உறுதி செய்கிறது.

### பயன்படுத்தப்பட்ட தொழில்நுட்பங்கள் & காரணங்கள்:
* **Python PIL / Pillow & ExifRead**: புகைப்படத்தின் தரம், நேரம் மற்றும் GPS இருப்பிடத்தை ஆராய்கிறது.
* **Private AWS S3 (Mumbai ap-south-1)**: புகைப்படங்கள் பொது இணையத்தில் கசியாமல் பாதுகாப்பாகச் சேமிக்கப்படுகின்றன.
* **FastAPI Streaming Upload**: கிராமப்புறங்களில் இணைய வேகம் குறைவாக இருந்தாலும் புகைப்படங்களை எளிதாகப் பதிவேற்றுகிறது.

### இது எவ்வாறு செயல்படுகிறது?
1. விவசாயி வயலில் பயிரைப் படம் எடுத்துப் பதிவேற்றுகிறார்.
2. அமைப்பானது படத்தின் EXIF தகவலில் இருந்து GPS அட்சரேகை/தீர்க்கரேகையைப் பிரித்தெடுக்கிறது.
3. புகைப்படம் நில எல்லைக்குள் எடுக்கப்பட்டதா என சரிபார்க்கப்படுகிறது.
4. படம் பாதுகாப்பாக S3-ல் சேமிக்கப்பட்டு, பயிர் நோய் கண்டறியும் AI-க்கு அனுப்பப்படுகிறது.

---

## 4. Crop Phenotype & Health (பயிர் வகை & ஆரோக்கியக் கண்காணிப்பு)

### இந்த அம்சம் என்ன செய்கிறது?
வயல் புகைப்படத்தைப் பார்த்து:
1. என்ன பயிர் சாகுபடி செய்யப்பட்டுள்ளது (நெல், வாழை, சோளம், தென்னை)?
2. பயிர் எந்த வளர்ச்சிப் பருவத்தில் உள்ளது (நாற்றுப் பருவம், தூர் கட்டும் பருவம், கதிர் உருவாகும் பருவம், முதிர்ச்சிப் பருவம்)?
3. பூச்சி அல்லது பூஞ்சாண நோய்களின் தாக்குதல் உள்ளதா (எ.கா: புகையான் பூச்சி, பாக்டீரியா இலைக்கருகல், இலைப்புள்ளி நோய்)?
4. பயிரின் ஆரோக்கிய மதிப்பீடு (Health Score: 0-100%) ஆகியவற்றைத் துல்லியமாகக் கண்டறிகிறது.

### பயன்படுத்தப்பட்ட தொழில்நுட்பங்கள் & காரணங்கள்:
* **Gemini 1.5 Flash Multimodal Vision**: புகைப்படத்தில் உள்ள பயிர் அறிகுறிகளைத் துல்லியமாகவும் குறைந்த செலவிலும் கண்டறியும் திறன் கொண்டது.
* **Bedrock Titan Multimodal Embeddings (மாற்று வழி)**: இணையத் தடங்கல் ஏற்பட்டால் நோய் மாதிரிகளை ஒப்பிட்டுப் பார்க்க உதவும் உள்ளூர் மாதிரித் தொகுப்பு.
* **Pydantic Schemas**: தகவல்கள் குழப்பமின்றி முறையான தரவுகளாக (JSON) மாற்றப்படுவதை உறுதி செய்கிறது.

### இது எவ்வாறு செயல்படுகிறது?
1. புகைப்படம் AI பார்வை மாதிரிக்கு அனுப்பப்படுகிறது.
2. தாவரவியல் விதிகளின்படி பயிரின் இலை நிறம், தூர்களின் எண்ணிக்கை மற்றும் நோய்க்குறிகள் ஆராயப்படுகின்றன.
3. பயிர் பெயர், வளர்ச்சி நிலை மற்றும் பாதிப்புகள் கண்டறியப்பட்டு அடுத்தடுத்த முடிவுகளுக்காக அனுப்பப்படுகின்றன.

---

## 5. Micro-Climate & Agro-Met (நுண் வானிலை & வேளாண் எச்சரிக்கைகள்)

### இந்த அம்சம் என்ன செய்கிறது?
விவசாயியின் நிலத்திற்குரிய நேரடி 7-நாள் வானிலை முன்னறிவிப்பைப் பெறுகிறது. மழைப்பொழிவு, ஈரப்பதம், காற்றின் வேகம் ஆகியவற்றை அடிப்படையாகக் கொண்டு விவசாயிகளுக்கு முன்கூட்டியே எச்சரிக்கைகளை வழங்குகிறது.

### பயன்படுத்தப்பட்ட தொழில்நுட்பங்கள் & காரணங்கள்:
* **Open-Meteo Weather API**: கட்டணமில்லாத மற்றும் தடையற்ற வானிலை முன்னறிவிப்பு சேவை.
* **Agro-Meteorological Rule Engine (`weather_service.py`)**: வானிலை எண்களை நடைமுறை விவசாய எச்சரிக்கைகளாக மாற்றும் விதிகளின் தொகுப்பு.

### இது எவ்வாறு செயல்படுகிறது?
1. நிலத்தின் மையப்புள்ளிக்கான வானிலை பெறப்படுகிறது.
2. **மழை உரம் இழப்பு எச்சரிக்கை**: அடுத்த 48 மணி நேரத்தில் 15 மி.மீ-க்கு மேல் மழை பெய்யும் வாய்ப்பிருந்தால், யூரியா போன்ற மேலுரமிடுவதைத் தள்ளிப்போட எச்சரிக்கிறது.
3. **பூஞ்சாண நோய் எச்சரிக்கை**: காற்றின் ஈரப்பதம் 85%-க்கு அதிகமாகவும், வெப்பநிலை 24–28°C ஆகவும் இருந்தால், குலைநோய் (Blast) தாக்குதல் வர வாய்ப்புள்ளதாக எச்சரிக்கிறது.
4. **மருந்து தெளிக்கும் நேரம்**: காற்றின் வேகம் குறைவாகவும், மழை இல்லாத நேரமாகவும் இருப்பதை உறுதி செய்கிறது.

---

## 6. Soil Health & Chemical Profile (மண்வளம் மற்றும் ஊட்டச்சத்து பகுப்பாய்வு — ஆழமான தொழில்நுட்ப விளக்கம்)

### இந்த அம்சம் என்ன செய்கிறது?
விவசாயியின் நிலத்திற்கான விரிவான **மண்வள அட்டை (Soil Health Card)** அறிக்கையை உருவாக்குகிறது. மண்ணின் வகை, கார-அமிலத்தன்மை (pH), கரிமக் கரிமம் (Organic Carbon), முதன்மை சத்துக்களான தழைச்சத்து (N), மணிச்சத்து (P), சாம்பல்சத்து (K) மற்றும் உவர்-அமில நிலையை ஆராய்கிறது.

### பயன்படுத்தப்பட்ட தொழில்நுட்பங்கள் & காரணங்கள்:
* **TNAU மண் ஆய்வு நெறிமுறைகள்**: தமிழ்நாட்டின் வேளாண் மண்டலங்களுக்கான (காவிரி டெல்டா, மேற்கு மண்டலம், தென் மண்டலம்) அதிகாரப்பூர்வ மண் வள அளவுகோல்கள்.
* **தேசிய மண்வள அட்டைத் திட்டம் (SHC)**: ஊட்டச்சத்துக்களின் அளவை முறைப்படுத்துகிறது (கிலோ/ஹெக்டேர்).
* **Deterministic Cryptographic Simulation (`soil_service.py`)**: மாதிரி சர்வே எண்களை SHA-256 முறையில் குறியாக்கம் செய்வதன் மூலம், பக்கத்தைப் புதுப்பித்தாலும் (Refresh) அதே நம்பகமான மண் பண்புகள் மாறாமல் காட்டப்படுகின்றன.
* **UI (`SoilHealthCard.jsx`)**: pH அளவீட்டு மானி, ஊட்டச்சத்து நிலைப் பட்டைகள் மற்றும் உர பயன்பாட்டுத் திறன் காட்டி.

### ஆழமான அறிவியல் மற்றும் செயல்பாட்டுக் கோட்பாடுகள்:

#### 1. உர பயன்பாட்டுத் திறன் கணக்கீடு (Fertilizer Uptake Efficiency Formula)
மண்ணில் இடப்படும் ரசாயன உரங்கள் அனைத்தையும் பயிர்களால் உடனடியாக உறிஞ்சிவிட முடியாது. மண்ணின் pH மற்றும் கரிமக் கரிமத்தைப் பொறுத்தே சத்துக்கள் கிடைக்கின்றன:
$$\text{pH Penalty} = |\text{pH} - 7.0| \times 12.0$$
$$\text{OC Boost} = (\text{Organic Carbon} - 0.5) \times 15.0$$
$$\text{Efficiency Score} = \text{Clamp}(85 - \text{pH Penalty} + \text{OC Boost}, 52\%, 92\%)$$

* **விளக்கம்**: நடுநிலையான மண்ணில் (pH 6.8–7.2) உர பயன்பாட்டுத் திறன் **88%** வரை இருக்கும். ஆனால் மண் காரத்தன்மையுடன் (pH 8.2) இருக்கும்போது, மணிச்சத்து சுண்ணாம்புடன் பிணைக்கப்பட்டு பயிர்களுக்குக் கிடைக்காமல் போகிறது; மேலும் யூரியா வாயுவாக வீணாகிறது. இதனால் பயன்பாட்டுத் திறன் **62%** ஆகக் குறைகிறது.

#### 2. மண் சீர்திருத்தப் பரிந்துரைகள் (Soil Amendments):
* **மண் காரத்தன்மை அதிகமாக இருந்தால் (pH > 7.8)**:
  * **ஜிப்சம் இடுதல்**: ஏக்கருக்கு **100 கிலோ வேளாண் ஜிப்சம் ($CaSO_4 \cdot 2H_2O$)** இடப் பரிந்துரைக்கப்படுகிறது. இது மண்ணில் உள்ள சோடியத்தை நீக்கி நீர்ப்பிடிப்புத் திறனை உயர்த்துகிறது.
  * **பசுந்தாள் உரம்**: தக்கைப்பூண்டு (Daincha) அல்லது சணப்பை ஏக்கருக்கு 20 கிலோ விதைத்து 45-வது நாளில் மடக்கி உழ வேண்டும்.
  * **உர மாற்றம்**: சாதாரண யூரியாவைத் தவிர்த்து **வேப்பம்பூசப்பட்ட யூரியாவைப்** பிரித்து இட வேண்டும். துத்தநாகக் குறைபாட்டைத் தடுக்க **துத்தநாக சல்பேட் (Zinc Sulphate 21%) ஏக்கருக்கு 10 கிலோ** அடிஉரமாக இட வேண்டும்.
* **மண் அமிலத்தன்மை அதிகமாக இருந்தால் (pH < 6.3)**:
  * ஏக்கருக்கு **120 கிலோ வேளாண் சுண்ணாம்பு (டாலமைட்)** இட வேண்டும்.
  * ராக் பாஸ்பேட் (Rock Phosphate) உரத்தைப் பயன்படுத்த வேண்டும்.
* **கரிமக் கரிமம் குறைவாக இருந்தால் (OC < 0.50%)**:
  * ஏக்கருக்கு **5 டன் மக்கிய தொழுவுரம் (FYM)** அல்லது 2 டன் மண்புழு உரம் இடுவது கட்டாயமாக்கப்படுகிறது.

---

## 7. Personalised Agronomic Advisory (தனிப்பயனாக்கப்பட்ட வேளாண் ஆலோசனை — ஆழமான தொழில்நுட்ப விளக்கம்)

### இந்த அம்சம் என்ன செய்கிறது?
விவசாயியின் பயிர் நிலை, மண் பரிசோதனை முடிவுகள் மற்றும் வானிலை முன்னறிவிப்பு ஆகிய மூன்றையும் ஒருங்கிணைத்து, அந்த நிலத்திற்கேற்ற பிரத்யேக வேளாண் செயல் திட்டத்தை உருவாக்குகிறது.

### பயன்படுத்தப்பட்ட தொழில்நுட்பங்கள் & காரணங்கள்:
* **TNAU பயிர் சாகுபடி வழிகாட்டித் தரவு**: நெல், வாழை, சோளம், தென்னை, பயறு வகைகளுக்கான சாகுபடி கையேடு.
* **LangGraph Multi-Agent Synthesis (`knowledge_agent.py`)**: அனைத்து துணை ஏஜென்ட்டுகளின் தரவுகளையும் ஒருங்கிணைக்கும் அறிவு இயந்திரம்.
* **Claude 3.5 Sonnet Verifier (`verifier_agent.py`)**: பரிந்துரைக்கப்பட்ட மருந்துகளின் அளவுகள் பாதுகாப்பானதா என்பதை தணிக்கை செய்து உறுதி செய்கிறது.
* **தமிழ் குரல் வாசிப்பு வசதி (`TTSButton.jsx`)**: விவசாயிகள் வாசிக்க சிரமப்பட்டால், ஆலோசனைகளைத் தூய தமிழில் குரல் வடிவில் வாசித்துக் காட்டுகிறது.

### ஆழமான அறிவியல் மற்றும் செயல்பாட்டுக் கோட்பாடுகள்:

#### 1. மண் நிலைக்கு ஏற்ப உர அளவை மாற்றியமைக்கும் முறை (Dynamic Dosage Adjustment)
பொதுவான வேளாண் அட்டவணைகள் அனைவருக்கும் ஒரே அளவிலான உரத்தையே பரிந்துரைக்கும் (எ.கா: நெல்லுக்கு ஏக்கருக்கு 120:38:38 கிலோ NPK). ஆனால் FarmWise AI மண்ணின் தரத்திற்கேற்ப உர அளவை மாற்றியமைக்கிறது:
* **மணிச்சத்து (Phosphorus) குறைப்பு**:
  * மண்ணில் மணிச்சத்து அதிகமாக இருந்தால் (>22.0 கிலோ/ஹெக்டேர்), இரசாயன **DAP உரத்தின் அளவை 20% குறைத்து** செலவை மிச்சப்படுத்துகிறது.
  * மணிச்சத்து குறைவாக இருந்தால், முழு அளவிலான சிங்கிள் சூப்பர் பாஸ்பேட் (SSP 100 கிலோ) இடப் பரிந்துரைக்கிறது.
* **மண் சீர்திருத்தப் பருவம் சேர்த்தல்**:
  * மண்ணின் pH இயல்பை விட அதிகமாகவோ குறைவாகவோ இருந்தால், அட்டவணையில் *"பருவம் 0: மண் சீர்திருத்தம்"* சேர்க்கப்பட்டு, நடுவுக்கு 15 நாட்களுக்கு முன்பே ஜிப்சம் அல்லது சுண்ணாம்பு இட அறிவுறுத்துகிறது.
* **உயிர் உரங்கள் சேர்த்தல்**:
  * *அசோஸ்பைரில்லம்* மற்றும் *பாஸ்போபாக்டீரியா* தலா 2 கிலோவை 50 கிலோ தொழுவுரத்துடன் கலந்து இடப் பரிந்துரைப்பதன் மூலம், இரசாயன தழைச்சத்துத் தேவையை 25% குறைக்கிறது.

#### 2. வானிலை முரண்பாடு சரிபார்ப்பு (Weather-Conflict Verification Interlock)
உர அட்டவணையை வெளியிடுவதற்கு முன், அடுத்த 48 மணி நேர மழை முன்னறிவிப்புடன் அது ஒப்பிடப்படுகிறது:
* **விதி**:
  * அடுத்த 48 மணி நேரத்தில் 15 மி.மீ-க்கு மேல் மழை பெய்யும் வாய்ப்பிருந்து, அதே நேரத்தில் யூரியா மேலுரமிட வேண்டிய நிலை இருந்தால்:
  * உரமிடும் காலம் உடனடியாக **"மழைக்குப் பின் இடவும் (மழை நீர் வடிந்த பிறகு 24–48 மணி நேரம் கழித்து இடவும்)"** என மாற்றப்படும்.
  * *"மழையினால் உரங்கள் அடித்துச் செல்லப்பட்டு வீணாவதைத் தடுக்கவே இந்த மாற்றம்"* என்ற குறிப்பும் இணைக்கப்படும்.

#### 3. தமிழ் குரல் வடிவமைப்பு (Bilingual Voice Delivery)
விவசாயிகள் திரையில் உள்ள ஸ்பீக்கர் பொத்தானை அழுத்தினால், முழு ஆலோசனைகளும் தெளிவான தமிழில் ஒலிக்கின்றன. வேளாண் கலைச்சொற்கள் துல்லியமாக உச்சரிக்கப்படுகின்றன (எ.கா: வேப்பம்பூசப்பட்ட யூரியா, டி.ஏ.பி).

---

## 8. அமைப்பில் உள்ள பிற முக்கிய அம்சங்கள்

| கூடுதல் அம்சம் | பயன்படுத்தப்பட்ட தொழில்நுட்பம் | என்ன செய்கிறது & எவ்வாறு இயங்குகிறது? |
| :--- | :--- | :--- |
| **இருமொழி குரல் உதவியாளர் (தமிழ் & ஆங்கிலம்)** | Web Speech API + Gemini Audio | விவசாயிகள் மைக்ரோஃபோன் பொத்தானை அழுத்தி தமிழில் பேசலாம் (*"என் நிலத்திற்கு எப்போது உரம் போட வேண்டும்?"*). AI அதனைப் புரிந்துகொண்டு தமிழிலேயே பதிலளிக்கிறது. |
| **அரசு மாதிரி அச்சு அறிக்கை (Printable Report)** | React Print CSS / `@media print` | நில வரைபடம், பயிர் நிலை, மண் அட்டை மற்றும் ஆலோசனைகளை அரசு அதிகாரிகள், பயிர் காப்பீடு மற்றும் வங்கி கடன் பெறுவதற்கு ஏற்ற ஆவணமாக அச்சிட்டுத் தருகிறது. |
| **நேரடி ஒழுங்குமுறை விற்பனைக் கூட (APMC Mandi) விலை நிலவரம்** | e-NAM / Agmarknet RAG Engine | அருகிலுள்ள சந்தைகளில் (தென்காசி, திருநெல்வேலி, மதுரை) தற்போதைய விளைபொருட்களின் விற்பனை விலையைக் (குறைந்தபட்ச, அதிகபட்ச விலை ₹/குவிண்டால்) காட்டுகிறது. |
| **தவறுகளைத் தணிக்கை செய்யும் முறை (Decision Trace)** | Claude 3.5 Sonnet / Bedrock Verifier | AI ஒவ்வொரு முடிவையும் எவ்வாறு எடுத்தது, எந்தப் பல்கலைக்கழகப் புத்தகத்திலிருந்து மேற்கோள் காட்டியது என்பதை வெளிப்படையாகத் திரையில் காட்டுகிறது. |
| **விவசாயி தரவுப் பாதுகாப்பு (PII Masking)** | Privacy Engine (`privacy_service.py`) | பட்டாதாரரின் தனிப்பட்ட விவரங்களை மறைத்து (எ.கா: `M****** S.`) பொதுப்பார்வைக்கு பாதுகாப்பாக வைக்கிறது; அதிகாரிகள் உள்நுழையும் போது மட்டுமே முழு விவரமும் தெரியும். |
