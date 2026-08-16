import { Hero } from "@/components/landing/hero"
import { Features } from "@/components/landing/features"
import { Pricing } from "@/components/landing/pricing"
import { CTA } from "@/components/landing/cta"
import { LandingNavbar } from "@/components/landing/navbar"
import { LandingFooter } from "@/components/landing/footer"

export default function LandingPage() {
  return (
    <>
      <LandingNavbar />
      <main className="flex-1">
        <Hero />
        <Features />
        <Pricing />
        <CTA />
      </main>
      <LandingFooter />
    </>
  )
}
