"use client";

import { useState } from "react";
import { Chat, useChat } from "@openai/chatkit";
import { Send, User, Bot, Loader2 } from "lucide-react";

export default function ChatInterface({ userId }: { userId: string }) {
    const [conversationId, setConversationId] = useState<string | null>(null);

    const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
        api: `http://localhost:8000/api/${userId}/chat`,
        onResponse: (response) => {
            // In a real ChatKit implementation, we'd handle the response structure
            // For now, we assume the API returns the ChatResponse model
        },
        body: {
            conversation_id: conversationId,
        },
    });

    return (
        <div className="flex flex-col h-screen max-w-4xl mx-auto p-4 bg-gray-900 text-white">
            <header className="py-6 border-b border-gray-800">
                <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                    AI Todo Assistant
                </h1>
                <p className="text-gray-400 italic">Manage your tasks with natural language</p>
            </header>

            <main className="flex-1 overflow-y-auto py-4 space-y-4">
                {messages.map((m) => (
                    <div
                        key={m.id}
                        className={`flex items-start gap-3 ${m.role === "user" ? "justify-end" : "justify-start"
                            }`}
                    >
                        {m.role === "assistant" && (
                            <div className="p-2 rounded-full bg-blue-600">
                                <Bot size={20} />
                            </div>
                        )}
                        <div
                            className={`max-w-[80%] p-4 rounded-2xl ${m.role === "user"
                                    ? "bg-blue-600 text-white rounded-tr-none"
                                    : "bg-gray-800 text-gray-100 rounded-tl-none"
                                }`}
                        >
                            {m.content}
                        </div>
                        {m.role === "user" && (
                            <div className="p-2 rounded-full bg-gray-700">
                                <User size={20} />
                            </div>
                        )}
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start items-center gap-3">
                        <div className="p-2 rounded-full bg-blue-600">
                            <Bot size={20} />
                        </div>
                        <div className="p-4 rounded-2xl bg-gray-800 text-gray-100 rounded-tl-none">
                            <Loader2 className="animate-spin" size={20} />
                        </div>
                    </div>
                )}
            </main>

            <footer className="py-4 border-t border-gray-800">
                <form onSubmit={handleSubmit} className="relative">
                    <input
                        className="w-full p-4 pr-12 bg-gray-800 border border-gray-700 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                        value={input}
                        placeholder="e.g., 'Add a task to buy groceries'"
                        onChange={handleInputChange}
                    />
                    <button
                        type="submit"
                        disabled={isLoading || !input.trim()}
                        className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:cursor-not-allowed rounded-lg transition-colors"
                    >
                        <Send size={20} />
                    </button>
                </form>
            </footer>
        </div>
    );
}
