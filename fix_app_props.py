import sys

filepath = r"d:\NETRA\SIH2026\backend\src\main\resources\application.properties"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "${DB_PASSWORD:Yash@123}",
    "${DB_PASSWORD:postgres}"
)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
