import { Link } from "react-router-dom";
import { ArrowRight, HelpCircle, Leaf } from "lucide-react";
import { Button } from "../components/ui/button";
import { cn } from "../lib/utils";
import handshakeImage from "../assets/images/handshake.png";
import landingMobileImage from "../assets/images/landing-mobile.png";

export function LandingPage() {
  return (
    <>
      {/* Mobile: single-column premium app-like layout */}
      <div
        className={cn(
          "flex min-h-screen min-h-[100dvh] flex-col bg-white",
          "pt-[env(safe-area-inset-top)] pb-[env(safe-area-inset-bottom)]",
          "lg:hidden"
        )}
      >
        <div className="flex flex-1 flex-col items-center justify-center px-8 py-10 sm:px-10 sm:py-12">
          <div className="w-full max-w-sm text-center">
            <h1 className="font-heading text-[1.6rem] font-medium leading-tight text-slate-700 sm:text-2xl">
              Welcome to WedConnect
            </h1>
            <p className="font-heading mt-2 text-2xl font-bold leading-tight text-slate-900 sm:text-3xl">
              Your Personal CRM!
            </p>
            <p className="mt-5 flex items-center justify-center gap-2 text-center text-[0.9375rem] leading-relaxed text-stone-600 sm:text-base">
              Manage your clients, income, and schedule – all in one place
              <Leaf className="h-4 w-4 shrink-0 text-emerald-500/90" aria-hidden />
            </p>
          </div>
          <div className="my-10 flex flex-1 items-center justify-center sm:my-12">
            <img
              src={landingMobileImage}
              alt="Manage your business with WedConnect"
              className="h-52 w-52 max-w-[80vw] object-contain sm:h-60 sm:w-60"
            />
          </div>
          <div className="w-full max-w-sm space-y-5">
            <Button
              asChild
              size="lg"
              className="h-14 w-full rounded-2xl bg-slate-800 py-6 text-base font-semibold shadow-md shadow-slate-900/20 transition-shadow hover:bg-slate-900 hover:shadow-lg hover:shadow-slate-900/25 active:scale-[0.98]"
            >
              <Link to="/vendor/login" className="inline-flex items-center justify-center gap-2.5">
                Get Started
                <ArrowRight className="h-5 w-5" strokeWidth={2.5} />
              </Link>
            </Button>
            <p className="text-center text-[0.9375rem] text-stone-600">
              Already have an account?{" "}
              <Link
                to="/vendor/login"
                className="font-semibold text-blue-600 underline underline-offset-2 decoration-2 hover:text-blue-700"
              >
                Sign In
              </Link>
            </p>
          </div>
        </div>
      </div>

      {/* Desktop: two-column layout */}
      <div className="hidden min-h-screen flex-col lg:flex lg:flex-row">
        {/* Left panel - branding */}
        <aside
        className={cn(
          "relative flex flex-col items-center justify-between overflow-hidden px-8 py-12",
          "lg:w-[42%] lg:min-h-screen"
        )}
        style={{
          background:
            "linear-gradient(180deg, #46326a 0%, #3d2a5c 22%, #342255 45%, #2a1848 70%, #1e0a2e 100%)",
        }}
      >
        {/* Subtle radial overlay for depth and premium feel */}
        <div
          className="pointer-events-none absolute inset-0 opacity-40"
          style={{
            background:
              "radial-gradient(ellipse 80% 60% at 50% 40%, rgba(120, 80, 160, 0.15) 0%, transparent 60%)",
          }}
          aria-hidden
        />
        <div className="relative z-10 w-full text-center">
          <h1 className="font-heading text-2xl font-semibold tracking-[0.35em] text-white drop-shadow-sm md:text-3xl">
            WEDCONNECT
          </h1>
        </div>

        <div className="relative z-10 flex flex-1 flex-col items-center justify-center py-8">
          <div className="flex h-40 w-40 items-center justify-center rounded-full bg-white/[0.08] shadow-[inset_0_0_60px_rgba(255,255,255,0.03)] backdrop-blur-sm md:h-52 md:w-52">
            <img
              src={handshakeImage}
              alt="Partnership handshake"
              className="h-20 w-20 object-contain md:h-28 md:w-28"
            />
          </div>
          <p className="font-heading mt-10 max-w-[260px] text-center text-sm font-semibold uppercase tracking-widest text-white/95">
            Become an exclusive member
          </p>
          <p className="font-heading mt-2 max-w-[260px] text-center text-xs font-medium uppercase tracking-[0.2em] text-white/80">
            Sign up and join the partnership
          </p>
        </div>

        <div className="relative z-10 h-8" aria-hidden />
      </aside>

      {/* Right panel - main content */}
      <main className="relative flex flex-1 flex-col bg-stone-50/95 lg:min-h-screen">
        {/* Top bar - Sign In */}
        <header className="flex justify-end px-6 py-5 lg:px-12">
          <p className="text-sm text-stone-600">
            Already have an account?{" "}
            <Link
              to="/vendor/login"
              className="font-medium text-blue-600 transition-colors hover:text-blue-700 hover:underline"
            >
              Sign In
            </Link>
          </p>
        </header>

        {/* Centered welcome block */}
        <div className="flex flex-1 flex-col items-center justify-center px-6 pb-24 pt-8 lg:px-16">
          <div className="w-full max-w-md text-center">
            <h2 className="font-heading text-2xl font-semibold leading-tight text-slate-800 md:text-3xl lg:text-4xl">
              Welcome to{" "}
              <span className="block text-slate-900">WedConnect – Your Personal CRM</span>
            </h2>
            <p className="mt-5 text-center text-base text-stone-600 md:text-lg">
              Manage your clients, income, and schedule — all in one place
            </p>
            <div className="mt-8">
              <Button
                asChild
                size="lg"
                className="h-12 rounded-lg bg-slate-800 px-8 text-base font-semibold shadow-md transition-shadow hover:bg-slate-900 hover:shadow-lg"
              >
                <Link to="/vendor/login" className="inline-flex items-center gap-2">
                  Get Started
                  <ArrowRight className="h-5 w-5" />
                </Link>
              </Button>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="flex flex-wrap items-center justify-between gap-4 border-t border-stone-200/80 bg-white/50 px-6 py-4 lg:px-12">
          <p className="text-xs text-stone-500">
            © 2021 – {new Date().getFullYear()} WedConnect. All rights reserved.
          </p>
          <Link
            to="/help"
            className="inline-flex items-center gap-1.5 text-xs text-stone-500 transition-colors hover:text-stone-700"
          >
            <HelpCircle className="h-4 w-4" />
            Need help?
          </Link>
        </footer>
      </main>
      </div>
    </>
  );
}
