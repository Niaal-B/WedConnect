import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LandingPage } from "./pages/LandingPage";
import { PlaceholderPage } from "./pages/PlaceholderPage";
import { AdminLogin } from "./pages/admin/AdminLogin";
import { AdminDashboard } from "./pages/admin/AdminDashboard";
import { AdminVendors } from "./pages/admin/AdminVendors";
import { AdminLayout } from "./components/layout/AdminLayout";
import { VendorLogin } from "./pages/vendor/VendorLogin";
import { VendorLayout } from "./components/layout/VendorLayout";
import { VendorBookings } from "./pages/vendor/VendorBookings";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<PlaceholderPage title="Sign In" />} />
        <Route path="/register" element={<PlaceholderPage title="Get Started" />} />
        <Route path="/help" element={<PlaceholderPage title="Need help?" />} />
        
        {/* Admin Routes */}
        <Route path="/admin/login" element={<AdminLogin />} />
        
        {/* Protected Area Layout */}
        <Route path="/admin" element={<AdminLayout />}>
          <Route path="dashboard" element={<AdminDashboard />} />
          <Route path="bookings" element={<PlaceholderPage title="Bookings Table" />} />
          <Route path="vendors" element={<AdminVendors />} />
          <Route path="settings" element={<PlaceholderPage title="Admin Settings" />} />
        </Route>

        <Route path="/vendor/login" element={<VendorLogin />} />
        <Route path="/vendor" element={<VendorLayout />}>
          <Route path="dashboard" element={<PlaceholderPage title="Vendor Overview Dashboard" />} />
          <Route path="bookings" element={<VendorBookings />} />
          <Route path="calendar" element={<PlaceholderPage title="Event Calendar" />} />
          <Route path="settings" element={<PlaceholderPage title="Profile Settings" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
