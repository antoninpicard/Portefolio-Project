import React, { createContext, useContext, useState } from 'react';

interface CircuitContextProps {
  circuit: any;
  setCircuit: (c: any) => void;
}

const CircuitContext = createContext<CircuitContextProps | undefined>(undefined);

export const CircuitProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [circuit, setCircuit] = useState<any>(null);
  return (
    <CircuitContext.Provider value={{ circuit, setCircuit }}>
      {children}
    </CircuitContext.Provider>
  );
};

export const useCircuit = () => {
  const context = useContext(CircuitContext);
  if (!context) throw new Error('useCircuit must be used within a CircuitProvider');
  return context;
};
