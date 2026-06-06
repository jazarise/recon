# Dashboard Design

The ReconX Dashboard is built on **FastAPI + Jinja2 + HTMX**.
- **Server-Side Rendering:** Pages are served entirely from Python to eliminate NPM/Node dependencies.
- **HTMX:** Used for SPA-like transitions (`hx-get`, `hx-target`) and WebSocket communication (`hx-ext="ws"`).
- **CSS Architecture:** Zero-dependency modern CSS using CSS Variables for a seamless dark-mode operator experience.
