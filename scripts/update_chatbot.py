import re

with open(r"d:\NETRA\SIH2026\src\components\Chatbot.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Replace ActionCards
action_cards_start = content.find("function ActionCards")
action_cards_end = content.find("function AssistantBubble")
if action_cards_start != -1 and action_cards_end != -1:
    new_action_cards = """function ActionCards({ actions, onAction }: { actions: ActionItem[]; onAction: (action: ActionItem) => void }) {
  if (!actions?.length) return null;
  const getIcon = (type: string) => {
    switch(type) {
      case "GRAPH": return <Compass className="w-4 h-4" />;
      case "CROSS_CASE": return <LinkIcon className="w-4 h-4" />;
      case "EVIDENCE": return <FileText className="w-4 h-4" />;
      case "ANALYTICS": return <BarChart3 className="w-4 h-4" />;
      case "ENTITY": return <User className="w-4 h-4" />;
      case "RELATIONSHIP": return <Share2 className="w-4 h-4" />;
      default: return <Search className="w-4 h-4" />;
    }
  };

  const recommended = actions.find(a => a.is_recommended);
  const others = actions.filter(a => !a.is_recommended);

  return (
    <div className="mt-6 border-t border-outline-variant/50 pt-4">
      <h3 className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mb-3">Continue Investigating</h3>
      <div className="flex flex-col gap-2">
        {recommended && (
          <button
            onClick={() => onAction(recommended)}
            className="w-full text-left bg-surface border border-primary/40 hover:border-primary/80 hover:shadow-md transition-all p-3 rounded-lg flex flex-col gap-1 relative group"
          >
            <div className="flex items-center gap-2 text-primary mb-1">
              {getIcon(recommended.type)}
              <span className="font-bold text-[11px] uppercase tracking-wider">★ {recommended.label}</span>
            </div>
            {recommended.description && (
              <p className="text-[11px] text-on-surface-variant line-clamp-2 pr-6">{recommended.description}</p>
            )}
            <ArrowRight className="w-3 h-3 text-primary absolute bottom-3 right-3 opacity-50 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
          </button>
        )}

        {others.map((a, i) => (
          <button
            key={i}
            onClick={() => onAction(a)}
            className="w-full text-left bg-surface border border-outline-variant hover:border-primary/40 hover:bg-surface-container-lowest transition-all p-3 rounded-lg flex flex-col gap-1 relative group"
          >
            <div className="flex items-center gap-2 text-on-surface mb-1 group-hover:text-primary transition-colors">
              {getIcon(a.type)}
              <span className="font-semibold text-xs tracking-wide">{a.label}</span>
            </div>
            {a.description && (
              <p className="text-[11px] text-on-surface-variant line-clamp-2 pr-6">{a.description}</p>
            )}
            <ArrowRight className="w-3 h-3 text-on-surface-variant absolute bottom-3 right-3 opacity-50 group-hover:text-primary group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
          </button>
        ))}
      </div>
    </div>
  );
}

"""
    content = content[:action_cards_start] + new_action_cards + content[action_cards_end:]

# Replace AssistantBubble
assistant_start = content.find("function AssistantBubble")
assistant_end = content.find("export default function Chatbot")
if assistant_start != -1 and assistant_end != -1:
    new_assistant = """function AssistantBubble({ msg, onAction }: { msg: StructuredMessage; onAction: (action: ActionItem) => void }) {
  const mainText = msg.answer || msg.text || "";
  const hasSections = (msg.facts?.length || msg.observations?.length || msg.uncertainties?.length);

  return (
    <div className="flex flex-col gap-2 mb-4 bg-surface p-4 rounded-xl border border-outline-variant shadow-sm">
      <div className="flex items-center gap-2 mb-2 border-b border-outline-variant/30 pb-2">
        <Bot className="w-4 h-4 text-primary" />
        <span className="text-[11px] font-bold text-primary uppercase tracking-wider">NETRA</span>
      </div>

      <div className="text-on-surface text-sm space-y-5">
        <p className="leading-relaxed whitespace-pre-wrap">{mainText}</p>

        {hasSections ? (
          <div className="space-y-5 pt-1">
            {msg.facts && msg.facts.length > 0 && (
              <div>
                <p className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mb-2">
                  What I Found
                </p>
                <ul className="space-y-2">
                  {msg.facts.map((f, i) => (
                    <li key={i} className="text-xs text-on-surface flex items-start gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-primary/60 mt-1 shrink-0" />
                      <span className="leading-relaxed">{f.text}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {msg.observations && msg.observations.length > 0 && (
              <div className="bg-amber-500/10 border-l-2 border-amber-500 pl-3 py-2 rounded-r-lg">
                <p className="text-[10px] font-bold text-amber-700 uppercase tracking-widest mb-1.5">
                  Why This Matters
                </p>
                <ul className="space-y-1.5">
                  {msg.observations.map((o, i) => (
                    <li key={i} className="text-xs text-on-surface leading-relaxed">
                      {o.text}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {msg.uncertainties && msg.uncertainties.length > 0 && (
              <div>
                <p className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mb-2">
                  What Remains Unknown
                </p>
                <ul className="space-y-2">
                  {msg.uncertainties.map((u, i) => (
                    <li key={i} className="text-xs text-on-surface-variant flex items-start gap-2">
                      <HelpCircle className="w-3.5 h-3.5 mt-0.5 shrink-0 opacity-60" />
                      <span className="leading-relaxed">{u.text}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ) : null}

        <TracePanel trace={msg.trace} />
      </div>
      <ActionCards actions={msg.actions || []} onAction={onAction} />
    </div>
  );
}

"""
    content = content[:assistant_start] + new_assistant + content[assistant_end:]

# Replace Messages Mapping in Chatbot component
body_start = content.find('<div ref={bodyRef} className="h-96 overflow-y-auto p-4 bg-surface flex flex-col gap-4 text-sm">')
if body_start != -1:
    body_inner_start = content.find('{messages.map((m, idx) => (', body_start)
    body_end = content.find('{isLoading && (', body_inner_start)
    
    if body_inner_start != -1 and body_end != -1:
        new_map = """{messages.map((m, idx) => (
            m.role === "user" ? (
              <div key={idx} className="flex justify-end mb-4">
                <div className="bg-surface-container-high border border-outline-variant px-4 py-2.5 rounded-2xl rounded-tr-sm max-w-[80%] text-on-surface shadow-sm">
                  {m.text}
                </div>
              </div>
            ) : (
              <AssistantBubble key={idx} msg={m} onAction={handleActionClick} />
            )
          ))}
          """
        content = content[:body_inner_start] + new_map + content[body_end:]

with open(r"d:\NETRA\SIH2026\src\components\Chatbot.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated successfully")
