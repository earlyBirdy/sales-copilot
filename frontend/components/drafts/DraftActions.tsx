const passiveActions = ["Copy", "Pin", "Rewrite", "Shorten", "Soften", "More technical", "More commercial"];

type Props = {
  onSelect?: () => void;
  disabled?: boolean;
};

export function DraftActions({ onSelect, disabled = false }: Props) {
  return (
    <div className="mt-3 flex flex-wrap gap-2">
      <button
        className="rounded-full border border-slate-300 px-2.5 py-1 text-xs text-slate-700 disabled:opacity-50"
        onClick={onSelect}
        disabled={disabled}
      >
        Select
      </button>
      {passiveActions.map((action) => (
        <button key={action} className="rounded-full border border-slate-300 px-2.5 py-1 text-xs text-slate-700">
          {action}
        </button>
      ))}
    </div>
  );
}
