'use client';

import React, { useState } from 'react';
import { DashboardLayout } from '@/components/dashboard/layout';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';
import { useToast } from '@/hooks/use-toast';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { PlaceHolderImages } from '@/lib/placeholder-images';

const courses = [
  { id: 'CS-461', name: 'Introduction to AI' },
  { id: 'CS-250', name: 'Data Structures' },
];

const studentsByCourse = {
  'CS-461': [
    { id: 'S001', name: 'Alice Johnson' },
    { id: 'S002', name: 'Bob Williams' },
    { id: 'S003', name: 'Charlie Brown' },
    { id: 'S004', name: 'Diana Miller' },
  ],
  'CS-250': [
    { id: 'S005', name: 'Eve Davis' },
    { id: 'S006', name: 'Frank White' },
    { id: 'S007', name: 'Grace Hall' },
  ],
};

type AttendanceStatus = 'present' | 'absent';
type AttendanceState = Record<string, AttendanceStatus>;


export default function AttendancePage() {
  const [selectedCourse, setSelectedCourse] = useState(courses[0].id);
  const [attendance, setAttendance] = useState<AttendanceState>({});
  const { toast } = useToast();

  const students = studentsByCourse[selectedCourse as keyof typeof studentsByCourse] || [];
  
  const studentAvatar = PlaceHolderImages.find((img) => img.id === 'avatar-1');

  React.useEffect(() => {
    const initialAttendance: AttendanceState = {};
    for (const student of students) {
        initialAttendance[student.id] = 'present';
    }
    setAttendance(initialAttendance);
  }, [selectedCourse, students]);


  const handleAttendanceChange = (studentId: string, value: AttendanceStatus) => {
    setAttendance((prev) => ({ ...prev, [studentId]: value }));
  };

  const handleSubmit = () => {
    console.log('Submitting attendance:', attendance);
    toast({
      title: 'Attendance Submitted',
      description: `Attendance for ${courses.find(c => c.id === selectedCourse)?.name} has been recorded.`,
    });
  };

  return (
    <DashboardLayout role="faculty">
      <div className="space-y-6">
        <h2 className="text-3xl font-bold tracking-tight">Mark Attendance</h2>
        <Card>
          <CardHeader>
            <CardTitle>Select Course and Date</CardTitle>
            <div className="flex flex-col gap-4 pt-2 sm:flex-row">
              <div className="w-full sm:w-[300px]">
                <Select value={selectedCourse} onValueChange={setSelectedCourse}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a course" />
                  </SelectTrigger>
                  <SelectContent>
                    {courses.map((course) => (
                      <SelectItem key={course.id} value={course.id}>
                        {course.name} - {course.id}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <input
                type="date"
                defaultValue={new Date().toISOString().substring(0, 10)}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto"
              />
            </div>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Student</TableHead>
                  <TableHead className="w-[250px] text-right">Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {students.map((student) => (
                  <TableRow key={student.id}>
                    <TableCell>
                      <div className="flex items-center gap-3">
                        <Avatar>
                            {studentAvatar && <AvatarImage src={studentAvatar.imageUrl} alt={student.name} />}
                            <AvatarFallback>{student.name.charAt(0)}</AvatarFallback>
                        </Avatar>
                        <div>
                            <div className="font-medium">{student.name}</div>
                            <div className="text-sm text-muted-foreground">{student.id}</div>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell className="text-right">
                      <RadioGroup
                        value={attendance[student.id] || 'present'}
                        onValueChange={(value) => handleAttendanceChange(student.id, value as AttendanceStatus)}
                        className="flex justify-end gap-4"
                      >
                        <div className="flex items-center space-x-2">
                          <RadioGroupItem value="present" id={`${student.id}-present`} />
                          <Label htmlFor={`${student.id}-present`}>Present</Label>
                        </div>
                        <div className="flex items-center space-x-2">
                          <RadioGroupItem value="absent" id={`${student.id}-absent`} />
                          <Label htmlFor={`${student.id}-absent`}>Absent</Label>
                        </div>
                      </RadioGroup>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
            <div className="mt-6 flex justify-end">
              <Button onClick={handleSubmit}>Submit Attendance</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
