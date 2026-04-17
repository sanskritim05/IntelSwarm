const AGENTS = [
  { key: 'product', label: 'Product', icon: '✦' },
  { key: 'hiring', label: 'Hiring', icon: '◌' },
  { key: 'funding', label: 'Funding', icon: '⬢' },
  { key: 'news', label: 'News', icon: '✺' },
  { key: 'culture', label: 'Culture', icon: '◈' },
  { key: 'orchestrator', label: 'Orchestrator', icon: '◎' },
]

function progressPercent(progress) {
  const completeCount = AGENTS.filter((agent) => {
    const status = progress[agent.key]?.status
    return status === 'complete'
  }).length
  return Math.round((completeCount / AGENTS.length) * 100)
}

function statusStyles(status) {
  if (status === 'complete') {
    return 'border-emerald-400/30 bg-emerald-400/10 text-emerald-200'
  }
  if (status === 'rerunning') {
    return 'border-orange-400/30 bg-orange-400/10 text-orange-100'
  }
  if (status === 'running' || status === 'synthesizing') {
    return 'border-cyan-300/30 bg-cyan-300/10 text-cyan-100'
  }
  return 'border-white/10 bg-white/5 text-stone-300'
}

function statusLabel(status) {
  if (!status) return 'Waiting'
  if (status === 'synthesizing') return 'Synthesizing'
  return status.charAt(0).toUpperCase() + status.slice(1)
}

export default function AgentProgress({ company, progress, onCancelError, error }) {
  const percent = progressPercent(progress)

  return (
    <section className="mx-auto max-w-5xl px-6 py-12">
      <div className="rounded-[2rem] border border-white/10 bg-stone-950/50 p-8 shadow-[0_24px_80px_rgba(14,165,233,0.12)] backdrop-blur">
        <div className="flex flex-col gap-4 border-b border-white/10 pb-6 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-cyan-200/70">Research in progress</p>
            <h2 className="mt-2 text-4xl font-semibold text-orange-50">{company}</h2>
            <p className="mt-3 text-stone-400">
              This may take 2-4 minutes — agents are searching the web and reviewing each other&apos;s output.
            </p>
          </div>
          <div className="min-w-56">
            <div className="mb-2 flex justify-between text-sm text-stone-300">
              <span>Overall progress</span>
              <span>{percent}%</span>
            </div>
            <div className="h-3 rounded-full bg-white/10">
              <div
                className="h-3 rounded-full bg-gradient-to-r from-amber-400 to-cyan-400 transition-all duration-500"
                style={{ width: `${percent}%` }}
              />
            </div>
          </div>
        </div>

        {error ? (
          <div className="mt-6 flex items-center justify-between rounded-2xl border border-rose-300/20 bg-rose-300/10 px-4 py-3 text-sm text-rose-100">
            <span>{error}</span>
            <button type="button" className="font-medium underline" onClick={onCancelError}>
              Dismiss
            </button>
          </div>
        ) : null}

        <div className="mt-8 grid gap-4">
          {AGENTS.map((agent) => {
            const item = progress[agent.key] || { status: 'waiting' }
            return (
              <div
                key={agent.key}
                className="flex flex-col gap-3 rounded-2xl border border-white/10 bg-black/20 px-5 py-4 md:flex-row md:items-center md:justify-between"
              >
                <div className="flex items-center gap-4">
                  <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-white/8 text-lg text-orange-100">
                    {agent.icon}
                  </div>
                  <div>
                    <p className="text-base font-medium text-stone-100">{agent.label}</p>
                    <p className="text-sm text-stone-400">
                      {item.reason ? `Rerun reason: ${item.reason}` : 'Specialist agent status'}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`rounded-full border px-3 py-1 text-sm ${statusStyles(item.status)}`}>
                    {statusLabel(item.status)}
                  </span>
                  <span className="rounded-full border border-white/10 px-3 py-1 text-sm text-stone-200">
                    {item.score ? `Quality ${item.score}/10` : 'Quality -'}
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}

