import { useState } from "react";
import { X, Loader2, Plus, Trash2 } from "lucide-react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import type { CreateBookingPayload, BookingDate, BookingSlot, District } from "../../types";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (payload: CreateBookingPayload) => Promise<void>;
  districts: District[];
}

const emptySlot = (): BookingSlot => ({ start_time: "09:00", end_time: "17:00" });
const emptyDate = (): BookingDate => ({
  event_date: new Date().toISOString().split("T")[0],
  slots: [emptySlot()],
});

export function CreateBookingModal({ isOpen, onClose, onSubmit, districts }: Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [formData, setFormData] = useState<CreateBookingPayload>({
    customer_name: "",
    district: undefined,
    address: "",
    phone_number: "",
    alternative_phone_number: "",
    map_url: "",
    total_amount: 0,
    advance_amount: 0,
    dates: [emptyDate()],
  });

  if (!isOpen) return null;

  const addDate = () => setFormData(p => ({ ...p, dates: [...p.dates, emptyDate()] }));
  const removeDate = (i: number) => setFormData(p => ({ ...p, dates: p.dates.filter((_, idx) => idx !== i) }));
  const updateDate = (i: number, field: string, value: string) => {
    setFormData(p => {
      const dates = [...p.dates];
      dates[i] = { ...dates[i], [field]: value };
      return { ...p, dates };
    });
  };
  const addSlot = (dateIdx: number) => {
    setFormData(p => {
      const dates = [...p.dates];
      dates[dateIdx] = { ...dates[dateIdx], slots: [...dates[dateIdx].slots, emptySlot()] };
      return { ...p, dates };
    });
  };
  const removeSlot = (dateIdx: number, slotIdx: number) => {
    setFormData(p => {
      const dates = [...p.dates];
      dates[dateIdx] = { ...dates[dateIdx], slots: dates[dateIdx].slots.filter((_, i) => i !== slotIdx) };
      return { ...p, dates };
    });
  };
  const updateSlot = (dateIdx: number, slotIdx: number, field: keyof BookingSlot, value: string) => {
    setFormData(p => {
      const dates = [...p.dates];
      const slots = [...dates[dateIdx].slots];
      slots[slotIdx] = { ...slots[slotIdx], [field]: value };
      dates[dateIdx] = { ...dates[dateIdx], slots };
      return { ...p, dates };
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await onSubmit(formData);
      onClose();
    } catch (err) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const resp = (err as Record<string, any>)?.response?.data;
      if (resp) {
        const key = Object.keys(resp)[0];
        setError(Array.isArray(resp[key]) ? resp[key][0] : String(resp[key]));
      } else {
        setError(err instanceof Error ? err.message : "Failed to create booking.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-[100] flex flex-col justify-end sm:items-center sm:justify-center bg-black/60 backdrop-blur-sm sm:p-4">
      <div className="absolute inset-0" onClick={onClose} />
      <div className="bg-white w-full sm:max-w-2xl sm:rounded-2xl rounded-t-3xl shadow-2xl flex flex-col max-h-[92dvh] sm:max-h-[85vh] relative z-10">

        {/* Pull indicator */}
        <div className="w-full flex justify-center pt-3 pb-1 sm:hidden">
          <div className="w-12 h-1.5 bg-zinc-200 rounded-full" />
        </div>

        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-zinc-100 shrink-0">
          <div>
            <h2 className="text-lg sm:text-xl font-semibold text-zinc-900">New Booking</h2>
            <p className="text-xs text-zinc-500 mt-0.5">Fill in client details and event dates.</p>
          </div>
          <button onClick={onClose} className="p-2 -mr-2 rounded-full text-zinc-400 hover:bg-zinc-100">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col flex-1 overflow-hidden">
          <div className="p-6 space-y-6 overflow-y-auto flex-1 overscroll-contain">
            {error && <div className="bg-red-50 text-red-600 text-sm p-3 rounded-xl border border-red-100">{error}</div>}

            {/* Section: Client Info */}
            <div>
              <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-4">Client Details</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-zinc-700">Customer Name *</label>
                  <Input required placeholder="e.g. Rahul & Priya" value={formData.customer_name}
                    onChange={e => setFormData({ ...formData, customer_name: e.target.value })} />
                </div>
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-zinc-700">Phone Number *</label>
                  <Input required type="tel" placeholder="9876543210" value={formData.phone_number}
                    onChange={e => setFormData({ ...formData, phone_number: e.target.value })} />
                </div>
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-zinc-700">Alternative Phone</label>
                  <Input type="tel" placeholder="Optional" value={formData.alternative_phone_number}
                    onChange={e => setFormData({ ...formData, alternative_phone_number: e.target.value })} />
                </div>
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-zinc-700">District</label>
                  <select className="flex h-10 w-full rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-zinc-950"
                    value={formData.district || ""} onChange={e => setFormData({ ...formData, district: Number(e.target.value) || undefined })}>
                    <option value="">Select district</option>
                    {districts.map(d => <option key={d.id} value={d.id}>{d.name}</option>)}
                  </select>
                </div>
                <div className="sm:col-span-2 space-y-1.5">
                  <label className="text-sm font-medium text-zinc-700">Address *</label>
                  <textarea required rows={2} placeholder="Event venue address"
                    className="flex w-full rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm resize-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-zinc-950 placeholder:text-zinc-500"
                    value={formData.address} onChange={e => setFormData({ ...formData, address: e.target.value })} />
                </div>
                <div className="sm:col-span-2 space-y-1.5">
                  <label className="text-sm font-medium text-zinc-700">Google Maps URL</label>
                  <Input type="url" placeholder="https://maps.google.com/..." value={formData.map_url}
                    onChange={e => setFormData({ ...formData, map_url: e.target.value })} />
                </div>
              </div>
            </div>

            {/* Section: Financials */}
            <div>
              <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400 mb-4">Financials</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-zinc-700">Total Amount (₹) *</label>
                  <Input required type="number" min="0" placeholder="0"
                    value={formData.total_amount || ""}
                    onChange={e => setFormData({ ...formData, total_amount: Number(e.target.value) })} />
                </div>
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-zinc-700">Advance Paid (₹)</label>
                  <Input type="number" min="0" placeholder="0"
                    value={formData.advance_amount || ""}
                    onChange={e => setFormData({ ...formData, advance_amount: Number(e.target.value) })} />
                </div>
              </div>
            </div>

            {/* Section: Event Dates & Slots */}
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400">Event Dates & Time Slots</h3>
                <button type="button" onClick={addDate}
                  className="inline-flex items-center gap-1 text-xs font-medium text-zinc-600 hover:text-zinc-900 border border-zinc-200 rounded-full px-3 py-1 hover:bg-zinc-50 transition-colors">
                  <Plus className="w-3.5 h-3.5" /> Add Date
                </button>
              </div>
              <div className="space-y-4">
                {formData.dates.map((date, di) => (
                  <div key={di} className="border border-zinc-200 rounded-xl p-4 bg-zinc-50/60">
                    <div className="flex items-center justify-between mb-3">
                      <Input type="date" required className="w-40 text-sm bg-white"
                        value={date.event_date} onChange={e => updateDate(di, "event_date", e.target.value)} />
                      <div className="flex items-center gap-2">
                        <button type="button" onClick={() => addSlot(di)}
                          className="text-xs text-zinc-600 hover:text-zinc-900 border border-zinc-200 rounded-full px-2.5 py-1 flex items-center gap-1 hover:bg-white transition-colors">
                          <Plus className="w-3 h-3" /> Slot
                        </button>
                        {formData.dates.length > 1 && (
                          <button type="button" onClick={() => removeDate(di)} className="p-1.5 text-zinc-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-colors">
                            <Trash2 className="w-4 h-4" />
                          </button>
                        )}
                      </div>
                    </div>
                    <div className="space-y-2">
                      {date.slots.map((slot, si) => (
                        <div key={si} className="flex items-center gap-2 bg-white border border-zinc-200 rounded-lg p-2">
                          <span className="text-xs text-zinc-500 w-8">From</span>
                          <Input type="time" required className="flex-1 text-sm h-8 border-0 p-0 focus-visible:ring-0"
                            value={slot.start_time} onChange={e => updateSlot(di, si, "start_time", e.target.value)} />
                          <span className="text-xs text-zinc-500">To</span>
                          <Input type="time" required className="flex-1 text-sm h-8 border-0 p-0 focus-visible:ring-0"
                            value={slot.end_time} onChange={e => updateSlot(di, si, "end_time", e.target.value)} />
                          {date.slots.length > 1 && (
                            <button type="button" onClick={() => removeSlot(di, si)} className="p-1 text-zinc-300 hover:text-red-400 transition-colors">
                              <X className="w-3.5 h-3.5" />
                            </button>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="flex items-center justify-end gap-3 p-4 sm:p-6 border-t border-zinc-100 bg-white shrink-0 sm:rounded-b-2xl">
            <Button type="button" variant="ghost" onClick={onClose} disabled={loading} className="hidden sm:inline-flex">Cancel</Button>
            <Button type="submit" disabled={loading} className="w-full sm:w-auto bg-zinc-900 hover:bg-black text-white h-12 sm:h-10 text-base sm:text-sm rounded-xl sm:rounded-md min-w-[140px]">
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Save Booking"}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
