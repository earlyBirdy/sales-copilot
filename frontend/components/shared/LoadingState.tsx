type Props = { label?: string };

export function LoadingState({ label = "Loading..." }: Props) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center gap-3">
        <div className="h-4 w-4 animate-spin rounded-full border-2 border-slate-300 border-t-slate-700" />
        <div className="text-sm text-slate-600">{label}</div>
      </div>
    </div>
  );
}
