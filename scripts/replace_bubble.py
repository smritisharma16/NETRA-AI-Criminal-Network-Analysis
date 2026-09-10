with open(r"d:\NETRA\SIH2026\src\components\Chatbot.tsx", "r", encoding="utf-8") as f:
    content = f.read()

start = content.find("function AssistantBubble")
end = content.find("export default function Chatbot") if content.find("export default function Chatbot") != -1 else content.find("const Chatbot = ")

with open(r"d:\NETRA\SIH2026\scripts\assistant_bubble.txt", "r", encoding="utf-8") as f:
    bubble_code = f.read()

content = content[:start] + bubble_code + "\n\n" + content[end:]

with open(r"d:\NETRA\SIH2026\src\components\Chatbot.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Replaced bubble")
