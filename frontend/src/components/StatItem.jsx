import React from "react";

const formatNumber = (num) => {
  if (num === undefined || num === null) return "-";
  if (num >= 1000000) return (num / 1000000).toFixed(1) + "M";
  if (num >= 1000) return (num / 1000).toFixed(1) + "K";
  return num.toString();
};

export function StatItem({ label, value }) {
  return (
    <div className="stat-item">
      <div className="stat-value">{formatNumber(value)}</div>
      <div className="stat-label">{label}</div>
    </div>
  );
}
