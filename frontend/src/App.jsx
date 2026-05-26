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

const API_URL = "http://localhost:8000";

function App() {
  const [metrics, setMetrics] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [backups, setBackups] = useState([]);
  const [queries, setQueries] = useState([]);
  const [replication, setReplication] = useState([]);
  const [cache, setCache] = useState({});
  const [snapshots, setSnapshots] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();

    const interval = setInterval(loadData, 5000);

    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const [
        metricsRes,
        alertsRes,
        backupsRes,
        queriesRes,
        replicationRes,
        cacheRes,
        snapshotsRes
      ] = await Promise.all([
        axios.get(`${API_URL}/metrics/`),
        axios.get(`${API_URL}/alerts/`),
        axios.get(`${API_URL}/backups/`),
        axios.get(`${API_URL}/queries/`),
        axios.get(`${API_URL}/replication/`),
        axios.get(`${API_URL}/cache/summary`),
        axios.get(`${API_URL}/snapshots/`)
      ]);

      setMetrics(metricsRes.data.slice(-20));
      setAlerts(alertsRes.data);
      setBackups(backupsRes.data);
      setQueries(queriesRes.data);
      setReplication(replicationRes.data.slice(-20));
      setCache(cacheRes.data);
      setSnapshots(snapshotsRes.data);
      setLoading(false);
    } catch (error) {
      console.log("Error cargando dashboard:", error);
      setLoading(false);
    }
  };

  const alertSummary = [
    {
      name: "Alertas",
      warning: alerts.filter((a) => a.severity === "WARNING").length,
      critical: alerts.filter((a) => a.severity === "CRITICAL").length
    }
  ];

  const cacheSummary = [
    {
      name: "Redis",
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
    <main className="dashboard">
      <section className="hero">
        <div>
          <p className="eyebrow">DataOps Platform</p>
          <h1>DataOps Control Center</h1>
          <p className="subtitle">
            Monitoreo, alertas, backups, recuperación cloud y analítica en tiempo real.
          </p>
        </div>

        <div className="status-pill">
          <span></span>
          Sistema activo
        </div>
      </section>

      {loading ? (
        <div className="loading">Cargando dashboard...</div>
      ) : (
        <>
          <section className="cards">
            <Card title="Métricas" value={metrics.length} detail="Health checks activos" />
            <Card title="Alertas" value={alerts.length} detail="Eventos registrados" />
            <Card title="Backups" value={backups.length} detail="FULL / DIFF / INC" />
            <Card title="Queries" value={queries.length} detail="Análisis SQL" />
            <Card title="Replicación" value={replication.length} detail="Lag monitoreado" />
            <Card title="Redis Hit Ratio" value={`${cache.hit_ratio || 0}%`} detail={`H:${cache.hits || 0} M:${cache.misses || 0}`} />
            <Card title="Snapshots" value={snapshots.length} detail="PRE_DEPLOY / TEST / IMPORT" />
          </section>

          <section className="grid">
            <ChartCard title="CPU en tiempo real">
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={metrics}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="id" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="cpu" strokeWidth={3} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="Memoria en tiempo real">
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={metrics}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="id" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="memory" strokeWidth={3} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="Alertas por severidad">
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={alertSummary}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="warning" />
                  <Bar dataKey="critical" />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="Redis Cache">
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={cacheSummary}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="hits" />
                  <Bar dataKey="misses" />
                </BarChart>
              </ResponsiveContainer>
            </ChartCard>

            <ChartCard title="Replication Lag">
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={replication}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="id" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="replication_lag" strokeWidth={3} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </ChartCard>
          </section>

          <section className="tables">
            <TableCard title="Snapshots y SLA">
              <table>
                <thead>
                  <tr>
                    <th>Nombre</th>
                    <th>RPO</th>
                    <th>RTO</th>
                    <th>SLA</th>
                  </tr>
                </thead>
                <tbody>
                  {snapshots.map((snapshot) => (
                    <tr key={snapshot.id}>
                      <td>{snapshot.name}</td>
                      <td>{snapshot.rpo_minutes} min</td>
                      <td>{snapshot.rto_minutes} min</td>
                      <td>
                        <span className={`badge ${snapshot.sla_status === "CUMPLE" ? "ok" : "danger"}`}>
                          {snapshot.sla_status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </TableCard>

            <TableCard title="Últimas alertas">
              <table>
                <thead>
                  <tr>
                    <th>Severidad</th>
                    <th>Condición</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {latestAlerts.map((alert) => (
                    <tr key={alert.id}>
                      <td>
                        <span className={`badge ${alert.severity === "CRITICAL" ? "danger" : "warning"}`}>
                          {alert.severity}
                        </span>
                      </td>
                      <td>{alert.condition}</td>
                      <td>{alert.status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </TableCard>

            <TableCard title="Top 10 Queries lentas">
              <table>
                <thead>
                  <tr>
                    <th>Clasificación</th>
                    <th>Duración</th>
                    <th>Query</th>
                  </tr>
                </thead>
                <tbody>
                  {slowQueries.map((query) => (
                    <tr key={query.id}>
                      <td>
                        <span className={`badge ${query.classification === "CRITICAL" ? "danger" : "warning"}`}>
                          {query.classification}
                        </span>
                      </td>
                      <td>{query.duration_ms.toFixed(2)} ms</td>
                      <td className="query">{query.query_text}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </TableCard>
          </section>
        </>
      )}
    </main>
  );
}

function Card({ title, value, detail }) {
  return (
    <article className="card">
      <p>{title}</p>
      <h2>{value}</h2>
      <span>{detail}</span>
    </article>
  );
}

function ChartCard({ title, children }) {
  return (
    <article className="panel">
      <h3>{title}</h3>
      {children}
    </article>
  );
}

function TableCard({ title, children }) {
  return (
    <article className="panel table-panel">
      <h3>{title}</h3>
      {children}
    </article>
  );
}

export default App;