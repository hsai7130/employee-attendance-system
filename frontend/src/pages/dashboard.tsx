export default function Dashboard() {
  return (
    <main className="min-h-screen bg-slate-100 p-8">
      <div className="mx-auto max-w-7xl">
        <div className="rounded-3xl bg-white p-8 shadow-lg">
          <h1 className="text-3xl font-semibold text-slate-900">Dashboard</h1>
          <div className="mt-8 grid gap-6 md:grid-cols-3">
            {[
              { title: "Total Employees", value: "1,024" },
              { title: "Present Today", value: "802" },
              { title: "Pending Leave Requests", value: "24" },
            ].map((card) => (
              <div key={card.title} className="rounded-3xl border border-slate-200 bg-slate-50 p-6">
                <p className="text-sm uppercase tracking-[0.2em] text-slate-500">{card.title}</p>
                <p className="mt-4 text-4xl font-semibold text-slate-900">{card.value}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}
