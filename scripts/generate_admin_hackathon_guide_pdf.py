import os
import subprocess
import sys

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>FarmWise AI — Admin GIS Dashboard Hackathon Master Guide</title>
<style>
  @page {
    size: A4;
    margin: 16mm 15mm 16mm 15mm;
  }

  * {
    box-sizing: border-box;
  }

  body {
    font-family: 'Segoe UI', Arial, sans-serif;
    color: #334155;
    font-size: 9.6pt;
    line-height: 1.56;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .hero-card {
    background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
    border: 1.5px solid #a7f3d0;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 14px;
  }
  .hero-badge {
    font-size: 8pt;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: #059669;
    text-transform: uppercase;
    margin-bottom: 4px;
  }
  .hero-title {
    font-size: 17pt;
    font-weight: 800;
    color: #064e3b;
    margin: 0 0 4px 0;
  }
  .hero-sub {
    font-size: 9.2pt;
    color: #047857;
    margin: 0;
  }

  .section-header {
    font-size: 13pt;
    font-weight: 800;
    color: #065f46;
    text-transform: uppercase;
    margin: 18px 0 10px 0;
    padding-bottom: 5px;
    border-bottom: 2px solid #10b981;
    page-break-after: avoid;
  }

  h2.sub-heading {
    font-size: 11pt;
    font-weight: 700;
    color: #0f766e;
    margin: 12px 0 5px 0;
    padding-bottom: 3px;
    border-bottom: 1px solid #e2e8f0;
    page-break-after: avoid;
  }

  h3.mini-heading {
    font-size: 9.6pt;
    font-weight: 700;
    color: #1e293b;
    margin: 8px 0 3px 0;
    page-break-after: avoid;
  }

  p {
    margin: 0 0 6px 0;
  }

  ul, ol {
    margin: 3px 0 8px 0;
    padding-left: 20px;
  }

  li {
    margin-bottom: 3.5px;
  }

  code {
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 8.5pt;
    background-color: #f1f5f9;
    color: #0f766e;
    padding: 1px 4px;
    border-radius: 3px;
  }

  .diagram-box {
    background-color: #0f172a;
    border-radius: 8px;
    padding: 12px;
    margin: 10px 0 12px 0;
    text-align: center;
    page-break-inside: avoid;
  }

  .callout-box {
    background-color: #f8fafc;
    border-left: 3.5px solid #10b981;
    padding: 8px 12px;
    margin: 8px 0 10px 0;
    font-size: 9pt;
    color: #0f172a;
    page-break-inside: avoid;
  }

  .highlight-grid {
    display: table;
    width: 100%;
    border-spacing: 8px;
    margin: 6px -8px 10px -8px;
  }
  .highlight-row {
    display: table-row;
  }
  .highlight-cell {
    display: table-cell;
    width: 50%;
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 9px 11px;
    vertical-align: top;
  }
  .highlight-cell-title {
    font-size: 9.5pt;
    font-weight: 700;
    color: #065f46;
    margin-bottom: 3px;
  }

  table.data-table {
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 12px 0;
    font-size: 8.6pt;
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

  .qa-card {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #059669;
    border-radius: 6px;
    padding: 8px 12px;
    margin-bottom: 9px;
    page-break-inside: avoid;
  }
  .qa-q {
    font-weight: 700;
    color: #0f172a;
    font-size: 9.5pt;
    margin-bottom: 4px;
  }
  .qa-a {
    color: #334155;
    font-size: 9pt;
    margin: 0;
  }

  .page-break {
    page-break-before: always;
  }
</style>
</head>
<body>

  <!-- HERO HEADER -->
  <div class="hero-card">
    <div class="hero-badge">FARMWISE AI &bull; HACKATHON REVIEW &amp; TECHNICAL PREPARATION GUIDE</div>
    <h1 class="hero-title">Admin Geographic Crop Monitoring GIS Dashboard — Master Guide</h1>
    <p class="hero-sub">Technologies Used &bull; Implementation Architecture &bull; Admin Workflow &bull; Standout Features &bull; Judge Cross-Questions &amp; Answers</p>
  </div>

  <!-- SECTION 1: TECHNOLOGIES USED -->
  <div class="section-header">1. Technologies Used &amp; Engineering Stack</div>
  <p>The <strong>Admin Geographic Crop Monitoring GIS Dashboard</strong> is a full-stack spatial surveillance, verification, and agricultural analytics system engineered to monitor <strong>14,643 registered cultivation records</strong> across <strong>21 revenue villages</strong> in Tenkasi and Thoothukudi districts.</p>

  <table class="data-table">
    <thead>
      <tr>
        <th style="width: 22%;">Layer</th>
        <th style="width: 28%;">Technology / Library</th>
        <th style="width: 50%;">Exact Role in Admin GIS Dashboard</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Frontend Core</strong></td>
        <td>React 19 + Vite 8 + Tailwind CSS v4</td>
        <td>Component-driven UI (<code>AdminDashboard.jsx</code>) with responsive grid layouts, utility styling, and fast Vite dev proxy (<code>/api &rarr; 127.0.0.1:8000</code>).</td>
      </tr>
      <tr>
        <td><strong>GIS &amp; Mapping</strong></td>
        <td>Leaflet 1.9 + <code>react-leaflet</code> v5 + Esri World Imagery + OpenStreetMap</td>
        <td>Renders dual-layer satellite/street maps, Cadastral GeoJSON parcel polygons, custom HTML <code>L.DivIcon</code> crop emoji markers, and interactive popups.</td>
      </tr>
      <tr>
        <td><strong>Data Visualization</strong></td>
        <td>Recharts 3 (<code>BarChart</code>, <code>PieChart</code>) + Lucide Icons</td>
        <td>Displays Crop-wise Cultivated Area (Acres), Health Status Donut distribution, and AI Seasonal Crop Recommendation profit comparisons.</td>
      </tr>
      <tr>
        <td><strong>HTTP Client &amp; Resilience</strong></td>
        <td>Axios (15s timeout + Fallback Cache)</td>
        <td>Parallel API calls via <code>Promise.all</code> in <code>api.js</code> with synchronized client-side fallback data if the backend is offline or slow.</td>
      </tr>
      <tr>
        <td><strong>Backend API</strong></td>
        <td>FastAPI (Python) + Uvicorn + Pydantic</td>
        <td>Exposes 9 REST endpoints under <code>/api/admin/crop-monitoring/*</code> and <code>/api/admin/crop-recommendations/analytics</code> with query filtering &amp; pagination.</td>
      </tr>
      <tr>
        <td><strong>Data &amp; Spatial Processing</strong></td>
        <td>Pandas + GeoJSON + Deterministic MD5 Hashing</td>
        <td>Parses <code>Ground_truth_Points.csv</code> (14,643 rows), <code>Park_Cadastral_Map.geojson</code>, and <code>Park_fmb_Map.geojson</code> in memory for sub-50ms filtering.</td>
      </tr>
    </tbody>
  </table>

  <!-- SECTION 2: HOW IT WAS IMPLEMENTED -->
  <div class="section-header">2. How It Was Implemented (Architecture &amp; Core Algorithms)</div>

  <div class="diagram-box">
    <svg width="500" height="175" viewBox="0 0 500 175" xmlns="http://www.w3.org/2000/svg">
      <rect x="15" y="10" width="470" height="32" rx="5" fill="#1e293b" stroke="#10b981" stroke-width="1.2"/>
      <text x="250" y="24" fill="#34d399" font-size="9" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">AdminDashboard.jsx (React State: selectedFilters, searchQuery, currentPage)</text>
      <text x="250" y="36" fill="#cbd5e1" font-size="7.5" text-anchor="middle" font-family="Segoe UI, sans-serif">AdminFilterToolbar (9 Cascading Filters) &bull; AdminCropMap &bull; AdminStatsOverview &bull; AdminRecommendationInsights &bull; AdminRecordTable</text>

      <line x1="125" y1="42" x2="125" y2="68" stroke="#38bdf8" stroke-width="1.2"/>
      <line x1="250" y1="42" x2="250" y2="68" stroke="#38bdf8" stroke-width="1.2"/>
      <line x1="375" y1="42" x2="375" y2="68" stroke="#38bdf8" stroke-width="1.2"/>
      <polygon points="121,64 129,64 125,70" fill="#38bdf8"/>
      <polygon points="246,64 254,64 250,70" fill="#38bdf8"/>
      <polygon points="371,64 379,64 375,70" fill="#38bdf8"/>

      <rect x="20" y="70" width="460" height="28" rx="5" fill="#090d16" stroke="#38bdf8" stroke-width="1.2"/>
      <text x="250" y="83" fill="#ffffff" font-size="8.8" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">FastAPI Parallel REST Layer (Promise.all in api.js)</text>
      <text x="250" y="93" fill="#94a3b8" font-size="7.3" text-anchor="middle" font-family="Segoe UI, sans-serif">/markers (limit=1500) &nbsp;|&nbsp; /overview &nbsp;|&nbsp; /records (page_size=25) &nbsp;|&nbsp; /cadastral-boundaries &nbsp;|&nbsp; /recommendations/analytics</text>

      <line x1="250" y1="98" x2="250" y2="115" stroke="#38bdf8" stroke-width="1.2"/>
      <polygon points="246,111 254,111 250,117" fill="#38bdf8"/>

      <rect x="20" y="117" width="220" height="48" rx="5" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
      <text x="130" y="131" fill="#fbbf24" font-size="8.5" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">CropMonitoringService (Singleton)</text>
      <text x="130" y="143" fill="#cbd5e1" font-size="7.3" text-anchor="middle" font-family="Segoe UI, sans-serif">&bull; Stratified 12-Crop Map Sampling</text>
      <text x="130" y="154" fill="#cbd5e1" font-size="7.3" text-anchor="middle" font-family="Segoe UI, sans-serif">&bull; Priority Engine (HIGH / MED / LOW) + Audit Log</text>

      <rect x="260" y="117" width="220" height="48" rx="5" fill="#1e293b" stroke="#a855f7" stroke-width="1.2"/>
      <text x="370" y="131" fill="#d8b4fe" font-size="8.5" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">CropRecommendationService</text>
      <text x="370" y="143" fill="#cbd5e1" font-size="7.3" text-anchor="middle" font-family="Segoe UI, sans-serif">&bull; TNAU/ICAR Seasonal Crop Scoring</text>
      <text x="370" y="154" fill="#cbd5e1" font-size="7.3" text-anchor="middle" font-family="Segoe UI, sans-serif">&bull; District Profit &amp; Market Projections</text>
    </svg>
  </div>

  <h2 class="sub-heading">2.1 Cascading Filters &amp; Synchronized State (<code>AdminFilterToolbar.jsx</code>)</h2>
  <p>Selecting a <strong>District</strong> dynamically filters available <strong>Taluks</strong>, which in turn filters <strong>Villages</strong>. Alongside geography, officers can filter by <strong>Cultivated Crop</strong>, <strong>Health Condition</strong>, <strong>Disease/Pest</strong>, <strong>Verification</strong> (<code>Verified</code>, <code>Verification Required</code>, <code>Rejected</code>, <code>Not Verified</code>), <strong>Alert Priority</strong>, <strong>Season</strong>, and free-text search (Survey #, Parcel ID, Farmer ID, Village, Crop). Any change triggers a synchronized <code>Promise.all</code> refresh across the map, KPIs, charts, and table.</p>

  <h2 class="sub-heading">2.2 Stratified Multi-Crop GIS Sampling (<code>crop_monitoring_service.py</code>)</h2>
  <p>With 14,643 records, rendering every point in the browser DOM would freeze Leaflet, so the map caps rendering at <code>limit=1500</code>. A naive <code>records[:1500]</code> slice cut off crops located later in the CSV (like Rice at index 4,989 and Sugarcane at index 14,210). To solve this, <code>get_map_markers()</code> implements <strong>stratified sampling</strong>:</p>
  <ul>
    <li>Groups filtered records by <code>crop_name</code> and guarantees at least <code>min_per_crop = 10</code> markers per crop variety.</li>
    <li>Distributes remaining quota proportionally across crops using evenly spaced indexing (<code>step = len(recs) / take_count</code>), ensuring all <strong>12 crops</strong> and <strong>21 villages</strong> appear simultaneously on the map.</li>
  </ul>

  <h2 class="sub-heading">2.3 Transparent Priority Classification &amp; Health Thresholds</h2>
  <div class="callout-box">
    <strong>Configurable Thresholds (<code>HEALTH_THRESHOLDS</code>):</strong> Healthy = <code>80–100%</code> | Moderate = <code>50–79%</code> | Critical = <code>&lt;50%</code> | Missing (<code>None</code>) = <code>Health Data Unavailable</code> (never misclassified as Healthy).<br/>
    <strong>Priority Rules (<code>compute_priority</code>):</strong><br/>
    &bull; <strong>HIGH (Red):</strong> Critical health (&lt;50%) OR confirmed <code>Disease Detected</code> / <code>Pest Detected</code>. <em>Cannot be downgraded even if Verified.</em><br/>
    &bull; <strong>MEDIUM (Amber):</strong> Moderate health (50–79%), missing health telemetry, <code>Diagnosis Pending</code>, or Verification Pending/Required.<br/>
    &bull; <strong>LOW (Green):</strong> Healthy (80–100%) AND Verified with zero unresolved alerts. Every record stores a human-readable <code>priority_reason</code>.
  </div>

  <h2 class="sub-heading">2.4 Leaflet Map Rendering, Marker Color Coding &amp; Table-to-Map Sync</h2>
  <ul>
    <li><strong>Marker Visuals (<code>AdminCropMap.jsx</code>):</strong> Uses <code>L.DivIcon</code> (<code>.custom-crop-marker</code>) displaying the crop emoji inside a status-colored badge: <strong>Green</strong> (Healthy), <strong>Yellow</strong> (Moderate), <strong>Red</strong> (Critical), <strong>Orange</strong> (Not Verified / Verification Required), <strong>Dark Red</strong> (Disease/Pest Detected).</li>
    <li><strong>1-Click "Map" Locate Button:</strong> Clicking <strong>Map</strong> on any row in <code>AdminRecordTable.jsx</code> calls <code>handleSelectAndLocateRecord()</code>, which checks if the record is in the current 1,500 markers (injecting it if not), flies the map to <code>[lat, lng]</code> at zoom 16, highlights the marker, and smoothly scrolls up to the map.</li>
    <li><strong>Verification &amp; Audit Logging (<code>AdminRecordDetailModal.jsx</code>):</strong> Officers inspect the full parcel dossier, field photo, and priority reason, then edit crop/area/health or click <strong>Verify / Reject</strong> (rejection requires a mandatory written reason). Every change appends an immutable entry to <code>audit_log</code> via <code>PUT /api/admin/crop-monitoring/records/{record_id}</code>.</li>
  </ul>

  <!-- SECTION 3: ADMIN WORKFLOW -->
  <div class="page-break"></div>
  <div class="section-header">3. End-to-End Admin Officer Workflow</div>
  <p>This is the operational workflow an Agricultural / Revenue Officer follows inside the Admin Dashboard during daily monitoring or a live hackathon demonstration:</p>

  <div class="diagram-box">
    <svg width="500" height="90" viewBox="0 0 500 90" xmlns="http://www.w3.org/2000/svg">
      <rect x="5" y="20" width="88" height="48" rx="5" fill="#1e293b" stroke="#10b981" stroke-width="1.2"/>
      <text x="49" y="38" fill="#34d399" font-size="7.8" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">1. Select Region</text>
      <text x="49" y="50" fill="#cbd5e1" font-size="6.8" text-anchor="middle" font-family="Segoe UI, sans-serif">District / Taluk /</text>
      <text x="49" y="60" fill="#cbd5e1" font-size="6.8" text-anchor="middle" font-family="Segoe UI, sans-serif">Village Filter</text>

      <line x1="93" y1="44" x2="104" y2="44" stroke="#38bdf8" stroke-width="1.2"/>
      <polygon points="101,41 107,44 101,47" fill="#38bdf8"/>

      <rect x="107" y="20" width="88" height="48" rx="5" fill="#1e293b" stroke="#ef4444" stroke-width="1.2"/>
      <text x="151" y="38" fill="#fca5a5" font-size="7.8" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">2. Triage Alerts</text>
      <text x="151" y="50" fill="#cbd5e1" font-size="6.8" text-anchor="middle" font-family="Segoe UI, sans-serif">Filter HIGH Priority</text>
      <text x="151" y="60" fill="#cbd5e1" font-size="6.8" text-anchor="middle" font-family="Segoe UI, sans-serif">/ Disease / Critical</text>

      <line x1="195" y1="44" x2="206" y2="44" stroke="#38bdf8" stroke-width="1.2"/>
      <polygon points="203,41 209,44 203,47" fill="#38bdf8"/>

      <rect x="209" y="20" width="88" height="48" rx="5" fill="#1e293b" stroke="#38bdf8" stroke-width="1.2"/>
      <text x="253" y="38" fill="#7dd3fc" font-size="7.8" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">3. GIS Inspect</text>
      <text x="253" y="50" fill="#cbd5e1" font-size="6.8" text-anchor="middle" font-family="Segoe UI, sans-serif">Satellite + FMB</text>
      <text x="253" y="60" fill="#cbd5e1" font-size="6.8" text-anchor="middle" font-family="Segoe UI, sans-serif">Parcel Boundary</text>

      <line x1="297" y1="44" x2="308" y2="44" stroke="#38bdf8" stroke-width="1.2"/>
      <polygon points="305,41 311,44 305,47" fill="#38bdf8"/>

      <rect x="311" y="20" width="88" height="48" rx="5" fill="#1e293b" stroke="#f59e0b" stroke-width="1.2"/>
      <text x="355" y="38" fill="#fbbf24" font-size="7.8" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">4. Verify / Edit</text>
      <text x="355" y="50" fill="#cbd5e1" font-size="6.8" text-anchor="middle" font-family="Segoe UI, sans-serif">Inspect Photo &amp;</text>
      <text x="355" y="60" fill="#cbd5e1" font-size="6.8" text-anchor="middle" font-family="Segoe UI, sans-serif">Approve / Reject</text>

      <line x1="399" y1="44" x2="410" y2="44" stroke="#38bdf8" stroke-width="1.2"/>
      <polygon points="407,41 413,44 407,47" fill="#38bdf8"/>

      <rect x="413" y="20" width="82" height="48" rx="5" fill="#1e293b" stroke="#a855f7" stroke-width="1.2"/>
      <text x="454" y="38" fill="#d8b4fe" font-size="7.8" font-weight="bold" text-anchor="middle" font-family="Segoe UI, sans-serif">5. Audit &amp; Plan</text>
      <text x="454" y="50" fill="#cbd5e1" font-size="6.8" text-anchor="middle" font-family="Segoe UI, sans-serif">Audit Log + AI</text>
      <text x="454" y="60" fill="#cbd5e1" font-size="6.8" text-anchor="middle" font-family="Segoe UI, sans-serif">Crop Insights</text>
    </svg>
  </div>

  <ol>
    <li><strong>Jurisdiction Selection:</strong> Officer switches to <em>Admin Dashboard</em> from the top Navbar and narrows scope using District &rarr; Taluk &rarr; Village cascading dropdowns (or searches a specific Survey #).</li>
    <li><strong>Urgent Triage:</strong> Officer filters by <code>HIGH</code> Priority or <code>Disease Detected</code> or <code>Verification Required</code>. The registry table automatically sorts <code>HIGH</code> priority parcels to the top.</li>
    <li><strong>Geospatial Verification:</strong> Officer clicks a crop emoji marker on the satellite map—or clicks <strong>Map</strong> on a table row—to inspect the parcel's FMB cadastral boundary, coordinates, health score, and priority trigger banner.</li>
    <li><strong>Dossier Review &amp; Ground Action:</strong> Clicking <strong>View</strong> (or <em>Inspect &amp; Verify Record</em> in the map popup) opens <code>AdminRecordDetailModal</code> showing the field photograph, farmer details, and audit history. The officer can update crop/area/health or click <strong>Approve &amp; Verify</strong> / <strong>Reject (with Reason)</strong>.</li>
    <li><strong>Macro Analytics &amp; Policy Planning:</strong> Below the map, the officer reviews the 6 state-wide KPI cards, crop acreage bar chart, health donut chart, and <strong>AI Seasonal Crop Recommendations &amp; Profit Projections</strong> to plan district-level subsidies and extension outreach.</li>
  </ol>

  <!-- SECTION 4: ATTRACTIVE & BEST FEATURES -->
  <div class="section-header">4. Attractive &amp; Standout Features to Highlight in Demo</div>
  <div class="highlight-grid">
    <div class="highlight-row">
      <div class="highlight-cell">
        <div class="highlight-cell-title">1. Live Satellite + FMB Cadastral GIS</div>
        Real-time Esri World Imagery &amp; OpenStreetMap toggle overlaid with actual Tamil Nadu Cadastral parcel polygons and tooltips showing Survey # and Village.
      </div>
      <div class="highlight-cell">
        <div class="highlight-cell-title">2. Stratified 12-Crop Emoji Markers</div>
        Every crop variety (Rice, Coconut, Maize, Banana, Sugarcane, Groundnut, Cotton, Mango, etc.) renders simultaneously with intuitive emojis and 5-tier status color rings.
      </div>
    </div>
    <div class="highlight-row">
      <div class="highlight-cell">
        <div class="highlight-cell-title">3. Safety-First Priority Engine</div>
        Transparent rule engine with human-readable reasons. Critical health (&lt;50%) or active disease stays <code>HIGH</code> priority even after administrative verification.
      </div>
      <div class="highlight-cell">
        <div class="highlight-cell-title">4. 1-Click Table-to-Map Fly-To</div>
        Clicking <strong>Map</strong> on any of the 14,643 table rows guarantees the parcel marker is pinned onto the GIS map, centers smoothly, and opens its popup.
      </div>
    </div>
    <div class="highlight-row">
      <div class="highlight-cell">
        <div class="highlight-cell-title">5. Immutable Officer Audit Trail</div>
        Every verification, rejection (requiring a mandatory justification), or field edit records timestamp, officer ID, and before/after values.
      </div>
      <div class="highlight-cell">
        <div class="highlight-cell-title">6. AI Profit Insights &amp; PII Masking</div>
        Combines TNAU/ICAR seasonal profit projections (&#8377;/acre) with privacy-by-design farmer name masking (<code>R. K****</code>) in non-privileged views.
      </div>
    </div>
  </div>

  <!-- SECTION 5: HACKATHON CROSS QUESTIONS & ANSWERS -->
  <div class="page-break"></div>
  <div class="section-header">5. Hackathon Review Cross-Questions &amp; Winning Answers</div>
  <p>Prepare for technical, architectural, and domain cross-questions from hackathon judges using these exact answers grounded in the codebase:</p>

  <div class="qa-card">
    <div class="qa-q">Q1. You have 14,643 parcels—doesn't rendering 14,000+ DOM markers freeze Leaflet? How did you handle performance?</div>
    <p class="qa-a"><strong>Answer:</strong> We cap map rendering at <code>limit=1500</code> markers per viewport query and paginate the registry table (<code>page_size=25</code>). Crucially, instead of naive <code>[:1500]</code> slicing—which hid crops appearing later in the CSV—we implemented <strong>stratified multi-crop sampling</strong> in <code>crop_monitoring_service.py</code>, guaranteeing at least 10 markers per crop and evenly spacing samples across all 21 villages. If an admin clicks <strong>Map</strong> on a table row outside the 1,500 slice, the frontend dynamically injects that exact parcel marker on demand.</p>
  </div>

  <div class="qa-card">
    <div class="qa-q">Q2. What happens if a parcel has missing crop health data? Do you treat it as Healthy or Critical?</div>
    <p class="qa-a"><strong>Answer:</strong> Neither. In <code>classify_health()</code>, missing health scores (<code>None</code>) are explicitly categorized as <code>"Health Data Unavailable"</code>, never defaulted to Healthy. In <code>compute_priority()</code>, missing telemetry automatically assigns <code>MEDIUM</code> priority with the reason <em>"Missing crop health telemetry"</em> so officers schedule follow-up inspection.</p>
  </div>

  <div class="qa-card">
    <div class="qa-q">Q3. If an admin marks a Critical-health parcel as "Verified", does its priority drop to LOW?</div>
    <p class="qa-a"><strong>Answer:</strong> No. Our priority engine evaluates <code>HIGH</code> triggers first: if <code>health_score &lt; 50</code> or <code>Disease Detected</code> / <code>Pest Detected</code> is active, it immediately returns <code>HIGH</code> priority regardless of verification status. Verification only resolves the <em>"Verification pending"</em> <code>MEDIUM</code> trigger—it never masks an active agronomic emergency.</p>
  </div>

  <div class="qa-card">
    <div class="qa-q">Q4. Do you infer Disease Detected automatically from a low health score?</div>
    <p class="qa-a"><strong>Answer:</strong> No. Verification status, crop health status, disease status, and priority are stored and evaluated as independent attributes. Low health scores without confirmed pathology trigger Critical Health, whereas disease status comes strictly from the crop-health / vision analysis fields (<code>Disease Detected</code>, <code>Pest Detected</code>, <code>No Disease Detected</code>, <code>Diagnosis Pending</code>).</p>
  </div>

  <div class="qa-card">
    <div class="qa-q">Q5. Why did you use custom Leaflet DivIcons instead of standard map pins?</div>
    <p class="qa-a"><strong>Answer:</strong> Officers need to see <em>both</em> the crop type and its risk status at a single glance without clicking 1,500 pins. Our <code>createCropMarkerIcon()</code> renders the crop emoji (🌾, 🥥, 🍌, 🌽, 🎋) inside a 34px circular badge colored by risk status (Green, Yellow, Red, Orange, Dark Red), backed by <code>.custom-crop-marker</code> CSS so Leaflet's default square styles don't collide.</p>
  </div>

  <div class="qa-card">
    <div class="qa-q">Q6. How do you ensure accountability when an admin officer rejects or edits a farmer's crop record?</div>
    <p class="qa-a"><strong>Answer:</strong> In <code>AdminRecordDetailModal.jsx</code> and <code>update_crop_record()</code>, rejecting a record enforces a mandatory written reason. Every mutation appends a structured entry to <code>self.audit_log</code> recording timestamp, officer identity, action taken, reason, and modified fields, viewable via <code>GET /api/admin/crop-monitoring/audit-log</code>.</p>
  </div>

  <div class="qa-card">
    <div class="qa-q">Q7. How do you protect farmer personal data (PII) on the dashboard?</div>
    <p class="qa-a"><strong>Answer:</strong> Farmer names are masked by default (e.g., <code>R. K****</code> via <code>farmer_name_masked</code>) across map popups and public/overview views, while full unmasked records are restricted to the authorized officer inspection workflow.</p>
  </div>

  <div class="qa-card">
    <div class="qa-q">Q8. What happens during a live demo if the backend server is slow or temporarily unreachable?</div>
    <p class="qa-a"><strong>Answer:</strong> <code>frontend/src/services/api.js</code> uses a 15-second timeout and a synchronized offline fallback cache (<code>window.__FALLBACK_CROP_RECORDS__</code>). Even if the backend drops, the GIS map, filters, KPI charts, and paginated table stay synchronized with representative Sivagiri/Tenkasi parcel data instead of crashing or showing empty tables.</p>
  </div>

  <div class="qa-card">
    <div class="qa-q">Q9. Are your thresholds (80%, 50%) hardcoded everywhere?</div>
    <p class="qa-a"><strong>Answer:</strong> No—they are centralized in <code>HEALTH_THRESHOLDS = {"HEALTHY_MIN": 80, "MODERATE_MIN": 50}</code> in <code>crop_monitoring_service.py</code>, making policy adjustments a single-line config change.</p>
  </div>

  <div class="qa-card">
    <div class="qa-q">Q10. How does the AI Recommendation Insights panel on the Admin page avoid recommending crops just because market prices are high?</div>
    <p class="qa-a"><strong>Answer:</strong> <code>CropRecommendationService</code> scores crops using a weighted multi-factor model (Soil 35%, Weather &amp; Water 25%, Net Profit Economics after cultivation cost 25%, TNAU Seasonal Suitability 15%), and aggregates district-level profit projections and TNAU agronomic advisories into <code>AdminRecommendationInsights.jsx</code>.</p>
  </div>

  <div class="qa-card">
    <div class="qa-q">Q11. How would you scale this from in-memory CSV/GeoJSON to production AWS?</div>
    <p class="qa-a"><strong>Answer:</strong> Our backend is already structured around service adapters. In production on AWS (<code>ap-south-1</code> Mumbai), GeoJSON boundaries and field images live in private S3 buckets, while parcel records, audit logs, and spatial indexes map cleanly to DynamoDB tables without changing any frontend React components or API contracts.</p>
  </div>

  <div class="qa-card">
    <div class="qa-q">Q12. How does the Admin GIS Dashboard connect with the Farmer Advisory side?</div>
    <p class="qa-a"><strong>Answer:</strong> Both views share the same canonical Survey Numbers, Cadastral GeoJSON boundaries, and <code>CropRecommendationService</code>. When a farmer submits field data or gets an AI recommendation, it feeds the same registry that officers monitor, verify, and audit on the GIS map.</p>
  </div>

</body>
</html>
"""

def generate_admin_guide_pdf():
    os.makedirs("docs", exist_ok=True)
    html_path = os.path.abspath("docs/FarmWise_AI_Admin_Dashboard_Hackathon_Master_Guide.html")
    pdf_path = os.path.abspath("docs/FarmWise_AI_Admin_Dashboard_Hackathon_Master_Guide.pdf")

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
        print("Error: Neither Chrome nor Edge was found.", file=sys.stderr)
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
    print(f"Rendering Admin Hackathon Master Guide PDF using {os.path.basename(browser)}...")
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if res.returncode != 0:
        print("Browser error:", res.stderr, file=sys.stderr)
        sys.exit(res.returncode)

    if os.path.exists(pdf_path):
        print(f"Successfully generated PDF: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
    else:
        print("Error: PDF file was not created.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    generate_admin_guide_pdf()
