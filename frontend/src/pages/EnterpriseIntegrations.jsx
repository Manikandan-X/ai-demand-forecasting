import { useState, useEffect } from "react";

// ─── API base (matches your Vite proxy) ───
const API = "http://localhost:8000";

const token = () => localStorage.getItem("token");

const apiFetch = async (path, opts = {}) => {
  const res = await fetch(`${API}${path}`, {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token()}`,
      ...opts.headers,
    },
    ...opts,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
};

// ─── Icon components ───────────────────────
const Icon = ({ d, size = 18, color = "currentColor" }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
    stroke={color} strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
    <path d={d} />
  </svg>
);

const ICONS = {
  plug:    "M18 13v6a2 2 0 01-2 2H5a2 2 0 01-2-2V8a2 2 0 012-2h6M15 3h6v6M10 14L21 3",
  webhook: "M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07 19.5 19.5 0 01-6-6 19.79 19.79 0 01-3.07-8.67A2 2 0 014.11 2h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L8.09 9.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z",
  key:     "M21 2l-2 2m-7.61 7.61a5.5 5.5 0 11-7.778 7.778 5.5 5.5 0 017.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4",
  check:   "M20 6L9 17l-5-5",
  x:       "M18 6L6 18M6 6l12 12",
  refresh: "M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0114.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0020.49 15",
  trash:   "M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a1 1 0 011-1h4a1 1 0 011 1v2",
  plus:    "M12 5v14M5 12h14",
  zap:     "M13 2L3 14h9l-1 8 10-12h-9l1-8z",
  eye:     "M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8zM12 9a3 3 0 100 6 3 3 0 000-6z",
  log:     "M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8zM14 2v6h6M16 13H8M16 17H8M10 9H8",
  copy:    "M8 17.929H6c-1.105 0-2-.912-2-2.036V5.036C4 3.91 4.895 3 6 3h8c1.105 0 2 .911 2 2.036v1.866m-6 .17h8c1.105 0 2 .91 2 2.035v10.857C20 21.09 19.105 22 18 22h-8c-1.105 0-2-.911-2-2.036V9.107c0-1.124.895-2.036 2-2.036z",
};

// ─── Colours / status ──────────────────────
const STATUS_COLOR = {
  active:   { bg: "#0d2e1a", text: "#4ade80", dot: "#22c55e" },
  inactive: { bg: "#1e1b2e", text: "#a78bfa", dot: "#8b5cf6" },
  error:    { bg: "#2d1515", text: "#f87171", dot: "#ef4444" },
};

const TYPE_COLOR = {
  erp:       "#3b82f6",
  crm:       "#8b5cf6",
  ecommerce: "#f59e0b",
  custom:    "#14b8a6",
};

// ─── Toast ─────────────────────────────────
const Toast = ({ msg, type, onClose }) => {
  useEffect(() => { const t = setTimeout(onClose, 3500); return () => clearTimeout(t); }, []);
  return (
    <div style={{
      position: "fixed", bottom: 28, right: 28, zIndex: 9999,
      background: type === "error" ? "#2d1515" : "#0d2e1a",
      border: `1px solid ${type === "error" ? "#ef4444" : "#22c55e"}`,
      color: type === "error" ? "#f87171" : "#4ade80",
      padding: "12px 20px", borderRadius: 10, fontSize: 13,
      fontFamily: "'DM Mono', monospace", maxWidth: 340,
      boxShadow: "0 8px 32px rgba(0,0,0,0.5)",
      animation: "slideIn 0.25s ease",
    }}>{msg}</div>
  );
};

// ─── Modal shell ───────────────────────────
const Modal = ({ title, onClose, children }) => (
  <div style={{
    position: "fixed", inset: 0, background: "rgba(0,0,0,0.75)",
    display: "flex", alignItems: "center", justifyContent: "center",
    zIndex: 1000, padding: 20,
  }} onClick={(e) => e.target === e.currentTarget && onClose()}>
    <div style={{
      background: "#111827", border: "1px solid #1f2937",
      borderRadius: 14, padding: 28, width: "100%", maxWidth: 520,
      maxHeight: "90vh", overflowY: "auto",
      fontFamily: "'DM Sans', sans-serif",
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 22 }}>
        <span style={{ color: "#f9fafb", fontWeight: 700, fontSize: 17 }}>{title}</span>
        <button onClick={onClose} style={{ background: "none", border: "none", color: "#6b7280", cursor: "pointer" }}>
          <Icon d={ICONS.x} />
        </button>
      </div>
      {children}
    </div>
  </div>
);

// ─── Form field ────────────────────────────
const Field = ({ label, children }) => (
  <div style={{ marginBottom: 16 }}>
    <label style={{ display: "block", color: "#9ca3af", fontSize: 12, marginBottom: 6, textTransform: "uppercase", letterSpacing: "0.05em" }}>{label}</label>
    {children}
  </div>
);

const Input = (props) => (
  <input {...props} style={{
    width: "100%", background: "#1f2937", border: "1px solid #374151",
    borderRadius: 8, padding: "9px 12px", color: "#f9fafb", fontSize: 14,
    outline: "none", boxSizing: "border-box",
    fontFamily: "'DM Sans', sans-serif",
    ...props.style,
  }} />
);

const Select = ({ value, onChange, options }) => (
  <select value={value} onChange={onChange} style={{
    width: "100%", background: "#1f2937", border: "1px solid #374151",
    borderRadius: 8, padding: "9px 12px", color: "#f9fafb", fontSize: 14,
    outline: "none", boxSizing: "border-box",
    fontFamily: "'DM Sans', sans-serif",
  }}>
    {options.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
  </select>
);

const Btn = ({ children, onClick, variant = "primary", disabled, style: sx }) => {
  const styles = {
    primary:  { background: "#2563eb", color: "#fff" },
    danger:   { background: "#dc2626", color: "#fff" },
    ghost:    { background: "#1f2937", color: "#9ca3af" },
    success:  { background: "#16a34a", color: "#fff" },
  };
  return (
    <button onClick={onClick} disabled={disabled} style={{
      ...styles[variant], border: "none", borderRadius: 8,
      padding: "9px 16px", fontSize: 13, fontWeight: 600,
      cursor: disabled ? "not-allowed" : "pointer", opacity: disabled ? 0.6 : 1,
      display: "flex", alignItems: "center", gap: 6,
      fontFamily: "'DM Sans', sans-serif", transition: "opacity 0.15s",
      ...sx,
    }}>{children}</button>
  );
};

// ─────────────────────────────────────────────────────────────
// TAB: INTEGRATIONS
// ─────────────────────────────────────────────────────────────
function IntegrationsTab() {
  const [list, setList]         = useState([]);
  const [stats, setStats]       = useState(null);
  const [loading, setLoading]   = useState(true);
  const [showAdd, setShowAdd]   = useState(false);
  const [showLogs, setShowLogs] = useState(null);   // integration obj
  const [logs, setLogs]         = useState([]);
  const [toast, setToast]       = useState(null);
  const [busy, setBusy]         = useState({});

  const toast$ = (msg, type = "success") => setToast({ msg, type });

  const load = async () => {
    setLoading(true);
    try {
      const [data, s] = await Promise.all([
        apiFetch("/integrations"),
        apiFetch("/integrations/stats"),
      ]);
      setList(data);
      setStats(s);
    } catch (e) { toast$(e.message, "error"); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const test = async (id) => {
    setBusy(b => ({ ...b, [id]: "test" }));
    try {
      const r = await apiFetch(`/integrations/${id}/test`, { method: "POST" });
      toast$(r.message, r.success ? "success" : "error");
      load();
    } catch (e) { toast$(e.message, "error"); }
    finally { setBusy(b => ({ ...b, [id]: null })); }
  };

  const sync = async (id) => {
    setBusy(b => ({ ...b, [id]: "sync" }));
    try {
      const r = await apiFetch(`/integrations/${id}/sync`, { method: "POST" });
      toast$(r.message, r.success ? "success" : "error");
    } catch (e) { toast$(e.message, "error"); }
    finally { setBusy(b => ({ ...b, [id]: null })); }
  };

  const del = async (id) => {
    if (!confirm("Delete this integration?")) return;
    try {
      await apiFetch(`/integrations/${id}`, { method: "DELETE" });
      toast$("Integration deleted");
      load();
    } catch (e) { toast$(e.message, "error"); }
  };

  const openLogs = async (integration) => {
    setShowLogs(integration);
    const data = await apiFetch(`/integrations/${integration.id}/logs`);
    setLogs(data);
  };

  return (
    <div>
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}

      {/* Stats Row */}
      {stats && (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 14, marginBottom: 24 }}>
          {[
            { label: "Total", value: stats.total, color: "#60a5fa" },
            { label: "Active", value: stats.active, color: "#4ade80" },
            { label: "Inactive", value: stats.inactive, color: "#a78bfa" },
            { label: "Errors", value: stats.error, color: "#f87171" },
          ].map(s => (
            <div key={s.label} style={{
              background: "#111827", border: "1px solid #1f2937",
              borderRadius: 10, padding: "16px 20px",
            }}>
              <div style={{ color: "#6b7280", fontSize: 11, textTransform: "uppercase", letterSpacing: "0.08em" }}>{s.label}</div>
              <div style={{ color: s.color, fontSize: 28, fontWeight: 700, marginTop: 4 }}>{s.value}</div>
            </div>
          ))}
        </div>
      )}

      {/* Toolbar */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <span style={{ color: "#9ca3af", fontSize: 13 }}>{list.length} integration(s) configured</span>
        <Btn onClick={() => setShowAdd(true)}>
          <Icon d={ICONS.plus} size={15} /> Add Integration
        </Btn>
      </div>

      {/* List */}
      {loading ? (
        <div style={{ color: "#6b7280", textAlign: "center", padding: 48 }}>Loading…</div>
      ) : list.length === 0 ? (
        <div style={{
          background: "#111827", border: "1px dashed #374151",
          borderRadius: 12, padding: 48, textAlign: "center", color: "#6b7280",
        }}>
          <div style={{ fontSize: 32, marginBottom: 12 }}>🔌</div>
          No integrations yet. Add your first one.
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {list.map(item => {
            const sc = STATUS_COLOR[item.status] || STATUS_COLOR.inactive;
            const tc = TYPE_COLOR[item.integration_type] || "#6b7280";
            return (
              <div key={item.id} style={{
                background: "#111827", border: "1px solid #1f2937",
                borderRadius: 12, padding: "16px 20px",
                display: "flex", alignItems: "center", gap: 16,
              }}>
                {/* Type badge */}
                <div style={{
                  background: tc + "22", color: tc,
                  padding: "4px 10px", borderRadius: 6,
                  fontSize: 11, fontWeight: 700, textTransform: "uppercase",
                  letterSpacing: "0.06em", minWidth: 72, textAlign: "center",
                }}>{item.integration_type}</div>

                {/* Info */}
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ color: "#f9fafb", fontWeight: 600, fontSize: 14 }}>{item.name}</div>
                  <div style={{ color: "#6b7280", fontSize: 12, marginTop: 2, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                    {item.base_url}
                  </div>
                </div>

                {/* Status */}
                <div style={{
                  background: sc.bg, color: sc.text,
                  padding: "4px 10px", borderRadius: 6,
                  fontSize: 12, fontWeight: 600,
                  display: "flex", alignItems: "center", gap: 5,
                }}>
                  <div style={{ width: 6, height: 6, borderRadius: "50%", background: sc.dot }} />
                  {item.status}
                </div>

                {/* Sync info */}
                <div style={{ color: "#4b5563", fontSize: 11, minWidth: 80, textAlign: "right" }}>
                  {item.last_synced_at
                    ? new Date(item.last_synced_at).toLocaleString()
                    : "Never synced"}
                </div>

                {/* Actions */}
                <div style={{ display: "flex", gap: 6 }}>
                  <Btn variant="ghost" onClick={() => test(item.id)} disabled={!!busy[item.id]} sx={{ padding: "7px 10px" }}>
                    <Icon d={ICONS.zap} size={14} />
                    {busy[item.id] === "test" ? "Testing…" : "Test"}
                  </Btn>
                  <Btn variant="ghost" onClick={() => sync(item.id)} disabled={item.status !== "active" || !!busy[item.id]} sx={{ padding: "7px 10px" }}>
                    <Icon d={ICONS.refresh} size={14} />
                    {busy[item.id] === "sync" ? "Syncing…" : "Sync"}
                  </Btn>
                  <Btn variant="ghost" onClick={() => openLogs(item)} sx={{ padding: "7px 10px" }}>
                    <Icon d={ICONS.log} size={14} />
                  </Btn>
                  <Btn variant="danger" onClick={() => del(item.id)} sx={{ padding: "7px 10px" }}>
                    <Icon d={ICONS.trash} size={14} />
                  </Btn>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Add modal */}
      {showAdd && (
        <AddIntegrationModal
          onClose={() => { setShowAdd(false); load(); }}
          toast$={toast$}
        />
      )}

      {/* Logs modal */}
      {showLogs && (
        <Modal title={`Logs — ${showLogs.name}`} onClose={() => setShowLogs(null)}>
          {logs.length === 0 ? (
            <div style={{ color: "#6b7280", textAlign: "center", padding: 32 }}>No logs yet.</div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {logs.map(log => (
                <div key={log.id} style={{
                  background: "#1f2937", borderRadius: 8, padding: "10px 14px",
                  display: "flex", gap: 12, alignItems: "flex-start",
                }}>
                  <span style={{
                    fontSize: 11, fontWeight: 700,
                    color: log.status === "SUCCESS" ? "#4ade80" : "#f87171",
                    minWidth: 55,
                  }}>{log.status}</span>
                  <span style={{ color: "#9ca3af", fontSize: 12, flex: 1 }}>{log.message}</span>
                  <span style={{ color: "#4b5563", fontSize: 11 }}>
                    {new Date(log.created_at).toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
          )}
        </Modal>
      )}
    </div>
  );
}

function AddIntegrationModal({ onClose, toast$ }) {
  const [form, setForm] = useState({
    name: "", integration_type: "erp", base_url: "",
    auth_type: "api_key", credentials: "", description: "",
    sync_direction: "both", sync_interval_minutes: 60,
  });
  const [busy, setBusy] = useState(false);

  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }));

  const submit = async () => {
    if (!form.name || !form.base_url) {
      toast$("Name and Base URL are required", "error"); return;
    }
    setBusy(true);
    try {
      await apiFetch("/integrations", {
        method: "POST",
        body: JSON.stringify({ ...form, sync_interval_minutes: Number(form.sync_interval_minutes) }),
      });
      toast$("Integration created");
      onClose();
    } catch (e) { toast$(e.message, "error"); }
    finally { setBusy(false); }
  };

  return (
    <Modal title="Add Integration" onClose={onClose}>
      <Field label="Name"><Input value={form.name} onChange={set("name")} placeholder="e.g. SAP ERP Production" /></Field>
      <Field label="Type">
        <Select value={form.integration_type} onChange={set("integration_type")}
          options={[
            { value: "erp",       label: "ERP" },
            { value: "crm",       label: "CRM" },
            { value: "ecommerce", label: "E-Commerce" },
            { value: "custom",    label: "Custom API" },
          ]} />
      </Field>
      <Field label="Base URL"><Input value={form.base_url} onChange={set("base_url")} placeholder="https://api.yoursystem.com" /></Field>
      <Field label="Auth Type">
        <Select value={form.auth_type} onChange={set("auth_type")}
          options={[
            { value: "api_key", label: "API Key (Bearer)" },
            { value: "basic",   label: "Basic Auth" },
            { value: "oauth2",  label: "OAuth 2.0" },
          ]} />
      </Field>
      <Field label="Credentials (JSON)">
        <textarea value={form.credentials} onChange={set("credentials")}
          placeholder='{"api_key": "your-key-here"}'
          style={{
            width: "100%", background: "#1f2937", border: "1px solid #374151",
            borderRadius: 8, padding: "9px 12px", color: "#f9fafb", fontSize: 13,
            outline: "none", boxSizing: "border-box", fontFamily: "'DM Mono', monospace",
            resize: "vertical", minHeight: 80,
          }} />
      </Field>
      <Field label="Sync Direction">
        <Select value={form.sync_direction} onChange={set("sync_direction")}
          options={[
            { value: "both",     label: "Both (Push & Pull)" },
            { value: "inbound",  label: "Inbound (Pull only)" },
            { value: "outbound", label: "Outbound (Push only)" },
          ]} />
      </Field>
      <Field label="Sync Interval (minutes)">
        <Input type="number" value={form.sync_interval_minutes} onChange={set("sync_interval_minutes")} min={0} />
      </Field>
      <Field label="Description"><Input value={form.description} onChange={set("description")} /></Field>
      <div style={{ display: "flex", gap: 10, justifyContent: "flex-end", marginTop: 8 }}>
        <Btn variant="ghost" onClick={onClose}>Cancel</Btn>
        <Btn onClick={submit} disabled={busy}>{busy ? "Creating…" : "Create Integration"}</Btn>
      </div>
    </Modal>
  );
}

// ─────────────────────────────────────────────────────────────
// TAB: WEBHOOKS
// ─────────────────────────────────────────────────────────────
const EVENTS_LIST = [
  "forecast.completed", "forecast.failed",
  "dataset.uploaded", "dataset.processed",
  "alert.generated", "integration.synced",
  "automation.job_completed",
];

function WebhooksTab() {
  const [list, setList]         = useState([]);
  const [loading, setLoading]   = useState(true);
  const [showAdd, setShowAdd]   = useState(false);
  const [showLogs, setShowLogs] = useState(null);
  const [logs, setLogs]         = useState([]);
  const [toast, setToast]       = useState(null);
  const [busy, setBusy]         = useState({});

  const toast$ = (msg, type = "success") => setToast({ msg, type });

  const load = async () => {
    setLoading(true);
    try { setList(await apiFetch("/webhooks")); }
    catch (e) { toast$(e.message, "error"); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const test = async (id) => {
    setBusy(b => ({ ...b, [id]: true }));
    try {
      const r = await apiFetch(`/webhooks/${id}/test`, { method: "POST" });
      toast$(r.message, r.success ? "success" : "error");
    } catch (e) { toast$(e.message, "error"); }
    finally { setBusy(b => ({ ...b, [id]: false })); }
  };

  const toggle = async (wh) => {
    try {
      await apiFetch(`/webhooks/${wh.id}`, {
        method: "PUT",
        body: JSON.stringify({ is_active: !wh.is_active }),
      });
      toast$(wh.is_active ? "Webhook disabled" : "Webhook enabled");
      load();
    } catch (e) { toast$(e.message, "error"); }
  };

  const del = async (id) => {
    if (!confirm("Delete this webhook?")) return;
    try {
      await apiFetch(`/webhooks/${id}`, { method: "DELETE" });
      toast$("Webhook deleted");
      load();
    } catch (e) { toast$(e.message, "error"); }
  };

  const openLogs = async (wh) => {
    setShowLogs(wh);
    const data = await apiFetch(`/webhooks/${wh.id}/logs`);
    setLogs(data);
  };

  return (
    <div>
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <span style={{ color: "#9ca3af", fontSize: 13 }}>{list.length} webhook(s) configured</span>
        <Btn onClick={() => setShowAdd(true)}>
          <Icon d={ICONS.plus} size={15} /> Add Webhook
        </Btn>
      </div>

      {loading ? (
        <div style={{ color: "#6b7280", textAlign: "center", padding: 48 }}>Loading…</div>
      ) : list.length === 0 ? (
        <div style={{
          background: "#111827", border: "1px dashed #374151",
          borderRadius: 12, padding: 48, textAlign: "center", color: "#6b7280",
        }}>
          <div style={{ fontSize: 32, marginBottom: 12 }}>🔗</div>
          No webhooks configured yet.
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {list.map(wh => (
            <div key={wh.id} style={{
              background: "#111827", border: "1px solid #1f2937",
              borderRadius: 12, padding: "16px 20px",
            }}>
              <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 10 }}>
                <div style={{ flex: 1 }}>
                  <div style={{ color: "#f9fafb", fontWeight: 600, fontSize: 14 }}>{wh.name}</div>
                  <div style={{ color: "#6b7280", fontSize: 12, marginTop: 2, fontFamily: "'DM Mono', monospace" }}>
                    {wh.target_url}
                  </div>
                </div>
                <div style={{
                  padding: "4px 10px", borderRadius: 6, fontSize: 12, fontWeight: 600,
                  background: wh.is_active ? "#0d2e1a" : "#1e1b2e",
                  color: wh.is_active ? "#4ade80" : "#a78bfa",
                }}>{wh.is_active ? "Active" : "Inactive"}</div>
                <div style={{ color: wh.failure_count > 0 ? "#f87171" : "#6b7280", fontSize: 12 }}>
                  {wh.failure_count} failures
                </div>
                <div style={{ display: "flex", gap: 6 }}>
                  <Btn variant="ghost" onClick={() => test(wh.id)} disabled={busy[wh.id]} sx={{ padding: "7px 10px" }}>
                    <Icon d={ICONS.zap} size={14} />
                    {busy[wh.id] ? "Sending…" : "Test"}
                  </Btn>
                  <Btn variant={wh.is_active ? "ghost" : "success"} onClick={() => toggle(wh)} sx={{ padding: "7px 10px" }}>
                    {wh.is_active ? "Disable" : "Enable"}
                  </Btn>
                  <Btn variant="ghost" onClick={() => openLogs(wh)} sx={{ padding: "7px 10px" }}>
                    <Icon d={ICONS.log} size={14} />
                  </Btn>
                  <Btn variant="danger" onClick={() => del(wh.id)} sx={{ padding: "7px 10px" }}>
                    <Icon d={ICONS.trash} size={14} />
                  </Btn>
                </div>
              </div>
              {/* Events */}
              <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                {wh.events.split(",").map(ev => (
                  <span key={ev} style={{
                    background: "#1f2937", color: "#60a5fa",
                    padding: "3px 8px", borderRadius: 5, fontSize: 11,
                    fontFamily: "'DM Mono', monospace",
                  }}>{ev.trim()}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {showAdd && <AddWebhookModal onClose={() => { setShowAdd(false); load(); }} toast$={toast$} />}

      {showLogs && (
        <Modal title={`Delivery Logs — ${showLogs.name}`} onClose={() => setShowLogs(null)}>
          {logs.length === 0 ? (
            <div style={{ color: "#6b7280", textAlign: "center", padding: 32 }}>No delivery logs yet.</div>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {logs.map(log => (
                <div key={log.id} style={{
                  background: "#1f2937", borderRadius: 8, padding: "10px 14px",
                }}>
                  <div style={{ display: "flex", gap: 10, alignItems: "center", marginBottom: 4 }}>
                    <span style={{
                      fontSize: 11, fontWeight: 700,
                      color: log.status === "success" ? "#4ade80" : "#f87171",
                    }}>{log.status.toUpperCase()}</span>
                    <span style={{ color: "#60a5fa", fontSize: 11, fontFamily: "'DM Mono', monospace" }}>{log.event}</span>
                    <span style={{ color: "#6b7280", fontSize: 11 }}>HTTP {log.response_code}</span>
                    <span style={{ color: "#4b5563", fontSize: 11, marginLeft: "auto" }}>
                      {new Date(log.triggered_at).toLocaleString()}
                    </span>
                  </div>
                  {log.response_body && (
                    <div style={{ color: "#6b7280", fontSize: 11, fontFamily: "'DM Mono', monospace", marginTop: 4 }}>
                      {log.response_body}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </Modal>
      )}
    </div>
  );
}

function AddWebhookModal({ onClose, toast$ }) {
  const [form, setForm] = useState({ name: "", target_url: "", secret: "", is_active: true });
  const [selectedEvents, setSelectedEvents] = useState([]);
  const [busy, setBusy] = useState(false);

  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }));

  const toggleEvent = (ev) => setSelectedEvents(s =>
    s.includes(ev) ? s.filter(x => x !== ev) : [...s, ev]
  );

  const submit = async () => {
    if (!form.name || !form.target_url || selectedEvents.length === 0) {
      toast$("Name, URL, and at least one event are required", "error"); return;
    }
    setBusy(true);
    try {
      await apiFetch("/webhooks", {
        method: "POST",
        body: JSON.stringify({ ...form, events: selectedEvents }),
      });
      toast$("Webhook created");
      onClose();
    } catch (e) { toast$(e.message, "error"); }
    finally { setBusy(false); }
  };

  return (
    <Modal title="Add Webhook" onClose={onClose}>
      <Field label="Name"><Input value={form.name} onChange={set("name")} placeholder="e.g. Slack Forecast Alerts" /></Field>
      <Field label="Target URL"><Input value={form.target_url} onChange={set("target_url")} placeholder="https://hooks.slack.com/..." /></Field>
      <Field label="HMAC Secret (optional)"><Input value={form.secret} onChange={set("secret")} placeholder="leave blank if not needed" /></Field>
      <Field label="Subscribe to Events">
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginTop: 4 }}>
          {EVENTS_LIST.map(ev => (
            <button key={ev} onClick={() => toggleEvent(ev)} style={{
              background: selectedEvents.includes(ev) ? "#1d4ed8" : "#1f2937",
              color: selectedEvents.includes(ev) ? "#bfdbfe" : "#6b7280",
              border: `1px solid ${selectedEvents.includes(ev) ? "#3b82f6" : "#374151"}`,
              borderRadius: 6, padding: "5px 10px", fontSize: 11, cursor: "pointer",
              fontFamily: "'DM Mono', monospace",
            }}>{ev}</button>
          ))}
        </div>
      </Field>
      <div style={{ display: "flex", gap: 10, justifyContent: "flex-end", marginTop: 8 }}>
        <Btn variant="ghost" onClick={onClose}>Cancel</Btn>
        <Btn onClick={submit} disabled={busy}>{busy ? "Creating…" : "Create Webhook"}</Btn>
      </div>
    </Modal>
  );
}

// ─────────────────────────────────────────────────────────────
// TAB: API KEYS
// ─────────────────────────────────────────────────────────────
function ApiKeysTab() {
  const [list, setList]       = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAdd, setShowAdd] = useState(false);
  const [newKey, setNewKey]   = useState(null);   // raw key shown once
  const [toast, setToast]     = useState(null);

  const toast$ = (msg, type = "success") => setToast({ msg, type });

  const load = async () => {
    setLoading(true);
    try { setList(await apiFetch("/api-keys")); }
    catch (e) { toast$(e.message, "error"); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const revoke = async (id) => {
    if (!confirm("Revoke this API key?")) return;
    try {
      await apiFetch(`/api-keys/${id}/revoke`, { method: "PATCH" });
      toast$("Key revoked");
      load();
    } catch (e) { toast$(e.message, "error"); }
  };

  const del = async (id) => {
    if (!confirm("Permanently delete this key?")) return;
    try {
      await apiFetch(`/api-keys/${id}`, { method: "DELETE" });
      toast$("Key deleted");
      load();
    } catch (e) { toast$(e.message, "error"); }
  };

  const copy = (text) => {
    navigator.clipboard.writeText(text);
    toast$("Copied to clipboard");
  };

  const SCOPE_COLOR = { read: "#3b82f6", write: "#f59e0b", admin: "#ef4444" };

  return (
    <div>
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}

      {/* One-time key display */}
      {newKey && (
        <div style={{
          background: "#0d2e1a", border: "1px solid #16a34a",
          borderRadius: 10, padding: "16px 20px", marginBottom: 20,
        }}>
          <div style={{ color: "#4ade80", fontWeight: 700, marginBottom: 8, fontSize: 14 }}>
            ✅ Key created — copy it now, it won't be shown again
          </div>
          <div style={{
            display: "flex", alignItems: "center", gap: 10,
            background: "#111827", borderRadius: 8, padding: "10px 14px",
          }}>
            <code style={{ color: "#86efac", flex: 1, fontSize: 13, fontFamily: "'DM Mono', monospace", wordBreak: "break-all" }}>
              {newKey}
            </code>
            <button onClick={() => copy(newKey)} style={{
              background: "#16a34a", color: "#fff", border: "none",
              borderRadius: 6, padding: "6px 12px", cursor: "pointer", fontSize: 12,
            }}>Copy</button>
          </div>
          <button onClick={() => setNewKey(null)} style={{
            marginTop: 10, background: "none", border: "none",
            color: "#6b7280", cursor: "pointer", fontSize: 12,
          }}>Dismiss</button>
        </div>
      )}

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
        <span style={{ color: "#9ca3af", fontSize: 13 }}>{list.length} key(s) total</span>
        <Btn onClick={() => setShowAdd(true)}>
          <Icon d={ICONS.plus} size={15} /> Generate Key
        </Btn>
      </div>

      {loading ? (
        <div style={{ color: "#6b7280", textAlign: "center", padding: 48 }}>Loading…</div>
      ) : list.length === 0 ? (
        <div style={{
          background: "#111827", border: "1px dashed #374151",
          borderRadius: 12, padding: 48, textAlign: "center", color: "#6b7280",
        }}>
          <div style={{ fontSize: 32, marginBottom: 12 }}>🔑</div>
          No API keys yet.
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {list.map(k => (
            <div key={k.id} style={{
              background: "#111827", border: "1px solid #1f2937",
              borderRadius: 12, padding: "14px 20px",
              display: "flex", alignItems: "center", gap: 14, opacity: k.is_active ? 1 : 0.5,
            }}>
              <div style={{
                background: (SCOPE_COLOR[k.scope] || "#6b7280") + "22",
                color: SCOPE_COLOR[k.scope] || "#6b7280",
                padding: "4px 10px", borderRadius: 6,
                fontSize: 11, fontWeight: 700, textTransform: "uppercase",
                minWidth: 48, textAlign: "center",
              }}>{k.scope}</div>

              <div style={{ flex: 1 }}>
                <div style={{ color: "#f9fafb", fontWeight: 600, fontSize: 14 }}>{k.label}</div>
                <div style={{ color: "#6b7280", fontSize: 12, marginTop: 2, fontFamily: "'DM Mono', monospace" }}>
                  {k.key_prefix}••••••••••••••••••••
                </div>
              </div>

              <div style={{ color: "#6b7280", fontSize: 11, textAlign: "right" }}>
                <div>Used {k.usage_count}×</div>
                <div>{k.last_used_at ? new Date(k.last_used_at).toLocaleDateString() : "Never used"}</div>
              </div>

              <div style={{
                padding: "4px 10px", borderRadius: 6, fontSize: 12, fontWeight: 600,
                background: k.is_active ? "#0d2e1a" : "#1f2937",
                color: k.is_active ? "#4ade80" : "#6b7280",
              }}>{k.is_active ? "Active" : "Revoked"}</div>

              <div style={{ display: "flex", gap: 6 }}>
                {k.is_active && (
                  <Btn variant="ghost" onClick={() => revoke(k.id)} sx={{ padding: "7px 10px" }}>
                    Revoke
                  </Btn>
                )}
                <Btn variant="danger" onClick={() => del(k.id)} sx={{ padding: "7px 10px" }}>
                  <Icon d={ICONS.trash} size={14} />
                </Btn>
              </div>
            </div>
          ))}
        </div>
      )}

      {showAdd && (
        <AddKeyModal
          onClose={() => setShowAdd(false)}
          onCreated={(raw) => { setNewKey(raw); load(); }}
          toast$={toast$}
        />
      )}
    </div>
  );
}

function AddKeyModal({ onClose, onCreated, toast$ }) {
  const [form, setForm] = useState({ label: "", scope: "read", expires_at: "" });
  const [busy, setBusy] = useState(false);

  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }));

  const submit = async () => {
    if (!form.label) { toast$("Label is required", "error"); return; }
    setBusy(true);
    try {
      const body = { label: form.label, scope: form.scope };
      if (form.expires_at) body.expires_at = form.expires_at;
      const r = await apiFetch("/api-keys", { method: "POST", body: JSON.stringify(body) });
      onCreated(r.raw_key);
      onClose();
    } catch (e) { toast$(e.message, "error"); }
    finally { setBusy(false); }
  };

  return (
    <Modal title="Generate API Key" onClose={onClose}>
      <Field label="Label"><Input value={form.label} onChange={set("label")} placeholder="e.g. SAP Production Key" /></Field>
      <Field label="Scope">
        <Select value={form.scope} onChange={set("scope")}
          options={[
            { value: "read",  label: "Read — GET endpoints only" },
            { value: "write", label: "Write — GET + POST/PUT" },
            { value: "admin", label: "Admin — Full access" },
          ]} />
      </Field>
      <Field label="Expires At (optional)">
        <Input type="datetime-local" value={form.expires_at} onChange={set("expires_at")} />
      </Field>
      <div style={{ background: "#1f2937", borderRadius: 8, padding: 12, marginBottom: 16, color: "#9ca3af", fontSize: 12 }}>
        ⚠️ The raw key is shown <strong style={{ color: "#fbbf24" }}>once only</strong> after creation. Store it securely immediately.
      </div>
      <div style={{ display: "flex", gap: 10, justifyContent: "flex-end" }}>
        <Btn variant="ghost" onClick={onClose}>Cancel</Btn>
        <Btn onClick={submit} disabled={busy}>{busy ? "Generating…" : "Generate Key"}</Btn>
      </div>
    </Modal>
  );
}

// ─────────────────────────────────────────────────────────────
// ROOT PAGE
// ─────────────────────────────────────────────────────────────
const TABS = [
  { id: "integrations", label: "Integrations",    icon: ICONS.plug },
  { id: "webhooks",     label: "Webhooks",         icon: ICONS.webhook },
  { id: "api_keys",     label: "API Key Mgmt",     icon: ICONS.key },
];

export default function EnterpriseIntegrations() {
  const [tab, setTab] = useState("integrations");

  return (
    <div style={{
      minHeight: "100vh",
      background: "#0a0f1a",
      fontFamily: "'DM Sans', 'Segoe UI', sans-serif",
      color: "#f9fafb",
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=DM+Mono:wght@400;500&display=swap');
        * { box-sizing: border-box; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #111827; }
        ::-webkit-scrollbar-thumb { background: #374151; border-radius: 3px; }
        @keyframes slideIn { from { transform: translateY(12px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
      `}</style>

      <div style={{ maxWidth: 1100, margin: "0 auto", padding: "32px 24px" }}>

        {/* Header */}
        <div style={{ marginBottom: 32 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 6 }}>
            <div style={{
              background: "linear-gradient(135deg, #2563eb, #7c3aed)",
              borderRadius: 10, padding: 10,
              display: "flex", alignItems: "center", justifyContent: "center",
            }}>
              <Icon d={ICONS.plug} size={20} color="#fff" />
            </div>
            <h1 style={{ margin: 0, fontSize: 24, fontWeight: 700, color: "#f9fafb" }}>
              Enterprise Integration
            </h1>
          </div>
          <p style={{ margin: 0, color: "#6b7280", fontSize: 14 }}>
            Connect third-party systems, configure webhooks, and manage API keys
          </p>
        </div>

        {/* Tabs */}
        <div style={{
          display: "flex", gap: 4, marginBottom: 28,
          background: "#111827", borderRadius: 10, padding: 4,
          width: "fit-content",
        }}>
          {TABS.map(t => (
            <button key={t.id} onClick={() => setTab(t.id)} style={{
              background: tab === t.id ? "#1d4ed8" : "transparent",
              color: tab === t.id ? "#fff" : "#6b7280",
              border: "none", borderRadius: 8, padding: "8px 18px",
              fontSize: 13, fontWeight: 600, cursor: "pointer",
              display: "flex", alignItems: "center", gap: 7,
              transition: "all 0.15s",
              fontFamily: "'DM Sans', sans-serif",
            }}>
              <Icon d={t.icon} size={14} />
              {t.label}
            </button>
          ))}
        </div>

        {/* Tab content */}
        {tab === "integrations" && <IntegrationsTab />}
        {tab === "webhooks"     && <WebhooksTab />}
        {tab === "api_keys"     && <ApiKeysTab />}
      </div>
    </div>
  );
}
