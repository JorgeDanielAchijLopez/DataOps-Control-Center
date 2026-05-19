import { useEffect, useState } from "react";
import axios from "axios";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

import "./App.css";

function App() {

  const [metrics,setMetrics]=useState([])
  const [alerts,setAlerts]=useState([])
  const [backups,setBackups]=useState([])

  useEffect(()=>{

      loadData()

      const interval=setInterval(
        loadData,
        5000
      )

      return()=>clearInterval(
        interval
      )

  },[])


const loadData=async()=>{

try{

const metricsRes=
await axios.get(
"http://localhost:8000/metrics/"
)

const alertsRes=
await axios.get(
"http://localhost:8000/alerts/"
)

const backupsRes=
await axios.get(
"http://localhost:8000/backups/"
)

setMetrics(
metricsRes.data.slice(-15)
)

setAlerts(
alertsRes.data
)

setBackups(
backupsRes.data
)

}

catch(error){

console.log(error)

}

}


return(

<div
style={{
padding:"30px",
fontFamily:"Arial"
}}
>

<h1>
DataOps Control Center
</h1>


<div
style={{
display:"flex",
gap:"20px",
marginBottom:"30px"
}}
>

<div style={cardStyle}>

<h3>
Métricas
</h3>

<h2>
{metrics.length}
</h2>

</div>


<div style={cardStyle}>

<h3>
Alertas
</h3>

<h2>
{alerts.length}
</h2>

</div>


<div style={cardStyle}>

<h3>
Backups
</h3>

<h2>
{backups.length}
</h2>

</div>

</div>



<div
style={{
width:"100%",
height:"400px"
}}
>

<h2>
CPU en tiempo real
</h2>

<ResponsiveContainer>

<LineChart
data={metrics}
>

<CartesianGrid/>

<XAxis
dataKey="id"
/>

<YAxis/>

<Tooltip/>

<Line
type="monotone"
dataKey="cpu"
/>

</LineChart>

</ResponsiveContainer>

</div>

</div>

)

}


const cardStyle={

background:"#f4f4f4",
padding:"20px",
borderRadius:"10px",
width:"200px"

}


export default App