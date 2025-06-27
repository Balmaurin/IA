import React, { createContext, useState } from 'react';
export const AuthContext = createContext<any>(null);
export const AuthProvider = ({ children }: any) => {
  const [user, setUser] = useState(null);
  return <AuthContext.Provider value={{ user, setUser }}>{children}</AuthContext.Provider>;
};
