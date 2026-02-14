import { DashboardLayout } from '@/components/dashboard/layout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { MoreHorizontal } from 'lucide-react';

const allTickets = [
    { id: 'TKT-001', student: 'Alicia Keys', subject: 'Cannot access course materials', category: 'Technical', status: 'Open', lastUpdate: '2 hours ago' },
    { id: 'TKT-002', student: 'John Smith', subject: 'Question about assignment grading', category: 'Academic', status: 'In Progress', lastUpdate: '1 day ago' },
    { id: 'TKT-003', student: 'Jane Doe', subject: 'Fee payment issue', category: 'Billing', status: 'Closed', lastUpdate: '3 days ago' },
    { id: 'TKT-004', student: 'Mike Ross', subject: 'Library book renewal', category: 'Other', status: 'Open', lastUpdate: '4 hours ago' },
];

export default function AdminSupportPage() {
  return (
    <DashboardLayout role="admin">
      <div className="space-y-6">
        <h2 className="text-3xl font-bold tracking-tight">Support Tickets</h2>
        <Card>
            <CardHeader>
                <CardTitle>All Tickets</CardTitle>
                <CardDescription>View and manage all support tickets from students.</CardDescription>
            </CardHeader>
            <CardContent>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Ticket ID</TableHead>
                            <TableHead>Student</TableHead>
                            <TableHead>Subject</TableHead>
                            <TableHead>Status</TableHead>
                            <TableHead>Last Update</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {allTickets.map(ticket => (
                            <TableRow key={ticket.id}>
                                <TableCell className="font-medium">{ticket.id}</TableCell>
                                <TableCell>{ticket.student}</TableCell>
                                <TableCell>{ticket.subject}</TableCell>
                                <TableCell>
                                    <Badge variant={
                                        ticket.status === 'Open' ? 'destructive' :
                                        ticket.status === 'In Progress' ? 'default' : 'secondary'
                                    }>
                                        {ticket.status}
                                    </Badge>
                                </TableCell>
                                <TableCell>{ticket.lastUpdate}</TableCell>
                                <TableCell className="text-right">
                                    <DropdownMenu>
                                        <DropdownMenuTrigger asChild>
                                        <Button variant="ghost" className="h-8 w-8 p-0">
                                            <span className="sr-only">Open menu</span>
                                            <MoreHorizontal className="h-4 w-4" />
                                        </Button>
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent align="end">
                                            <DropdownMenuItem>View Ticket</DropdownMenuItem>
                                            <DropdownMenuItem>Mark as In Progress</DropdownMenuItem>
                                            <DropdownMenuItem>Mark as Closed</DropdownMenuItem>
                                        </DropdownMenuContent>
                                    </DropdownMenu>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}
