import { useState } from "react";
import { X, Loader2 } from "lucide-react";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import type { Category, District, CreateVendorPayload } from "../../types";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (payload: CreateVendorPayload) => Promise<void>;
  categories: Category[];
  districts: District[];
}

export function CreateVendorModal({ isOpen, onClose, onSubmit, categories, districts }: Props) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  
  const [formData, setFormData] = useState<CreateVendorPayload>({
    name: "",
    email: "",
    contact_number: "",
    whatsapp_number: "",
    years_of_experience: 0,
    category: undefined,
    districts: [],
  });

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      if (!formData.category) throw new Error("Please select a category");
      if (formData.districts?.length === 0) throw new Error("Please select at least one district");
      
      await onSubmit(formData);
      onClose(); // Automatically closes on success!
    } catch (err) {
      console.error("Failed to create vendor", err);
      // Attempt to peel off DRF array wrapper errors
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const respError = (err as Record<string, any>)?.response?.data;
      if (respError) {
        const firstKey = Object.keys(respError)[0];
        setError(Array.isArray(respError[firstKey]) ? respError[firstKey][0] : respError[firstKey]);
      } else {
        setError(err instanceof Error ? err.message : "An unexpected error occurred while creating vendor");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDistrictToggle = (districtId: number) => {
    setFormData(prev => {
      const current = prev.districts || [];
      const isSelected = current.includes(districtId);
      return {
        ...prev,
        districts: isSelected 
          ? current.filter(id => id !== districtId) 
          : [...current, districtId]
      };
    });
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl w-full max-w-2xl shadow-xl overflow-hidden animate-in fade-in zoom-in-95 duration-200 my-8">
        
        <div className="flex items-center justify-between p-6 border-b border-zinc-100 bg-zinc-50/50">
          <div>
            <h2 className="text-xl font-semibold text-zinc-900">Create New Vendor</h2>
            <p className="text-sm text-zinc-500 mt-1">
              They will receive an email containing their login username and dynamically generated password.
            </p>
          </div>
          <button 
            onClick={onClose}
            className="p-2 text-zinc-400 hover:text-zinc-600 hover:bg-zinc-100 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          
          {error && (
            <div className="bg-red-50 text-red-600 text-sm p-3 rounded-xl border border-red-100">
              {error}
            </div>
          )}

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div className="space-y-2">
              <label className="text-sm font-medium text-zinc-700">Business/Owner Name *</label>
              <Input 
                required
                placeholder="e.g. Dream Weddings" 
                value={formData.name}
                onChange={e => setFormData({...formData, name: e.target.value})}
              />
            </div>
            
            <div className="space-y-2">
              <label className="text-sm font-medium text-zinc-700">Email Address *</label>
              <Input 
                required
                type="email"
                placeholder="vendor@example.com" 
                value={formData.email}
                onChange={e => setFormData({...formData, email: e.target.value})}
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-zinc-700">Contact Number *</label>
              <Input 
                required
                type="tel"
                placeholder="1234567890" 
                value={formData.contact_number}
                onChange={e => setFormData({...formData, contact_number: e.target.value})}
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-zinc-700">WhatsApp Number</label>
              <Input 
                type="tel"
                placeholder="1234567890" 
                value={formData.whatsapp_number}
                onChange={e => setFormData({...formData, whatsapp_number: e.target.value})}
              />
            </div>
            
            <div className="space-y-2">
              <label className="text-sm font-medium text-zinc-700">Years of Experience</label>
              <Input 
                type="number"
                min="0"
                value={formData.years_of_experience}
                onChange={e => setFormData({...formData, years_of_experience: Number(e.target.value)})}
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-zinc-700">Category *</label>
              <select 
                required
                className="flex h-10 w-full rounded-md border border-zinc-200 bg-white px-3 py-2 text-sm ring-offset-white file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-zinc-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-zinc-950 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                value={formData.category || ""}
                onChange={e => setFormData({...formData, category: Number(e.target.value)})}
              >
                <option value="" disabled>Select a category</option>
                {categories.map(cat => (
                  <option key={cat.id} value={cat.id}>{cat.name}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Districts Tags Picker */}
          <div className="space-y-2 pt-2">
            <label className="text-sm font-medium text-zinc-700">Operating Districts *</label>
            <div className="flex flex-wrap gap-2 max-h-40 overflow-y-auto p-3 border border-zinc-200 rounded-lg bg-zinc-50">
              {districts.map(dict => {
                const isSelected = formData.districts?.includes(dict.id);
                return (
                  <button
                    key={dict.id}
                    type="button"
                    onClick={() => handleDistrictToggle(dict.id)}
                    className={`px-3 py-1.5 rounded-full text-xs font-medium cursor-pointer transition-colors border ${
                      isSelected 
                        ? "bg-zinc-900 border-zinc-900 text-white" 
                        : "bg-white border-zinc-200 text-zinc-600 hover:border-zinc-300"
                    }`}
                  >
                    {dict.name}
                  </button>
                )
              })}
              {districts.length === 0 && (
                <span className="text-zinc-400 text-xs">No districts loaded.</span>
              )}
            </div>
          </div>

          <div className="flex items-center justify-end space-x-4 pt-6 border-t border-zinc-100">
            <Button type="button" variant="ghost" onClick={onClose} disabled={loading}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading} className="bg-zinc-900 text-white min-w-[140px]">
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Create Vendor"}
            </Button>
          </div>

        </form>
      </div>
    </div>
  );
}
