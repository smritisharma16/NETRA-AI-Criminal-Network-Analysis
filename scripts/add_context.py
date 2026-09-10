import re

with open(r"d:\NETRA\SIH2026\src\components\Chatbot.tsx", "r", encoding="utf-8") as f:
    content = f.read()

import_lucide = 'import { fetchWithAuth } from "../api/apiClient";\nimport { useInvestigationContext } from "../context/InvestigationContext";'
if "useInvestigationContext" not in content:
    content = content.replace('import { fetchWithAuth } from "../api/apiClient";', import_lucide)

const_chatbot_idx = content.find("const Chatbot = ")
if const_chatbot_idx != -1:
    body_idx = content.find("{", const_chatbot_idx) + 1
    # Check if we already added it
    if "const { selectEntity } = useInvestigationContext();" not in content:
        # Find the end of props block
        props_end = content.find(") => {", const_chatbot_idx)
        if props_end != -1:
            insertion_point = props_end + 6
            content = content[:insertion_point] + "\n  const { selectEntity } = useInvestigationContext();\n" + content[insertion_point:]

# Replace `<AssistantBubble key={idx} msg={m} onAction={handleActionClick} />`
# with `<AssistantBubble key={idx} msg={m} onAction={handleActionClick} onEntityClick={(id, name, type) => selectEntity(id, name, type)} />`
content = content.replace(
    "<AssistantBubble key={idx} msg={m} onAction={handleActionClick} />",
    '<AssistantBubble key={idx} msg={m} onAction={handleActionClick} onEntityClick={(id, name, type) => selectEntity(id, name, type)} />'
)

with open(r"d:\NETRA\SIH2026\src\components\Chatbot.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Added selectEntity")
