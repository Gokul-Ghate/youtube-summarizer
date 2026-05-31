import { useState } from "react"

const API_BASE = "http://127.0.0.1:8000"

export default function App() {
  const [url, setUrl] = useState("")
  const [language, setLanguage] = useState("en")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [question, setQuestion] = useState("")
  const [answer, setAnswer] = useState(null)
  const [askingQuestion, setAskingQuestion] = useState(false)

  async function handleSummarize() {
    if (!url.trim()) return
    setLoading(true)
    setError(null)
    setResult(null)
    setAnswer(null)

    try {
      const response = await fetch(`${API_BASE}/summarize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, language })
      })

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || "Something went wrong")
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleAskQuestion() {
    if (!question.trim() || !url.trim()) return
    setAskingQuestion(true)
    setAnswer(null)

    try {
      const response = await fetch(`${API_BASE}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, question, language })
      })

      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || "Something went wrong")
      }

      const data = await response.json()
      setAnswer(data.answer)
    } catch (err) {
      setError(err.message)
    } finally {
      setAskingQuestion(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white px-4 py-10">
      <div className="max-w-3xl mx-auto space-y-8">

        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-white">YouTube Summarizer</h1>
          <p className="text-gray-400">Paste a YouTube URL to get an AI-powered summary, sentiment and chapters</p>
        </div>

        {/* Input */}
        <div className="bg-gray-900 rounded-2xl p-6 space-y-4">
          <input
            type="text"
            placeholder="https://www.youtube.com/watch?v=..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full bg-gray-800 text-white placeholder-gray-500 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
          />
          <div className="flex gap-3">
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-gray-800 text-white rounded-xl px-4 py-3 outline-none"
            >
              <option value="en">English</option>
              <option value="hi">Hindi</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
            </select>
            <button
              onClick={handleSummarize}
              disabled={loading || !url.trim()}
              className="flex-1 bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:cursor-not-allowed text-white font-semibold rounded-xl px-6 py-3 transition-colors"
            >
              {loading ? "Analyzing..." : "Summarize"}
            </button>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="bg-red-900/40 border border-red-500 text-red-300 rounded-xl px-4 py-3">
            {error}
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="space-y-6">

            {/* Summary */}
            <div className="bg-gray-900 rounded-2xl p-6 space-y-3">
              <h2 className="text-lg font-semibold text-blue-400">Summary</h2>
              <p className="text-gray-300 whitespace-pre-line">{result.summary}</p>
            </div>

            {/* Sentiment */}
            <div className="bg-gray-900 rounded-2xl p-6 space-y-3">
              <h2 className="text-lg font-semibold text-purple-400">Sentiment Analysis</h2>
              <p className="text-gray-300 whitespace-pre-line">{result.sentiment}</p>
            </div>

            {/* Chapters */}
            <div className="bg-gray-900 rounded-2xl p-6 space-y-3">
              <h2 className="text-lg font-semibold text-green-400">Chapters</h2>
              <p className="text-gray-300 whitespace-pre-line">{result.chapters}</p>
            </div>

            {/* Q&A */}
            <div className="bg-gray-900 rounded-2xl p-6 space-y-4">
              <h2 className="text-lg font-semibold text-yellow-400">Ask a Question</h2>
              <div className="flex gap-3">
                <input
                  type="text"
                  placeholder="What is this video about?"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleAskQuestion()}
                  className="flex-1 bg-gray-800 text-white placeholder-gray-500 rounded-xl px-4 py-3 outline-none focus:ring-2 focus:ring-yellow-500"
                />
                <button
                  onClick={handleAskQuestion}
                  disabled={askingQuestion || !question.trim()}
                  className="bg-yellow-600 hover:bg-yellow-500 disabled:bg-gray-700 disabled:cursor-not-allowed text-white font-semibold rounded-xl px-6 py-3 transition-colors"
                >
                  {askingQuestion ? "Thinking..." : "Ask"}
                </button>
              </div>
              {answer && (
                <div className="bg-gray-800 rounded-xl px-4 py-3 text-gray-300 whitespace-pre-line">
                  {answer}
                </div>
              )}
            </div>

          </div>
        )}

      </div>
    </div>
  )
}