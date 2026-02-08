import ChatInterface from "@/components/ChatInterface";

export default function Home() {
    const demoUserId = "ziakhan";

    return (
        <main className="min-h-screen bg-black">
            <ChatInterface userId={demoUserId} />
        </main>
    );
}
