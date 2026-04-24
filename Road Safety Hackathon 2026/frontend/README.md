# RoadSoS Frontend

This directory contains the React + Vite Progressive Web App (PWA) for the RoadSoS project.

## Features
- **Glassmorphism UI**: A stunning, premium dark-mode interface built with raw Vanilla CSS.
- **Progressive Web App (PWA)**: Configured using `vite-plugin-pwa` to cache resources for offline availability, fulfilling the critical "low-network conditions" hackathon requirement.
- **Real-time API integration**: Connected directly to the Python FastAPI backend to fetch emergency services based on natural language intent.

## Commands
- `npm install --legacy-peer-deps`: Install dependencies (Required to bypass Vite 8 peer dependency conflicts)
- `npm run dev`: Start the development server
- `npm run build`: Build the PWA for production
- `npm run preview`: Preview the production build locally
