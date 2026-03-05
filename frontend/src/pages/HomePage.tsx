import { Button } from "@/components/ui/button";
import { Layout } from "@/components/layout/Layout";

export function HomePage() {
  return (
    <Layout>
      <div className="flex flex-col items-center gap-6 py-12">
        <h1 className="text-3xl font-semibold tracking-tight">
          WedConnect
        </h1>
        <p className="text-muted-foreground">
          Wedding planning, together.
        </p>
        <Button>Get started</Button>
      </div>
    </Layout>
  );
}
