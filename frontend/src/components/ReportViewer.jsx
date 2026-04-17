import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import SectionCard from './SectionCard'

const SECTION_META = [
  { slug: 'products-technology', title: 'Products & Technology', icon: '✦' },
  { slug: 'hiring-signals-team-growth', title: 'Hiring Signals & Team Growth', icon: '◌' },
  { slug: 'funding-financial-signals', title: 'Funding & Financial Signals', icon: '⬢' },
  { slug: 'recent-news-developments', title: 'Recent News & Developments', icon: '✺' },
  { slug: 'culture-employer-brand', title: 'Culture & Employer Brand', icon: '◈' },
  { slug: 'strategic-recommendations', title: 'Strategic Recommendations', icon: '◎' },
]

function splitSections(markdown) {
  const chunks = markdown.split(/^##\s+/m)
  if (chunks.length <= 1) {
    return [{ title: 'Briefing', content: markdown }]
  }

  const [intro, ...rest] = chunks
  const sections = []
  if (intro.trim()) {
    sections.push({ title: 'Overview', content: intro.trim() })
  }

  rest.forEach((chunk) => {
    const [headingLine, ...bodyLines] = chunk.split('\n')
    sections.push({
      title: headingLine.trim(),
      content: `## ${headingLine}\n${bodyLines.join('\n').trim()}`.trim(),
    })
  })

  return sections
}

export default function ReportViewer({ report, scores, onReset, company }) {
  const sections = splitSections(report)

  async function copyMarkdown() {
    await navigator.clipboard.writeText(report)
  }

  function downloadMarkdown() {
    const blob = new Blob([report], { type: 'text/markdown;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${company || 'intelswarm-report'}.md`
    link.click()
    URL.revokeObjectURL(url)
  }

  return (
    <section className="mx-auto grid max-w-7xl gap-6 px-6 py-10 lg:grid-cols-[260px_1fr]">
      <aside className="rounded-[1.75rem] border border-white/10 bg-black/20 p-5 lg:sticky lg:top-6 lg:h-fit">
        <p className="text-sm uppercase tracking-[0.3em] text-cyan-200/70">Briefing map</p>
        <div className="mt-5 grid gap-2">
          {SECTION_META.map((section) => (
            <a
              key={section.slug}
              href={`#${section.slug}`}
              className="rounded-2xl px-3 py-2 text-sm text-stone-300 transition hover:bg-white/8 hover:text-white"
            >
              {section.title}
            </a>
          ))}
        </div>
        <div className="mt-8 grid gap-3">
          <button
            type="button"
            onClick={copyMarkdown}
            className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm font-medium text-stone-100 transition hover:bg-white/10"
          >
            📋 Copy Markdown
          </button>
          <button
            type="button"
            onClick={downloadMarkdown}
            className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm font-medium text-stone-100 transition hover:bg-white/10"
          >
            ⬇️ Download .md
          </button>
          <button
            type="button"
            onClick={onReset}
            className="rounded-2xl bg-gradient-to-r from-amber-400 to-cyan-400 px-4 py-3 text-sm font-semibold text-stone-950"
          >
            🔄 Research Another Company
          </button>
        </div>
      </aside>

      <div className="grid gap-5">
        {sections.map((section) => {
          const normalizedTitle = section.title.toLowerCase()
          const meta = SECTION_META.find((item) => normalizedTitle.includes(item.title.toLowerCase()))
          const scoreKey = meta?.title.toLowerCase().includes('product')
            ? 'product'
            : meta?.title.toLowerCase().includes('hiring')
              ? 'hiring'
              : meta?.title.toLowerCase().includes('funding')
                ? 'funding'
                : meta?.title.toLowerCase().includes('news')
                  ? 'news'
                  : meta?.title.toLowerCase().includes('culture')
                    ? 'culture'
                    : undefined

          return (
            <div id={meta?.slug} key={`${section.title}-${section.content.length}`}>
              {scoreKey ? (
                <SectionCard
                  title={section.title}
                  icon={meta?.icon || '•'}
                  content={section.content}
                  qualityScore={scores?.[scoreKey]}
                />
              ) : (
                <section className="rounded-[1.75rem] border border-white/10 bg-black/20 p-6">
                  <div className="prose-intelswarm">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{section.content}</ReactMarkdown>
                  </div>
                </section>
              )}
            </div>
          )
        })}
      </div>
    </section>
  )
}
