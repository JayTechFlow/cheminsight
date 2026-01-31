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

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const formatIndianDate = (dateStr) => {
    return new Date(dateStr).toLocaleString("en-IN", {
      dateStyle: "medium",
      timeStyle: "short",
    });
  };

  const fetchHistory = async () => {
    const res = await axios.get("http://127.0.0.1:8000/api/history/");
    setHistory(res.data);
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please select a CSV file");

    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(
      "http://127.0.0.1:8000/api/upload/",
      formData
    );

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
            "#0891b2",
            "#dc2626",
          ],
        },
      ],
    };

  return (
    <div className="page">
      <div className="container">
        <div className="header">
          <h1>ChemInsight</h1>
          <p>Chemical Equipment Analytics Tool</p>
        </div>

        {/* Upload */}
        <div className="card upload">
          <h3>Upload Equipment CSV</h3>
          <form onSubmit={handleSubmit}>
            <div className="upload-row">
              <input type="file" accept=".csv" onChange={handleFileChange} />
              <button type="submit">Upload</button>
            </div>
          </form>
        </div>

        {/* Summary */}
        {result && (
          <div className="card summary">
            <h3>Summary</h3>

            <div className="summary-grid">
              <div className="summary-item">
                Total Equipment: <span>{result.total_equipment}</span>
              </div>
              <div className="summary-item">
                Avg Flowrate: <span>{Number(result.avg_flowrate).toFixed(2)}</span>
              </div>
              <div className="summary-item">
                Avg Pressure: <span>{Number(result.avg_pressure).toFixed(2)}</span>
              </div>
              <div className="summary-item">
                Avg Temperature: <span>{Number(result.avg_temperature).toFixed(2)}</span>
              </div>
            </div>

            <h4>Equipment Distribution</h4>
            <ul>
              {Object.entries(result.type_distribution).map(([t, c]) => (
                <li key={t}>{t}: {c}</li>
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
              <li key={h.id} onClick={() => setResult(h)}>
                ▶ <b>{h.file_name}</b> <br />
                <small>{formatIndianDate(h.uploaded_at)}</small>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;
