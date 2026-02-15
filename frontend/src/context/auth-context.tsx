'use client';

import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { User } from '@supabase/supabase-js';
import { authApi, apiClient } from '@/lib/supabase';

type Role = 'student' | 'faculty' | 'admin' | 'super-admin';

interface UserProfile {
  id: string;
  email: string;
  role: Role;
  name: string;
  department?: string;
  avatar_url?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface AuthContextType {
  user: UserProfile | null;
  supabaseUser: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, userData: any) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
  resetPassword: (email: string) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [supabaseUser, setSupabaseUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // Fetch user profile from backend
  const fetchUserProfile = async () => {
    try {
      const profile = await apiClient.get('/auth/me');
      setUser(profile);
    } catch (error) {
      console.error('Error fetching user profile:', error);
      setUser(null);
    }
  };

  // Initialize auth state
  useEffect(() => {
    const initAuth = async () => {
      try {
        const user = await authApi.getCurrentUser();
        if (user) {
          setSupabaseUser(user);
          await fetchUserProfile();
        }
      } catch (error) {
        console.log('No active session');
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();

    // Subscribe to auth changes
    const { data: { subscription } } = authApi.onAuthStateChange(async (event, session) => {
      if (session?.user) {
        setSupabaseUser(session.user);
        await fetchUserProfile();
      } else {
        setUser(null);
        setSupabaseUser(null);
      }
      setIsLoading(false);
    });

    return () => {
      subscription.unsubscribe();
    };
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true);
      const data = await authApi.login(email, password);
      
      if (data.user) {
        setSupabaseUser(data.user);
        
        // Get user profile from backend
        const profile = await apiClient.get('/auth/me');
        setUser(profile);
        
        // Redirect based on role
        const role = data.user.user_metadata?.role || profile?.role || 'student';
        if (role === 'super-admin' || role === 'admin') {
          router.push('/admin');
        } else if (role === 'faculty') {
          router.push('/faculty');
        } else {
          router.push('/student');
        }
      }
    } catch (error: any) {
      throw new Error(error.message || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (email: string, password: string, userData: any) => {
    try {
      setIsLoading(true);
      await authApi.signup(email, password, {
        name: userData.name,
        role: userData.role,
        department: userData.department,
      });
      
      // Note: We don't auto-login anymore to avoid race conditions
      // User will be shown success message and can login manually
    } catch (error: any) {
      throw new Error(error.message || 'Signup failed');
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      setIsLoading(true);
      await authApi.logout();
      setUser(null);
      setSupabaseUser(null);
      router.push('/');
    } catch (error: any) {
      console.error('Logout error:', error);
      // Still clear local state even if API call fails
      setUser(null);
      setSupabaseUser(null);
      router.push('/');
    } finally {
      setIsLoading(false);
    }
  };

  const refreshUser = async () => {
    await fetchUserProfile();
  };

  const resetPassword = async (email: string) => {
    await authApi.resetPassword(email);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        supabaseUser,
        isLoading,
        isAuthenticated: !!user,
        login,
        signup,
        logout,
        refreshUser,
        resetPassword,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Hook for protected routes
export const useRequireAuth = (allowedRoles?: Role[]) => {
  const { user, isLoading, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (!isAuthenticated) {
        router.push('/');
      } else if (allowedRoles && user && !allowedRoles.includes(user.role)) {
        router.push('/unauthorized');
      }
    }
  }, [isLoading, isAuthenticated, user, allowedRoles, router]);

  return { user, isLoading, isAuthenticated };
};
