type Props = {
  approvalState?: string;
};

export function LeftSidebar({ approvalState = "drafted" }: Props) {
  const items = ["New Source", "Sessions", "Templates", "History"];
  return (
    <aside className="hidden w-56 shrink-0 rounded-xl border border-slate-200 bg-white p-3 shadow-sm lg:block">
      <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-500">Workspace</div>
      <div className="mb-3 rounded-lg border border-slate-200 bg-slate-50 p-2 text-xs text-slate-600">
        Approval state: <span className="font-semibold">{approvalState}</span>
      </div>
      <nav className="space-y-1">
        {items.map((item) => (
          <button key={item} className="block w-full rounded-lg px-3 py-2 text-left text-sm text-slate-700 hover:bg-slate-100">
            {item}
          </button>
        ))}
      </nav>
    </aside>
  );
}
