import { useState, useEffect, useCallback, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getPaper } from '../services/paper';
import { downloadReport } from '../services/report';
import {
  getQuiz, generateQuiz, deleteQuiz,
  getFlashcards, generateFlashcards, deleteFlashcards,
  getAdvice, generateAdvice, deleteAdvice
} from '../services/study';
import { getChatHistory, sendChatMessage } from '../services/chat';
import Navbar from '../components/Navbar';
import ReportViewer from '../components/ReportViewer';
import {
  ArrowLeft, Download, FileText, Brain, BookOpen,
  FlaskConical, ChevronLeft, ChevronRight, Sparkles,
  RotateCcw, CheckCircle, XCircle, Trophy, MessageSquare, Send, Trash2
} from 'lucide-react';
import toast from 'react-hot-toast';
import './PaperView.css';

const TABS = [
  { key: 'report', label: 'AI Report', icon: FileText },
  { key: 'quiz', label: 'Quiz', icon: Brain },
  { key: 'flashcards', label: 'Flashcards', icon: BookOpen },
  { key: 'study', label: 'Study Guide', icon: FlaskConical },
  { key: 'chat', label: 'Chat', icon: MessageSquare },
];

// ── Quiz Panel ────────────────────────────────────────────────────────────────
function QuizPanel({ paperId }) {
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    getQuiz(paperId).then(setQuiz).catch(() => {}).finally(() => setLoading(false));
  }, [paperId]);

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const data = await generateQuiz(paperId);
      setQuiz(data);
      setAnswers({});
      setSubmitted(false);
      toast.success('Quiz generated!');
    } catch {
      toast.error('Failed to generate quiz');
    } finally {
      setGenerating(false);
    }
  };

  const handleRegenerate = async () => {
    if (!window.confirm("Are you sure you want to delete and regenerate this quiz?")) return;
    setGenerating(true);
    try {
      await deleteQuiz(paperId);
      const data = await generateQuiz(paperId);
      setQuiz(data);
      setAnswers({});
      setSubmitted(false);
      toast.success('Quiz regenerated!');
    } catch {
      toast.error('Failed to regenerate quiz');
    } finally {
      setGenerating(false);
    }
  };

  const handleSelect = (qIdx, option) => {
    if (submitted) return;
    setAnswers(prev => ({ ...prev, [qIdx]: option }));
  };

  const handleSubmit = () => {
    if (Object.keys(answers).length < quiz.length) {
      toast.error('Please answer all questions first');
      return;
    }
    setSubmitted(true);
  };

  const handleRetry = () => {
    setAnswers({});
    setSubmitted(false);
  };

  const score = submitted ? quiz.filter((q, i) => answers[i] === q.correct_answer).length : 0;

  if (loading) return <div className="pv-panel-loading"><span className="spinner spinner-lg" /><p>Loading quiz…</p></div>;

  if (!quiz) return (
    <div className="pv-empty-state">
      <div className="pv-empty-icon"><Brain size={40} /></div>
      <h3>Test Your Knowledge</h3>
      <p>Generate a 5-question multiple-choice quiz powered by AI based on this paper.</p>
      <button className="btn btn-primary" onClick={handleGenerate} disabled={generating}>
        {generating ? <><span className="spinner" /> Generating…</> : <><Sparkles size={16} /> Generate Quiz</>}
      </button>
    </div>
  );

  return (
    <div className="pv-quiz">
      <div className="pv-panel-top-actions">
        <button className="btn btn-ghost btn-sm pv-regen-btn" onClick={handleRegenerate} disabled={generating}>
          {generating ? <span className="spinner" /> : <RotateCcw size={14} />} Regenerate Quiz
        </button>
      </div>
      {submitted && (
        <div className={`pv-score-banner ${score >= 4 ? 'score-great' : score >= 3 ? 'score-ok' : 'score-poor'}`}>
          <Trophy size={22} />
          <span>You scored <strong>{score}/{quiz.length}</strong> — {score === quiz.length ? '🎉 Perfect!' : score >= 3 ? 'Good job!' : 'Keep studying!'}</span>
          <button className="btn btn-ghost btn-sm" onClick={handleRetry}><RotateCcw size={14}/> Retry</button>
        </div>
      )}

      {quiz.map((q, i) => {
        const chosen = answers[i];
        const isCorrect = chosen === q.correct_answer;
        return (
          <div key={i} className={`pv-question ${submitted ? (isCorrect ? 'q-correct' : chosen ? 'q-wrong' : '') : ''}`}>
            <p className="pv-q-text"><span className="pv-q-num">{i + 1}</span>{q.question}</p>
            <div className="pv-options">
              {q.options.map((opt, j) => {
                let cls = 'pv-option';
                if (submitted) {
                  if (opt === q.correct_answer) cls += ' opt-correct';
                  else if (opt === chosen) cls += ' opt-wrong';
                } else if (opt === chosen) cls += ' opt-selected';
                return (
                  <button key={j} className={cls} onClick={() => handleSelect(i, opt)}>
                    <span className="opt-letter">{String.fromCharCode(65 + j)}</span>
                    {opt}
                    {submitted && opt === q.correct_answer && <CheckCircle size={16} className="opt-icon" />}
                    {submitted && opt === chosen && opt !== q.correct_answer && <XCircle size={16} className="opt-icon" />}
                  </button>
                );
              })}
            </div>
            {submitted && q.explanation && (
              <div className="pv-explanation">
                <strong>💡 Explanation:</strong> {q.explanation}
              </div>
            )}
          </div>
        );
      })}

      {!submitted && (
        <button className="btn btn-primary pv-submit-btn" onClick={handleSubmit}>
          Submit Answers
        </button>
      )}
    </div>
  );
}

// ── Flashcards Panel ──────────────────────────────────────────────────────────
function FlashcardsPanel({ paperId }) {
  const [cards, setCards] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [current, setCurrent] = useState(0);
  const [flipped, setFlipped] = useState(false);

  useEffect(() => {
    getFlashcards(paperId).then(setCards).catch(() => {}).finally(() => setLoading(false));
  }, [paperId]);

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const data = await generateFlashcards(paperId);
      setCards(data);
      setCurrent(0);
      setFlipped(false);
      toast.success('Flashcards generated!');
    } catch {
      toast.error('Failed to generate flashcards');
    } finally {
      setGenerating(false);
    }
  };

  const handleRegenerate = async () => {
    if (!window.confirm("Are you sure you want to delete and regenerate these flashcards?")) return;
    setGenerating(true);
    try {
      await deleteFlashcards(paperId);
      const data = await generateFlashcards(paperId);
      setCards(data);
      setCurrent(0);
      setFlipped(false);
      toast.success('Flashcards regenerated!');
    } catch {
      toast.error('Failed to regenerate flashcards');
    } finally {
      setGenerating(false);
    }
  };

  const prev = () => { setCurrent(c => Math.max(0, c - 1)); setFlipped(false); };
  const next = () => { setCurrent(c => Math.min(cards.length - 1, c + 1)); setFlipped(false); };

  if (loading) return <div className="pv-panel-loading"><span className="spinner spinner-lg" /><p>Loading flashcards…</p></div>;

  if (!cards) return (
    <div className="pv-empty-state">
      <div className="pv-empty-icon"><BookOpen size={40} /></div>
      <h3>Study Key Concepts</h3>
      <p>Generate 8–10 flashcards with key terms and definitions from this paper.</p>
      <button className="btn btn-primary" onClick={handleGenerate} disabled={generating}>
        {generating ? <><span className="spinner" /> Generating…</> : <><Sparkles size={16} /> Generate Flashcards</>}
      </button>
    </div>
  );

  const card = cards[current];
  return (
    <div className="pv-flashcards">
      <div className="pv-panel-top-actions">
        <button className="btn btn-ghost btn-sm pv-regen-btn" onClick={handleRegenerate} disabled={generating}>
          {generating ? <span className="spinner" /> : <RotateCcw size={14} />} Regenerate Flashcards
        </button>
      </div>
      <div className="pv-fc-counter">{current + 1} / {cards.length}</div>
      <div className={`pv-fc-scene`} onClick={() => setFlipped(f => !f)}>
        <div className={`pv-fc-card ${flipped ? 'is-flipped' : ''}`}>
          <div className="pv-fc-face pv-fc-front">
            <span className="pv-fc-label">Term</span>
            <p>{card.front}</p>
            <span className="pv-fc-hint">Click to reveal</span>
          </div>
          <div className="pv-fc-face pv-fc-back">
            <span className="pv-fc-label">Definition</span>
            <p>{card.back}</p>
          </div>
        </div>
      </div>
      <div className="pv-fc-nav">
        <button className="btn btn-ghost" onClick={prev} disabled={current === 0}><ChevronLeft size={20} /> Prev</button>
        <button className="btn btn-ghost" onClick={() => setFlipped(f => !f)}>
          <RotateCcw size={16} /> Flip
        </button>
        <button className="btn btn-ghost" onClick={next} disabled={current === cards.length - 1}>Next <ChevronRight size={20} /></button>
      </div>
      <div className="pv-fc-dots">
        {cards.map((_, i) => (
          <button key={i} className={`pv-fc-dot ${i === current ? 'active' : ''}`} onClick={() => { setCurrent(i); setFlipped(false); }} />
        ))}
      </div>
    </div>
  );
}

// ── Study Guide Panel ─────────────────────────────────────────────────────────
function StudyGuidePanel({ paperId }) {
  const [advice, setAdvice] = useState(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    getAdvice(paperId).then(setAdvice).catch(() => {}).finally(() => setLoading(false));
  }, [paperId]);

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const data = await generateAdvice(paperId);
      setAdvice(data);
      toast.success('Study guide generated!');
    } catch {
      toast.error('Failed to generate study guide');
    } finally {
      setGenerating(false);
    }
  };

  const handleRegenerate = async () => {
    if (!window.confirm("Are you sure you want to delete and regenerate this study guide?")) return;
    setGenerating(true);
    try {
      await deleteAdvice(paperId);
      const data = await generateAdvice(paperId);
      setAdvice(data);
      toast.success('Study guide regenerated!');
    } catch {
      toast.error('Failed to regenerate study guide');
    } finally {
      setGenerating(false);
    }
  };

  if (loading) return <div className="pv-panel-loading"><span className="spinner spinner-lg" /><p>Loading study guide…</p></div>;

  if (!advice) return (
    <div className="pv-empty-state">
      <div className="pv-empty-icon"><FlaskConical size={40} /></div>
      <h3>Get a Study Guide</h3>
      <p>Generate a structured guide with discussion questions, reading strategies, and practical exercises.</p>
      <button className="btn btn-primary" onClick={handleGenerate} disabled={generating}>
        {generating ? <><span className="spinner" /> Generating…</> : <><Sparkles size={16} /> Generate Study Guide</>}
      </button>
    </div>
  );

  return (
    <div className="pv-study-guide">
      <div className="pv-panel-top-actions" style={{ marginBottom: '12px' }}>
        <button className="btn btn-ghost btn-sm pv-regen-btn" onClick={handleRegenerate} disabled={generating}>
          {generating ? <span className="spinner" /> : <RotateCcw size={14} />} Regenerate Study Guide
        </button>
      </div>
      <div className="pv-report-body"><ReportViewer reportText={advice} title="Study Guide" /></div>
    </div>
  );
}

// ── Chat Panel ────────────────────────────────────────────────────────────────
function ChatPanel({ paperId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    getChatHistory(paperId)
      .then((history) => {
        const msgs = [];
        history.forEach((h) => {
          msgs.push({ id: `${h.id}-q`, sender: 'user', text: h.question });
          msgs.push({ id: `${h.id}-a`, sender: 'assistant', text: h.answer });
        });
        setMessages(msgs);
      })
      .catch(() => {
        toast.error('Failed to load chat history');
      })
      .finally(() => setLoading(false));
  }, [paperId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, sending]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || sending) return;

    const userText = input;
    setInput('');
    setSending(true);

    const userMsg = { id: Date.now() + '-user', sender: 'user', text: userText };
    setMessages((prev) => [...prev, userMsg]);

    try {
      const res = await sendChatMessage(paperId, userText);
      const assistantMsg = { id: Date.now() + '-assistant', sender: 'assistant', text: res.answer };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to send message');
    } finally {
      setSending(false);
    }
  };

  const renderMessageText = (text) => {
    if (!text) return null;
    const lines = text.split('\n');
    return lines.map((line, idx) => {
      const boldRegex = /\*\*(.*?)\*\*/g;
      const parts = [];
      let lastIndex = 0;
      let match;
      while ((match = boldRegex.exec(line)) !== null) {
        if (match.index > lastIndex) {
          parts.push(line.substring(lastIndex, match.index));
        }
        parts.push(<strong key={match.index}>{match[1]}</strong>);
        lastIndex = boldRegex.lastIndex;
      }
      if (lastIndex < line.length) {
        parts.push(line.substring(lastIndex));
      }

      if (line.trim().startsWith('- ') || line.trim().startsWith('• ')) {
        return (
          <li key={idx} style={{ marginLeft: '16px', listStyleType: 'disc', marginBottom: '4px' }}>
            {parts.length > 0 ? parts : line.replace(/^[-•]\s/, '')}
          </li>
        );
      }
      return <p key={idx} style={{ marginBottom: '8px', minHeight: '1em' }}>{parts.length > 0 ? parts : line}</p>;
    });
  };

  if (loading) return <div className="pv-panel-loading"><span className="spinner spinner-lg" /><p>Loading chat history…</p></div>;

  return (
    <div className="pv-chat-container">
      <div className="pv-chat-messages">
        {messages.length === 0 && (
          <div className="pv-empty-state" style={{ padding: '40px 20px' }}>
            <div className="pv-empty-icon"><MessageSquare size={40} /></div>
            <h3>Chat with Paper</h3>
            <p>Ask any question about the methodology, results, or limitations of this paper. The AI will answer using RAG context retrieval.</p>
          </div>
        )}
        {messages.map((m) => (
          <div key={m.id} className={`pv-chat-msg-row ${m.sender === 'user' ? 'msg-user' : 'msg-assistant'}`}>
            <div className="pv-chat-bubble">
              {renderMessageText(m.text)}
            </div>
          </div>
        ))}
        {sending && (
          <div className="pv-chat-msg-row msg-assistant">
            <div className="pv-chat-bubble typing-bubble">
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="pv-chat-input-bar">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about this paper..."
          className="pv-chat-input"
          disabled={sending}
        />
        <button type="submit" className="btn btn-primary pv-chat-send-btn" disabled={!input.trim() || sending}>
          <Send size={16} />
        </button>
      </form>
    </div>
  );
}

// ── Main PaperView ────────────────────────────────────────────────────────────
export default function PaperView() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);
  const [activeTab, setActiveTab] = useState('report');

  useEffect(() => {
    getPaper(id).then(setData).catch(() => {
      toast.error('Paper not found');
      navigate('/dashboard');
    }).finally(() => setLoading(false));
  }, [id]);

  const handleDownload = async () => {
    setDownloading(true);
    try {
      await downloadReport(id, data?.paper?.title);
      toast.success('Report PDF downloaded');
    } catch {
      toast.error('Download failed');
    } finally {
      setDownloading(false);
    }
  };

  if (loading) return (
    <div className="app-layout">
      <Navbar />
      <main className="page-content">
        <div className="pv-loading"><span className="spinner spinner-lg" /><p>Loading paper…</p></div>
      </main>
    </div>
  );

  const { paper, report } = data || {};

  return (
    <div className="app-layout">
      <div className="orb orb-1" />
      <Navbar />
      <main className="page-content">
        {/* Header */}
        <div className="pv-topbar fade-up">
          <button className="btn btn-ghost btn-sm pv-back" onClick={() => navigate('/dashboard')}>
            <ArrowLeft size={15} /> Dashboard
          </button>
          <h1 className="pv-title">{paper?.title || 'Untitled Paper'}</h1>
        </div>

        <div className="pv-layout">
          {/* Left — Tabbed Panel */}
          <section className="pv-report-panel glass-card fade-up">
            {/* Tabs */}
            <div className="pv-tabs">
              {TABS.map(({ key, label, icon: Icon }) => (
                <button
                  key={key}
                  className={`pv-tab ${activeTab === key ? 'active' : ''}`}
                  onClick={() => setActiveTab(key)}
                >
                  <Icon size={15} />
                  {label}
                </button>
              ))}
            </div>

            {/* Tab Content */}
            <div className="pv-tab-content">
              {activeTab === 'report' && (
                <div className="pv-report-body">
                  <ReportViewer reportText={report?.report_text} title={paper?.title} />
                </div>
              )}
              {activeTab === 'quiz' && <QuizPanel paperId={id} />}
              {activeTab === 'flashcards' && <FlashcardsPanel paperId={id} />}
              {activeTab === 'study' && <StudyGuidePanel paperId={id} />}
              {activeTab === 'chat' && <ChatPanel paperId={id} />}
            </div>
          </section>

          {/* Right — Sidebar */}
          <aside className="pv-sidebar fade-up" style={{ animationDelay: '0.1s' }}>
            {/* Download */}
            <div className="pv-action-card glass-card">
              <button
                className="btn btn-primary btn-lg pv-action-btn"
                onClick={handleDownload}
                disabled={downloading}
              >
                {downloading ? <span className="spinner" /> : <Download size={18} />}
                Download Report PDF
              </button>
            </div>

            {/* Phase 2 Action Shortcuts */}
            <div className="pv-action-card glass-card">
              <div className="pv-panel-header" style={{ marginBottom: '12px' }}>
                <Sparkles size={15} color="var(--accent-bright)" />
                <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-secondary)' }}>AI Study Tools</span>
              </div>
              <div className="pv-shortcut-list">
                <button className={`pv-shortcut-btn ${activeTab === 'quiz' ? 'active' : ''}`} onClick={() => setActiveTab('quiz')}>
                  <Brain size={16} /> Generate Quiz
                </button>
                <button className={`pv-shortcut-btn ${activeTab === 'flashcards' ? 'active' : ''}`} onClick={() => setActiveTab('flashcards')}>
                  <BookOpen size={16} /> Flashcards
                </button>
                <button className={`pv-shortcut-btn ${activeTab === 'study' ? 'active' : ''}`} onClick={() => setActiveTab('study')}>
                  <FlaskConical size={16} /> Study Guide
                </button>
                <button className={`pv-shortcut-btn ${activeTab === 'chat' ? 'active' : ''}`} onClick={() => setActiveTab('chat')}>
                  <MessageSquare size={16} /> Chat with Paper
                </button>
              </div>
            </div>

            {/* Paper meta */}
            {paper?.file_url && (
              <div className="pv-meta-card glass-card">
                <p className="pv-meta-label">Source PDF</p>
                <a
                  href={paper.file_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn btn-ghost btn-sm"
                  style={{ width: '100%', justifyContent: 'center' }}
                >
                  <FileText size={14} /> View Original
                </a>
              </div>
            )}
          </aside>
        </div>
      </main>
    </div>
  );
}
