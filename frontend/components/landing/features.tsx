import { Shield, Zap, FileText, Lock, MessageSquare, BarChart3 } from "lucide-react"

const features = [
  {
    icon: FileText,
    title: "Multi-Format Ingestion",
    description: "Upload PDFs, DOCX, PPTX, CSV, XLSX, HTML, images, and audio files."
  },
  {
    icon: Zap,
    title: "Hybrid Search",
    description: "Semantic + BM25 search with AI reranking for maximum accuracy."
  },
  {
    icon: Shield,
    title: "5-Layer Guardrails",
    description: "Input, auth, retrieval, prompt, and output security layers."
  },
  {
    icon: Lock,
    title: "Enterprise Security",
    description: "RBAC, audit logging, encryption, and compliance ready."
  },
  {
    icon: MessageSquare,
    title: "Human-in-the-Loop",
    description: "Review sensitive answers before they reach users."
  },
  {
    icon: BarChart3,
    title: "Analytics Dashboard",
    description: "Monitor usage, performance, and document health."
  }
]

export function Features() {
  return (
    <section id="features" className="container mx-auto px-4 py-24">
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          Everything you need for enterprise AI
        </h2>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Built for organizations that need security, scalability, and accuracy.
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {features.map((feature) => (
          <div
            key={feature.title}
            className="p-6 rounded-xl border bg-card hover:shadow-lg transition-shadow"
          >
            <feature.icon className="h-10 w-10 text-primary mb-4" />
            <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
            <p className="text-muted-foreground">{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
