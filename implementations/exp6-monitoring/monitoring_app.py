"""
Experiment 6: Monitoring & Logging
====================================
AIM: To implement logging, application monitoring, and log analysis
     using Python's logging module and monitoring libraries.

Setup:
  pip install flask prometheus-client psutil structlog colorlog

This creates:
  1. Structured application logging
  2. Prometheus metrics endpoint for monitoring
  3. Log file rotation
  4. Performance monitoring (CPU, Memory, Request time)
"""

import logging
import logging.handlers
import time
import os
import json
import psutil
from datetime import datetime
from functools import wraps
from flask import Flask, jsonify, request, g
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# ============================================================
# LOGGING SETUP
# ============================================================

def setup_logging(log_level=logging.DEBUG, log_dir="logs"):
    """Configure comprehensive application logging."""
    os.makedirs(log_dir, exist_ok=True)

    # Root logger
    logger = logging.getLogger("bookstore")
    logger.setLevel(log_level)

    # ---- Console Handler (colorized output) ----
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-8s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_format)

    # ---- File Handler (rotating logs) ----
    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_dir, "bookstore.log"),
        maxBytes=5 * 1024 * 1024,  # 5 MB per file
        backupCount=5,              # Keep 5 backup files
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        fmt="%(asctime)s [%(levelname)-8s] [%(name)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_format)

    # ---- JSON Handler (for log aggregation/ELK stack) ----
    json_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_dir, "bookstore_json.log"),
        maxBytes=10 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    json_handler.setLevel(logging.DEBUG)

    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "line": record.lineno,
            }
            if hasattr(record, 'extra'):
                log_entry.update(record.extra)
            if record.exc_info:
                log_entry["exception"] = self.formatException(record.exc_info)
            return json.dumps(log_entry)

    json_handler.setFormatter(JSONFormatter())

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(json_handler)

    return logger


# Initialize logger
logger = setup_logging()

# ============================================================
# PROMETHEUS METRICS
# ============================================================

# Request counter
REQUEST_COUNT = Counter(
    'bookstore_request_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

# Request duration
REQUEST_DURATION = Histogram(
    'bookstore_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

# Active connections
ACTIVE_CONNECTIONS = Gauge(
    'bookstore_active_connections',
    'Number of active HTTP connections'
)

# System metrics
CPU_USAGE = Gauge('bookstore_cpu_percent', 'CPU usage percent')
MEMORY_USAGE = Gauge('bookstore_memory_percent', 'Memory usage percent')

# Book-specific metrics
BOOK_SEARCH_COUNT = Counter(
    'bookstore_book_searches_total',
    'Total book searches',
    ['search_type']
)

# ============================================================
# FLASK APP
# ============================================================
app = Flask(__name__)

# In-memory book database
books = [
    {"id": 1, "title": "Clean Code", "author": "Robert C. Martin", "price": 450.0},
    {"id": 2, "title": "Python Crash Course", "author": "Eric Matthes", "price": 400.0},
]


# ============================================================
# MONITORING MIDDLEWARE
# ============================================================
def monitor_request(f):
    """Decorator to monitor every API request."""
    @wraps(f)
    def decorated(*args, **kwargs):
        start_time = time.time()
        ACTIVE_CONNECTIONS.inc()

        # Update system metrics
        CPU_USAGE.set(psutil.cpu_percent())
        MEMORY_USAGE.set(psutil.virtual_memory().percent)

        logger.info(
            f"→ REQUEST: {request.method} {request.path} | "
            f"IP: {request.remote_addr} | "
            f"User-Agent: {request.user_agent.string[:50]}"
        )

        try:
            response = f(*args, **kwargs)
            status_code = response[1] if isinstance(response, tuple) else 200

            # Record metrics
            duration = time.time() - start_time
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.path,
                status_code=status_code
            ).inc()
            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.path
            ).observe(duration)

            logger.info(
                f"← RESPONSE: {request.method} {request.path} | "
                f"Status: {status_code} | "
                f"Duration: {duration*1000:.2f}ms"
            )
            return response

        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                f"✗ ERROR: {request.method} {request.path} | "
                f"Exception: {type(e).__name__}: {str(e)} | "
                f"Duration: {duration*1000:.2f}ms",
                exc_info=True
            )
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.path,
                status_code=500
            ).inc()
            raise

        finally:
            ACTIVE_CONNECTIONS.dec()

    return decorated


# ============================================================
# ROUTES
# ============================================================
@app.route('/health')
@monitor_request
def health():
    """Health check with system metrics."""
    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent()
    disk = psutil.disk_usage('/')

    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "system": {
            "cpu_percent": cpu,
            "memory_percent": memory.percent,
            "memory_available_mb": round(memory.available / 1024 / 1024, 2),
            "disk_percent": disk.percent
        }
    }

    logger.info(f"Health check: CPU={cpu}%, Memory={memory.percent}%")
    return jsonify(health_data), 200


@app.route('/books')
@monitor_request
def get_books():
    """Get all books with logging."""
    logger.info(f"Fetching all books. Total: {len(books)}")
    return jsonify({"books": books, "total": len(books)}), 200


@app.route('/books/search')
@monitor_request
def search_books():
    """Search books with metric tracking."""
    query = request.args.get('q', '').strip()

    if not query:
        logger.warning("Empty search query received")
        BOOK_SEARCH_COUNT.labels(search_type='empty').inc()
        return jsonify({"results": [], "warning": "Empty search query"}), 200

    BOOK_SEARCH_COUNT.labels(search_type='title').inc()
    logger.info(f"Searching books with query: '{query}'")

    results = [b for b in books if query.lower() in b['title'].lower()]
    logger.info(f"Search '{query}' returned {len(results)} results")

    return jsonify({"query": query, "results": results, "total": len(results)}), 200


@app.route('/books', methods=['POST'])
@monitor_request
def add_book():
    """Add book with validation logging."""
    data = request.get_json()
    logger.debug(f"Add book request data: {data}")

    if not data or 'title' not in data:
        logger.warning(f"Invalid add book request: missing title. Data: {data}")
        return jsonify({"error": "title is required"}), 400

    new_book = {
        "id": len(books) + 1,
        "title": data['title'],
        "author": data.get('author', 'Unknown'),
        "price": float(data.get('price', 0))
    }
    books.append(new_book)
    logger.info(f"New book added: '{new_book['title']}' (ID: {new_book['id']})")

    return jsonify({"message": "Book added", "book": new_book}), 201


@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint."""
    logger.debug("Prometheus metrics scraped")
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}


@app.route('/logs')
def get_recent_logs():
    """Read and return recent log entries."""
    try:
        with open("logs/bookstore.log", "r") as f:
            lines = f.readlines()[-50:]  # Last 50 lines
        return jsonify({"logs": lines, "count": len(lines)}), 200
    except FileNotFoundError:
        return jsonify({"logs": [], "message": "Log file not found yet"}), 200


# ============================================================
# STARTUP LOGGING
# ============================================================
if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("  Online Book Store - Monitoring & Logging Demo")
    logger.info("=" * 60)
    logger.info("Starting Flask application...")
    logger.info(f"Python PID: {os.getpid()}")
    logger.info(f"Log files: logs/bookstore.log, logs/bookstore_json.log")
    logger.info(f"Metrics endpoint: http://localhost:5001/metrics")
    logger.info(f"Health endpoint: http://localhost:5001/health")

    app.run(host='0.0.0.0', port=5001, debug=False)
