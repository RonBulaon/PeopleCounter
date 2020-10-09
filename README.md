# PeopleCounter

## Background and Motivation:

In response to social distancing measures during COVID-19 pandemic, it has been imposed to limit the number of people in almost every location and educational institutions are not exempted to it. Hence the idea of counting the actual number of people inside the building became a requirement.

On each of library entrances (where I currently work), there are counters at the gate that logs each entry and exits. From these logs, reports are generated on a regular basis (monthly). However, this solution does not provide a live counter that can be viewed and monitored on a near real-time basis.

## How it works:

Re-configurations are made to the entrances’ people counters to send update to a server every few seconds. From the server, the information is parsed, and calculations are made for the occupancy count. The information is then displayed in a browser that refreshes every few seconds as shown below: 

Fig 1: Used as entrance display


Fig 2: Backend Display that has more details.

Historical data are then saved on Database and displayed using Dash by Plotly module. Using heatmap chart on a daily and hourly basis we’ll be able to see the occupancy trends across several days.

<p align="center">
  <img width="460" height="300" src="dashboard.gif">
  Fig 3: Heatmap 
</p>

![](dashboard.gif)




Live occupancy counter with dashboard for previous data.


