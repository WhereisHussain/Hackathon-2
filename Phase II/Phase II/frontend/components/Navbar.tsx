"use client"

import Link from "next/link"
import { useRouter } from "next/navigation"
import { authClient } from "@/lib/auth-client"
import { Button } from "@/components/ui/button"

export function Navbar() {
    const router = useRouter()
    const { data: session } = authClient.useSession()

    const handleSignOut = async () => {
        await authClient.signOut()
        router.push("/auth")
    }

    return (
        <nav className="border-b bg-background">
            <div className="flex h-16 items-center px-4 md:px-6">
                <Link href="/" className="font-bold text-lg">
                    Todo App
                </Link>
                <div className="ml-auto flex items-center gap-4">
                    {session ? (
                        <>
                            <span className="text-sm text-muted-foreground">
                                {session.user.name}
                            </span>
                            <Button variant="outline" size="sm" onClick={handleSignOut}>
                                Sign Out
                            </Button>
                        </>
                    ) : (
                        <Link href="/auth">
                            <Button size="sm">Sign In</Button>
                        </Link>
                    )}
                </div>
            </div>
        </nav>
    )
}
