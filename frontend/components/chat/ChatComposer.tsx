type Props = {
  value: string;
  onChange: (value: string) => void;
  onSend: () => void;
  disabled?: boolean;
};

export function ChatComposer({ value, onChange, onSend, disabled = false }: Props) {
  return (
    <div className="space-y-2">
      <textarea
        className="min-h-[100px] w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
        placeholder="Revise the selected draft..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
      <button className="rounded-lg bg-slate-900 px-3 py-2 text-sm text-white disabled:opacity-50" onClick={onSend} disabled={disabled}>
        Send
      </button>
    </div>
  );
}
