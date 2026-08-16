"use client"

import { useState, useEffect, useRef } from "react"
import { useRouter } from "next/navigation"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  sources?: any[]
  groundedness?: number
}

export default function ChatPage() {
  const router = useRouter()
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const token = localStorage.getItem("token")
    if (!token) {
      router.push("/login")
    }
  }, [router])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setLoading(true)

    try {
      const token = localStorage.getItem("token")
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ message: input })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || "Failed to get response")
      }

      const assistantMessage: Message = {
        id: data.message_id || Date.now().toString(),
        role: "assistant",
        content: data.message,
        sources: data.sources,
        groundedness: data.groundedness
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (err: any) {
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: "assistant",
        content: "Sorry, an error occurred. Please try again."
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen">
      <header className="border-b px-4 py-3">
        <div className="container mx-auto flex items-center justify-between">
          <a href="/" className="flex items-center gap-2.5">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-sm font-bold text-primary-foreground">
              S
            </div>
            <span className="font-semibold">SIA Chatbot</span>
          </a>
          <div className="flex items-center gap-4">
            <a href="/admin" className="text-sm text-muted-foreground hover:text-foreground">
              Admin
            </a>
            <button
              onClick={() => {
                localStorage.removeItem("token")
                localStorage.removeItem("user")
                router.push("/login")
              }}
              className="text-sm text-muted-foreground hover:text-foreground"
            >
              Sign out
            </button>
          </div>
        </div>
      </header>

      <main className="flex-1 overflow-y-auto">
        <div className="container mx-auto max-w-3xl px-4 py-6">
          {messages.length === 0 && (
            <div className="text-center py-20">
              <h1 className="text-3xl font-bold mb-4">How can I help you today?</h1>
              <p className="text-muted-foreground">
                Ask me anything about your organization's knowledge base.
              </p>
            </div>
          )}

          <div className="space-y-6">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${
                  message.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-xl px-4 py-3 ${
                    message.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted"
                  }`}
                >
                  <p className="whitespace-pre-wrap">{message.content}</p>
                  {message.sources && message.sources.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-border/50">
                      <p className="text-xs font-medium mb-1">Sources:</p>
                      {message.sources.map((source, i) => (
                        <p key={i} className="text-xs text-muted-foreground">
                          {source.title} {source.page && `- Page ${source.page}`}
                        </p>
                      ))}
                    </div>
                  )}
                  {message.groundedness !== undefined && (
                    <div className="mt-2">
                      <span className={`text-xs ${
                        message.groundedness > 0.8
                          ? "text-green-600"
                          : message.groundedness > 0.5
                          ? "text-yellow-600"
                          : "text-red-600"
                      }`}>
                        Groundedness: {Math.round(message.groundedness * 100)}%
                      </span>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="bg-muted rounded-xl px-4 py-3">
                  <div className="loading-dots flex gap-1">
                    <span className="w-2 h-2 bg-foreground/60 rounded-full"></span>
                    <span className="w-2 h-2 bg-foreground/60 rounded-full"></span>
                    <span className="w-2 h-2 bg-foreground/60 rounded-full"></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>
      </main>

      <footer className="border-t px-4 py-4">
        <form onSubmit={handleSubmit} className="container mx-auto max-w-3xl">
          <div className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
              className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="px-6 py-2 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 disabled:opacity-50 transition-colors"
            >
              Send
            </button>
          </div>
        </form>
      </footer>
    </div>
  )
}
