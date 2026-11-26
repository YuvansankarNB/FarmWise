# FarmWise AI — Admin Geographic Crop Monitoring GIS Dashboard (Complete Export Bundle)

This package contains the **complete, unmodified Frontend, Backend, and API Integration codebase** for the **Admin Geographic Crop Monitoring GIS Dashboard**, preserving 100% of its features, Leaflet satellite & cadastral map, stratified multi-crop markers, Recharts analytics, AI seasonal crop recommendation insights, verification registry table, and UI/color/format/tone.

---

## 1. Included Codebase Structure

```text
admin-gis-dashboard/
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── config.py                               # Dataset paths & environment config
│       ├── main.py                                 # FastAPI app + all /api/admin/* endpoints
│       ├── db/database.py                          # In-memory / SQLite persistence adapter
│       ├── rag/knowledge_base.py                   # TNAU/ICAR RAG engine
│       ├── agents/                                 # LangGraph multi-agent modules
│       └── services/
│           ├── crop_monitoring_service.py          # 14,643-parcel GIS engine, stratified sampling, priority rules, audit logs
│           ├── crop_recommendation_service.py      # AI seasonal crop recommendation & profit analytics
│           ├── soil_service.py                     # Deterministic SHC soil profiles
│           ├── weather_service.py                  # Open-Meteo integration
│           ├── privacy_service.py                  # PII landowner masking
│           └── aws_service.py                      # S3 / AWS adapter
└── frontend/
    ├── package.json                                # React 19, Vite, Tailwind v4, Leaflet, React-Leaflet, Recharts, Lucide, Axios
    ├── vite.config.js                              # Proxy (/api -> http://127.0.0.1:8000)
    ├── index.html
    ├── public/                                     # Sample crop fallback images (/samples/*)
    └── src/
        ├── App.jsx                                 # Standalone entry rendering <Navbar /> + <AdminDashboard />
        ├── main.jsx
        ├── index.css                               # Tailwind + .custom-crop-marker Leaflet DivIcon CSS
        ├── services/api.js                         # Complete Axios client + resilient offline fallback
        ├── utils/translations.js                   # Bilingual (en / ta) UI labels
        └── components/
            ├── Navbar.jsx                          # FarmwiseAI top header bar
            ├── AdminDashboard.jsx                  # Main orchestrator (Filters, GIS Map, KPIs, Charts, Insights, Table, Modal)
            ├── AdminFilterToolbar.jsx              # 9 cascading geographic & agronomic filters + search
            ├── AdminCropMap.jsx                    # Leaflet Satellite/OSM map, Cadastral GeoJSON, Emoji markers, Popups
            ├── AdminStatsOverview.jsx              # 6 KPI cards + Recharts BarChart & Donut PieChart
            ├── AdminRecommendationInsights.jsx     # AI Seasonal Crop Recommendations & Profit Projections panel
            ├── AdminRecordTable.jsx                # Paginated table with Priority badges, Map locate button & View modal trigger
            ├── AdminRecordDetailModal.jsx          # Full parcel dossier, edit crop/area/health, Verify/Reject with audit log
            └── AdminAlertCards.jsx                 # Optional alert KPI cards component
```

---

## 2. Backend API Endpoints Exposed

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/admin/crop-monitoring/filters` | Cascading districts, taluks, villages, crops, seasons, stages, health, verification, disease, priority |
| `GET` | `/api/admin/crop-monitoring/overview` | Aggregated KPIs, alert counts, crop area chart, health distribution |
| `GET` | `/api/admin/crop-monitoring/markers` | Stratified geo-referenced markers (`lat`, `lng`, `crop_emoji`, `marker_color`, `priority`) |
| `GET` | `/api/admin/crop-monitoring/cadastral-boundaries` | GeoJSON cadastral parcel polygons for Leaflet overlay |
| `GET` | `/api/admin/crop-monitoring/records` | Paginated & priority-sorted parcel registry table with search & multi-filter |
| `GET` | `/api/admin/crop-monitoring/records/{record_id}` | Full parcel dossier + field photo + audit history |
| `PUT` | `/api/admin/crop-monitoring/records/{record_id}` | Verify / Reject / Update crop record with mandatory audit logging |
| `GET` | `/api/admin/crop-monitoring/audit-log` | Officer verification & edit audit trail |
| `GET` | `/api/admin/crop-recommendations/analytics` | State/district AI seasonal crop recommendation & profit trends |

---

## 3. How to Run Standalone

### Step 1: Dataset Folder
Copy the `Datasets/` folder from the root repository (`Ground_truth_Points.csv`, `Park_Cadastral_Map.geojson`, `Park_fmb_Map.geojson`, `images/`) next to `backend/` (so `BASE_DIR / "Datasets"` resolves in `backend/app/config.py`).

### Step 2: Start Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Step 3: Start Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev
```
Open `http://127.0.0.1:5173` — the Admin Geographic Crop Monitoring Dashboard will load immediately.

---

## 4. Integrating Into Another Website

1. Install frontend dependencies in your existing React project:
   ```bash
   npm install leaflet react-leaflet recharts lucide-react axios tailwindcss @tailwindcss/vite
   ```
2. Copy `frontend/src/components/Admin*.jsx`, `frontend/src/services/api.js`, and the `.custom-crop-marker` rules from `frontend/src/index.css`.
3. Render `<AdminDashboard onBackToFarmerView={() => navigate('/')} />` inside your route.
4. Set `VITE_API_BASE_URL=http://your-backend-host:8000` (or keep Vite's `/api` proxy).
