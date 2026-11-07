type Props = {
  onClick: () => void;
  disabled?: boolean;
};

export function GenerateDraftsButton({ onClick, disabled = false }: Props) {
  return (
    <button
      className="rounded-lg bg-slate-900 px-3 py-2 text-sm text-white disabled:opacity-50"
      onClick={onClick}
      disabled={disabled}
    >
      Generate Drafts
    </button>
  );
}
