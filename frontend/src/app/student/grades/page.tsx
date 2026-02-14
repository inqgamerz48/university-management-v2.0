import { DashboardLayout } from '@/components/dashboard/layout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, TrendingDown } from 'lucide-react';

const gradesData = [
  { course: 'Calculus II', code: 'MATH-201', grade: 'A-', progress: 92, trend: 'up' },
  { course: 'World History', code: 'HIST-101', grade: 'B+', progress: 88, trend: 'up' },
  { course: 'Introduction to AI', code: 'CS-461', grade: 'A', progress: 95, trend: 'up' },
  { course: 'General Chemistry', code: 'CHEM-101', grade: 'B', progress: 85, trend: 'down' },
];

export default function GradesPage() {
  const overallGpa = 3.8;

  return (
    <DashboardLayout role="student">
      <div className="space-y-6">
        <h2 className="text-3xl font-bold tracking-tight">My Grades</h2>
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            <Card>
                <CardHeader>
                    <CardTitle>Overall GPA</CardTitle>
                    <CardDescription>Your cumulative Grade Point Average.</CardDescription>
                </CardHeader>
                <CardContent>
                    <p className="text-5xl font-bold text-primary">{overallGpa.toFixed(2)}</p>
                    <p className="text-sm text-muted-foreground">Well done, keep up the great work!</p>
                </CardContent>
            </Card>
             <Card className="lg:col-span-2">
                <CardHeader>
                    <CardTitle>Performance Overview</CardTitle>
                    <CardDescription>Your grade distribution across all courses.</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {gradesData.map((course) => (
                      <div key={course.code} className="flex items-center justify-between">
                        <div>
                          <p className="font-medium">{course.course}</p>
                          <p className="text-sm text-muted-foreground">{course.code}</p>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-lg font-bold">{course.grade}</span>
                          <span className="text-sm text-muted-foreground">({course.progress}%)</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
            </Card>
        </div>

        <Card>
            <CardHeader>
                <CardTitle>Course Grades</CardTitle>
                <CardDescription>Detailed breakdown of your grades for the current semester.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
                {gradesData.map((course) => (
                <div key={course.code} className="rounded-lg border p-4">
                    <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                        <div>
                            <h3 className="font-semibold">{course.course}</h3>
                            <p className="text-sm text-muted-foreground">{course.code}</p>
                        </div>
                        <div className="flex items-center gap-4">
                            <Badge className="text-lg" variant="default">{course.grade}</Badge>
                             {course.trend === 'up' ? (
                                <TrendingUp className="h-5 w-5 text-green-500" />
                            ) : (
                                <TrendingDown className="h-5 w-5 text-red-500" />
                            )}
                        </div>
                    </div>
                    <div className="mt-4">
                        <Progress value={course.progress} className="h-2" />
                        <p className="mt-1 text-right text-xs text-muted-foreground">{course.progress}% Course Completion</p>
                    </div>
                </div>
                ))}
            </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
