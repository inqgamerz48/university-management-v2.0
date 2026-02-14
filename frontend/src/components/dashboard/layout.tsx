'use client';

import type { ReactNode } from 'react';
import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar';
import { DashboardSidebar } from '@/components/dashboard/sidebar';
import { DashboardHeader } from '@/components/dashboard/header';
import { useAuth } from '@/context/auth-context';

type DashboardLayoutProps = {
  children: ReactNode;
  role: 'student' | 'faculty' | 'admin';
};

export function DashboardLayout({ children, role }: DashboardLayoutProps) {
  const { user } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!user) {
      router.push('/');
      return;
    }

    let isAuthorized = user.role === role;
    // Allow super-admin to access admin pages
    if (role === 'admin' && user.role === 'super-admin') {
      isAuthorized = true;
    }

    if (!isAuthorized) {
      router.push('/');
    }
  }, [user, role, router]);

  if (!user || (user.role !== role && !(role === 'admin' && user.role === 'super-admin'))) {
    return (
        <div className="flex h-screen w-full items-center justify-center">
            <p>Loading...</p>
        </div>
    );
  }

  return (
    <SidebarProvider>
      <div className="min-h-screen w-full bg-background">
        <DashboardSidebar role={user.role} />
        <SidebarInset>
          <DashboardHeader role={user.role} />
          <main className="p-4 pt-20 sm:p-6 lg:p-8">{children}</main>
        </SidebarInset>
      </div>
    </SidebarProvider>
  );
}
