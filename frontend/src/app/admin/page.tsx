import { DashboardLayout } from '@/components/dashboard/layout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Users, BookOpen, Settings, Activity, GraduationCap, FileUp, Megaphone } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';

const stats = [
  {
    title: 'Total Students',
    value: '12,405',
    change: '+12.5% this month',
    icon: Users,
  },
  {
    title: 'Total Faculty',
    value: '852',
    change: '+2.1% this month',
    icon: GraduationCap,
  },
  {
    title: 'Active Courses',
    value: '1,200',
    change: '+50 new courses',
    icon: BookOpen,
  },
  {
    title: 'Server Health',
    value: '99.9% Uptime',
    change: 'All systems operational',
    icon: Activity,
  },
];

export default function AdminDashboard() {
  return (
    <DashboardLayout role="admin">
      <div className="space-y-6">
        <h2 className="text-3xl font-bold tracking-tight">System Overview</h2>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat) => (
            <Card key={stat.title}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">
                  {stat.title}
                </CardTitle>
                <stat.icon className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stat.value}</div>
                <p className="text-xs text-muted-foreground">{stat.change}</p>
              </CardContent>
            </Card>
          ))}
        </div>
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <Card>
                <CardHeader>
                    <CardTitle>Quick Actions</CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-2 gap-4 md:grid-cols-3">
                    <ActionCard icon={Users} title="Manage Users" />
                    <ActionCard icon={BookOpen} title="Manage Courses" />
                    <ActionCard icon={Settings} title="System Settings" />
                </CardContent>
            </Card>
            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardTitle>Create Announcement</CardTitle>
                        <Megaphone className="h-5 w-5 text-muted-foreground" />
                    </div>
                    <CardDescription>
                        Post an announcement to all students and faculty.
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <Input placeholder="Announcement Title" />
                    <Textarea placeholder="Write your announcement here..." rows={3} />
                </CardContent>
                <CardFooter>
                    <Button className="ml-auto">Post Announcement</Button>
                </CardFooter>
            </Card>
        </div>
        <Card>
          <CardHeader>
            <CardTitle>Bulk Student Import</CardTitle>
            <CardDescription>
              Upload a CSV or Excel file to import multiple students at once.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-4 sm:flex-row sm:items-center">
            <div className="flex-1">
              <Input
                id="bulk-import"
                type="file"
                accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
              />
            </div>
            <Button>
              <FileUp className="mr-2 h-4 w-4" />
              Import Students
            </Button>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}

function ActionCard({ icon: Icon, title }: { icon: React.ElementType, title: string }) {
    return (
        <div className="flex cursor-pointer flex-col items-center justify-center gap-2 rounded-lg border p-4 transition-colors hover:bg-accent/50 hover:text-accent-foreground">
            <Icon className="h-8 w-8 text-primary" />
            <span className="text-center text-sm font-medium">{title}</span>
        </div>
    )
}
