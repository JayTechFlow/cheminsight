import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);

  const API_BASE = "http://127.0.0.1:8000/api";

  const formatIndianDate = (dateStr) => {
    return new Date(dateStr).toLocaleString("en-IN", {
      dateStyle: "medium",
      timeStyle: "short",
    });
  };

  const fetchHistory = async () => {
    const res = await axios.get(`${API_BASE}/history/`);
    setHistory(res.data);
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(`${API_BASE}/upload/`, formData);
    setResult(res.data);
    fetchHistory();
  };

  const chartData =
    result && {
      labels: Object.keys(result.type_distribution),
      datasets: [
        {
          label: "Equipment Count",
          data: Object.values(result.type_distribution),
          backgroundColor: [
            "#2563eb",
            "#16a34a",
            "#f97316",
            "#7c3aed",
            "#dc2626",
            "#0891b2",
          ],
        },
      ],
    };

  return (
    <div className="page">
      <div className="container">
        {/* Header */}
        <div className="header">
          <h1>ChemInsight</h1>
          <p>Chemical Equipment Analytics Tool</p>
        </div>

        {/* Upload */}
        <div className="card upload">
          <h3>Upload Equipment CSV</h3>
          <form onSubmit={handleSubmit}>
            <div className="upload-row">
              <input
                type="file"
                accept=".csv"
                onChange={(e) => setFile(e.target.files[0])}
              />
              <button type="submit">Upload</button>
            </div>
          </form>
        </div>

        {/* Summary */}
        {result && (
          <div className="card summary">
            <h3>Summary</h3>

            <div className="summary-grid">
              <div>Total Equipment: <b>{result.total_equipment}</b></div>
              <div>Avg Flowrate: <b>{result.avg_flowrate.toFixed(2)}</b></div>
              <div>Avg Pressure: <b>{result.avg_pressure.toFixed(2)}</b></div>
              <div>Avg Temperature: <b>{result.avg_temperature.toFixed(2)}</b></div>
            </div>

            <h4>Equipment Distribution</h4>
            <ul>
              {Object.entries(result.type_distribution).map(([k, v]) => (
                <li key={k}>{k}: {v}</li>
              ))}
            </ul>

            <div className="chart">
              <Bar data={chartData} />
            </div>
          </div>
        )}

        {/* History */}
        <div className="card">
          <h3>Upload History (Last 5)</h3>

          <ul className="history">
            {history.map((h) => (
              <li key={h.id}>
                <div
                  className="history-file"
                  onClick={() =>
                    setResult({
                      total_equipment: h.total_equipment,
                      avg_flowrate: h.avg_flowrate,
                      avg_pressure: h.avg_pressure,
                      avg_temperature: h.avg_temperature,
                      type_distribution: h.type_distribution,
                    })
                  }
                >
                  ▶ {h.file_name}
                </div>

                <small>{formatIndianDate(h.uploaded_at)}</small>

                <div className="history-actions">
                  <button
  onClick={() =>
    window.open(
      `http://127.0.0.1:8000/api/report/pdf/${h.id}/`,
      "_blank"
    )
  }
>
  Report Download
</button>

                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;
