import { useState, useRef, useEffect } from "react";
import { fetchWithAuth } from "../api/apiClient";
import { useInvestigationContext } from "../context/InvestigationContext";
import { 
  Bot, Search, Link as LinkIcon, FileText, 
  BarChart3, User, Share2, ArrowRight, 
  HelpCircle, ChevronRight, Compass, X
} from "lucide-react";

// ─── Types ────────────────────────────────────────────────────────────────────

interface ActionItem {
  label: string;
  description?: string; // Human readable description of action
  prompt?: string;      // Natural language question sent when clicked
  type: string;         // GRAPH | CROSS_CASE | EVIDENCE | ANALYTICS | etc.
  target_id?: string;
  is_recommended?: boolean;
}

interface FactItem {
  text: string;
  source?: string;
}

interface StructuredMessage {
  role: "user" | "assistant";
  text?: string;               // fallback plain text
  answer?: string;             // main conversational response
  facts?: FactItem[];
  observations?: FactItem[];
  uncertainties?: FactItem[];
  actions?: ActionItem[];
  trace?: { tools_used?: { tool: string; arguments?: any }[]; truncated?: boolean };
}

// ─── Sub-components ─────────────────────────────────────────────────────────────

function renderText(text: string, onEntityClick: (id: string, name: string, type: string) => void, onRelationshipClick?: (id: string, type: string) => void) {
  if (!text) return text;
  
  const regex = /\[([^\]]+)\]\((entity|evidence|relationship):([^)]+)\)/g;
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

function TracePanel({ trace }: { trace: StructuredMessage["trace"] }) {
  const [open, setOpen] = useState(false);
  if (!trace?.tools_used?.length) return null;
  return (
    <div className="mt-2 pt-2 border-t border-primary/10 text-[11px] text-on-surface-variant">
      <button
        onClick={() => setOpen(o => !o)}
        className="flex items-center gap-1 hover:text-primary transition-colors font-semibold"
      >
        <ChevronRight className={`w-3 h-3 transition-transform ${open ? "rotate-90" : ""}`} />
        Investigation Details
      </button>
      {open && (
        <ul className="mt-1 pl-4 font-mono space-y-1">
          {trace.tools_used.map((t, i) => (
            <li key={i} className="text-[10px]">
              <span className="text-primary">{t.tool}</span>
              {t.arguments && Object.keys(t.arguments).length > 0 && (
                <span className="text-on-surface-variant ml-1">
                  ({Object.entries(t.arguments).map(([k, v]) => `${k}=${v}`).join(", ")})
                </span>
              )}
            </li>
          ))}
        </ul>
      )}
      {trace.truncated && (
        <p className="mt-1 text-amber-600 italic">⚠ Results were truncated. Use Graph Explorer for the full view.</p>
      )}
    </div>
  );
}

function ActionCards({ actions, onAction }: { actions: ActionItem[]; onAction: (action: ActionItem) => void }) {
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

﻿function AssistantBubble({ msg, onAction, onEntityClick, onRelationshipClick }: { msg: StructuredMessage; onAction: (action: ActionItem) => void; onEntityClick: (id: string, name: string, type: string) => void, onRelationshipClick: (id: string, type: string) => void }) {
  const mainText = msg.answer || msg.text || "";
  const hasSections = (msg.facts?.length || msg.observations?.length || msg.uncertainties?.length);

  return (
    <div className="flex flex-col gap-2 mb-4 bg-surface p-4 rounded-xl border border-outline-variant shadow-sm">
      <div className="flex items-center gap-2 mb-2 border-b border-outline-variant/30 pb-2">
        <Bot className="w-4 h-4 text-primary" />
        <span className="text-[11px] font-bold text-primary uppercase tracking-wider">NETRA Assistant</span>
      </div>

      <div className="text-on-surface text-sm space-y-5">
        <p className="leading-relaxed whitespace-pre-wrap">{renderText(mainText, onEntityClick, onRelationshipClick)}</p>

        {hasSections ? (
          <div className="space-y-5 pt-1">
            {msg.facts && msg.facts.length > 0 && (
              <div>
                <p className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mb-2 border-b border-outline-variant/30 pb-1">
                  What I Found
                </p>
                <ul className="space-y-2">
                  {msg.facts.map((f, i) => (
                    <li key={i} className="text-xs text-on-surface flex items-start gap-2">
                      <span className="w-1 h-1 rounded-full bg-primary mt-1.5 shrink-0" />
                      <span className="leading-relaxed">{renderText(f.text, onEntityClick, onRelationshipClick)}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {msg.observations && msg.observations.length > 0 && (
              <div className="bg-amber-500/5 border-l-2 border-amber-500 pl-3 py-2 rounded-r-lg">
                <p className="text-[10px] font-bold text-amber-700 uppercase tracking-widest mb-1.5">
                  Why This Matters
                </p>
                <ul className="space-y-1.5">
                  {msg.observations.map((o, i) => (
                    <li key={i} className="text-xs text-on-surface leading-relaxed">
                      {renderText(o.text, onEntityClick, onRelationshipClick)}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {msg.uncertainties && msg.uncertainties.length > 0 && (
              <div>
                <p className="text-[10px] font-bold text-on-surface-variant uppercase tracking-widest mb-2 border-b border-outline-variant/30 pb-1">
                  What Remains Unknown
                </p>
                <ul className="space-y-2">
                  {msg.uncertainties.map((u, i) => (
                    <li key={i} className="text-xs text-on-surface-variant flex items-start gap-2">
                      <HelpCircle className="w-3.5 h-3.5 mt-0.5 shrink-0 opacity-60 text-on-surface-variant" />
                      <span className="leading-relaxed">{renderText(u.text, onEntityClick, onRelationshipClick)}</span>
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


// ─── Main Component ─────────────────────────────────────────────────────────────

interface ChatbotProps {
  caseId?: string;
  selectedEntityId?: string;
  selectedEntityName?: string;
  selectedEntityType?: string;
  selectedRelationshipId?: string;
  selectedRelationshipType?: string;
}

const Chatbot = ({
  caseId,
  selectedEntityId,
  selectedEntityName,
  selectedEntityType,
  selectedRelationshipId,
  selectedRelationshipType
}: ChatbotProps) => {
  const { selectEntity, selectRelationship } = useInvestigationContext();

  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<StructuredMessage[]>([
    {
      role: "assistant",
      answer: `I'm ready to investigate ${caseId || "this case"}.\n\nWhat would you like to explore?`,
      actions: [
        { label: "Case overview", description: "Summarize the key entities and relationships.", prompt: "Summarize the key entities and relationships in this case.", type: "GRAPH", is_recommended: true },
        { label: "Key entities", description: "List the most important nodes.", prompt: "What are the most important entities in this case?", type: "ENTITY" },
        { label: "Investigative leads", description: "Show flagged anomalies.", prompt: "Show me the flagged investigative leads for this case.", type: "ANALYTICS" },
        { label: "Cross-case connections", description: "Find links to other cases.", prompt: "Are there any cross-case connections in this network?", type: "CROSS_CASE" },
      ]
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [threadId, setThreadId] = useState<string | null>(null);
  const bodyRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    if (bodyRef.current) {
      bodyRef.current.scrollTop = bodyRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  // Auto-open and pre-fill question when graph context changes
  useEffect(() => {
    if (selectedEntityId && selectedEntityName) {
      setIsOpen(true);
      // Optional: automatically send the query or just pre-fill.
      setQuery(`Tell me what is known about ${selectedEntityName}.`);
    }
    if (selectedRelationshipId) {
      setIsOpen(true);
      setQuery(`Explain relationship ${selectedRelationshipType || selectedRelationshipId}.`);
    }
  }, [selectedEntityId, selectedRelationshipId]);

  const buildContext = () => {
    const ctx: Record<string, string> = {};
    if (caseId) ctx.case_id = caseId;
    if (selectedEntityId) {
      ctx.selected_entity_id = selectedEntityId;
      ctx.selected_entity_name = selectedEntityName || selectedEntityId;
      ctx.selected_entity_type = selectedEntityType || "unknown";
    }
    if (selectedRelationshipId) {
      ctx.selected_relationship_id = selectedRelationshipId;
      ctx.selected_relationship_type = selectedRelationshipType || "unknown";
    }
    return Object.keys(ctx).length ? ctx : undefined;
  };

  const sendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMsg: StructuredMessage = { role: "user", text };
    setMessages(prev => [...prev, userMsg]);
    setQuery("");
    setIsLoading(true);

    try {
      const res = await fetchWithAuth("/api/v1/investigations/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          case_id: caseId || "GLOBAL",
          question: text,
          thread_id: threadId,
          context: buildContext()
        })
      });

      if (!res.ok) throw new Error("Agent failed to respond.");

      const data = await res.json();
      if (data.thread_id && !threadId) setThreadId(data.thread_id);

      const assistantMsg: StructuredMessage = {
        role: "assistant",
        answer: data.answer,
        text: data.answer,
        facts: data.facts,
        observations: data.observations,
        uncertainties: data.uncertainties,
        actions: data.actions,
        trace: data.trace
      };

      setMessages(prev => [...prev, assistantMsg]);
    } catch (e: any) {
      setMessages(prev => [...prev, { 
        role: "assistant", 
        answer: "NETRA couldn't complete that investigation step. Your case context has been preserved.",
        actions: [{ label: "Try again", prompt: text, type: "default" }]
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleActionClick = (action: ActionItem) => {
    // Submit the natural language prompt defined by the action card, falling back to label
    const question = action.prompt || action.label;
    sendMessage(question);
  };

  const contextBadge = selectedEntityName
    ? `📍 ${selectedEntityName}`
    : selectedRelationshipType
    ? `🔗 ${selectedRelationshipType}`
    : null;

  return (
    <div className="fixed bottom-6 right-6 z-[60] flex flex-col items-end">
      {/* Chat Window */}
      <div
        className={`mb-2 w-96 bg-surface-container-lowest rounded-xl shadow-2xl border border-outline-variant overflow-hidden flex flex-col transition-all duration-300 origin-bottom-right ${
          isOpen ? "opacity-100 scale-100 translate-y-0" : "opacity-0 scale-95 translate-y-4 pointer-events-none"
        }`}
      >
        {/* Header */}
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
        
        {/* Body */}
        <div ref={bodyRef} className="h-96 overflow-y-auto p-4 bg-surface flex flex-col gap-4 text-sm">
          {messages.map((m, idx) => (
            m.role === "user" ? (
              <div key={idx} className="flex justify-end mb-4">
                <div className="bg-surface-container-high border border-outline-variant px-4 py-2.5 rounded-2xl rounded-tr-sm max-w-[80%] text-on-surface shadow-sm">
                  {m.text}
                </div>
              </div>
            ) : (
              <AssistantBubble key={idx} msg={m} onAction={handleActionClick} onEntityClick={(id, name, type) => selectEntity(id, name, type)} onRelationshipClick={(id, type) => selectRelationship(id, type)} />
            )
          ))}
          {isLoading && (
            <div className="flex items-start gap-2">
              <div className="w-8 h-8 bg-primary-container rounded-full flex items-center justify-center shrink-0">
                <Search className="w-4 h-4 text-on-primary animate-spin" />
              </div>
              <div className="p-3 bg-primary-container/20 rounded-lg rounded-tl-none border border-primary/20 text-on-surface flex gap-1 items-center">
                <span className="text-xs text-on-surface-variant italic">Investigating...</span>
                <span className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce ml-2"></span>
                <span className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></span>
                <span className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></span>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-outline-variant bg-surface-container-lowest">
          <div className="flex gap-2">
            <input
              type="text"
              value={query}
              onChange={e => setQuery(e.target.value)}
              onKeyDown={e => e.key === "Enter" && sendMessage(query)}
              placeholder={selectedEntityName ? `Ask about ${selectedEntityName}...` : "Ask about this case..."}
              className="flex-1 bg-surface-container-low border border-outline-variant rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary"
            />
            <button
              onClick={() => sendMessage(query)}
              disabled={isLoading}
              className="bg-primary text-on-primary px-3 rounded-lg hover:bg-primary-container transition-colors flex items-center justify-center disabled:opacity-50"
            >
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="group relative flex items-center gap-2 bg-primary-container text-on-primary rounded-full px-4 py-3 shadow-[0_0_20px_rgba(255,153,51,0.6)] hover:shadow-[0_0_30px_rgba(255,153,51,0.8)] transition-all active:scale-95 z-10"
      >
        <Bot className="w-5 h-5" />
        <span className="font-bold tracking-wider uppercase text-sm">Ask AI</span>
        {contextBadge && (
          <span className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-surface"></span>
        )}
        <div className="absolute inset-0 rounded-full border-2 border-saffron-accent opacity-50"></div>
      </button>
    </div>
  );
};

export default Chatbot;
