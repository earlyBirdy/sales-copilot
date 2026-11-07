type Props = {
  value: string;
  onChange: (value: string) => void;
};

export function ToneSelector({ value, onChange }: Props) {
  return (
    <select
      className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    >
      <option>technical_commercial</option>
      <option>professional_neutral</option>
      <option>warm_consultative</option>
      <option>executive_brief</option>
      <option>social_light</option>
    </select>
  );
}
