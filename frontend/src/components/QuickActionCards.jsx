import React from 'react';
import { Camera, Map, TrendingUp } from 'lucide-react';
import { translations } from '../utils/translations';

export default function QuickActionCards({ lang, onOpenUpload, onSelectDefaultSurvey, onOpenMarket, inline = false }) {
  const t = translations[lang] || translations.en;

  const actions = [
    {
      title: t.actionUpload,
      desc: t.actionUploadDesc,
      icon: Camera,
      color: "from-emerald-500 to-teal-600",
      bgColor: "bg-emerald-50/60 hover:bg-emerald-50",
      borderColor: "border-emerald-200/80",
      textColor: "text-emerald-900",
      onClick: onOpenUpload,
      tag: t.tagVision || "Multimodal Vision"
    },
    {
      title: t.actionMap,
      desc: t.actionMapDesc,
      icon: Map,
      color: "from-amber-500 to-orange-600",
      bgColor: "bg-amber-50/60 hover:bg-amber-50",
      borderColor: "border-amber-200/80",
      textColor: "text-amber-900",
      onClick: () => onSelectDefaultSurvey("1342"),
      tag: t.tagMap || "Cadastral & FMB"
    },
    {
      title: t.actionMarket || "Mandi Market Rates",
      desc: t.actionMarketDesc || "Live APMC prices for Tenkasi, Kovilpatti & Tirunelveli",
      icon: TrendingUp,
      color: "from-purple-500 to-pink-600",
      bgColor: "bg-purple-50/60 hover:bg-purple-50",
      borderColor: "border-purple-200/80",
      textColor: "text-purple-900",
      onClick: onOpenMarket,
      tag: t.tagMarket || "eNAM Benchmarks"
    }
  ];

  const gridClass = "grid grid-cols-1 sm:grid-cols-3 gap-3.5";

  const containerClass = inline
    ? "w-full pt-2"
    : "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-6 sm:-mt-8 mb-10 relative z-20";

  return (
    <div className={containerClass}>
      <div className={gridClass}>
        {actions.map((act, idx) => {
          const Icon = act.icon;
          return (
            <div
              key={idx}
              onClick={act.onClick}
              className={`p-3.5 sm:p-4 rounded-2xl border ${act.borderColor} ${act.bgColor} bg-white shadow-xs hover:shadow-md transition-all duration-200 cursor-pointer flex flex-col justify-between group active:scale-[0.98]`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <div className={`w-9 h-9 sm:w-10 sm:h-10 rounded-xl bg-gradient-to-tr ${act.color} text-white flex items-center justify-center shadow-xs group-hover:scale-105 transition-transform`}>
                    <Icon className="w-4 h-4 sm:w-5 sm:h-5" />
                  </div>
                  <span className="text-[9px] sm:text-[10px] font-semibold tracking-wider uppercase px-2 py-0.5 rounded-full bg-white/80 border border-slate-200 text-slate-600 shadow-2xs">
                    {act.tag}
                  </span>
                </div>
                <h3 className={`font-bold text-xs sm:text-sm ${act.textColor} group-hover:text-emerald-700 transition-colors`}>
                  {act.title}
                </h3>
                <p className="text-[11px] text-slate-500 mt-1 line-clamp-2">
                  {act.desc}
                </p>
              </div>

              <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] font-semibold text-emerald-700">
                <span>{t.launchAction || "Launch"}</span>
                <span className="group-hover:translate-x-1 transition-transform">→</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
