import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true,
  },
});

// API Client for Python Backend
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const apiClient = {
  async fetch(endpoint: string, options: RequestInit = {}) {
    const session = await supabase.auth.getSession();
    const token = session.data.session?.access_token;

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...((options.headers as Record<string, string>) || {}),
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  },

  get(endpoint: string) {
    return this.fetch(endpoint, { method: 'GET' });
  },

  post(endpoint: string, data: any) {
    return this.fetch(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  put(endpoint: string, data: any) {
    return this.fetch(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  },

  delete(endpoint: string) {
    return this.fetch(endpoint, { method: 'DELETE' });
  },
};

// Auth API
export const authApi = {
  async login(email: string, password: string) {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });

    if (error) throw error;
    return data;
  },

  async signup(email: string, password: string, userData: any) {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: userData,
      },
    });

    if (error) throw error;
    return data;
  },

  async logout() {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
  },

  async getCurrentUser() {
    const { data: { user }, error } = await supabase.auth.getUser();
    if (error) throw error;
    return user;
  },

  async resetPassword(email: string) {
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/auth/reset-password`,
    });
    if (error) throw error;
  },

  onAuthStateChange(callback: (event: string, session: any) => void) {
    return supabase.auth.onAuthStateChange(callback);
  },
};

// Users API
export const usersApi = {
  getAll(params?: { role?: string; department?: string; search?: string }) {
    const queryParams = new URLSearchParams();
    if (params?.role) queryParams.append('role', params.role);
    if (params?.department) queryParams.append('department', params.department);
    if (params?.search) queryParams.append('search', params.search);
    
    return apiClient.get(`/users/?${queryParams.toString()}`);
  },

  getById(id: string) {
    return apiClient.get(`/users/${id}`);
  },

  update(id: string, data: any) {
    return apiClient.put(`/users/${id}`, data);
  },

  delete(id: string) {
    return apiClient.delete(`/users/${id}`);
  },

  getCourses(id: string) {
    return apiClient.get(`/users/${id}/courses`);
  },
};

// Courses API
export const coursesApi = {
  getAll(params?: any) {
    const queryParams = new URLSearchParams();
    if (params?.department_id) queryParams.append('department_id', params.department_id);
    if (params?.search) queryParams.append('search', params.search);
    
    return apiClient.get(`/courses/?${queryParams.toString()}`);
  },

  getById(id: number) {
    return apiClient.get(`/courses/${id}`);
  },

  create(data: any) {
    return apiClient.post('/courses/', data);
  },

  update(id: number, data: any) {
    return apiClient.put(`/courses/${id}`, data);
  },

  delete(id: number) {
    return apiClient.delete(`/courses/${id}`);
  },

  enrollStudent(courseId: number, studentId: string) {
    return apiClient.post(`/courses/${courseId}/enroll?student_id=${studentId}`, {});
  },

  getEnrollments(courseId: number) {
    return apiClient.get(`/courses/${courseId}/enrollments`);
  },
};

// Assignments API
export const assignmentsApi = {
  getAll(params?: any) {
    const queryParams = new URLSearchParams();
    if (params?.course_id) queryParams.append('course_id', params.course_id);
    if (params?.status) queryParams.append('status', params.status);
    
    return apiClient.get(`/assignments/?${queryParams.toString()}`);
  },

  getById(id: number) {
    return apiClient.get(`/assignments/${id}`);
  },

  create(data: any) {
    return apiClient.post('/assignments/', data);
  },

  update(id: number, data: any) {
    return apiClient.put(`/assignments/${id}`, data);
  },

  delete(id: number) {
    return apiClient.delete(`/assignments/${id}`);
  },

  submit(assignmentId: number, file: File, comments?: string) {
    const formData = new FormData();
    formData.append('file', file);
    if (comments) formData.append('comments', comments);

    return apiClient.fetch(`/assignments/${assignmentId}/submit`, {
      method: 'POST',
      body: formData,
      headers: {}, // Let browser set content-type with boundary
    });
  },

  getMySubmission(assignmentId: number) {
    return apiClient.get(`/assignments/${assignmentId}/my-submission`);
  },

  gradeSubmission(assignmentId: number, submissionId: number, data: any) {
    return apiClient.put(`/assignments/${assignmentId}/submissions/${submissionId}/grade`, data);
  },
};

// Attendance API
export const attendanceApi = {
  getCourseAttendance(courseId: number, params?: any) {
    const queryParams = new URLSearchParams();
    if (params?.start_date) queryParams.append('start_date', params.start_date);
    if (params?.end_date) queryParams.append('end_date', params.end_date);
    
    return apiClient.get(`/attendance/course/${courseId}?${queryParams.toString()}`);
  },

  getByDate(courseId: number, date: string) {
    return apiClient.get(`/attendance/course/${courseId}/date/${date}`);
  },

  markAttendance(courseId: number, data: any) {
    return apiClient.post(`/attendance/course/${courseId}/mark`, data);
  },

  markBulk(courseId: number, data: any) {
    return apiClient.post(`/attendance/course/${courseId}/mark-bulk`, data);
  },

  getMyAttendance(params?: any) {
    const queryParams = new URLSearchParams();
    if (params?.course_id) queryParams.append('course_id', params.course_id);
    
    return apiClient.get(`/attendance/my-attendance?${queryParams.toString()}`);
  },

  getStatistics(courseId: number) {
    return apiClient.get(`/attendance/course/${courseId}/statistics`);
  },
};

// Announcements API
export const announcementsApi = {
  getAll(params?: any) {
    const queryParams = new URLSearchParams();
    if (params?.pinned_only) queryParams.append('pinned_only', 'true');
    if (params?.priority) queryParams.append('priority', params.priority);
    
    return apiClient.get(`/announcements/?${queryParams.toString()}`);
  },

  getById(id: number) {
    return apiClient.get(`/announcements/${id}`);
  },

  create(data: any) {
    return apiClient.post('/announcements/', data);
  },

  update(id: number, data: any) {
    return apiClient.put(`/announcements/${id}`, data);
  },

  delete(id: number) {
    return apiClient.delete(`/announcements/${id}`);
  },
};

// Notifications API
export const notificationsApi = {
  getAll(unreadOnly?: boolean) {
    const queryParams = new URLSearchParams();
    if (unreadOnly) queryParams.append('unread_only', 'true');
    
    return apiClient.get(`/notifications/?${queryParams.toString()}`);
  },

  getUnreadCount() {
    return apiClient.get('/notifications/unread-count');
  },

  markAsRead(id: number) {
    return apiClient.post(`/notifications/${id}/mark-read`, {});
  },

  markAllAsRead(ids: number[]) {
    return apiClient.post('/notifications/mark-all-read', { notification_ids: ids });
  },

  delete(id: number) {
    return apiClient.delete(`/notifications/${id}`);
  },

  clearAll() {
    return apiClient.delete('/notifications/');
  },
};

// Dashboard API
export const dashboardApi = {
  getAdminStats() {
    return apiClient.get('/dashboard/admin/stats');
  },

  getStudentDashboard() {
    return apiClient.get('/dashboard/student');
  },

  getFacultyDashboard() {
    return apiClient.get('/dashboard/faculty');
  },
};

// File Upload
export const storageApi = {
  async uploadFile(bucket: string, path: string, file: File) {
    const { data, error } = await supabase.storage
      .from(bucket)
      .upload(path, file);
    
    if (error) throw error;
    
    const { data: { publicUrl } } = supabase.storage
      .from(bucket)
      .getPublicUrl(data.path);
    
    return { ...data, publicUrl };
  },

  async deleteFile(bucket: string, path: string) {
    const { error } = await supabase.storage
      .from(bucket)
      .remove([path]);
    
    if (error) throw error;
    return true;
  },

  getPublicUrl(bucket: string, path: string) {
    const { data: { publicUrl } } = supabase.storage
      .from(bucket)
      .getPublicUrl(path);
    
    return publicUrl;
  },
};
