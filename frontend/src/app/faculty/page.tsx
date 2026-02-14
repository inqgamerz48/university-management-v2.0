import { DashboardLayout } from '@/components/dashboard/layout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Users, BarChart, Bell, Megaphone, FileUp } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export default function FacultyDashboard() {
  return (
    <DashboardLayout role="faculty">
      <div className="space-y-6">
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Announcements</CardTitle>
                <CardDescription>
                  Important updates and information for faculty members.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                  <div className="flex items-start gap-4">
                      <div className="rounded-full bg-primary/10 p-3 text-primary">
                          <Megaphone className="h-5 w-5" />
                      </div>
                      <div className="flex-1">
                          <p className="font-medium">Library System Update</p>
                          <p className="text-sm text-muted-foreground">The online library portal will be down for scheduled maintenance this Sunday from 2 AM to 4 AM.</p>
                          <p className="text-xs text-muted-foreground">Posted just now</p>
                      </div>
                  </div>
                  <div className="flex items-start gap-4">
                      <div className="rounded-full bg-primary/10 p-3 text-primary">
                          <Megaphone className="h-5 w-5" />
                      </div>
                      <div className="flex-1">
                          <p className="font-medium">Faculty Meeting Scheduled</p>
                          <p className="text-sm text-muted-foreground">A mandatory all-faculty meeting is scheduled for next Friday at 10:00 AM in the main conference hall.</p>
                          <p className="text-xs text-muted-foreground">Posted 1 day ago</p>
                      </div>
                  </div>
                  <div className="flex items-start gap-4">
                      <div className="rounded-full bg-primary/10 p-3 text-primary">
                          <Megaphone className="h-5 w-5" />
                      </div>
                      <div className="flex-1">
                          <p className="font-medium">New Grading Policy</p>
                          <p className="text-sm text-muted-foreground">Please review the updated grading policy document available on the faculty portal before the start of the new semester.</p>
                          <p className="text-xs text-muted-foreground">Posted 3 days ago</p>
                      </div>
                  </div>
              </CardContent>
            </Card>
          </div>
          <div className="space-y-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">My Courses</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">4</div>
                <p className="text-xs text-muted-foreground">
                  +2 from last semester
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Avg. Student Performance</CardTitle>
                <BarChart className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">88%</div>
                <p className="text-xs text-muted-foreground">
                  Class average across all courses
                </p>
              </CardContent>
            </Card>
             <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Recent Activity</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4 text-sm">
                  <div className="flex items-center gap-3">
                      <div className="rounded-full bg-primary/10 p-2 text-primary">
                          <Bell className="h-4 w-4" />
                      </div>
                      <p className="text-muted-foreground">3 new submissions for <span className="font-semibold text-foreground">Project Alpha</span>.</p>
                  </div>
                   <div className="flex items-center gap-3">
                      <div className="rounded-full bg-primary/10 p-2 text-primary">
                          <Bell className="h-4 w-4" />
                      </div>
                      <p className="text-muted-foreground">You graded <span className="font-semibold text-foreground">Midterm Exams</span>.</p>
                  </div>
              </CardContent>
            </Card>
          </div>
        </div>
        <Card>
          <CardHeader>
            <CardTitle>Bulk Student Import</CardTitle>
            <CardDescription>
              Upload a CSV or Excel file to import students into your courses.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-4 sm:flex-row sm:items-center">
            <div className="flex-1">
              <Input
                id="bulk-import-faculty"
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
