import re

with open(r"d:\NETRA\SIH2026\src\components\Chatbot.tsx", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("const isOpen = false; // Placeholder if missing state definition\n  const setIsOpen = (b: boolean) => {}; // Placeholder", "const [isOpen, setIsOpen] = useState(false);")

with open(r"d:\NETRA\SIH2026\src\components\Chatbot.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Restored isOpen")
