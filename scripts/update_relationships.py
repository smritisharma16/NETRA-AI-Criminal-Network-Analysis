import re

with open(r"d:\NETRA\SIH2026\src\components\Chatbot.tsx", "r", encoding="utf-8") as f:
    content = f.read()

render_text_start = content.find("function renderText")
render_text_end = content.find("function TracePanel")

new_render = """function renderText(text: string, onEntityClick: (id: string, name: string, type: string) => void, onRelationshipClick?: (id: string, type: string) => void) {
  if (!text) return text;
  
  const regex = /\\[([^\\]]+)\\]\\((entity|evidence|relationship):([^)]+)\\)/g;
  const parts = [];
  let lastIndex = 0;
  
  let match;
  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.substring(lastIndex, match.index));
    }
    
    const [_, label, type, id] = match;
    parts.push(
      <button 
        key={lastIndex}
        onClick={() => {
          if (type === 'entity') onEntityClick(id, label, "UNKNOWN");
          if (type === 'relationship' && onRelationshipClick) onRelationshipClick(id, label);
        }}
        className={`font-semibold rounded px-1.5 -my-1 py-0.5 inline-flex items-center gap-1 transition-colors ${
          type === 'entity' ? 'bg-primary/10 text-primary hover:bg-primary/20' :
          type === 'evidence' ? 'bg-amber-500/10 text-amber-700 hover:bg-amber-500/20' :
          'bg-indigo-500/10 text-indigo-700 hover:bg-indigo-500/20'
        }`}
      >
        {type === 'evidence' && <FileText className="w-3 h-3" />}
        {type === 'relationship' && <Share2 className="w-3 h-3" />}
        {label}
      </button>
    );
    
    lastIndex = regex.lastIndex;
  }
  
  if (lastIndex < text.length) {
    parts.push(text.substring(lastIndex));
  }
  
  return parts.length ? parts : text;
}

"""

if render_text_start != -1 and render_text_end != -1:
    content = content[:render_text_start] + new_render + content[render_text_end:]

# Update AssistantBubble definition
content = content.replace(
    "function AssistantBubble({ msg, onAction, onEntityClick }: { msg: StructuredMessage; onAction: (action: ActionItem) => void; onEntityClick: (id: string, name: string, type: string) => void }) {",
    "function AssistantBubble({ msg, onAction, onEntityClick, onRelationshipClick }: { msg: StructuredMessage; onAction: (action: ActionItem) => void; onEntityClick: (id: string, name: string, type: string) => void, onRelationshipClick: (id: string, type: string) => void }) {"
)

# Update AssistantBubble invocations of renderText
content = content.replace("renderText(mainText, onEntityClick)", "renderText(mainText, onEntityClick, onRelationshipClick)")
content = content.replace("renderText(f.text, onEntityClick)", "renderText(f.text, onEntityClick, onRelationshipClick)")
content = content.replace("renderText(o.text, onEntityClick)", "renderText(o.text, onEntityClick, onRelationshipClick)")
content = content.replace("renderText(u.text, onEntityClick)", "renderText(u.text, onEntityClick, onRelationshipClick)")

# Pass selectRelationship to AssistantBubble
content = content.replace("const { selectEntity } = useInvestigationContext();", "const { selectEntity, selectRelationship } = useInvestigationContext();")
content = content.replace("onEntityClick={(id, name, type) => selectEntity(id, name, type)} />", "onEntityClick={(id, name, type) => selectEntity(id, name, type)} onRelationshipClick={(id, type) => selectRelationship(id, type)} />")


with open(r"d:\NETRA\SIH2026\src\components\Chatbot.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated relationship handler")
