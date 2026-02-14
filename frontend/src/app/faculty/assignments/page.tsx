
'use client';

import { useState } from 'react';
import { DashboardLayout } from '@/components/dashboard/layout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Users, Clock } from 'lucide-react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"


const departments = ['All Departments', 'Computer Science', 'History', 'Mathematics', 'Chemistry'];

const assignmentsByDept = {
    'Computer Science': [
        {
            course: 'Introduction to AI - CS-461',
            title: 'Project 1: Search Algorithms',
            dueDate: '2024-11-01',
            submissions: 45,
            pending: 10,
        },
        {
            course: 'Data Structures - CS-250',
            title: 'Homework 3: Trees and Graphs',
            dueDate: '2024-10-28',
            submissions: 52,
            pending: 5,
        },
    ],
    'History': [
        {
            course: 'World History - HIST-101',
            title: 'Midterm Essay: The Roman Empire',
            dueDate: '2024-10-20',
            submissions: 30,
            pending: 0,
        },
    ],
    'Mathematics': [
         {
            course: 'Calculus II - MATH-201',
            title: 'Homework 5: Integration Techniques',
            dueDate: '2024-10-26',
            submissions: 60,
            pending: 25,
        },
    ],
     'Chemistry': [
         {
            course: 'General Chemistry - CHEM-101',
            title: 'Lab Report 4: Titration',
            dueDate: '2024-10-15',
            submissions: 48,
            pending: 0,
        },
    ]
};

const allAssignments = Object.values(assignmentsByDept).flat();


export default function FacultyAssignmentsPage() {
    const [selectedDept, setSelectedDept] = useState('All Departments');

    const assignments = selectedDept === 'All Departments'
        ? allAssignments
        : assignmentsByDept[selectedDept as keyof typeof assignmentsByDept] || [];

  return (
    <DashboardLayout role="faculty">
      <div className="space-y-6">
        <div className="flex items-center justify-between">
            <h2 className="text-3xl font-bold tracking-tight">Assignments Overview</h2>
            <div className="w-[250px]">
                <Select value={selectedDept} onValueChange={setSelectedDept}>
                    <SelectTrigger>
                        <SelectValue placeholder="Filter by Department" />
                    </SelectTrigger>
                    <SelectContent>
                        {departments.map(dept => (
                            <SelectItem key={dept} value={dept}>{dept}</SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </div>
        </div>

        <Card>
            <CardHeader>
                <CardTitle>
                    {selectedDept === 'All Departments' ? 'All Assignments' : `${selectedDept} Assignments`}
                </CardTitle>
                <CardDescription>
                    Review submissions and manage assignments for your courses.
                </CardDescription>
            </CardHeader>
            <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Course & Assignment</TableHead>
                      <TableHead>Due Date</TableHead>
                      <TableHead className="text-center">Submissions</TableHead>
                      <TableHead className="text-center">Pending Review</TableHead>
                      <TableHead className="text-right">Action</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {assignments.length > 0 ? assignments.map((assignment) => (
                      <TableRow key={assignment.title}>
                        <TableCell>
                          <div className="font-medium">{assignment.title}</div>
                          <div className="text-sm text-muted-foreground">{assignment.course}</div>
                        </TableCell>
                        <TableCell>
                            <div className="flex items-center gap-2">
                                <Clock className="h-4 w-4" />
                                {new Date(assignment.dueDate).toLocaleDateString()}
                            </div>
                        </TableCell>
                        <TableCell className="text-center">
                            <div className="flex items-center justify-center gap-2">
                                <Users className="h-4 w-4" />
                                {assignment.submissions}
                            </div>
                        </TableCell>
                        <TableCell className="text-center">
                            <Badge variant={assignment.pending > 0 ? "destructive" : "secondary"}>{assignment.pending}</Badge>
                        </TableCell>
                        <TableCell className="text-right">
                          <Button variant="outline" size="sm">View Submissions</Button>
                        </TableCell>
                      </TableRow>
                    )) : (
                        <TableRow>
                            <TableCell colSpan={5} className="h-24 text-center">
                                No assignments found for this department.
                            </TableCell>
                        </TableRow>
                    )}
                  </TableBody>
                </Table>
            </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
