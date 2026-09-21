# Renderer boundary

The Phase 0 PPTX renderer is implemented at `apps/api/app/services/pptx_renderer.py` so the API can package it simply. It accepts only validated `PresentationIR` and returns bytes. This directory reserves the independent renderer service boundary for future web/PDF renderers without introducing a premature microservice.
