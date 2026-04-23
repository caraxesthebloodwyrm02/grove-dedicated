import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { error: Error | null }
> {
  public state: { error: Error | null } = { error: null };

  public static getDerivedStateFromError(error: Error) {
    return { error };
  }

  public componentDidCatch(error: Error) {
    // eslint-disable-next-line no-console
    console.error('Hogwarts Visualizer crashed:', error);
  }

  public render() {
    if (this.state.error) {
      return (
        <div
          style={{
            padding: 16,
            color: '#e5e5e5',
            fontFamily:
              'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace',
          }}
        >
          <div style={{ fontSize: 14, fontWeight: 700, marginBottom: 8 }}>
            Hogwarts Visualizer crashed
          </div>
          <div style={{ fontSize: 12, opacity: 0.8, marginBottom: 12 }}>
            Open DevTools Console for details.
          </div>
          <pre style={{ fontSize: 12, whiteSpace: 'pre-wrap' }}>
            {String(this.state.error.stack ?? this.state.error.message)}
          </pre>
        </div>
      );
    }

    return this.props.children;
  }
}

const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error('Could not find root element to mount to');
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>,
);
