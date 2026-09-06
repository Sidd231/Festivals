export default function ErrorBox({ message }) {
  if (!message) return null;
  return (
    <div className="rounded border border-danger/30 bg-danger/5 px-4 py-3 text-sm text-danger">
      {message}
    </div>
  );
}
