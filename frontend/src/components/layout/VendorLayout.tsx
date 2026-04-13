import { Link, Outlet, useLocation } from "react-router-dom";
import { 
  Home, 
  BookOpen, 
  Calendar, 
  Settings as SettingsIcon,
  Bell
} from "lucide-react";

export function VendorLayout() {
  const location = useLocation();

  const navItems = [
    { name: "Overview", href: "/vendor/dashboard", icon: Home },
    { name: "Bookings", href: "/vendor/bookings", icon: BookOpen },
    { name: "Calendar", href: "/vendor/calendar", icon: Calendar },
    { name: "Settings", href: "/vendor/settings", icon: SettingsIcon },
  ];

  return (
    <div className="flex h-[100dvh] bg-stone-50 overflow-hidden font-sans">
      
      {/* Desktop Sidebar (Vendor Theme) */}
      <aside className="hidden lg:flex w-64 bg-stone-900 text-stone-300 flex-col">
        <div className="h-20 flex items-center px-8 border-b border-stone-800 font-bold text-xl tracking-tight text-white">
          VENDOR HUB
        </div>
        <nav className="flex-1 overflow-y-auto py-6 px-4 space-y-1">
          {navItems.map((item) => {
            const isActive = location.pathname.startsWith(item.href);
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center px-4 py-3 rounded-lg text-sm font-medium transition-colors relative ${
                  isActive 
                    ? "bg-white/10 text-white" 
                    : "text-stone-400 hover:bg-white/5 hover:text-stone-200"
                }`}
              >
                <Icon className={`w-5 h-5 mr-4 ${isActive ? "text-white" : "text-stone-400"}`} />
                {item.name}
                {isActive && (
                  <div className="absolute left-0 w-1 h-8 bg-white rounded-r-full" />
                )}
              </Link>
            );
          })}
        </nav>
        <div className="p-4 border-t border-stone-800">
          <div className="flex items-center space-x-3">
             <div className="w-10 h-10 rounded-full bg-stone-800 flex items-center justify-center text-white font-bold">V</div>
             <div>
               <p className="text-sm font-medium text-white">Your Business</p>
               <p className="text-xs text-stone-400">vendor@email.com</p>
             </div>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-[100dvh] w-full pb-16 lg:pb-0 relative">
        
        {/* Top Header */}
        <header className="h-16 lg:h-20 bg-white border-b border-stone-200 flex items-center justify-between px-4 lg:px-8 shadow-sm z-10">
          <h1 className="text-xl lg:text-2xl font-semibold text-stone-900 hidden sm:block">Dashboard</h1>
          <span className="font-bold text-lg tracking-tight text-stone-900 sm:hidden">
            VENDOR HUB
          </span>
          
          <div className="flex items-center space-x-2 sm:space-x-6">
            <button className="p-2 rounded-full bg-stone-100 text-stone-600 hover:text-stone-900 relative">
              <Bell className="w-5 h-5" />
            </button>
            <div className="w-8 h-8 sm:h-10 sm:w-10 rounded-full overflow-hidden border border-stone-200 shrink-0 lg:hidden">
               <div className="w-full h-full bg-stone-900 flex items-center justify-center text-white font-bold text-sm">V</div>
            </div>
          </div>
        </header>

        {/* Dashboard Content Outlet */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-stone-50 p-4 lg:p-8">
          <Outlet />
        </main>

        {/* Mobile Bottom Navigation */}
        <nav className="lg:hidden fixed bottom-0 left-0 right-0 h-16 bg-white border-t border-stone-200 flex justify-around items-center px-2 z-50">
          {navItems.map((item) => {
            const isActive = location.pathname.startsWith(item.href);
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                to={item.href}
                className="flex flex-col items-center justify-center w-16 h-full space-y-1"
              >
                <div className={`p-1.5 rounded-full transition-colors ${isActive ? 'bg-stone-100' : 'bg-transparent'}`}>
                  <Icon className={`w-5 h-5 ${isActive ? "text-stone-900" : "text-stone-500"}`} />
                </div>
                <span className={`text-[10px] font-medium ${isActive ? "text-stone-900" : "text-stone-500"}`}>
                  {item.name}
                </span>
              </Link>
            );
          })}
        </nav>
      </div>
    </div>
  );
}
