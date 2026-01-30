import { Assistant } from "../assistant";
import Link from "next/link";
import { Home } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function ChatPage() {
    return (
        <div className="relative h-screen w-full">
            <div className="absolute top-4 left-4 z-50">
                <Link href="/">
                    <Button variant="outline" size="icon" className="rounded-full bg-background/50 backdrop-blur-md shadow-md border-border/40 hover:bg-primary/10 hover:border-primary/50 transition-all">
                        <Home size={18} />
                    </Button>
                </Link>
            </div>
            <Assistant />
        </div>
    );
}
