"use client";

import * as React from "react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Loader2 } from "lucide-react";
import { useAuth } from "@/context/auth-context";
import Link from "next/link";

type Role = "student" | "faculty" | "admin";

export function RegisterForm({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  const { signup } = useAuth();
  const [isLoading, setIsLoading] = React.useState(false);
  const [isSuccess, setIsSuccess] = React.useState(false);
  const [formData, setFormData] = React.useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "" as Role | "",
    department: "",
  });
  const [errors, setErrors] = React.useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "",
    general: "",
  });

  const validate = () => {
    const newErrors = {
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
      role: "",
      general: "",
    };
    let isValid = true;

    if (!formData.name.trim()) {
      newErrors.name = "Name is required.";
      isValid = false;
    }

    if (!formData.email) {
      newErrors.email = "Please enter an email address.";
      isValid = false;
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Please enter a valid email address.";
      isValid = false;
    }

    if (!formData.password) {
      newErrors.password = "Please enter a password.";
      isValid = false;
    } else if (formData.password.length < 8) {
      newErrors.password = "Password must be at least 8 characters.";
      isValid = false;
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match.";
      isValid = false;
    }

    if (!formData.role) {
      newErrors.role = "You need to select a role.";
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  };

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!validate()) {
      return;
    }

    setIsLoading(true);
    setErrors({ ...errors, general: "" });

    try {
      await signup(formData.email, formData.password, {
        name: formData.name,
        role: formData.role,
        department: formData.department,
      });
      setIsSuccess(true);
    } catch (error: any) {
      setErrors({
        ...errors,
        general: error.message || "Registration failed. Please try again.",
      });
    } finally {
      setIsLoading(false);
    }
  }

  if (isSuccess) {
    return (
      <div className={cn("grid gap-6", className)} {...props}>
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="rounded-full bg-green-500/20 p-4">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="h-8 w-8 text-green-500"
            >
              <path d="M20 6L9 17l-5-5" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold">Registration Successful!</h3>
          <p className="text-muted-foreground">
            Your account has been created. You will be redirected to your dashboard.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={cn("grid gap-6", className)} {...props}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="name">Full Name</Label>
          <Input
            id="name"
            placeholder="John Doe"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            disabled={isLoading}
          />
          {errors.name && <p className="text-sm font-medium text-destructive">{errors.name}</p>}
        </div>

        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            placeholder="name@university.edu"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            disabled={isLoading}
          />
          {errors.email && <p className="text-sm font-medium text-destructive">{errors.email}</p>}
        </div>

        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            type="password"
            placeholder="********"
            value={formData.password}
            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
            disabled={isLoading}
          />
          {errors.password && <p className="text-sm font-medium text-destructive">{errors.password}</p>}
        </div>

        <div className="space-y-2">
          <Label htmlFor="confirmPassword">Confirm Password</Label>
          <Input
            id="confirmPassword"
            type="password"
            placeholder="********"
            value={formData.confirmPassword}
            onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
            disabled={isLoading}
          />
          {errors.confirmPassword && (
            <p className="text-sm font-medium text-destructive">{errors.confirmPassword}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label>Role</Label>
          <Select
            onValueChange={(value: Role) => setFormData({ ...formData, role: value })}
            value={formData.role}
            disabled={isLoading}
          >
            <SelectTrigger>
              <SelectValue placeholder="Select your role" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="student">Student</SelectItem>
              <SelectItem value="faculty">Faculty</SelectItem>
              <SelectItem value="admin">Admin</SelectItem>
            </SelectContent>
          </Select>
          {errors.role && <p className="text-sm font-medium text-destructive">{errors.role}</p>}
        </div>

        <div className="space-y-2">
          <Label htmlFor="department">Department (Optional)</Label>
          <Input
            id="department"
            placeholder="e.g., Computer Science"
            value={formData.department}
            onChange={(e) => setFormData({ ...formData, department: e.target.value })}
            disabled={isLoading}
          />
        </div>

        {errors.general && (
          <div className="rounded-lg bg-destructive/10 p-3 text-sm text-destructive">
            {errors.general}
          </div>
        )}

        <Button type="submit" className="w-full" disabled={isLoading}>
          {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          Create Account
        </Button>

        <p className="text-center text-sm text-muted-foreground">
          Already have an account?{" "}
          <Link href="/" className="text-primary underline-offset-4 hover:underline">
            Sign in
          </Link>
        </p>
      </form>
    </div>
  );
}
