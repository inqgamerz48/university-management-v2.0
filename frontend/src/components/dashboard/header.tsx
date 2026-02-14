'use client';
import { Bell, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { SidebarTrigger } from '@/components/ui/sidebar';
import { UserNav } from '@/components/dashboard/user-nav';

type DashboardHeaderProps = {
  role: 'student' | 'faculty' | 'admin' | 'super-admin';
};

export function DashboardHeader({ role }: DashboardHeaderProps) {
  return (
    <header className="fixed left-0 right-0 top-0 z-10 flex h-16 items-center gap-4 border-b bg-background/80 px-4 backdrop-blur-sm sm:px-6 peer-data-[state=open]:[data-variant=sidebar]:pl-[var(--sidebar-width)] peer-data-[state=open]:[data-variant=sidebar]:lg:pl-[var(--sidebar-width)] peer-data-[variant=inset]:pr-2 peer-data-[variant=inset]:md:left-[calc(var(--sidebar-width)_+_0.5rem)] peer-data-[state=collapsed]:peer-data-[variant=inset]:md:left-[calc(var(--sidebar-width-icon)_+_1rem)]">
      <div className="flex items-center gap-2">
        <SidebarTrigger className="md:hidden" />
        <h1 className="text-lg font-semibold capitalize hidden md:block">
          {role.replace('-', ' ')} Dashboard
        </h1>
      </div>

      <div className="ml-auto flex items-center gap-4">
        <div className="relative hidden w-full max-w-sm items-center md:flex">
          <Input id="search" type="search" placeholder="Search..." className="pl-10" />
          <span className="absolute inset-y-0 left-0 flex items-center justify-center pl-3">
            <Search className="h-5 w-5 text-muted-foreground" />
          </span>
        </div>
        <Button variant="ghost" size="icon" className="rounded-full">
          <Bell className="h-5 w-5 text-muted-foreground" />
          <span className="sr-only">Toggle notifications</span>
        </Button>
        <div className="md:hidden">
          <UserNav role={role} />
        </div>
      </div>
    </header>
  );
}
