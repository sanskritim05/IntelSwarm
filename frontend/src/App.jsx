import { useEffect, useState } from 'react'
import { fetchReport, fetchReports, startResearch, streamResearch } from './api/client'
import AgentProgress from './components/AgentProgress'
import CompanyInput from './components/CompanyInput'
import ReportViewer from './components/ReportViewer'

const INITIAL_PROGRESS = {
  product: { status: 'waiting', score: null, reason: null },
  hiring: { status: 'waiting', score: null, reason: null },
  funding: { status: 'waiting', score: null, reason: null },
  news: { status: 'waiting', score: null, reason: null },
  culture: { status: 'waiting', score: null, reason: null },
  orchestrator: { status: 'waiting', score: null, reason: null },
}

export default function App() {
  const [view, setView] = useState('input')
  const [company, setCompany] = useState('')
  const [jobId, setJobId] = useState(null)
  const [progress, setProgress] = useState(INITIAL_PROGRESS)
  const [report, setReport] = useState('')
  const [scores, setScores] = useState({})
  const [reports, setReports] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchReports()
      .then((data) => setReports(data.reports || []))
      .catch(() => {})
  }, [])

  useEffect(() => {
    if (!jobId) return undefined

    const stop = streamResearch(jobId, {
      onEvent: (event) => {
        if (event.agent) {
          setProgress((current) => ({
            ...current,
            [event.agent]: {
              status: event.status || current[event.agent]?.status || 'waiting',
              score: event.score ?? current[event.agent]?.score ?? null,
              reason: event.reason ?? null,
            },
          }))
        }
      },
      onDone: (event) => {
        setReport(event.report || '')
        setScores(event.scores || {})
        setView('report')
        setJobId(null)
        setLoading(false)
        fetchReports()
          .then((data) => setReports(data.reports || []))
          .catch(() => {})
      },
      onError: (streamError) => {
        setError(streamError.message)
        setLoading(false)
      },
    })

    return stop
  }, [jobId])

  async function handleSubmit(event) {
    event.preventDefault()
    if (!company.trim()) {
      setError('Enter a company name to begin.')
      return
    }

    try {
      setLoading(true)
      setError('')
      setProgress(INITIAL_PROGRESS)
      setReport('')
      setScores({})
      const data = await startResearch(company.trim())
      setJobId(data.job_id)
      setView('research')
    } catch (submitError) {
      setLoading(false)
      setError(submitError.message)
    }
  }

  async function handleOpenReport(savedReport) {
    try {
      const markdown = await fetchReport(savedReport.filename)
      setCompany(savedReport.company)
      setReport(markdown)
      setScores({})
      setView('report')
    } catch (openError) {
      setError(openError.message)
    }
  }

  function reset() {
    setView('input')
    setCompany('')
    setJobId(null)
    setProgress(INITIAL_PROGRESS)
    setReport('')
    setScores({})
    setError('')
    setLoading(false)
  }

  return (
    <main className="min-h-screen pb-12 text-stone-100">
      <div className="mx-auto max-w-7xl">
        {view === 'input' ? (
          <CompanyInput
            company={company}
            setCompany={setCompany}
            onSubmit={handleSubmit}
            loading={loading}
            reports={reports}
            onOpenReport={handleOpenReport}
            error={error}
          />
        ) : null}

        {view === 'research' ? (
          <AgentProgress
            company={company}
            progress={progress}
            error={error}
            onCancelError={() => setError('')}
          />
        ) : null}

        {view === 'report' ? (
          <ReportViewer report={report} scores={scores} onReset={reset} company={company} />
        ) : null}
      </div>
    </main>
  )
}

