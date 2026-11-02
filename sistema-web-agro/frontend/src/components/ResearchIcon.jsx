import React from 'react'

const paths = {
  dashboard: 'M3 3h7v7H3z M14 3h7v4h-7z M14 11h7v10h-7z M3 14h7v7H3z',
  fob: 'M3 6h18v12H3z M3 10c3 0 4-1 4-4 M17 6c0 3 1 4 4 4 M3 14c3 0 4 1 4 4 M17 18c0-3 1-4 4-4 M12 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6',
  volume: 'M5 8h14l2 13H3z M9 8V6a3 3 0 0 1 6 0v2 M9 14h6',
  markets: 'M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0 M3 12h18 M12 3c-5 5-5 13 0 18 M12 3c5 5 5 13 0 18',
  coverage: 'M4 4h16v16H4z M4 9h16 M9 4v16 M9 14h11 M14 9v11',
  unit: 'M4 19V5 M4 19h17 M7 15l4-5 4 2 5-7',
  source: 'M4 5c4-2 6-2 8 0 2-2 4-2 8 0v15c-4-2-6-2-8 0-2-2-4-2-8 0z M12 5v15',
  info: 'M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0 M12 11v6 M12 7v1',
}
export default function ResearchIcon({ name, className = '' }) {
  return <svg className={className} width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false"><path d={paths[name] || paths.unit} /></svg>
}
