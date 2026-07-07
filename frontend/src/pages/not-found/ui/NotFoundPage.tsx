import { Link } from 'react-router-dom';

function NotFoundPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-background text-foreground text-center">
      <h1 className="text-6xl font-extrabold mb-4">404</h1>
      <p className="text-xl text-muted-foreground mb-6">Page not found.</p>
      <Link to="/" className="text-primary hover:underline">
        Back to Dashboard
      </Link>
    </div>
  );
}

export default NotFoundPage;
