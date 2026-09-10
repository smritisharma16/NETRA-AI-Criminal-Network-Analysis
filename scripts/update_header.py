import re

with open(r"d:\NETRA\SIH2026\src\components\Chatbot.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace Header block
header_start = content.find("{/* Header */}")
body_start = content.find("{/* Body */}")

if header_start != -1 and body_start != -1:
    new_header = """{/* Header */}
        <div className="bg-surface p-4 border-b border-outline-variant flex justify-between items-start">
          <div className="flex gap-3">
            <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center shrink-0 border border-primary/20">
              <Bot className="w-6 h-6 text-primary" />
            </div>
            <div>
              <h2 className="text-on-surface font-bold text-sm tracking-wide uppercase">NETRA Assistant</h2>
              <p className="text-on-surface-variant text-[11px] font-medium tracking-wide mt-0.5">
                {caseId || "C-001"} • Case Investigation
              </p>
              <div className="flex items-center gap-1.5 mt-1.5 text-[11px]">
                <span className="text-on-surface-variant uppercase tracking-wider font-semibold text-[9px]">Focus:</span>
                <span className="bg-primary/10 text-primary px-2 py-0.5 rounded font-medium truncate max-w-[200px]">
                  {selectedEntityName || selectedRelationshipType || "Entire Case"}
                </span>
              </div>
            </div>
          </div>
          <button
            onClick={() => setIsOpen(false)}
            className="text-on-surface-variant hover:text-on-surface hover:bg-surface-container rounded-lg p-1.5 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
        
        """
    content = content[:header_start] + new_header + content[body_start:]

with open(r"d:\NETRA\SIH2026\src\components\Chatbot.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Replaced Header")
