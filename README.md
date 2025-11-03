# Click Detection App

A simple human-vs-bot click behaviour collection prototype featuring a Flask API backend and a React (Vite) frontend. The frontend renders a TikTok-style full-screen canvas that logs every click to the backend, where the events are persisted to SQLite.

## Project structure

```
click-detection-app/
├── backend/
│   ├── app.py             # Flask API server that records click events in SQLite
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── index.html         # Vite entry point
│   ├── package.json       # React + Axios dependencies
│   ├── src/App.jsx        # Full-screen click interface
│   ├── src/App.css        # Heart animation styles
│   └── src/main.jsx       # React bootstrap
└── README.md
```

## Getting started

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

The backend listens on `http://localhost:5000` and exposes two endpoints:

- `POST /api/click` — accepts `{ x, y, t }`, appends a server timestamp, and persists the event
- `GET /api/stats` — returns the total number of events and the full event list

Events are stored in `backend/clicks.db`. Feel free to inspect it with any SQLite client while the server is running.

### Frontend

```bash
cd frontend
npm install
# Optional: copy env template and adjust the backend URL if needed
cp .env.example .env
npm run dev
```

The Vite development server runs on `http://localhost:5173`. Visiting the page displays a black full-screen canvas. Each click sends the click coordinates and timestamp to the backend and renders a temporary ❤️ animation. Keyboard users can press <kbd>Enter</kbd> or <kbd>Space</kbd> while the canvas is focused to trigger the same interaction.

The frontend reads `VITE_API_BASE_URL` from `.env` (defaulting to `http://localhost:5000`) to know where to send API requests. Adjust the value if your backend runs on a different host or port.

## Next steps

- Analyse click patterns (timing, movement, entropy)
- Prototype a simple ML model to classify human vs. bot behaviour
- Explore deployment (Flask on Render/Railway, React on Vercel)
