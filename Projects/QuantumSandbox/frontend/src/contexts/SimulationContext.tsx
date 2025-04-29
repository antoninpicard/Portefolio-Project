import React, { createContext, useContext, useState } from 'react';

interface SimulationContextProps {
  simulationResult: any;
  setSimulationResult: (r: any) => void;
}

const SimulationContext = createContext<SimulationContextProps | undefined>(undefined);

export const SimulationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [simulationResult, setSimulationResult] = useState<any>(null);
  return (
    <SimulationContext.Provider value={{ simulationResult, setSimulationResult }}>
      {children}
    </SimulationContext.Provider>
  );
};

export const useSimulation = () => {
  const context = useContext(SimulationContext);
  if (!context) throw new Error('useSimulation must be used within a SimulationProvider');
  return context;
};
