import re

with open(r"d:\NETRA\SIH2026\ai-service\app\agent\prompts.py", "r", encoding="utf-8") as f:
    content = f.read()

rule_add = """4. Keep answers concise, readable, and focused on the facts. Use short sections and bullet points.
5. CLICKABLE REFERENCES: If you mention a specific entity that has an ID (e.g., E-123), you MUST format it as a markdown link: `[Entity Name](entity:E-123)`. If you mention evidence, format it as `[EV-123](evidence:EV-123)`. Do not use this syntax for things without IDs."""

content = content.replace("4. Keep answers concise, readable, and focused on the facts. Use short sections and bullet points.", rule_add)

with open(r"d:\NETRA\SIH2026\ai-service\app\agent\prompts.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated prompt rules")
