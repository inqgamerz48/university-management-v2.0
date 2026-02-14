import {
  LayoutDashboard,
  FileText,
  GraduationCap,
  User,
  Users,
  BookOpen,
  Settings,
  Shield,
  CalendarCheck,
  LifeBuoy,
  Ticket,
} from "lucide-react";

export type NavLink = {
  href: string;
  label: string;
  icon: React.ElementType;
};

export const studentNavLinks: NavLink[] = [
  { href: "/student", label: "Dashboard", icon: LayoutDashboard },
  { href: "/student/assignments", label: "Assignments", icon: FileText },
  { href: "/student/grades", label: "Grades", icon: GraduationCap },
  { href: "/student/attendance", label: "Attendance", icon: CalendarCheck },
  { href: "/student/support", label: "Support", icon: LifeBuoy },
  { href: "#", label: "Profile", icon: User },
];

export const facultyNavLinks: NavLink[] = [
  { href: "/faculty", label: "Dashboard", icon: LayoutDashboard },
  { href: "/faculty/assignments", label: "Assignments", icon: FileText },
  { href: "/faculty/attendance", label: "Attendance", icon: CalendarCheck },
  { href: "#", label: "My Students", icon: Users },
  { href: "#", label: "Profile", icon: User },
];

export const adminNavLinks: NavLink[] = [
  { href: "/admin", label: "Dashboard", icon: LayoutDashboard },
  { href: "/admin/support", label: "Support Tickets", icon: Ticket },
  { href: "#", label: "Manage Users", icon: Users },
  { href: "#", label: "Courses", icon: BookOpen },
  { href: "#", label: "System Settings", icon: Settings },
  { href: "#", label: "Security", icon: Shield },
];

export const navLinks: Record<string, NavLink[]> = {
  student: studentNavLinks,
  faculty: facultyNavLinks,
  admin: adminNavLinks,
  "super-admin": adminNavLinks,
};
