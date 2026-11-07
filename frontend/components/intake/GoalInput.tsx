type Props = {
  value: string;
  onChange: (value: string) => void;
};

export function GoalInput({ value, onChange }: Props) {
  return (
    <input
      className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
      placeholder="Goal, e.g. Create customer and LinkedIn drafts"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    />
  );
}
