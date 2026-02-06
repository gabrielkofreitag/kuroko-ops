import React, { useEffect, useState } from 'react';
import { useChatStore } from '../stores/chat-store';

interface Thought {
    agent: string;
    content: string;
    timestamp: string;
}

export const ThoughtStream: React.FC = () => {
    const [thoughts, setThoughts] = useState<Thought[]>([]);
    const { lastMessage } = useChatStore();

    useEffect(() => {
        if (lastMessage && lastMessage.type === 'thought') {
            const newThought: Thought = {
                agent: lastMessage.agent,
                content: lastMessage.content,
                timestamp: new Date().toLocaleTimeString(),
            };
            setThoughts((prev) => [newThought, ...prev].slice(0, 50));
        }
    }, [lastMessage]);

    if (thoughts.length === 0) return null;

    return (
        <div className="thought-stream-container bg-slate-900/50 p-4 rounded-lg border border-slate-700/50 my-4 max-h-60 overflow-y-auto">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Agent Thoughts</h3>
            <div className="space-y-2">
                {thoughts.map((thought, index) => (
                    <div key={index} className="thought-item animate-in fade-in slide-in-from-left-2 duration-300">
                        <span className="text-[10px] text-slate-500 mr-2">{thought.timestamp}</span>
                        <span className={`text-xs font-semibold px-2 py-0.5 rounded ${thought.agent === 'Planner' ? 'bg-blue-500/20 text-blue-400' :
                                thought.agent === 'Coder' ? 'bg-green-500/20 text-green-400' :
                                    'bg-purple-500/20 text-purple-400'
                            }`}>
                            {thought.agent}
                        </span>
                        <p className="text-xs text-slate-300 mt-1 pl-12 border-l border-slate-700">
                            {thought.content}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
};
