# Your Name — Electrical Engineering + Data Science

A standard-library booking website with SQLite for local development and optional Neon Postgres for deployment.

## Local run

```bash
python3 server.py
```

Open `http://localhost:8000`. No package installation is required for local SQLite mode.

## Neon Postgres

1. Create a Neon project and copy the pooled connection string from the Neon dashboard.
2. In the deployment environment, set `DATABASE_URL` to the pooled URL with `sslmode=require`.
3. Install the optional driver in that deployment environment:

```bash
python -m pip install "psycopg[binary]>=3.2"
```

4. Set an admin token:

```bash
ADMIN_TOKEN=use-a-long-random-secret
```

5. Start the server. Tables and seed services are created automatically.

The app uses SQLite when `DATABASE_URL` is empty and Psycopg 3 when it is set. Use `/api/health` to confirm which database is active.

## Booking operations

- `/` — public website and booking flow
- `/admin.html?token=YOUR_ADMIN_TOKEN` — payment verification dashboard
- `GET /api/services` — service catalog
- `GET /api/availability?service_id=1&date=YYYY-MM-DD` — conflict-aware slots
- `POST /api/bookings` — creates a pending bKash/Rocket booking
- `POST /api/bookings/:id/cancel` — client email-verified cancellation
- `POST /api/bookings/:id/reschedule` — client email-verified reschedule
- `/api/bookings/:id/calendar.ics` — calendar event export

Payment is currently transaction-ID based: the client selects bKash or Rocket, sends the fee to the configured merchant number, and enters the transaction ID. The admin marks payment as verified.
