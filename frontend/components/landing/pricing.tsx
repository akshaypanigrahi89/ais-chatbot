import Link from "next/link"

const plans = [
  {
    name: "Free",
    price: "$0",
    period: "/month",
    description: "Perfect for evaluation",
    features: [
      "1 bot",
      "1,000 queries/month",
      "100MB storage",
      "Basic guardrails",
      "Community support"
    ],
    cta: "Get Started",
    ctaHref: "/register",
    highlighted: false
  },
  {
    name: "Pro",
    price: "$49",
    period: "/month",
    description: "For growing teams",
    features: [
      "5 bots",
      "10,000 queries/month",
      "1GB storage",
      "Full 5-layer guardrails",
      "HITL review workflow",
      "Email support"
    ],
    cta: "Start Pro Trial",
    ctaHref: "/register",
    highlighted: true
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "",
    description: "For large organizations",
    features: [
      "Unlimited bots",
      "Unlimited queries",
      "Unlimited storage",
      "SSO/SAML",
      "Custom guardrails",
      "Dedicated support",
      "99.9% SLA"
    ],
    cta: "Contact Sales",
    ctaHref: "#",
    highlighted: false
  }
]

export function Pricing() {
  return (
    <section id="pricing" className="container mx-auto px-4 py-24 bg-muted/50">
      <div className="text-center mb-16">
        <h2 className="text-3xl md:text-4xl font-bold mb-4">
          Simple, transparent pricing
        </h2>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Start for free, upgrade as you grow.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
        {plans.map((plan) => (
          <div
            key={plan.name}
            className={`p-8 rounded-xl border ${
              plan.highlighted
                ? "border-primary shadow-lg bg-card"
                : "bg-card"
            }`}
          >
            {plan.highlighted && (
              <div className="text-sm font-medium text-primary mb-4">Most Popular</div>
            )}
            <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
            <div className="mb-4">
              <span className="text-4xl font-bold">{plan.price}</span>
              <span className="text-muted-foreground">{plan.period}</span>
            </div>
            <p className="text-sm text-muted-foreground mb-6">{plan.description}</p>
            <ul className="space-y-3 mb-8">
              {plan.features.map((feature) => (
                <li key={feature} className="flex items-center text-sm">
                  <svg className="h-4 w-4 text-primary mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  {feature}
                </li>
              ))}
            </ul>
            <Link
              href={plan.ctaHref}
              className={`block w-full py-2.5 text-center text-sm font-medium rounded-lg transition-colors ${
                plan.highlighted
                  ? "bg-primary text-primary-foreground hover:bg-primary/90"
                  : "border hover:bg-muted"
              }`}
            >
              {plan.cta}
            </Link>
          </div>
        ))}
      </div>
    </section>
  )
}
