type Props = {
  values: string[];
  onChange: (values: string[]) => void;
};

export function LengthSelector({ values, onChange }: Props) {
  const toggle = (value: string) => {
    if (values.includes(value)) {
      onChange(values.filter((v) => v !== value));
    } else {
      onChange([...values, value]);
    }
  };

  return (
    <div className="flex flex-wrap gap-2">
      {["short", "medium", "long"].map((item) => (
        <label key={item} className="inline-flex items-center gap-2 rounded-lg border border-slate-300 px-3 py-2 text-sm">
          <input type="checkbox" checked={values.includes(item)} onChange={() => toggle(item)} />
          {item}
        </label>
      ))}
    </div>
  );
}
