import { SelectedDraftBadge } from "../drafts/SelectedDraftBadge";

type Props = {
  label: string;
};

export function ActiveDraftBadge({ label }: Props) {
  return <SelectedDraftBadge label={label} />;
}
