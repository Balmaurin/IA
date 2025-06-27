import { useContext } from 'react';
import { ChatContext } from '../contexts/ChatContext';
export const useChat = () => useContext(ChatContext);
