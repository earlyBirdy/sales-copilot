type Props = { message: string };

export function ErrorState({ message }: Props) {
  if (!message) return null;
  return (
    <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 shadow-sm">
      <div className="font-medium">Something needs attention</div>
      <div className="mt-1">{message}</div>
    </div>
  );
}
