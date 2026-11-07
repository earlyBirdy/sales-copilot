import { SectionCard } from "../shared/SectionCard";
import { Chip } from "../shared/Chip";
import { DraftActions } from "./DraftActions";

type Props = {
  draft: {
    draft_id: string;
    length: string;
    text: string;
  };
  selected?: boolean;
  onSelect?: () => void;
  disabled?: boolean;
};

export function DraftCard({ draft, selected = false, onSelect, disabled = false }: Props) {
  return (
    <SectionCard title="Draft">
      <div className="flex items-center gap-2">
        <Chip label={draft.length} />
        {selected ? <Chip label="selected" /> : null}
      </div>
      <p className="whitespace-pre-wrap text-sm text-slate-800">{draft.text}</p>
      <DraftActions onSelect={onSelect} disabled={disabled} />
    </SectionCard>
  );
}
