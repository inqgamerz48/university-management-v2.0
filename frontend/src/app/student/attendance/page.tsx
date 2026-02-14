
'use client';
import { DashboardLayout } from '@/components/dashboard/layout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Calendar } from '@/components/ui/calendar';
import { Check, X } from 'lucide-react';
import React from 'react';

const attendanceData = [
  { course: 'Calculus II', code: 'MATH-201', present: 28, total: 30 },
  { course: 'World History', code: 'HIST-101', present: 25, total: 25 },
  { course: 'Introduction to AI', code: 'CS-461', present: 29, total: 30 },
  { course: 'General Chemistry', code: 'CHEM-101', present: 22, total: 24 },
];

const absentDates = [
    new Date(2024, 9, 15), // Oct 15
    new Date(2024, 9, 21), // Oct 21
    new Date(2024, 10, 2), // Nov 2
];

export default function AttendancePage() {
  const [date, setDate] = React.useState<Date | undefined>(new Date());

  const getAttendancePercentage = (present: number, total: number) => {
    if (total === 0) return 100;
    return (present / total) * 100;
  };

  return (
    <DashboardLayout role="student">
      <div className="space-y-6">
        <h2 className="text-3xl font-bold tracking-tight">My Attendance</h2>
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="space-y-6 lg:col-span-2">
            {attendanceData.map((item) => {
              const percentage = getAttendancePercentage(item.present, item.total);
              return (
                <Card key={item.code}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                        <div>
                            <CardTitle>{item.course}</CardTitle>
                            <CardDescription>{item.code}</CardDescription>
                        </div>
                        <Badge variant={percentage >= 80 ? 'default' : 'destructive'}>
                            {percentage.toFixed(1)}%
                        </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground">
                      Attended {item.present} out of {item.total} classes.
                    </p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
          <div className="lg:col-span-1">
             <Card>
                <CardHeader>
                    <CardTitle>Attendance Calendar</CardTitle>
                    <CardDescription>Days you were marked absent are highlighted.</CardDescription>
                </CardHeader>
                <CardContent className="flex justify-center">
                    <Calendar
                        mode="single"
                        selected={date}
                        onSelect={setDate}
                        className="rounded-md border p-0"
                        modifiers={{
                            absent: absentDates,
                        }}
                        modifiersStyles={{
                            absent: { 
                                color: 'hsl(var(--destructive-foreground))',
                                backgroundColor: 'hsl(var(--destructive))',
                             },
                        }}
                    />
                </CardContent>
             </Card>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
