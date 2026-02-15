import { RegisterForm } from '@/components/auth/register-form';
import Link from 'next/link';

export default function RegisterPage() {
  return (
    <main className="min-h-screen w-full bg-background">
      <div className="flex h-screen w-full items-center justify-center p-6">
        <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[450px]">
          <div className="flex flex-col space-y-2 text-center">
            <div className="flex items-center justify-center gap-2 text-lg font-medium">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="h-6 w-6 text-primary"
              >
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
              </svg>
              UniManager Pro
            </div>
            <h1 className="text-2xl font-semibold tracking-tight">
              Create an Account
            </h1>
            <p className="text-sm text-muted-foreground">
              Enter your details to register for UniManager Pro
            </p>
          </div>
          
          <RegisterForm />
          
          <p className="px-8 text-center text-sm text-muted-foreground">
            By clicking create account, you agree to our{' '}
            <Link
              href="/terms"
              className="underline underline-offset-4 hover:text-primary"
            >
              Terms of Service
            </Link>{' '}
            and{' '}
            <Link
              href="/privacy"
              className="underline underline-offset-4 hover:text-primary"
            >
              Privacy Policy
            </Link>
            .
          </p>
        </div>
      </div>
    </main>
  );
}
