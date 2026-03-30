# SUSi

## About

The Brazilian public health system (SUS) serves millions of people, but is often plagued by long and unpredictable queues. Patients can wait for hours or even days for appointments and procedures, with little to no information about their position in the queue or estimated waiting time. This lack of transparency generates anxiety, frustration and can even lead to patients missing their turn.

SUSi is an open-source project that aims to solve this problem by providing a virtual queue management system. With out platform, patients can track their position in the queue in real-time, receive an estimate of the waiting time and be notified when their turn is approaching. This brings more transparency, efficiency and a better experience for everyone involved.

## Features

- Real-Time Queue Tracking: Patients can see their position in the queue at any time.
- Waiting Time Estimation: The system provides an estimate of the waiting time based on the average service time and the number of people in front.
- Notifications: Patients receive notifications when their turn is approaching, so they don't have to wait at the health unit.
- Multi-Platform Access: The platform can be accessed from any device with an internet connection, inclusing smartphones, tablets and computers.

## Stack

| Technology | Role | Rationale |
| :--- | :--- | :--- |
| React | Front-End | For building a fast, responsive and modern user interface. |
| Node.js | Back-End | For creating a scalable and efficient RESTful API. |
| PostgreSQL | Database | A robust and reliable open-source relational database. |
| Docker | Containerization | To ensure a consistent development and production environment. |

## Architecture

The system is based on a microservices architecture. The front-end is a single-page application (SPA) built with React that communicates with the back-end via a RESTful API. The back-end is composed of multiple microservices, each responsible for a specific domain. The services are containerized with Docker and can be orchestrated with a tool like Kubernetes.