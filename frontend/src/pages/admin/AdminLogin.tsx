import { useState } from "react";
import { Shield } from "lucide-react";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { adminLogin } from "../../api/adminAuth";

export function AdminLogin() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await adminLogin({ username, password });
      // TODO: Handle successful login (store token, redirect)
      console.log("Admin Login Successful", response);
      alert("Login successful!");
    } catch (err) {
      console.error(err);
      if (typeof err === "object" && err !== null && "response" in err) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const errorResp = (err as Record<string, any>).response?.data;
        setError(
          errorResp?.error || 
          errorResp?.non_field_errors?.[0] || 
          "Failed to login. Please check your credentials."
        );
      } else {
        setError("Failed to login. Please check your credentials.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-zinc-50 px-4">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-xl shadow-lg p-8 border border-zinc-100">
          <div className="flex flex-col items-center mb-8">
            <div className="bg-zinc-100 p-3 rounded-full mb-4">
              <Shield className="w-8 h-8 text-zinc-900" />
            </div>
            <h1 className="text-2xl font-semibold text-zinc-900 tracking-tight">
              WedConnect Admin
            </h1>
            <p className="text-zinc-500 text-sm mt-2">
              Sign in to manage vendors and platform settings
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="bg-red-50 text-red-600 text-sm p-3 rounded-md">
                {error}
              </div>
            )}
            
            <div className="space-y-1">
              <label className="text-sm font-medium text-zinc-700" htmlFor="username">
                Username
              </label>
              <Input
                id="username"
                type="text"
                placeholder="admin"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>

            <div className="space-y-1">
              <label className="text-sm font-medium text-zinc-700" htmlFor="password">
                Password
              </label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <Button
              type="submit"
              className="w-full bg-zinc-900 text-white hover:bg-black transition-colors"
              disabled={loading}
            >
              {loading ? "Signing in..." : "Sign in to Dashboard"}
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
}
