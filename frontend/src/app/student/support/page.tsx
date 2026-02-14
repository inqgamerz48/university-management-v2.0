'use client';
import React from 'react';
import { DashboardLayout } from '@/components/dashboard/layout';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { LifeBuoy, Clock } from 'lucide-react';
import { Label } from '@/components/ui/label';

const myTickets = [
    { id: 'TKT-001', subject: 'Cannot access course materials', category: 'Technical', status: 'Open', lastUpdate: '2 hours ago' },
    { id: 'TKT-002', subject: 'Question about assignment grading', category: 'Academic', status: 'In Progress', lastUpdate: '1 day ago' },
    { id: 'TKT-003', subject: 'Fee payment issue', category: 'Billing', status: 'Closed', lastUpdate: '3 days ago' },
]

export default function SupportPage() {
  return (
    <DashboardLayout role="student">
      <div className="space-y-6">
          <h2 className="text-3xl font-bold tracking-tight">Support Center</h2>
          <div className="grid gap-6 md:grid-cols-1 lg:grid-cols-5">
            <div className="space-y-6 lg:col-span-3">
                <Card>
                    <CardHeader>
                        <CardTitle>My Support Tickets</CardTitle>
                        <CardDescription>Track the status of your support requests.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        {myTickets.map(ticket => (
                            <div key={ticket.id} className="flex items-center justify-between rounded-lg border p-4">
                                <div>
                                    <h3 className="font-semibold">{ticket.subject}</h3>
                                    <p className="text-sm text-muted-foreground">
                                        <span className="font-medium">{ticket.id}</span> - Category: {ticket.category}
                                    </p>
                                    <div className="mt-1 flex items-center text-xs text-muted-foreground">
                                        <Clock className="mr-1.5 h-3 w-3" />
                                        Updated {ticket.lastUpdate}
                                    </div>
                                </div>
                                <Badge variant={
                                    ticket.status === 'Open' ? 'destructive' :
                                    ticket.status === 'In Progress' ? 'default' : 'secondary'
                                }>
                                    {ticket.status}
                                </Badge>
                            </div>
                        ))}
                    </CardContent>
                </Card>
            </div>

            <div className="lg:col-span-2">
                <Card>
                    <CardHeader>
                        <div className="flex items-center gap-3">
                            <LifeBuoy className="h-6 w-6 text-primary" />
                            <CardTitle>Create New Ticket</CardTitle>
                        </div>
                        <CardDescription>Have an issue? Let us know.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <Label htmlFor="category">Category</Label>
                            <Select>
                                <SelectTrigger id="category">
                                    <SelectValue placeholder="Select a category" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="technical">Technical</SelectItem>
                                    <SelectItem value="academic">Academic</SelectItem>
                                    <SelectItem value="billing">Billing</SelectItem>
                                    <SelectItem value="other">Other</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="subject">Subject</Label>
                            <Input id="subject" placeholder="e.g., Unable to upload assignment" />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="description">Description</Label>
                            <Textarea id="description" placeholder="Please describe your issue in detail..." rows={5} />
                        </div>
                    </CardContent>
                    <CardFooter>
                        <Button className="w-full">Submit Ticket</Button>
                    </CardFooter>
                </Card>
            </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
