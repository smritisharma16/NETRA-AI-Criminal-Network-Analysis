import sys

filepath = r"d:\NETRA\SIH2026\ai-service\app\agent\workflow.py"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    'DB_URI = "postgresql://postgres:Yash%40123@localhost:5433/postgres"',
    'import os\nDB_URI = f"postgresql://{os.getenv(\'POSTGRES_USER\', \'postgres\')}:{os.getenv(\'POSTGRES_PASSWORD\', \'postgres\')}@{os.getenv(\'POSTGRES_HOST\', \'127.0.0.1\')}:{os.getenv(\'POSTGRES_PORT\', \'5433\')}/{os.getenv(\'POSTGRES_DB\', \'postgres\')}"'
)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
