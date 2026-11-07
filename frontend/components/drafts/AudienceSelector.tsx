type Props = {
  value: string;
  onChange: (value: string) => void;
};

export function AudienceSelector({ value, onChange }: Props) {
  return (
    <select
      className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    >
      <option>customer</option>
      <option>internal</option>
      <option>prospect</option>
      <option>partner</option>
      <option>linkedin_dm</option>
      <option>linkedin_post</option>
      <option>crm_note</option>
    </select>
  );
}
