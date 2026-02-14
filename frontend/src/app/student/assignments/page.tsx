import { DashboardLayout } from '@/components/dashboard/layout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { FileText, Clock, CheckCircle } from 'lucide-react';

const assignments = [
  {
    title: 'Calculus II - Homework 5',
    course: 'MATH-201',
    dueDate: '2024-10-26',
    status: 'Pending',
  },
  {
    title: 'History 101 - Midterm Essay',
    course: 'HIST-101',
    dueDate: '2024-10-20',
    status: 'Submitted',
  },
  {
    title: 'Introduction to AI - Project 1',
    course: 'CS-461',
    dueDate: '2024-11-01',
    status: 'Pending',
  },
    {
    title: 'General Chemistry - Lab Report',
    course: 'CHEM-101',
    dueDate: '2024-10-15',
    status: 'Graded',
    grade: 'A-',
  },
];


export default function AssignmentsPage() {
  const pendingAssignments = assignments.filter(a => a.status === 'Pending');
  const submittedAssignments = assignments.filter(a => a.status === 'Submitted' || a.status === 'Graded');

  return (
    <DashboardLayout role="student">
      <div className="space-y-6">
        <h2 className="text-3xl font-bold tracking-tight">Assignments</h2>
        <Tabs defaultValue="all">
          <TabsList>
            <TabsTrigger value="all">All</TabsTrigger>
            <TabsTrigger value="pending">Pending</TabsTrigger>
            <TabsTrigger value="submitted">Submitted & Graded</TabsTrigger>
          </TabsList>
          <TabsContent value="all">
            <AssignmentList assignments={assignments} />
          </TabsContent>
          <TabsContent value="pending">
             <AssignmentList assignments={pendingAssignments} />
          </TabsContent>
          <TabsContent value="submitted">
             <AssignmentList assignments={submittedAssignments} />
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
}

function AssignmentList({ assignments }: { assignments: typeof assignments }) {
    if (assignments.length === 0) {
        return <p className="mt-4 text-muted-foreground">No assignments in this category.</p>;
    }
    return (
        <div className="mt-4 grid gap-4">
            {assignments.map((assignment) => (
                <Card key={assignment.title}>
                    <CardHeader className="grid grid-cols-[1fr_120px] items-start gap-4 space-y-0">
                        <div className="space-y-1">
                            <CardTitle>{assignment.title}</CardTitle>
                            <CardDescription>
                                {assignment.course} - Due: {new Date(assignment.dueDate).toLocaleDateString()}
                            </CardDescription>
                        </div>
                        <Button variant={assignment.status === 'Pending' ? 'default' : 'outline'} size="sm" className="ml-auto">
                            {assignment.status === 'Pending' ? 'Submit' : 'View Submission'}
                        </Button>
                    </CardHeader>
                    <CardContent>
                        <div className="flex space-x-4 text-sm text-muted-foreground">
                            <div className="flex items-center">
                                {assignment.status === 'Pending' && <Clock className="mr-1 h-4 w-4 text-yellow-500" />}
                                {assignment.status === 'Submitted' && <FileText className="mr-1 h-4 w-4 text-blue-500" />}
                                {assignment.status === 'Graded' && <CheckCircle className="mr-1 h-4 w-4 text-green-500" />}
                                Status: <Badge variant={
                                    assignment.status === 'Pending' ? 'destructive' : 
                                    assignment.status === 'Submitted' ? 'secondary' : 'default'
                                } className="ml-2">{assignment.status}</Badge>
                                {assignment.grade && <span className="ml-4">Grade: <strong>{assignment.grade}</strong></span>}
                            </div>
                        </div>
                    </CardContent>
                </Card>
            ))}
        </div>
    )
}
