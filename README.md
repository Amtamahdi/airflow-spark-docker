# Data Engineering Platform

A comprehensive data engineering platform combining Apache Airflow, Apache Spark, and Jupyter Lab in a Docker environment.

This project is a rework of [airflow-spark](https://github.com/cordon-thiago/airflow-spark) by [@cordon-thiago](https://github.com/cordon-thiago), with updates and improvements.

## 🚀 Features

- **Apache Airflow** for workflow orchestration
- **Apache Spark** for distributed data processing
- **Jupyter Lab** for interactive development
- **PostgreSQL** for metadata storage
- Scalable Spark workers
- Persistent storage volumes
- Secure configuration

## 🏗 Architecture

```
┌─────────────────┐     ┌─────────────────┐      ┌──────────────────┐
│  Airflow UI     │     │Airflow Scheduler│      │   Spark Master   │
│    :8081        │────▶│                 │────▶│      :8080       │
└─────────────────┘     └─────────────────┘      └──────────┬───────┘
         │                       │                          │
         │                       │               ┌──────────┴───────┐
         │                       │               │   Spark Workers  │
         │                       │               │    (1..n)        │
         │                       │               └──────────────────┘
         │                       │                          ▲
         │                       │                          │
         ▼                       ▼                          │
┌─────────────────┐     ┌───────────────┐          ┌─────────┴───────┐
│   PostgreSQL    │     │ Jupyter Lab   │          │                 │
│     :5432       │     │    :8888      │───────▶ │  Spark Session  │
└─────────────────┘     └───────────────┘          └─────────────────┘
```

## 🔧 Prerequisites

- Docker Engine 20.10.0+
- Docker Compose v2.0.0+
- 8GB RAM minimum
- 10GB disk space minimum

## 📦 Installation

1. Clone the repository
```bash
git clone https://github.com/Amtamahdi/airflow-spark-docker.git
cd airflow-spark-docker
```

2. Generate Fernet key for Airflow
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

3. Copy the generated key to `.env` file
```bash
AIRFLOW__CORE__FERNET_KEY=your_generated_key
```

## 🚀 Quick Start

1. Build and start the services with 3 Spark workers:
```bash
docker-compose up --scale spark-worker=3 -d
```

2. Get Jupyter access token:
```bash
docker-compose logs jupyter
```
Look for URL with token: `http://localhost:8888/lab?token=<your_token>`

3. Access the services:
   - Airflow: http://localhost:8081 (admin/admin)
   - Spark Master: http://localhost:8080
   - Jupyter Lab: http://localhost:8888

## 📁 Project Structure

```
.
├── config/                  # Configuration files
├── dags/                   # Airflow DAG files
│   ├── spark_test.py       # Example Spark job
│   └── test_spark_dag.py   # Example Airflow DAG
├── docker/                 # Dockerfile definitions
│   ├── Dockerfile.airflow
│   ├── Dockerfile.jupyter
│   ├── Dockerfile.postgres
│   └── Dockerfile.spark
├── logs/                   # Log files
├── notebooks/              # Jupyter notebooks
├── plugins/               # Airflow plugins
├── scripts/               # Utility scripts
├── spark-apps/           # Spark applications
├── .env                  # Environment variables
└── docker-compose.yml    # Service definitions
```

## 🛠 Configuration

### Environment Variables
Key environment variables in `.env`:
```
# Database
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
POSTGRES_PORT=5432

# Airflow
AIRFLOW_UID=50000
AIRFLOW_GID=0
AIRFLOW_WEBSERVER_PORT=8081
AIRFLOW_BASE_URL=http://localhost:8081
AIRFLOW__CORE__FERNET_KEY=8sl5Z7QWQAoWXqsXbB4rWogfz4xJ0y82bPunpG98E38=

# Spark
SPARK_MASTER_PORT=7077
SPARK_MASTER_WEBUI_PORT=8080
SPARK_WORKER_MEMORY=1G
SPARK_WORKER_CORES=1

# Jupyter
JUPYTER_PORT=8888
JUPYTER_ENABLE_LAB=yes
```

### PostgreSQL Configuration
The PostgreSQL service is configured with optimized settings in `postgres/postgresql.conf`:
```ini
listen_addresses = '*'
max_connections = 100
shared_buffers = 128MB
effective_cache_size = 384MB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.7
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
effective_io_concurrency = 200
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB
```

### Spark Configuration
Default Spark settings in `spark-defaults.conf`:
```properties
spark.driver.memory 1g
spark.executor.memory 1g
spark.sql.warehouse.dir /opt/spark/work-dir
spark.serializer org.apache.spark.serializer.KryoSerializer
```

## 🚀 Usage

### Scaling Spark Workers
To adjust the number of Spark workers:
```bash
docker-compose up --scale spark-worker=<number_of_workers> -d
```

### Complete Cleanup
To remove all containers, images, and volumes:
```bash
docker compose down && docker rmi $(docker images -q) --force && docker system prune -a --volumes --force
```

## 🐛 Troubleshooting

Common issues and solutions:

1. **Spark workers not connecting:**
   - Check network connectivity
   - Verify Spark master URL
   - Ensure consistent Python versions (Python 3.11 is used across all services)

2. **Airflow-Spark connection issues:**
   - Verify Spark connection configuration
   - Check Airflow logs
   - Ensure correct permissions

3. **Jupyter connectivity issues:**
   - Check Jupyter logs for the token: `docker-compose logs jupyter`
   - Verify port mapping
   - Ensure no port conflicts

4. **PostgreSQL connection issues:**
   - Verify PostgreSQL service is healthy
   - Check environment variables
   - Ensure database initialization completed successfully
