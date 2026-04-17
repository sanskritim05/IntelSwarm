import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

export default function SectionCard({ title, icon, content, qualityScore }) {
  return (
    <section className="rounded-[1.75rem] border border-white/10 bg-black/20 p-6">
      <div className="mb-4 flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-white/8 text-orange-100">
            {icon}
          </div>
          <h3 className="text-xl font-semibold text-orange-50">{title}</h3>
        </div>
        {qualityScore ? (
          <span className="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1 text-sm text-cyan-100">
            Research quality: {qualityScore}/10
          </span>
        ) : null}
      </div>
      <div className="prose-intelswarm">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
      </div>
    </section>
  )
}

