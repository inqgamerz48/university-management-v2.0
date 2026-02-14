'use client';

import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { PlaceHolderImages } from '@/lib/placeholder-images';
import { useAuth } from '@/context/auth-context';

type UserNavProps = {
  role: 'student' | 'faculty' | 'admin' | 'super-admin';
};

const avatarIds: Record<string, string> = {
    student: 'avatar-1',
    faculty: 'avatar-2',
    admin: 'avatar-3',
    'super-admin': 'avatar-3',
}

export function UserNav({ role }: UserNavProps) {
  const { user, logout } = useAuth();
  
  if (!user) {
    return null;
  }

  const avatarImage = PlaceHolderImages.find((img) => img.id === avatarIds[user.role]);
  const fallback = user.name.split(' ').map(n => n[0]).join('');

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="relative h-9 w-9 rounded-full">
          <Avatar className="h-9 w-9">
            {avatarImage && (
              <AvatarImage 
                src={avatarImage.imageUrl} 
                alt={user.name}
                data-ai-hint={avatarImage.imageHint} 
              />
            )}
            <AvatarFallback>{fallback}</AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56" align="end" forceMount>
        <DropdownMenuLabel className="font-normal">
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium leading-none">{user.name}</p>
            <p className="text-xs leading-none text-muted-foreground">
              {user.email}
            </p>
          </div>
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuGroup>
          <DropdownMenuItem>Profile</DropdownMenuItem>
          <DropdownMenuItem>Settings</DropdownMenuItem>
        </DropdownMenuGroup>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={() => logout()}>
          Log out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
