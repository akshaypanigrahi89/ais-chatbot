import Link from "next/link"

export function CTA() {
  return (
    <section className="container mx-auto px-4 py-24">
      <div className="mx-auto max-w-3xl text-center">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          Ready to transform your organization?
        </h2>
        <p className="text-lg text-muted-foreground mb-8">
          Join leading enterprises using SIA Chatbot to unlock the power of their knowledge base.
        </p>
        <Link
          href="/register"
          className="inline-block px-8 py-3 text-base font-medium bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
        >
          Start Free Today
        </Link>
      </div>
    </section>
  )
}
