# Frontend Technical Assessment — Completed

## 📋 Overview
This repository contains a small React frontend (node-based pipeline UI) and a FastAPI backend. The project was enhanced to implement the four assessment parts:

- **Part 1 — Node Abstraction:** Created a reusable `BaseNode` and refactored existing nodes to use it. Added five demonstration nodes to show how easy it is to create new nodes.
- **Part 2 — Styling & Themes:** Implemented a consistent visual style, interactive node behaviours, and **Light / Dark** themes with a toolbar switcher and keyboard shortcut.
- **Part 3 — Text Node Logic:** Enhanced the Text node with auto-resizing textarea and dynamic variable detection (`{{var}}`) that creates left-side Handles for each variable.
- **Part 4 — Backend Integration:** Integrated frontend `Submit` to POST nodes/edges to the backend endpoint `/pipelines/parse` which returns node/edge counts and whether the pipeline is a DAG.

---

## 🔧 What's included / Key files
- Frontend (React): `frontend/`
  - `src/nodes/BaseNode.js` — central node abstraction
  - `src/nodes/*.js` — node implementations (refactored to use `BaseNode`)
    - `textNode.js` — auto-resize, variable parsing, dynamic inputs
    - `constantNode.js`, `addNode.js`, `multiplyNode.js`, `transformNode.js`, `loggerNode.js` — demo nodes
  - `src/nodes/nodes.css` — node styling + interactive states
  - `src/index.css` — design tokens + theme variables (Light/Dark)
  - `src/toolbar.js` + `src/toolbar.css` — toolbar and ThemeSwitcher
  - `src/submit.js` — sends pipeline to backend and shows results
  - `src/App.js` — global keyboard shortcuts (Ctrl/Cmd+Enter to Submit, Ctrl/Cmd+Shift+L to toggle theme)
  - `src/store.js` — Zustand store for nodes/edges and update helpers

- Backend (FastAPI): `backend/main.py`
  - `POST /pipelines/parse` — accepts `nodes` and `edges` and returns:
    ```json
    {
      "num_nodes": int,
      "num_edges": int,
      "is_dag": bool,
      "topological_order": [ ... ]
    }
    ```
  - CORS enabled for local dev (`http://localhost:3000`).

---

## ▶️ How to run locally
1. **Backend**
   - Create a Python environment and install dependencies (FastAPI, Uvicorn):
     ```bash
     cd backend
     pip install -r requirements.txt  # if you have one, or pip install fastapi uvicorn
     uvicorn main:app --reload
     ```
   - By default server will run on `http://127.0.0.1:8000`.

2. **Frontend**
   - Install and run:
     ```bash
     cd frontend
     npm install
     npm start
     ```
   - The app will run on `http://localhost:3000` by default.

---

## ✅ How to test implemented features
- **Create a pipeline:** Drag nodes from the toolbar into the canvas and connect handles.
- **Text node variables:** Add a `Text` node and type `Hello {{name}}, ID {{id}}`. You should see two input handles (left) for `name` and `id` and the text area will auto-resize.
- **Submit & Parse:** Click the **Submit** button (or press `Ctrl/Cmd + Enter`) — an alert will show `num_nodes`, `num_edges`, and whether the pipeline is a DAG. The response detail is also shown below the button.
- **Themes & shortcuts:** Switch Light/Dark from the toolbar or press `Ctrl/Cmd + Shift + L` to toggle theme (persisted in localStorage).

---

## ⚠️ Notes & Implementation Details
- Variable parsing in `TextNode` accepts only valid JavaScript identifiers (regex) and supports comma-separated lists inside braces e.g. `{{ a, b }}`.
- The backend performs a basic DAG check (Kahn's algorithm) and returns a topological order when acyclic.
- CORS is enabled for `localhost:3000` to support frontend dev server.

---

