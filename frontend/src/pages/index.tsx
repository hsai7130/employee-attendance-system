import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50 p-8">
      <div className="mx-auto max-w-6xl rounded-3xl bg-white p-10 shadow-lg">
        <h1 className="text-4xl font-semibold text-slate-900">Employee Attendance System</h1>
        <p className="mt-4 text-slate-600">Enterprise cloud-native HR management with attendance, leave, and payroll modules.</p>

        <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            { label: "Login", href: "/login" },
            { label: "Dashboard", href: "/dashboard" },
            { label: "Employee Master", href: "/employees" },
            { label: "Reports", href: "/reports" },
          ].map((item) => (
            <Link key={item.href} href={item.href} className="rounded-2xl border border-slate-200 bg-slate-50 px-6 py-5 text-lg font-medium text-slate-900 transition hover:bg-slate-100">
              {item.label}
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}
