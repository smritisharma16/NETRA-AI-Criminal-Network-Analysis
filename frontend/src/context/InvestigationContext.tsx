/**
 * InvestigationContext.tsx
 *
 * Shared investigation state between Graph Explorer and Chat Assistant.
 * Enables context-aware chat: clicking an entity in the graph automatically
 * sets the chat context so the investigator can ask "what else is connected to it?"
 */
import React, { createContext, useContext, useState } from "react";

export interface InvestigationContextState {
  caseId: string | null;
  selectedEntityId: string | null;
  selectedEntityName: string | null;
  selectedEntityType: string | null;
  selectedRelationshipId: string | null;
  selectedRelationshipType: string | null;
  setCaseId: (id: string | null) => void;
  selectEntity: (id: string, name: string, type: string) => void;
  selectRelationship: (id: string, type: string) => void;
  clearSelection: () => void;
}

const InvestigationCtx = createContext<InvestigationContextState | null>(null);

export function InvestigationContextProvider({ children }: { children: React.ReactNode }) {
  const [caseId, setCaseId] = useState<string | null>(null);
  const [selectedEntityId, setSelectedEntityId] = useState<string | null>(null);
  const [selectedEntityName, setSelectedEntityName] = useState<string | null>(null);
  const [selectedEntityType, setSelectedEntityType] = useState<string | null>(null);
  const [selectedRelationshipId, setSelectedRelationshipId] = useState<string | null>(null);
  const [selectedRelationshipType, setSelectedRelationshipType] = useState<string | null>(null);

  const selectEntity = (id: string, name: string, type: string) => {
    setSelectedEntityId(id);
    setSelectedEntityName(name);
    setSelectedEntityType(type);
    setSelectedRelationshipId(null);
    setSelectedRelationshipType(null);
  };

  const selectRelationship = (id: string, type: string) => {
    setSelectedRelationshipId(id);
    setSelectedRelationshipType(type);
    setSelectedEntityId(null);
    setSelectedEntityName(null);
    setSelectedEntityType(null);
  };

  const clearSelection = () => {
    setSelectedEntityId(null);
    setSelectedEntityName(null);
    setSelectedEntityType(null);
    setSelectedRelationshipId(null);
    setSelectedRelationshipType(null);
  };

  return (
    <InvestigationCtx.Provider value={{
      caseId, selectedEntityId, selectedEntityName, selectedEntityType,
      selectedRelationshipId, selectedRelationshipType,
      setCaseId, selectEntity, selectRelationship, clearSelection
    }}>
      {children}
    </InvestigationCtx.Provider>
  );
}

export function useInvestigationContext() {
  const ctx = useContext(InvestigationCtx);
  if (!ctx) throw new Error("useInvestigationContext must be used inside InvestigationContextProvider");
  return ctx;
}
