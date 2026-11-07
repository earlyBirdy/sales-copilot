type Props = {
  value: string;
  onChange: (value: string) => void;
};

export function SourceTypeSelect({ value, onChange }: Props) {
  return (
    <select
      className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    >
      <option value="email">Email</option>
      <option value="article">Article</option>
      <option value="press_release">Press release</option>
      <option value="announcement">Announcement</option>
      <option value="note">Note</option>
    </select>
  );
}
