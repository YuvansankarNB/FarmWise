import React, { useState, useEffect } from 'react';
import { 
  Sparkles, TrendingUp, IndianRupee, Sprout, Calendar, 
  Droplet, Award, ArrowRight, ShieldCheck, Info, ChevronRight, 
  Layers, BarChart2, CheckCircle2, AlertCircle, HelpCircle, Eye 
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  LineChart, Line, CartesianGrid, Legend, Cell 
} from 'recharts';
import { api } from '../services/api';

export default function SmartCropRecommendations({ 
  surveyNumber = '1342', 
  lang = 'en',
  activeParcel = null 
}) {
  const isTamil = lang === 'ta';

  // State
  const [landArea, setLandArea] = useState(1.0);
  const [seasonFilter, setSeasonFilter] = useState('ALL');
  const [recommendationData, setRecommendationData] = useState(null);
  const [selectedCrop, setSelectedCrop] = useState(null);
  const [marketTrends, setMarketTrends] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isTrendsLoading, setIsTrendsLoading] = useState(false);

  // Fetch recommendations whenever survey, land area, or season changes
  useEffect(() => {
    let isMounted = true;
    async function fetchRecs() {
      setIsLoading(true);
      try {
        const res = await api.getCropRecommendations(surveyNumber, landArea, seasonFilter);
        if (isMounted && res) {
          setRecommendationData(res);
          if (res.top_5_recommendations && res.top_5_recommendations.length > 0) {
            setSelectedCrop(res.top_5_recommendations[0]);
          }
        }
      } catch (err) {
        console.error("Error loading crop recommendations:", err);
      } finally {
        if (isMounted) setIsLoading(false);
      }
    }
    fetchRecs();
    return () => { isMounted = false; };
  }, [surveyNumber, landArea, seasonFilter]);

  // Fetch market trends when selected crop changes
  useEffect(() => {
    let isMounted = true;
    if (!selectedCrop) return;

    async function fetchTrends() {
      setIsTrendsLoading(true);
      try {
        const trends = await api.getCropMarketTrends(surveyNumber, selectedCrop.crop_name);
        if (isMounted && trends) {
          setMarketTrends(trends);
        }
      } catch (err) {
        console.error("Error loading market trends:", err);
      } finally {
        if (isMounted) setIsTrendsLoading(false);
      }
    }
    fetchTrends();
    return () => { isMounted = false; };
  }, [selectedCrop, surveyNumber]);

  if (isLoading && !recommendationData) {
    return (
      <div className="bg-white rounded-3xl p-8 border border-emerald-100 shadow-sm text-center space-y-3">
        <div className="w-12 h-12 rounded-2xl bg-emerald-100 text-emerald-700 mx-auto flex items-center justify-center animate-spin">
          <Sparkles className="w-6 h-6" />
        </div>
        <p className="text-sm font-bold text-slate-800">
          {isTamil ? "AI பயிர் பரிந்துரைகள் மற்றும் லாபக் கணிப்புகள் உருவாக்கப்படுகின்றன..." : "Synthesizing AI Seasonal Crop Recommendations & Profit Projections..."}
        </p>
        <p className="text-xs text-slate-500">
          {isTamil ? "மண்வளம், வானிலை, TNAU பயிர் கையேடு மற்றும் APMC சந்தை விலைகளை ஆய்வு செய்கிறது" : "Cross-referencing Soil Health, 7-Day Agro-Met, TNAU Manuals, and APMC Mandi Rates"}
        </p>
      </div>
    );
  }

  const landSummary = recommendationData?.land_summary || {};
  const topCrops = recommendationData?.top_5_recommendations || [];
  const comparisonChart = recommendationData?.comparison_chart || [];

  return (
    <div className="space-y-6">
      {/* ─── SECTION 1: HEADER & LAND SUMMARY ─── */}
      <div className="bg-gradient-to-r from-emerald-800 via-teal-900 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-lg space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-emerald-700/50 pb-5">
          <div className="flex items-center gap-3.5">
            <div className="w-12 h-12 rounded-2xl bg-white/10 backdrop-blur-md flex items-center justify-center text-emerald-300 shadow-inner">
              <Sparkles className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-lg sm:text-xl font-black tracking-tight">
                  {isTamil ? "AI பருவ பயிர் பரிந்துரை & லாபக் கணிப்பு முறை" : "AI-Powered Seasonal Crop Recommendation & Profit Prediction"}
                </h2>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-emerald-400/20 text-emerald-200 border border-emerald-400/30 font-mono">
                  TNAU-ICAR Engine
                </span>
              </div>
              <p className="text-xs text-emerald-200/80 mt-0.5">
                {isTamil ? "உங்கள் நிலத்தின் மண்வளம், தற்போதைய பருவநிலை மற்றும் சந்தை விலைக்கு உகந்த பயிர்கள்" : "Top 5 high-yield, climate-resilient and economically optimal crops for your land parcel"}
              </p>
            </div>
          </div>

          {/* Land Area Calculator Input */}
          <div className="flex items-center gap-2 bg-white/10 backdrop-blur-md p-1.5 rounded-2xl border border-white/10 text-xs">
            <span className="text-emerald-200 pl-2 font-medium">
              {isTamil ? "நிலப் பரப்பளவு:" : "Cultivated Area:"}
            </span>
            <input
              type="number"
              step="0.5"
              min="0.5"
              max="50"
              value={landArea}
              onChange={(e) => setLandArea(Math.max(0.5, parseFloat(e.target.value) || 1.0))}
              className="w-16 py-1 px-2 bg-white text-slate-900 font-bold rounded-xl text-center focus:outline-none font-mono"
            />
            <span className="text-white pr-2 font-bold">{isTamil ? "ஏக்கர்" : "Acres"}</span>
          </div>
        </div>

        {/* Farmer Land & Soil Health Snapshot Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3 text-xs">
          <div className="bg-white/10 backdrop-blur-xs p-3 rounded-2xl border border-white/5">
            <span className="text-emerald-300 text-[10px] uppercase font-bold block">{isTamil ? "சர்வே எண்" : "Survey Number"}</span>
            <span className="text-white font-mono font-bold text-sm">#{landSummary.survey_number}</span>
            <span className="text-emerald-200/70 block text-[10px]">{landSummary.village}, {landSummary.taluk}</span>
          </div>

          <div className="bg-white/10 backdrop-blur-xs p-3 rounded-2xl border border-white/5">
            <span className="text-emerald-300 text-[10px] uppercase font-bold block">{isTamil ? "நடப்பு பருவம்" : "Current Season"}</span>
            <span className="text-white font-bold text-sm">{landSummary.current_season}</span>
            <span className="text-emerald-200/70 block text-[10px]">{isTamil ? "விதைப்பு காலம்" : "Sowing Window Active"}</span>
          </div>

          <div className="bg-white/10 backdrop-blur-xs p-3 rounded-2xl border border-white/5">
            <span className="text-emerald-300 text-[10px] uppercase font-bold block">{isTamil ? "மண் வகை & pH" : "Soil Type & pH"}</span>
            <span className="text-white font-bold text-sm">pH {landSummary.soil_summary?.ph}</span>
            <span className="text-emerald-200/70 block text-[10px] truncate">{landSummary.soil_summary?.soil_type}</span>
          </div>

          <div className="bg-white/10 backdrop-blur-xs p-3 rounded-2xl border border-white/5">
            <span className="text-emerald-300 text-[10px] uppercase font-bold block">{isTamil ? "கரிமக் கரிமம் (OC)" : "Organic Carbon"}</span>
            <span className="text-white font-bold text-sm">{landSummary.soil_summary?.organic_carbon_percent}%</span>
            <span className="text-emerald-200/70 block text-[10px]">{landSummary.soil_summary?.ph_status}</span>
          </div>

          <div className="bg-white/10 backdrop-blur-xs p-3 rounded-2xl border border-white/5">
            <span className="text-emerald-300 text-[10px] uppercase font-bold block">{isTamil ? "மண் சத்துக்கள் (NPK)" : "Available NPK"}</span>
            <span className="text-white font-mono font-bold text-sm">{landSummary.soil_summary?.nitrogen_kg_ha}/{landSummary.soil_summary?.phosphorus_kg_ha}/{landSummary.soil_summary?.potassium_kg_ha}</span>
            <span className="text-emerald-200/70 block text-[10px]">kg/ha (Macro nutrients)</span>
          </div>

          <div className="bg-white/10 backdrop-blur-xs p-3 rounded-2xl border border-white/5">
            <span className="text-emerald-300 text-[10px] uppercase font-bold block">{isTamil ? "நுண் வானிலை" : "Microclimate"}</span>
            <span className="text-white font-bold text-sm">{landSummary.weather_summary?.temperature}°C</span>
            <span className="text-emerald-200/70 block text-[10px]">{landSummary.weather_summary?.condition} &bull; {landSummary.weather_summary?.humidity}% Hum</span>
          </div>
        </div>
      </div>

      {/* ─── SECTION 2: TOP 5 RECOMMENDED CROPS CARDS ─── */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-bold text-slate-900 text-base">
              {isTamil ? "பரிந்துரைக்கப்பட்ட முதல் 5 பயிர்கள்" : "Top 5 Recommended Crops"}
            </h3>
            <p className="text-xs text-slate-500">
              {isTamil ? "மண்வளம், வானிலை மற்றும் நிகர லாபத்தின் அடிப்படையில் வரிசைப்படுத்தப்பட்டுள்ளது" : "Ranked based on Soil Compatibility (30%), Season (25%), Profitability (20%), Weather (15%), and APMC Trends (10%)"}
            </p>
          </div>

          <span className="text-xs font-semibold px-2.5 py-1 rounded-xl bg-emerald-50 text-emerald-800 border border-emerald-200">
            {isTamil ? `கணக்கீடு: ${landArea} ஏக்கர் நிலத்திற்கு` : `Projected for: ${landArea} Acres`}
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-3.5">
          {topCrops.map((crop, idx) => {
            const isSelected = selectedCrop?.crop_name === crop.crop_name;
            const netProfit = crop.financials?.total_land?.total_net_profit || 0;
            const roi = crop.financials?.per_acre?.roi_percentage || 0;

            return (
              <div
                key={crop.crop_name}
                onClick={() => setSelectedCrop(crop)}
                className={`bg-white rounded-3xl p-4 border transition-all cursor-pointer relative overflow-hidden flex flex-col justify-between space-y-3 ${
                  isSelected
                    ? 'border-emerald-500 shadow-md ring-2 ring-emerald-500/20'
                    : 'border-slate-200/80 hover:border-emerald-300 shadow-xs hover:shadow-sm'
                }`}
              >
                {/* Rank Badge */}
                <div className="flex items-center justify-between">
                  <span className={`text-[11px] font-black font-mono w-6 h-6 rounded-full flex items-center justify-center ${
                    idx === 0 ? 'bg-amber-100 text-amber-800 border border-amber-300' : 'bg-slate-100 text-slate-700'
                  }`}>
                    #{idx + 1}
                  </span>

                  {/* Recommendation Score Pill */}
                  <div className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-black">
                    <Award className="w-3.5 h-3.5 text-emerald-600" />
                    <span>{crop.recommendation_score} / 100</span>
                  </div>
                </div>

                {/* Crop Name & Emoji */}
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-2xl">{crop.emoji}</span>
                    <div>
                      <h4 className="font-bold text-slate-900 text-sm leading-tight">
                        {isTamil ? crop.tamil_name.split(" ")[0] : crop.crop_name}
                      </h4>
                      <span className="text-[10px] text-slate-400 font-medium block">
                        {crop.category} &bull; {crop.duration}
                      </span>
                    </div>
                  </div>
                  <p className="text-[11px] text-slate-600 line-clamp-2 mt-1">
                    {isTamil ? crop.tamil_explanation : crop.explanation}
                  </p>
                </div>

                {/* Key Financial Snapshot */}
                <div className="bg-slate-50 p-2.5 rounded-2xl border border-slate-100 space-y-1 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400 text-[10px]">{isTamil ? "நிகர லாபம்:" : "Net Profit:"}</span>
                    <span className="font-black text-emerald-700 font-mono">₹{netProfit.toLocaleString()}</span>
                  </div>
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-slate-400 text-[10px]">{isTamil ? "முதலீட்டு வருவாய்:" : "Est. ROI:"}</span>
                    <span className="font-bold text-slate-800 font-mono">+{roi}%</span>
                  </div>
                  <div className="flex items-center justify-between text-[10px] text-slate-500 pt-0.5 border-t border-slate-200/60">
                    <span>{isTamil ? "சந்தை விலை:" : "Mandi Rate:"}</span>
                    <span className="font-semibold text-slate-800">₹{crop.financials.per_acre.selling_price_per_unit}/{crop.financials.per_acre.yield_unit}</span>
                  </div>
                </div>

                {/* Selection Indicator */}
                <div className="pt-1">
                  <button
                    className={`w-full py-1.5 px-3 rounded-xl text-xs font-bold flex items-center justify-center gap-1 transition-colors ${
                      isSelected
                        ? 'bg-emerald-700 text-white'
                        : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                    }`}
                  >
                    <span>{isSelected ? (isTamil ? "தேர்ந்தெடுக்கப்பட்டது" : "Viewing Details") : (isTamil ? "விவரங்கள் காண்க" : "View Details")}</span>
                    <ChevronRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* ─── SECTION 3: PROFIT COMPARISON & FINANCIAL BREAKDOWN ─── */}
      {selectedCrop && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left Column (7 cols): Selected Crop Detailed Financials & TNAU Agronomy */}
          <div className="lg:col-span-7 bg-white rounded-3xl p-6 border border-slate-200/80 shadow-xs space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-3">
                <span className="text-3xl">{selectedCrop.emoji}</span>
                <div>
                  <h4 className="font-bold text-slate-900 text-base">
                    {isTamil ? `${selectedCrop.tamil_name} — விரிவான நிதி மற்றும் சாகுபடி பகுப்பாய்வு` : `${selectedCrop.crop_name} — Detailed Financial & Cultivation Blueprint`}
                  </h4>
                  <p className="text-xs text-slate-500">
                    {isTamil ? `TNAU பரிந்துரைக்கப்பட்ட வழிகாட்டுதல்கள் (${landArea} ஏக்கர் நிலத்திற்கு கணக்கிடப்பட்டது)` : `Based on official TNAU Crop Production Manual (Calculated for ${landArea} Acres)`}
                  </p>
                </div>
              </div>

              <div className="text-right">
                <span className="text-[10px] uppercase font-bold text-slate-400 block">{isTamil ? "மொத்த நிகர லாபம்" : "Total Net Profit"}</span>
                <span className="text-lg font-black text-emerald-700 font-mono">
                  ₹{selectedCrop.financials.total_land.total_net_profit.toLocaleString()}
                </span>
              </div>
            </div>

            {/* Financial Return Summary Cards (Per Acre vs Total Land) */}
            <div className="grid grid-cols-3 gap-3 text-xs">
              <div className="bg-rose-50/70 border border-rose-100 p-3 rounded-2xl">
                <span className="text-rose-700 text-[10px] font-bold uppercase block">{isTamil ? "மொத்த சாகுபடி செலவு" : "Total Cultivation Cost"}</span>
                <span className="text-base font-black text-rose-900 font-mono mt-0.5 block">
                  ₹{selectedCrop.financials.total_land.total_cultivation_cost.toLocaleString()}
                </span>
                <span className="text-[10px] text-rose-600">₹{selectedCrop.financials.per_acre.cost_of_cultivation.toLocaleString()} / acre</span>
              </div>

              <div className="bg-blue-50/70 border border-blue-100 p-3 rounded-2xl">
                <span className="text-blue-700 text-[10px] font-bold uppercase block">{isTamil ? "எதிர்பார்க்கப்படும் மொத்த வருவாய்" : "Gross Revenue"}</span>
                <span className="text-base font-black text-blue-900 font-mono mt-0.5 block">
                  ₹{selectedCrop.financials.total_land.total_gross_revenue.toLocaleString()}
                </span>
                <span className="text-[10px] text-blue-600">{selectedCrop.financials.total_land.total_yield} {selectedCrop.financials.total_land.yield_unit}</span>
              </div>

              <div className="bg-emerald-50 border border-emerald-200 p-3 rounded-2xl">
                <span className="text-emerald-700 text-[10px] font-bold uppercase block">{isTamil ? "மதிப்பிடப்பட்ட நிகர லாபம்" : "Estimated Net Profit"}</span>
                <span className="text-base font-black text-emerald-900 font-mono mt-0.5 block">
                  ₹{selectedCrop.financials.total_land.total_net_profit.toLocaleString()}
                </span>
                <span className="text-[10px] text-emerald-700 font-bold">+{selectedCrop.financials.per_acre.roi_percentage}% Net ROI</span>
              </div>
            </div>

            {/* Itemized Cultivation Expenses Breakdown */}
            <div className="space-y-2">
              <span className="text-xs font-bold text-slate-800 block">
                {isTamil ? `சாகுபடி செலவு விவரங்கள் (${landArea} ஏக்கர்)` : `Itemized Cultivation Expenses Breakdown (${landArea} Acres)`}
              </span>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
                {Object.entries(selectedCrop.financials.total_land.expenses_breakdown).map(([k, v]) => (
                  <div key={k} className="p-2.5 bg-slate-50 rounded-xl border border-slate-100 flex items-center justify-between">
                    <span className="capitalize text-slate-600">{k}:</span>
                    <span className="font-mono font-bold text-slate-900">₹{v.toLocaleString()}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Agronomic Guidance: Sowing, Water, TNAU Recommendations */}
            <div className="space-y-3 pt-2 border-t border-slate-100 text-xs">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="p-3 bg-amber-50/60 rounded-2xl border border-amber-100 space-y-1">
                  <span className="font-bold text-amber-900 flex items-center gap-1.5 text-xs">
                    <Calendar className="w-3.5 h-3.5 text-amber-700" />
                    <span>{isTamil ? "விதைப்பு காலம் & நீர் தேவை" : "Sowing Period & Water Requirement"}</span>
                  </span>
                  <p className="text-slate-700 text-[11px]">
                    <strong>{isTamil ? "விதைப்பு:" : "Window:"}</strong> {selectedCrop.sowing_period}
                  </p>
                  <p className="text-slate-700 text-[11px]">
                    <strong>{isTamil ? "நீர் தேவை:" : "Water Need:"}</strong> {selectedCrop.water_requirement_mm} ({selectedCrop.water_need_level})
                  </p>
                  <p className="text-slate-600 text-[11px] mt-1">{selectedCrop.irrigation_guidance}</p>
                </div>

                <div className="p-3 bg-emerald-50/60 rounded-2xl border border-emerald-100 space-y-1">
                  <span className="font-bold text-emerald-900 flex items-center gap-1.5 text-xs">
                    <Sprout className="w-3.5 h-3.5 text-emerald-700" />
                    <span>{isTamil ? "மண் உகந்த நிலை" : "Soil Suitability & Reaction"}</span>
                  </span>
                  <p className="text-slate-700 text-[11px]">
                    <strong>{isTamil ? "மண் தகுதி:" : "Status:"}</strong> {selectedCrop.soil_suitability.status} ({selectedCrop.soil_suitability.score}%)
                  </p>
                  <p className="text-slate-600 text-[11px] mt-1">{selectedCrop.soil_advisory}</p>
                </div>
              </div>

              {/* TNAU Guidelines */}
              <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200 text-slate-700 space-y-1">
                <span className="font-bold text-slate-900 flex items-center gap-1.5 text-xs">
                  <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                  <span>{isTamil ? "தமிழ்நாடு வேளாண் பல்கலைக்கழகம் (TNAU) பரிந்துரை" : "TNAU Agritech Research Recommendation"}</span>
                </span>
                <p className="text-slate-600 text-[11px]">{selectedCrop.tnau_recommendations}</p>
              </div>
            </div>
          </div>

          {/* Right Column (5 cols): Profit Comparison Chart & APMC Mandi Historical Trends */}
          <div className="lg:col-span-5 space-y-6">
            {/* Profit Comparison Bar Chart across Top 5 crops */}
            <div className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-xs space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                <h4 className="font-bold text-slate-900 text-xs uppercase tracking-wider flex items-center gap-1.5">
                  <BarChart2 className="w-4 h-4 text-emerald-600" />
                  <span>{isTamil ? "பயிர்களின் லாப ஒப்பீட்டு வரைபடம்" : "Comparative Net Profit (₹)"}</span>
                </h4>
                <span className="text-[10px] text-slate-400 font-mono">{landArea} ac</span>
              </div>

              <div className="h-56 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={comparisonChart} margin={{ top: 10, right: 10, left: 0, bottom: 20 }}>
                    <XAxis 
                      dataKey="crop" 
                      tick={{ fontSize: 10, fill: '#64748b' }} 
                      interval={0} 
                      angle={-20} 
                      textAnchor="end" 
                    />
                    <YAxis tick={{ fontSize: 10, fill: '#64748b' }} />
                    <Tooltip
                      content={({ active, payload }) => {
                        if (active && payload && payload.length) {
                          const d = payload[0].payload;
                          return (
                            <div className="bg-slate-900 text-white text-xs p-2 rounded-xl shadow-lg border border-slate-700">
                              <p className="font-bold flex items-center gap-1">
                                <span>{d.emoji}</span>
                                <span>{d.crop}</span>
                              </p>
                              <p className="text-emerald-400 font-mono font-bold mt-1">
                                Net Profit: ₹{d.net_profit?.toLocaleString()}
                              </p>
                              <p className="text-slate-300 text-[10px]">
                                Cost: ₹{d.cultivation_cost?.toLocaleString()}
                              </p>
                            </div>
                          );
                        }
                        return null;
                      }}
                    />
                    <Bar dataKey="net_profit" radius={[6, 6, 0, 0]}>
                      {comparisonChart.map((entry, index) => (
                        <Cell 
                          key={`comp-cell-${index}`} 
                          fill={entry.crop === selectedCrop.crop_name ? '#059669' : '#94a3b8'} 
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* APMC Mandi Historical Price Trends (6-Months) */}
            <div className="bg-white rounded-3xl p-6 border border-slate-200/80 shadow-xs space-y-3">
              <div className="flex items-center justify-between pb-2 border-b border-slate-100">
                <div>
                  <h4 className="font-bold text-slate-900 text-xs uppercase tracking-wider flex items-center gap-1.5">
                    <TrendingUp className="w-4 h-4 text-emerald-600" />
                    <span>{isTamil ? `${selectedCrop.crop_name} சந்தை விலை போக்கு` : `${selectedCrop.crop_name} APMC Price Trend`}</span>
                  </h4>
                  <span className="text-[10px] text-slate-400">
                    {marketTrends?.market_name || "Tenkasi APMC"} &bull; {marketTrends?.trend_direction || "Upward"}
                  </span>
                </div>
                <div className="text-right">
                  <span className="text-xs font-mono font-black text-emerald-700">{marketTrends?.modal_price}</span>
                </div>
              </div>

              {marketTrends && marketTrends.monthly_data && (
                <div className="h-44 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={marketTrends.monthly_data} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                      <XAxis dataKey="month" tick={{ fontSize: 10, fill: '#64748b' }} />
                      <YAxis tick={{ fontSize: 10, fill: '#64748b' }} domain={['dataMin - 100', 'dataMax + 100']} />
                      <Tooltip
                        content={({ active, payload }) => {
                          if (active && payload && payload.length) {
                            const d = payload[0].payload;
                            return (
                              <div className="bg-slate-900 text-white text-xs p-2 rounded-xl border border-slate-700">
                                <span className="font-bold">{d.month}</span>: <span className="text-emerald-400 font-mono font-bold">₹{d.price}</span>
                                <span className="block text-[10px] text-slate-400 mt-0.5">{d.status}</span>
                              </div>
                            );
                          }
                          return null;
                        }}
                      />
                      <Line 
                        type="monotone" 
                        dataKey="price" 
                        stroke="#059669" 
                        strokeWidth={2.5} 
                        dot={{ r: 4, fill: '#059669' }} 
                        activeDot={{ r: 6 }} 
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              )}

              <p className="text-[10px] text-slate-400 italic text-center pt-1">
                {isTamil ? "*கடைசி 6 மாத ஒழுங்குமுறை விற்பனைக் கூட (APMC Mandi) தரவுகளின் அடிப்படையில் கணக்கிடப்பட்டது." : "*Derived from 6-month APMC regulated market historical transaction records."}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* ─── SECTION 4: SCIENTIFIC TRANSPARENCY & DISCLAIMER ─── */}
      <div className="p-4 bg-slate-100/80 rounded-2xl border border-slate-200/80 text-xs text-slate-600 flex items-start gap-3">
        <Info className="w-5 h-5 text-slate-400 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <p className="font-semibold text-slate-800">
            {isTamil ? "வெளிப்படையான பரிந்துரை விதிமுறைகள் & மறுப்புரை:" : "Transparent Recommendation Scoring & Financial Disclaimer:"}
          </p>
          <p className="text-[11px] text-slate-500 leading-relaxed">
            {recommendationData?.disclaimer}
          </p>
          <div className="flex flex-wrap gap-x-4 gap-y-1 text-[10px] text-slate-400 pt-1">
            {recommendationData?.data_sources?.map((s, idx) => (
              <span key={idx}>&bull; {s}</span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
