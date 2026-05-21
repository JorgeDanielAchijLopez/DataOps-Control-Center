import { useEffect, useState } from "react";
import axios from "axios";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar,
  ResponsiveContainer
} from "recharts";

import "./App.css";

function App() {
  const [metrics, setMetrics] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [backups, setBackups] = useState([]);
  const [queries, setQueries] = useState([]);
  const [replication, setReplication] = useState([]);
  const [cache, setCache] = useState({});
  const [snapshots, setSnapshots] = useState([]);

  useEffect(() => {
    loadData();

    const interval = setInterval(() => {
      loadData();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const metricsRes = await axios.get("http://localhost:8000/metrics/");
      const alertsRes = await axios.get("http://localhost:8000/alerts/");
      const backupsRes = await axios.get("http://localhost:8000/backups/");
      const queriesRes = await axios.get("http://localhost:8000/queries/");
      const replicationRes = await axios.get("http://localhost:8000/replication/");
      const cacheRes = await axios.get("http://localhost:8000/cache/summary");
      const snapshotsRes = await axios.get("http://localhost:8000/snapshots/");

      setMetrics(metricsRes.data.slice(-15));
      setAlerts(alertsRes.data);
      setBackups(backupsRes.data);
      setQueries(queriesRes.data);
      setReplication(replicationRes.data.slice(-15));
      setCache(cacheRes.data);
      setSnapshots(snapshotsRes.data);
    } catch (error) {
      console.log("Error cargando dashboard:", error);
    }
  };

  const alertSummary = [
    {
      name: "Alertas",
      warning: alerts.filter((a) => a.severity === "WARNING").length,
      critical: alerts.filter((a) => a.severity === "CRITICAL").length
    }
  ];

  const querySummary = [
    {
      name: "Queries",
      fast: queries.filter((q) => q.classification === "FAST").length,
      medium: queries.filter((q) => q.classification === "MEDIUM").length,
      slow: queries.filter((q) => q.classification === "SLOW").length,
      critical: queries.filter((q) => q.classification === "CRITICAL").length
    }
  ];

  const cacheSummary = [
    {
      name: "Cache",
      hits: cache.hits || 0,
      misses: cache.misses || 0
    }
  ];

  const slowQueries = queries
    .filter((q) => q.classification === "SLOW" || q.classification === "CRITICAL")
    .sort((a, b) => b.duration_ms - a.duration_ms)
    .slice(0, 10);

  const latestAlerts = alerts.slice(-8).reverse();

  return (
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h1>DataOps Control Center</h1>

      <div style={cardsContainer}>
        <div style={cardStyle}>
          <h3>Métricas</h3>
          <h2>{metrics.length}</h2>
        </div>

        <div style={cardStyle}>
          <h3>Alertas</h3>
          <h2>{alerts.length}</h2>
        </div>

        <div style={cardStyle}>
          <h3>Backups</h3>
          <h2>{backups.length}</h2>
        </div>

        <div style={cardStyle}>
          <h3>Queries</h3>
          <h2>{queries.length}</h2>
        </div>

        <div style={cardStyle}>
          <h3>Replicación</h3>
          <h2>{replication.length}</h2>
        </div>

        <div style={cardStyle}>
          <h3>Cache Hit Ratio</h3>
          <h2>{cache.hit_ratio || 0}%</h2>
          <small>H:{cache.hits || 0} | M:{cache.misses || 0}</small>
        </div>

        <div style={cardStyle}>
          <h3>Snapshots</h3>
          <h2>{snapshots.length}</h2>
        </div>
      </div>

      <div style={chartsContainer}>
        <div style={chartBox}>
          <h2>CPU en tiempo real</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={metrics}>
              <CartesianGrid />
              <XAxis dataKey="id" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="cpu" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={chartBox}>
          <h2>Memoria en tiempo real</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={metrics}>
              <CartesianGrid />
              <XAxis dataKey="id" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="memory" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={chartBox}>
          <h2>Alertas por severidad</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={alertSummary}>
              <CartesianGrid />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="warning" />
              <Bar dataKey="critical" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div style={chartBox}>
          <h2>Queries por clasificación</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={querySummary}>
              <CartesianGrid />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="fast" />
              <Bar dataKey="medium" />
              <Bar dataKey="slow" />
              <Bar dataKey="critical" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div style={chartBox}>
          <h2>Replication Lag</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={replication}>
              <CartesianGrid />
              <XAxis dataKey="id" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="replication_lag" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div style={chartBox}>
          <h2>Redis Cache</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={cacheSummary}>
              <CartesianGrid />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="hits" />
              <Bar dataKey="misses" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div style={tablesContainer}>
        <div style={tableBox}>
          <h2>Snapshots y SLA</h2>

          <table style={tableStyle}>
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Descripción</th>
                <th>RPO</th>
                <th>RTO</th>
                <th>SLA</th>
              </tr>
            </thead>

            <tbody>
              {snapshots.map((snapshot) => (
                <tr key={snapshot.id}>
                  <td>{snapshot.name}</td>
                  <td>{snapshot.description}</td>
                  <td>{snapshot.rpo_minutes} min</td>
                  <td>{snapshot.rto_minutes} min</td>
                  <td>{snapshot.sla_status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div style={tableBox}>
          <h2>Últimas alertas</h2>

          <table style={tableStyle}>
            <thead>
              <tr>
                <th>Severidad</th>
                <th>Condición</th>
                <th>Mensaje</th>
                <th>Estado</th>
              </tr>
            </thead>

            <tbody>
              {latestAlerts.map((alert) => (
                <tr key={alert.id}>
                  <td>{alert.severity}</td>
                  <td>{alert.condition}</td>
                  <td>{alert.message}</td>
                  <td>{alert.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div style={tableBox}>
          <h2>Top 10 Queries lentas</h2>

          <table style={tableStyle}>
            <thead>
              <tr>
                <th>Clasificación</th>
                <th>Duración</th>
                <th>Query</th>
                <th>Plan</th>
              </tr>
            </thead>

            <tbody>
              {slowQueries.map((query) => (
                <tr key={query.id}>
                  <td>{query.classification}</td>
                  <td>{query.duration_ms.toFixed(2)} ms</td>
                  <td>{query.query_text}</td>
                  <td>{query.execution_plan}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

const cardsContainer = {
  display: "flex",
  gap: "20px",
  marginBottom: "30px",
  flexWrap: "wrap"
};

const chartsContainer = {
  display: "flex",
  gap: "40px",
  flexWrap: "wrap"
};

const tablesContainer = {
  display: "flex",
  gap: "40px",
  flexWrap: "wrap",
  marginTop: "40px"
};

const cardStyle = {
  background: "#f3f4f6",
  padding: "20px",
  borderRadius: "12px",
  width: "180px",
  boxShadow: "0 2px 8px rgba(0,0,0,0.15)"
};

const chartBox = {
  width: "520px",
  background: "#ffffff",
  padding: "20px",
  borderRadius: "12px",
  boxShadow: "0 2px 8px rgba(0,0,0,0.15)"
};

const tableBox = {
  width: "100%",
  background: "#ffffff",
  padding: "20px",
  borderRadius: "12px",
  boxShadow: "0 2px 8px rgba(0,0,0,0.15)"
};

const tableStyle = {
  width: "100%",
  borderCollapse: "collapse"
};

export default App;