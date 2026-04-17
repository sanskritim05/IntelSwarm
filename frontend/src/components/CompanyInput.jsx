export default function CompanyInput({
  company,
  setCompany,
  onSubmit,
  loading,
  reports,
  onOpenReport,
  error,
}) {
  return (
    <section className="mx-auto max-w-5xl px-6 py-12">
      <div className="rounded-[2rem] border border-white/10 bg-white/6 p-8 shadow-2xl shadow-amber-500/10 backdrop-blur">
        <div className="mb-10 max-w-3xl">
          <p className="mb-3 text-sm uppercase tracking-[0.35em] text-cyan-200/70">
            Local-first agent swarm
          </p>
          <h1 className="text-5xl font-semibold tracking-tight text-orange-50 sm:text-6xl">
            IntelSwarm
          </h1>
          <p className="mt-4 max-w-2xl text-lg leading-8 text-stone-300">
            Generate a recruiter style company briefing with a hierarchical multi-agent
            swarm powered by Strands Agents, Ollama, and live research progress.
          </p>
        </div>

        <form onSubmit={onSubmit} className="grid gap-4 md:grid-cols-[1fr_auto]">
          <input
            value={company}
            onChange={(event) => setCompany(event.target.value)}
            placeholder="Enter a company name..."
            className="h-16 rounded-2xl border border-white/10 bg-stone-950/70 px-5 text-lg text-stone-100 outline-none ring-0 transition focus:border-cyan-300/60"
          />
          <button
            type="submit"
            disabled={loading}
            className="h-16 rounded-2xl bg-gradient-to-r from-amber-400 via-orange-400 to-cyan-400 px-7 text-base font-semibold text-stone-950 transition hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-60"
          >
            Run Intelligence Swarm →
          </button>
        </form>

        {error ? <p className="mt-4 text-sm text-rose-300">{error}</p> : null}

        <div className="mt-12">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-semibold text-orange-50">Recent reports</h2>
            <p className="text-sm text-stone-400">Saved markdown briefings from previous runs</p>
          </div>
          <div className="grid gap-3">
            {reports.length === 0 ? (
              <div className="rounded-2xl border border-dashed border-white/10 bg-black/10 p-5 text-stone-400">
                No saved reports yet. Run your first company briefing above.
              </div>
            ) : (
              reports.map((report) => (
                <button
                  key={report.filename}
                  type="button"
                  onClick={() => onOpenReport(report)}
                  className="flex items-center justify-between rounded-2xl border border-white/10 bg-black/20 px-5 py-4 text-left transition hover:border-cyan-300/40 hover:bg-white/8"
                >
                  <span>
                    <span className="block text-base font-medium text-stone-100">{report.company}</span>
                    <span className="mt-1 block text-sm text-stone-400">{report.filename}</span>
                  </span>
                  <span className="rounded-full border border-amber-300/30 px-3 py-1 text-xs uppercase tracking-[0.2em] text-amber-100">
                    Open
                  </span>
                </button>
              ))
            )}
          </div>
        </div>
      </div>
    </section>
  )
}

