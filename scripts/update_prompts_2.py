import re

with open(r"d:\NETRA\SIH2026\ai-service\app\agent\prompts.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("If you mention evidence, format it as `[EV-123](evidence:EV-123)`.", "If you mention evidence, format it as `[EV-123](evidence:EV-123)`. If you mention a relationship, format it as `[LOCATED_AT](relationship:R-123)`.")

with open(r"d:\NETRA\SIH2026\ai-service\app\agent\prompts.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated prompt rules again")
