"use client";

import React from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Zap, Search, Terminal, Code2, Globe, MessageSquare } from "lucide-react";
import { Assistant } from "@/app/assistant";

const LandingPage = () => {
    const scrollToChat = () => {
        document.getElementById("chat-section")?.scrollIntoView({ behavior: "smooth" });
    };

    return (
        <div className="min-h-screen bg-background text-foreground selection:bg-primary/30">
            {/* Navbar */}
            <nav className="fixed top-0 z-50 w-full border-b border-border/40 bg-background/60 backdrop-blur-xl">
                <div className="container mx-auto flex h-16 items-center justify-between px-6">
                    <div className="flex items-center gap-2 font-bold text-xl tracking-tight">
                        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                            <Terminal size={18} />
                        </div>
                        <span>CP<span className="text-primary">-</span>Helper</span>
                    </div>
                    <div className="flex items-center gap-4">
                        <Button variant="ghost" size="sm" onClick={scrollToChat} className="hidden sm:flex text-muted-foreground hover:text-primary">
                            Chat Now
                        </Button>
                        <Button size="sm" onClick={scrollToChat} className="rounded-full px-6">
                            Get Started
                        </Button>
                    </div>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="relative overflow-hidden pt-32 pb-20 lg:pt-48 lg:pb-32 text-center">
                <div className="absolute top-0 left-1/2 -z-10 h-[1000px] w-[1000px] -translate-x-1/2 -translate-y-1/2 [background:radial-gradient(circle_at_center,var(--primary-foreground)_0%,transparent_70%)] opacity-20" />

                <div className="container mx-auto px-6">
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.5 }}
                        className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/10 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-primary mb-8"
                    >
                        <Zap size={14} /> Free Forever for Everyone
                    </motion.div>

                    <motion.h1
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.1 }}
                        className="text-5xl font-extrabold tracking-tight sm:text-7xl lg:text-8xl"
                    >
                        Your AI <span className="bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">Coding Mentor</span>
                    </motion.h1>

                    <motion.p
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.2 }}
                        className="mx-auto mt-8 max-w-2xl text-lg text-muted-foreground sm:text-xl"
                    >
                        Bridge the gap between your coding challenges and the best techniques.
                        CP-Helper is <span className="text-foreground font-semibold">completely free to use</span>,
                        built to help competitive programmers excel.
                    </motion.p>

                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.5, delay: 0.3 }}
                        className="mt-10"
                    >
                        <Button size="lg" onClick={scrollToChat} className="h-16 rounded-full px-12 text-lg font-bold shadow-lg shadow-primary/20 scale-105 hover:scale-110 transition-transform">
                            Start Chatting Now
                        </Button>
                    </motion.div>
                </div>
            </section>

            {/* Chat Section */}
            <section id="chat-section" className="relative py-20 bg-muted/20 border-t border-border/40">
                <div className="container mx-auto px-6">
                    <div className="mb-12 flex flex-col items-center text-center">
                        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10 text-primary">
                            <MessageSquare size={32} />
                        </div>
                        <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">Chat with CP-Helper</h2>
                        <p className="mt-4 text-muted-foreground max-w-md">
                            Ask about algorithms, debug code, or find the best approach for your problem.
                        </p>
                    </div>

                    <div className="mx-auto max-w-5xl overflow-hidden rounded-3xl border border-border/40 bg-card shadow-2xl h-[700px]">
                        <Assistant hideSidebar={true} />
                    </div>
                </div>
            </section>

            {/* Features Grid - Minimal */}
            <section className="py-24 bg-background">
                <div className="container mx-auto px-6">
                    <div className="grid gap-12 md:grid-cols-2 lg:grid-cols-3">
                        {[
                            {
                                icon: <Search className="text-primary" />,
                                title: "Context-Aware",
                                desc: "Uses RAG to pull in the latest CP techniques."
                            },
                            {
                                icon: <Zap className="text-primary" />,
                                title: "Instant Streaming",
                                desc: "Fast, real-time responses to keep your flow."
                            },
                            {
                                icon: <Code2 className="text-primary" />,
                                title: "Free Tools",
                                desc: "100% free access to all core features."
                            }
                        ].map((feature, i) => (
                            <div key={i} className="flex flex-col items-center text-center p-6">
                                <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">
                                    {feature.icon}
                                </div>
                                <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                                <p className="text-muted-foreground leading-relaxed">{feature.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="border-t border-border/40 py-12">
                <div className="container mx-auto px-6 flex flex-col items-center justify-center gap-6">
                    <div className="flex items-center gap-2 font-bold text-lg tracking-tight">
                        <div className="flex h-6 w-6 items-center justify-center rounded-md bg-primary text-primary-foreground">
                            <Terminal size={14} />
                        </div>
                        <span>CP-Helper</span>
                    </div>
                    <p className="text-sm text-muted-foreground">
                        © 2024 CP-Helper. Built for the coding community.
                    </p>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
