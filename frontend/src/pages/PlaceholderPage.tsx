import { Link } from "react-router-dom";
import { Button } from "../components/ui/button";

interface PlaceholderPageProps {
  title: string;
}

export function PlaceholderPage({ title }: PlaceholderPageProps) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-6 bg-stone-50 px-4">
      <h1 className="text-xl font-semibold text-stone-800">{title}</h1>
      <p className="text-sm text-stone-500">This page is coming soon.</p>
      <Button asChild variant="outline">
        <Link to="/">Back to home</Link>
      </Button>
    </div>
  );
}
