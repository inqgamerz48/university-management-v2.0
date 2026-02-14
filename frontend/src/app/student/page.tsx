import { DashboardLayout } from '@/components/dashboard/layout';
import { FileUpload } from '@/components/dashboard/file-upload';
import { Bell, FileCheck2, Clock } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

export default function StudentDashboard() {
  return (
    <DashboardLayout role="student">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Submit Your Assignment</CardTitle>
            <CardDescription>Upload your files for "Introduction to AI - Project 1".</CardDescription>
          </CardHeader>
          <CardContent>
            <FileUpload />
          </CardContent>
        </Card>
        <Card className="col-span-4 lg:col-span-3">
          <CardHeader className="flex flex-row items-center justify-between">
            <div className="space-y-1.5">
              <CardTitle>Notifications</CardTitle>
              <CardDescription>Recent updates and announcements.</CardDescription>
            </div>
            <Bell className="h-6 w-6 text-muted-foreground" />
          </CardHeader>
          <CardContent className="grid gap-4">
            <div className="flex items-start gap-4">
              <div className="rounded-full bg-primary/10 p-2 text-primary">
                <FileCheck2 className="h-5 w-5" />
              </div>
              <div className="flex-1 space-y-1">
                <p className="text-sm font-medium leading-none">New Grades Available</p>
                <p className="text-sm text-muted-foreground">Your grade for "History 101 Midterm" has been posted.</p>
                <p className="text-xs text-muted-foreground">2 hours ago</p>
              </div>
              <Button variant="outline" size="sm">View</Button>
            </div>
             <div className="flex items-start gap-4">
              <div className="rounded-full bg-yellow-500/10 p-2 text-yellow-500">
                <Clock className="h-5 w-5" />
              </div>
              <div className="flex-1 space-y-1">
                <p className="text-sm font-medium leading-none">Assignment Due Soon</p>
                <p className="text-sm text-muted-foreground">"Calculus II - Homework 5" is due tomorrow.</p>
                <p className="text-xs text-muted-foreground">1 day ago</p>
              </div>
              <Badge variant="secondary" className="bg-yellow-500/20 text-yellow-400">Urgent</Badge>
            </div>
             <div className="flex items-start gap-4">
              <div className="rounded-full bg-blue-500/10 p-2 text-blue-500">
                <Bell className="h-5 w-5" />
              </div>
              <div className="flex-1 space-y-1">
                <p className="text-sm font-medium leading-none">Library System Update</p>
                <p className="text-sm text-muted-foreground">The library portal will be down for maintenance on Sunday.</p>
                <p className="text-xs text-muted-foreground">2 days ago</p>
              </div>
            </div>
            <div className="flex items-start gap-4">
              <div className="rounded-full bg-blue-500/10 p-2 text-blue-500">
                <Bell className="h-5 w-5" />
              </div>
              <div className="flex-1 space-y-1">
                <p className="text-sm font-medium leading-none">Campus Event</p>
                <p className="text-sm text-muted-foreground">Annual tech fair is happening this Friday.</p>
                <p className="text-xs text-muted-foreground">3 days ago</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
