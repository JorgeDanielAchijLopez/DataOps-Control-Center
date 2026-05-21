# DataOps Control Center

Plataforma inteligente de monitoreo, análisis, recuperación y gestión de bases de datos empresariales desarrollada como proyecto final del curso. El sistema centraliza monitoreo, concurrencia, respaldo, replicación, alertas y análisis de rendimiento mediante una arquitectura distribuida basada en microservicios.

## Tecnologías utilizadas

Backend:

- Python
- FastAPI
- PostgreSQL
- Redis
- JWT
- Swagger/OpenAPI

Frontend:

- React
- Vite

Infraestructura:

- Docker
- Docker Compose

Servicios:

- Redis Cache
- Simulación de replicación
- Sistema de alertas
- Power BI

## Arquitectura

La arquitectura sigue un modelo por capas:

Presentación:
- React Dashboard

API:
- FastAPI

Persistencia:
- PostgreSQL

Servicios auxiliares:
- Redis
- Alert Engine
- Backup Service
- Replication Service

La comunicación se realiza mediante endpoints REST y documentación Swagger.

## Módulos implementados

### Módulo 1 — Registro de Motores

Permite registrar motores de base de datos simulados.

Características:

- Registro de conexiones
- Estado ACTIVE / INACTIVE
- Persistencia PostgreSQL
- Gestión centralizada

Endpoints:

```text
GET /connections
POST /connections
```

### Módulo 2 — Health Check Automático

Captura métricas periódicas mediante tareas automáticas.

Métricas:

- CPU
- Memoria
- Conexiones
- Locks
- Deadlocks
- Uso de disco

Endpoints:

```text
GET /metrics
GET /health-summary
```

### Módulo 3 — Slow Query Analyzer

Simulación y clasificación automática:

Fast:
<100 ms

Medium:
100–500 ms

Slow:
500–2000 ms

Critical:
>2000 ms

Endpoints:

```text
GET /queries
GET /queries/summary
```

### Módulo 4 — Concurrencia

Simula:

- 100 usuarios concurrentes
- operaciones mixtas
- detección automática de conflictos

Tipos:

- INSERT
- UPDATE
- DELETE
- SELECT

Endpoints:

```text
GET /transactions
GET /transactions/summary
```

### Módulo 5 — Backup Recovery

Implementa:

- FULL
- DIFF
- INC

Cadena demostrada:

```text
FULL → DIFF → INC
```

Snapshots:

- PRE_DEPLOY
- PRE_TEST
- PRE_IMPORT

Endpoints:

```text
POST /backups/run/FULL
POST /backups/run/DIFF
POST /backups/run/INC

GET /backups/

GET /snapshots
```

RPO objetivo:

```text
15 minutos
```

RTO objetivo:

```text
45 minutos
```

### Módulo 6 — Replicación Distribuida

Simulación:

Carga normal:

```text
2 segundos
```

Carga media:

```text
5 segundos
```

Carga alta:

```text
20 segundos
```

Endpoints:

```text
GET /replication
GET /replication/summary
```

### Módulo 7 — Redis Cache

Funciones:

- Cache hit
- Cache miss
- TTL
- invalidación manual
- hit ratio

Prueba:

Primera consulta:

```text
GET /cache/query/test1
```

Resultado:

```text
DATABASE ~400ms
```

Segunda:

```text
GET /cache/query/test1
```

Resultado:

```text
CACHE rápido
```

Invalidación:

```text
DELETE /cache/invalidate/test1
```

### Módulo 8 — Business Intelligence

Endpoints creados para Power BI:

```text
GET /bi/heatmap
GET /bi/top-slow-queries
GET /bi/backup-sla
GET /bi/availability
```

Dashboard:

- Heatmap
- Top queries
- SLA
- Disponibilidad global

### Módulo 9 — Motor de Alertas

Reglas:

CPU >85%

Deadlocks >3

Lag >10 segundos

Disco >90%

Conexiones > umbral

Endpoints:

```text
GET /alerts
```

Alertas registradas:

- timestamp
- severidad
- condición
- resolución

## JWT

Autenticación implementada mediante JWT.

Login:

```text
POST /auth/login
```

Credenciales:

```json
{
    "username":"admin",
    "password":"admin123"
}
```

## Business Intelligence Power BI

El dashboard ejecutivo consume:

```text
GET /bi/heatmap
GET /bi/top-slow-queries
GET /bi/backup-sla
GET /bi/availability
```

Visualizaciones:

- Heatmap actividad
- Ranking consultas
- SLA backups
- Disponibilidad global

## Análisis CAP

La arquitectura implementada prioriza:

- Disponibilidad
- Tolerancia a particiones

La consistencia se maneja como consistencia eventual debido al modelo primario-réplica.

## Estado AWS

El proyecto incluye estructura preparada para:

Amazon S3 / Azure Blob Storage

Características previstas:

- variables de entorno
- hash SHA256
- URL remota
- política de retención

La integración queda pendiente de activación de la cuenta AWS.

## Ejecución

Clonar:

```bash
git clone https://github.com/JorgeDanielAchijLopez/DataOps-Control-Center.git
```

Entrar:

```bash
cd DataOps-Control-Center
```

Ejecutar:

```bash
docker compose up --build
```

Frontend:

```text
http://localhost:5173
```

Swagger:

```text
http://localhost:8000/docs
```

Backend:

```text
http://localhost:8000
```