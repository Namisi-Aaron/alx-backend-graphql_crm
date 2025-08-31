# CRM Project - Celery + Redis Setup

This guide walks you through:
- setting up Redis,
- running Django migrations,
- and configuring celery_beat to generate scheduled CRM reports.

---

## 1. Install Redis and Dependencies

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install redis-server -y
````

### Windows

Download Redis from the official [Redis for Windows repository](https://github.com/microsoftarchive/redis/releases) and follow the installation instructions.

---

## 2. Start Redis

Check that Redis is running:

```bash
redis-cli ping
```

Expected output:

```
PONG
```

---

## 3. Install Python Dependencies

Make sure you are in your virtual environment, then install the required packages:

```bash
pip install -r requirements.txt
```

---

## 4. Run Database Migrations

Apply migrations to set up your database schema:

```bash
python manage.py migrate
```

---

## 5. Start Celery Worker

In one terminal window, start the Celery worker:

```bash
celery -A crm worker -l info
```

---

## 6. Start Celery Beat

In another terminal window, start Celery Beat:

```bash
celery -A crm beat -l info
```

This will ensure scheduled tasks are executed.

---

## 7. Verify Logs

The scheduled CRM report task writes logs to:

```
/tmp/crm_report_log.txt
```

Check the log contents:

```bash
cat /tmp/crm_report_log.txt
```

You should see entries in the format:

```
[YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue]
```

---

## 8. Troubleshooting

* Ensure Redis is running: `redis-cli ping`
* Restart Celery workers after making code changes.
* Check Celery logs for errors when tasks don’t run as expected.
