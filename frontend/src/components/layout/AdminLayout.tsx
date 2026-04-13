import { Link, Outlet, useLocation } from "react-router-dom";
import { 
  Home, 
  BookOpen, 
  Users, 
  MessageSquare, 
  Search,
  Settings as SettingsIcon,
  Bell
} from "lucide-react";
import { Input } from "../ui/input";

export function AdminLayout() {
  const location = useLocation();

  const navItems = [
    { name: "Dashboard", href: "/admin/dashboard", icon: Home },
    { name: "Bookings", href: "/admin/bookings", icon: BookOpen },
    { name: "Vendors", href: "/admin/vendors", icon: Users },
    { name: "Complaints", href: "/admin/complaints", icon: MessageSquare },
  ];

  return (
    <div className="flex h-[100dvh] bg-zinc-50 overflow-hidden font-sans">
      
      {/* Desktop Sidebar */}
      <aside className="hidden lg:flex w-64 bg-white border-r border-zinc-200 flex-col">
        <div className="h-20 flex items-center px-8 border-b border-zinc-50 font-bold text-xl tracking-tight text-zinc-900">
          WEDCONNECT
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
                    ? "bg-zinc-100 text-zinc-900" 
                    : "text-zinc-500 hover:bg-zinc-50 hover:text-zinc-900"
                }`}
              >
                <Icon className={`w-5 h-5 mr-4 ${isActive ? "text-zinc-900" : "text-zinc-400"}`} />
                {item.name}
                {isActive && (
                  <div className="absolute left-0 w-1 h-8 bg-zinc-900 rounded-r-full" />
                )}
              </Link>
            );
          })}
        </nav>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-[100dvh] w-full pb-16 lg:pb-0 relative">
        
        {/* Top Header */}
        <header className="h-16 lg:h-20 bg-white border-b border-zinc-100 flex items-center justify-between px-4 lg:px-8">
          <h1 className="text-xl lg:text-2xl font-semibold text-zinc-900 hidden sm:block">Overview</h1>
          {/* Logo on mobile replacing Overview text */}
          <span className="font-bold text-lg tracking-tight text-zinc-900 sm:hidden">
            WEDCONNECT
          </span>
          
          <div className="flex items-center space-x-2 sm:space-x-6">
            <div className="relative w-[150px] sm:w-full max-w-[200px] sm:max-w-[250px]">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-4 w-4 text-zinc-400" />
              </div>
              <Input 
                type="text" 
                placeholder="Search..." 
                className="pl-10 bg-zinc-50 border-none rounded-full h-9 lg:h-10 w-full text-sm placeholder:text-zinc-400"
              />
            </div>
            
            <div className="flex items-center space-x-2 sm:space-x-3">
              <button className="hidden sm:block p-2 rounded-full bg-zinc-50 text-zinc-500 hover:bg-zinc-100">
                <SettingsIcon className="w-5 h-5" />
              </button>
              <button className="p-2 rounded-full bg-zinc-50 text-zinc-500 hover:text-zinc-900 relative">
                <Bell className="w-5 h-5" />
                <span className="absolute top-2 right-2.5 w-2 h-2 bg-black rounded-full border border-white"></span>
              </button>
              <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-full overflow-hidden border border-zinc-200 shrink-0">
                <img 
                  src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" 
                  alt="Admin profile" 
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
          </div>
        </header>

        {/* Dashboard Content Outlet */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-zinc-50 p-4 lg:p-8">
          <Outlet />
        </main>

        {/* Mobile Bottom Navigation */}
        <nav className="lg:hidden fixed bottom-0 left-0 right-0 h-16 bg-white border-t border-zinc-200 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] flex justify-around items-center px-2 z-50">
          {navItems.map((item) => {
            const isActive = location.pathname.startsWith(item.href);
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                to={item.href}
                className="flex flex-col items-center justify-center w-16 h-full space-y-1"
              >
                <div className={`p-1.5 rounded-full ${isActive ? 'bg-zinc-100' : 'bg-transparent'}`}>
                  <Icon className={`w-5 h-5 ${isActive ? "text-zinc-900" : "text-zinc-500"}`} />
                </div>
                <span className={`text-[10px] font-medium ${isActive ? "text-zinc-900" : "text-zinc-500"}`}>
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
