import Link from "next/link"

export function Hero() {
  return (
    <section className="container mx-auto px-4 py-24 text-center">
      <div className="mx-auto max-w-3xl">
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
          Your Enterprise{" "}
          <span className="text-primary">AI Knowledge</span>{" "}
          Assistant
        </h1>
        <p className="text-lg md:text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
          Intelligent. Secure. Scalable. Build powerful AI chatbots from your
          organization's documents with enterprise-grade security and guardrails.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/register"
            className="px-8 py-3 text-base font-medium bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            Get Started Free
          </Link>
          <Link
            href="#features"
            className="px-8 py-3 text-base font-medium border rounded-lg hover:bg-muted transition-colors"
          >
            Learn More
          </Link>
        </div>
      </div>
    </section>
  )
}
