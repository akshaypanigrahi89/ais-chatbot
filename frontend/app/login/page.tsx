import type { Metadata } from "next"
import { LoginForm } from "@/components/auth/login-form"

export const metadata: Metadata = {
  title: "Sign In | SIA Chatbot",
}

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <div className="w-full max-w-sm">
        <div className="mb-8 text-center">
          <a href="/" className="inline-flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-primary text-lg font-bold text-primary-foreground">
              S
            </div>
            <span className="text-xl font-semibold">SIA Chatbot</span>
          </a>
          <h1 className="mt-6 text-2xl font-bold">Welcome back</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Sign in to your account to continue
          </p>
        </div>

        <LoginForm />

        <p className="mt-6 text-center text-sm text-muted-foreground">
          Don&apos;t have an account?{" "}
          <a href="/register" className="font-medium text-primary hover:underline">
            Sign up
          </a>
        </p>
      </div>
    </div>
  )
}
