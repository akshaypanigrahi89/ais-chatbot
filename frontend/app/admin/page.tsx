"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"

interface DashboardStats {
  total_documents: number
  indexed_documents: number
  processing_documents: number
  failed_documents: number
  total_chunks: number
  total_conversations: number
  total_messages: number
  departments: string[]
}

export default function AdminPage() {
  const router = useRouter()
  const [stats, setStats] = useState<DashboardStats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem("token")
    if (!token) {
      router.push("/login")
      return
    }

    fetchStats(token)
  }, [router])

  const fetchStats = async (token: string) => {
    try {
      const response = await fetch("/api/admin/dashboard", {
        headers: { "Authorization": `Bearer ${token}` }
      })

      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (err) {
      console.error("Failed to fetch stats")
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-muted-foreground">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-muted/50">
      <header className="border-b bg-background">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <a href="/" className="flex items-center gap-2.5">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-sm font-bold text-primary-foreground">
                S
              </div>
              <span className="font-semibold">SIA Chatbot</span>
            </a>
            <span className="text-muted-foreground">/</span>
            <span className="font-medium">Admin Dashboard</span>
          </div>
          <div className="flex items-center gap-4">
            <a href="/chat" className="text-sm text-muted-foreground hover:text-foreground">
              Chat
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

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold mb-6">Dashboard</h1>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="p-6 rounded-xl bg-card border">
            <p className="text-sm text-muted-foreground">Total Documents</p>
            <p className="text-3xl font-bold">{stats?.total_documents || 0}</p>
          </div>
          <div className="p-6 rounded-xl bg-card border">
            <p className="text-sm text-muted-foreground">Indexed</p>
            <p className="text-3xl font-bold text-green-600">{stats?.indexed_documents || 0}</p>
          </div>
          <div className="p-6 rounded-xl bg-card border">
            <p className="text-sm text-muted-foreground">Processing</p>
            <p className="text-3xl font-bold text-yellow-600">{stats?.processing_documents || 0}</p>
          </div>
          <div className="p-6 rounded-xl bg-card border">
            <p className="text-sm text-muted-foreground">Failed</p>
            <p className="text-3xl font-bold text-red-600">{stats?.failed_documents || 0}</p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="p-6 rounded-xl bg-card border">
            <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
            <div className="space-y-2">
              <button className="w-full py-2 px-4 text-left text-sm border rounded-lg hover:bg-muted transition-colors">
                Upload Document
              </button>
              <button className="w-full py-2 px-4 text-left text-sm border rounded-lg hover:bg-muted transition-colors">
                Manage Users
              </button>
              <button className="w-full py-2 px-4 text-left text-sm border rounded-lg hover:bg-muted transition-colors">
                View Audit Logs
              </button>
            </div>
          </div>

          <div className="p-6 rounded-xl bg-card border">
            <h2 className="text-lg font-semibold mb-4">Departments</h2>
            <div className="flex flex-wrap gap-2">
              {stats?.departments?.map((dept) => (
                <span
                  key={dept}
                  className="px-3 py-1 text-sm bg-muted rounded-full"
                >
                  {dept}
                </span>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
