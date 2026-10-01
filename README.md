<h1 align="center">NETRA 👁️</h1>
<p align="center"><b>National Evidence Tracking & Retrieval Architecture</b></p>
<p align="center"><i>SIH 2026 Submission — Unified AI Intelligence Platform for Law Enforcement</i></p>

> **🚨 SIMULATION ENVIRONMENT — FICTIONAL DATA — NO LIVE AGENCY INTEGRATION**  
> *This repository contains a prototype built for the Smart India Hackathon. All cases, names, and networks are procedurally generated mock data for demonstration purposes.*

---

## 📖 The Problem: Information Silos in Law Enforcement

Modern criminal networks, financial frauds, and terror operations cross state and agency boundaries. However, law enforcement agencies frequently operate in data silos. 

When investigators rely on fragmented databases, critical connections—such as shared phone numbers, overlapping financial transactions, or common associates—are missed or delayed. The lack of real-time knowledge synthesis drastically slows down time-sensitive investigations.

## 🚀 The Solution: NETRA

**NETRA** solves this by acting as an **AI-driven Unified Knowledge Graph**. 

Instead of treating case files as static documents, NETRA ingests multimodal evidence and automatically maps semantic relationships into a central graph database (Apache AGE). It equips investigators with **Multi-Agent AI** that can autonomously traverse suspect networks, generate behavioral profiles, and answer complex investigative queries in natural language.

---

## 📸 System Walkthrough

### 1. Unified Investigator Dashboard
NETRA provides a centralized, React-based dashboard where officers can track active cases, view recent intelligence alerts, and collaborate across agency boundaries with strict Role-Based Access Control (RBAC).

![Dashboard](images/Screenshot%202026-10-01%20203253.png)

### 2. AI-Assisted Investigation Thread (Multi-Agent Workflow)
Using a LangGraph-powered Multi-Agent architecture, investigators can chat directly with the case file. The AI agent translates natural language into secure graph queries, analyzes the evidence, and generates actionable criminal profiles.

![AI Investigation](images/Screenshot%202026-10-01%20203309.png)

### 3. Dynamic Network & Graph Visualization
The core of NETRA is its knowledge graph. Investigators can visually explore relationships (e.g., "FUNDS", "CALLS", "ASSOCIATED_WITH") to uncover hidden rings, shell companies, and the hierarchy of organized crime syndicates.

![Graph Explorer](images/Screenshot%202026-10-01%20203320.png)

---

## 🛠️ Product Requirements & Features (PRD Core)

1. **Intelligent Ingestion Engine:** Parses unstructured FIRs, CDRs (Call Detail Records), and financial logs into a structured canonical model.
2. **Knowledge Graph (Apache AGE):** Maps N-degree relationships automatically. If Suspect A in Delhi shares a bank account with Suspect B in Mumbai, the graph links them instantly.
3. **Autonomous AI Agents:** Python/FastAPI microservice utilizing LangGraph to reason through evidence, query the graph safely, and prevent LLM hallucinations.
4. **Strict Data Sovereignty (RBAC):** Spring Boot security layer ensures officers only see the intelligence their clearance level permits.
5. **Generative Criminal Profiling:** AI-driven synthesis of suspect behaviors, flight risks, and operational signatures based on historical graph data.

---

## 🏗️ Architecture & Tech Stack

NETRA uses a decoupled, microservice-inspired architecture to ensure scalability and separation of concerns.

- **Frontend (`/frontend`):** React 18, Vite, TypeScript, Tailwind CSS, i18next (Multi-language).
- **Backend API (`/backend`):** Java 17, Spring Boot, Spring Security (JWT), Maven.
- **AI Service (`/ai-service`):** Python 3.12, FastAPI, LangGraph, Llama.cpp (Local LLM), Uvicorn.
- **Database:** PostgreSQL with **Apache AGE** (Graph extension).

---

## ⚙️ One-Go Installation (For Evaluators)

We have provided dynamic batch scripts to launch the entire stack seamlessly. 

### Prerequisites
- Node.js (v18+)
- Java 17 & Maven
- Python 3.12
- PostgreSQL (with Apache AGE extension running on port `5433`)
- WSL (Windows Subsystem for Linux) for the local LLM server.

### Startup
1. Open `start-netra.bat` in a text editor.
2. Update the **CONFIGURATION** block at the top with the path to your local `llama-server` and `.gguf` model.
3. Double click `start-netra.bat`. 

This script will automatically start:
- The Local AI Inference Server
- The Python AI Microservice (Port 8000)
- The Spring Boot Gateway (Port 8080)
- The React Frontend (Port 5173)

To safely terminate all services, run `stop-netra.bat`.

---

## 🤝 SIH 2026
Built for the Smart India Hackathon.
