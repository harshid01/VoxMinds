# VoxMinds Architecture

## Decision-support principle
The LLM/voice layer extracts structured facts. Deterministic validation, normalized skills, NSQF records, eligibility rules and a transparent scoring layer produce recommendations. The language model should not independently invent a qualification or guarantee employment.

## Data flow
Voice → transcript → profile extraction → normalization → competency set → eligible roles → local opportunity signal → suitability score → explainability → skill gap → roadmap → outcomes.

## Low-tech channels
The backend exposes channel-status and adapter-ready boundaries. WhatsApp/IVR credentials are intentionally not hard-coded.
