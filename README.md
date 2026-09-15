# VoxMinds — SIH 2026

**Your Voice. Your Skills. Your Livelihood.**

VoxMinds is a multilingual, voice-first livelihood decision-support prototype for **SIH26097**, designed around PM-AJAY/GIA use cases. It converts a beneficiary's spoken profile into structured skills, ranks NSQF-aligned demonstration pathways, explains the ranking, identifies competency gaps and builds a livelihood roadmap.

## Architecture

React/Vite → FastAPI → SQLAlchemy/SQLite → profile extraction → skill normalization → competency mapping → pathway ranking → skill gap → roadmap → programme analytics.

## Features

- English/Hindi/Gujarati voice assessment prototype
- Adaptive interview
- Beneficiary persistence
- Skill normalization and competency mapping
- Explainable multi-factor pathway ranking
- Skill-gap analysis
- Training pathway UI
- Personalized livelihood roadmap
- Local opportunity intelligence
- Demand vs training-capacity dashboard
- Outcome tracking
- WhatsApp/IVR adapter-ready status endpoint
- Docker configuration

## Important data note

The included NSQF/job-role and opportunity records are **synthetic demonstration data** and are not official government data. Replace them with verified authorized sources before production or final claims.

## Run locally

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed_nsqf
uvicorn app.main:app --reload
```

Swagger: http://127.0.0.1:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## Docker

```bash
docker compose up --build
```

## Demo flow

1. Open Voice assessment.
2. Choose English, Hindi or Gujarati.
3. Speak answers in Chrome.
4. Save the generated profile.
5. Review AI pathways.
6. Open a roadmap and skill gap.
7. Select a training pathway.
8. Open the programme dashboard.

## Production next steps

- Replace synthetic NSQF/opportunity data with verified authorized sources.
- Use production Indian-language ASR/TTS rather than browser speech recognition.
- Move SQLite to PostgreSQL and add migrations.
- Add authentication, RBAC, consent and audit logging.
- Connect approved WhatsApp and IVR providers.
- Add automated tests and deployment monitoring.

## Authentication & role-based access

The application now starts at a login page. Beneficiaries are sent to their own personal dashboard; administrators are sent to a separate admin workspace.

Demo accounts:
- Beneficiary: `user@voxminds.in` / `user123`
- Admin: `admin@voxminds.in` / `admin123`

Before first run, seed the authentication accounts:
```bash
python -m app.seed_auth
```
For Docker, `docker compose up --build` seeds them automatically.

This is a prototype authentication layer. For production, replace demo credentials and add HTTPS, secure secret management, refresh tokens/session revocation, MFA where appropriate, consent/audit logging and a production identity provider.

## Security architecture
- JWT access tokens are short-lived (15 minutes by default).
- Refresh tokens are JWTs stored in an HttpOnly cookie and tracked server-side by JTI, allowing revocation on logout and refresh-token rotation.
- Passwords use Argon2 via `pwdlib` rather than reversible storage.
- Frontend stores only the short-lived access token in `sessionStorage`; it does not persist refresh tokens in JavaScript storage.
- Axios automatically refreshes an expired access token once and retries the request.
- `/api/auth/me` validates the current session on application startup.
- Admin APIs enforce the `admin` role on the server; UI route protection is not treated as a security boundary.
- Beneficiary self-service endpoints resolve the beneficiary from the authenticated user instead of trusting a client-supplied beneficiary ID.
- In production set a strong random `VOXMINDS_JWT_SECRET`, use HTTPS, set the refresh cookie `Secure`, use PostgreSQL, add migrations, rate limiting, audit logs, CSRF strategy appropriate to deployment, and replace demo seed accounts/data.

### Local development
The development startup automatically creates/refreshes the two demo accounts when `VOXMINDS_ENV=development` (default). You normally only need:

```powershell
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload
```

Demo accounts:
- Beneficiary: `user@voxminds.in` / `user123`
- Admin: `admin@voxminds.in` / `admin123`

Change or remove these accounts before any public deployment.
