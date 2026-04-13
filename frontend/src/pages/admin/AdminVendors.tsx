import { useEffect, useState } from "react";
import { getVendors, getCategories, getDistricts, createVendor } from "../../api/adminVendors";
import type { Vendor, Category, District, CreateVendorPayload } from "../../types";
import { Search, Plus, MoreVertical, CheckCircle2, XCircle, Users } from "lucide-react";
import { Button } from "../../components/ui/button";
import { Input } from "../../components/ui/input";
import { CreateVendorModal } from "../../components/admin/CreateVendorModal";

export function AdminVendors() {
  const [vendors, setVendors] = useState<Vendor[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [categories, setCategories] = useState<Category[]>([]);
  const [districts, setDistricts] = useState<District[]>([]);

  useEffect(() => {
    fetchVendors();
    fetchFormOptions();
  }, []);

  const fetchFormOptions = async () => {
    try {
      const [cats, dists] = await Promise.all([getCategories(), getDistricts()]);
      setCategories(cats || []);
      setDistricts(dists || []);
    } catch (err) {
      console.error("Failed to load form options", err);
    }
  };

  const handleCreateVendor = async (payload: CreateVendorPayload) => {
    await createVendor(payload);
    fetchVendors(); // Refresh table on success
  };

  const fetchVendors = async () => {
    try {
      const data = await getVendors();
      setVendors(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch vendors. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const filteredVendors = vendors.filter(v => 
    v.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    v.email?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header Area */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-semibold text-zinc-900 tracking-tight">Vendors</h2>
          <p className="text-sm text-zinc-500">Manage wedding service providers and their access.</p>
        </div>
        <Button 
          onClick={() => setIsModalOpen(true)}
          className="bg-zinc-900 hover:bg-black text-white px-4 py-2 flex items-center space-x-2 w-full sm:w-auto"
        >
          <Plus className="w-4 h-4" />
          <span>Add Vendor</span>
        </Button>
      </div>

      {/* Toolbar */}
      <div className="bg-white p-4 rounded-xl border border-zinc-200 shadow-sm flex flex-col sm:flex-row gap-4 justify-between">
        <div className="relative w-full max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-zinc-400" />
          <Input 
            type="text" 
            placeholder="Search vendors by name or email..." 
            className="pl-9 bg-zinc-50 border-zinc-200"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div className="flex space-x-2">
          {/* Optional filter buttons could go here */}
          <Button variant="outline" className="border-zinc-200 bg-white hover:bg-zinc-50 text-zinc-600">
            Export CSV
          </Button>
        </div>
      </div>

      {/* Error state */}
      {error && (
        <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-100 flex items-center space-x-2">
          <XCircle className="w-5 h-5 flex-shrink-0" />
          <p className="text-sm font-medium">{error}</p>
        </div>
      )}

      {/* Table Area */}
      <div className="bg-white rounded-xl border border-zinc-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-zinc-500 uppercase bg-zinc-50 w-full border-b border-zinc-200">
              <tr>
                <th className="px-6 py-4 font-medium">Vendor</th>
                <th className="px-6 py-4 font-medium">Contact</th>
                <th className="px-6 py-4 font-medium">Joined</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-200">
              {loading ? (
                // Skeletons
                [...Array(5)].map((_, i) => (
                  <tr key={i} className="animate-pulse bg-white">
                    <td className="px-6 py-4"><div className="h-4 bg-zinc-200 rounded w-3/4 mb-2"></div><div className="h-3 bg-zinc-100 rounded w-1/2"></div></td>
                    <td className="px-6 py-4"><div className="h-4 bg-zinc-200 rounded w-24"></div></td>
                    <td className="px-6 py-4"><div className="h-4 bg-zinc-200 rounded w-20"></div></td>
                    <td className="px-6 py-4"><div className="h-5 bg-zinc-200 rounded-full w-16"></div></td>
                    <td className="px-6 py-4"><div className="h-4 bg-zinc-200 rounded w-4 ml-auto"></div></td>
                  </tr>
                ))
              ) : filteredVendors.length > 0 ? (
                filteredVendors.map((vendor) => (
                  <tr key={vendor.id} className="bg-white hover:bg-zinc-50 transition-colors group">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="h-10 w-10 flex-shrink-0 rounded-full bg-zinc-100 flex items-center justify-center text-zinc-600 font-bold border border-zinc-200 shadow-sm uppercase">
                          {vendor.name?.charAt(0) || 'V'}
                        </div>
                        <div className="ml-4">
                          <div className="font-semibold text-zinc-900">{vendor.name}</div>
                          <div className="text-zinc-500 text-xs">{vendor.email}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="text-zinc-600">{vendor.contact_number}</span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-zinc-500">
                      {new Date(vendor.joining_date).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {vendor.is_active ? (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-50 text-green-700 border border-green-200">
                          <CheckCircle2 className="w-3 h-3 mr-1" /> Active
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-zinc-100 text-zinc-600 border border-zinc-200">
                          <XCircle className="w-3 h-3 mr-1" /> Inactive
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button className="text-zinc-400 hover:text-zinc-900 transition-colors p-2 lg:-mr-2">
                        <MoreVertical className="w-4 h-4 ml-auto" />
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={5} className="px-6 py-12 text-center text-zinc-500">
                    <div className="flex flex-col items-center justify-center">
                      <Users className="w-12 h-12 text-zinc-300 mb-4" />
                      <p className="text-lg font-medium text-zinc-900">No vendors found</p>
                      <p className="text-sm mt-1">Try adjusting your search criteria or add a new vendor.</p>
                    </div>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <CreateVendorModal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreateVendor}
        categories={categories}
        districts={districts}
      />
    </div>
  );
}
