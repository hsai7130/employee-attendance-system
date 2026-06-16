import { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-800 to-slate-950 text-white">
      <div className="mx-auto flex min-h-screen max-w-4xl items-center justify-center px-4 py-16">
        <div className="w-full rounded-3xl bg-slate-900/90 p-10 shadow-2xl backdrop-blur-xl sm:p-14">
          <h1 className="text-3xl font-semibold">Login</h1>
          <p className="mt-2 text-slate-400">Access the HR system with your corporate account.</p>

          <form className="mt-10 space-y-6">
            <label className="block">
              <span className="text-sm text-slate-300">Email address</span>
              <input
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-sky-500"
                placeholder="name@company.com"
              />
            </label>

            <label className="block">
              <span className="text-sm text-slate-300">Password</span>
              <input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-sky-500"
                placeholder="********"
              />
            </label>

            <button type="submit" className="w-full rounded-2xl bg-sky-500 px-5 py-3 text-base font-semibold text-white transition hover:bg-sky-400">
              Sign in
            </button>
          </form>
        </div>
      </div>
    </main>
  );
}
