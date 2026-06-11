import './ReportViewer.css';

function parseSection(text) {
  const lines = text.split('\n');
  const sections = [];
  let current = null;

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    if (trimmed.startsWith('## ')) {
      if (current) sections.push(current);
      current = { heading: trimmed.slice(3), content: [] };
    } else if (current) {
      current.content.push(trimmed);
    } else {
      if (!current) current = { heading: null, content: [] };
      current.content.push(trimmed);
    }
  }
  if (current) sections.push(current);
  return sections;
}

function renderLine(line, idx) {
  if (line.startsWith('- ') || line.startsWith('• ')) {
    return (
      <li key={idx} className="report-bullet">{line.replace(/^[-•]\s/, '')}</li>
    );
  }
  return <p key={idx} className="report-para">{line}</p>;
}

export default function ReportViewer({ reportText, title }) {
  if (!reportText) {
    return (
      <div className="report-empty">
        <p>No report generated yet.</p>
      </div>
    );
  }

  const sections = parseSection(reportText);

  return (
    <div className="report-viewer">
      {title && <h1 className="report-main-title">{title}</h1>}

      {sections.map((section, i) => (
        <div key={i} className="report-section fade-up" style={{ animationDelay: `${i * 0.06}s` }}>
          {section.heading && (
            <h2 className="report-section-heading">{section.heading}</h2>
          )}
          <div className="report-section-body">
            {section.content.some(l => l.startsWith('- ') || l.startsWith('• ')) ? (
              <ul className="report-list">
                {section.content.map((l, j) => renderLine(l, j))}
              </ul>
            ) : (
              section.content.map((l, j) => renderLine(l, j))
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
