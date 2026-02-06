import React from 'react';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
    DialogDescription,
} from '../ui/dialog';
import { Button } from '../ui/button';
import { ScrollArea } from '../ui/scroll-area';
import { useWorkspaceStore, approveTool, denyTool } from '../../stores/workspace-store';
import { Check, X, Terminal, Box } from 'lucide-react';

export function ToolApprovalModal() {
    const pendingApprovals = useWorkspaceStore(s => s.pendingApprovals);
    const currentRequest = pendingApprovals[0];

    if (!currentRequest) return null;

    return (
        <Dialog open={!!currentRequest} onOpenChange={() => { }}>
            <DialogContent className="sm:max-w-[500px] border-primary/20 shadow-2xl">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2 text-xl">
                        <Box className="h-5 w-5 text-primary" />
                        Tool Approval Required
                    </DialogTitle>
                    <DialogDescription>
                        The agent is requesting permission to execute a tool.
                    </DialogDescription>
                </DialogHeader>

                <div className="space-y-4 py-4">
                    <div className="flex items-center gap-3 p-3 bg-muted rounded-lg border border-border">
                        <Terminal className="h-5 w-5 text-muted-foreground" />
                        <div>
                            <p className="text-sm font-medium leading-none">Tool Name</p>
                            <p className="text-lg font-mono text-primary mt-1">{currentRequest.tool}</p>
                        </div>
                    </div>

                    <div className="space-y-2">
                        <p className="text-sm font-medium">Input Arguments</p>
                        <ScrollArea className="h-[200px] w-full rounded-md border border-border bg-black/5 p-4">
                            <pre className="text-xs font-mono">
                                {JSON.stringify(currentRequest.input, null, 2)}
                            </pre>
                        </ScrollArea>
                    </div>
                </div>

                <DialogFooter className="gap-2 sm:gap-0">
                    <Button
                        variant="outline"
                        onClick={() => denyTool(currentRequest.id)}
                        className="flex-1 gap-2"
                    >
                        <X className="h-4 w-4" />
                        Deny
                    </Button>
                    <Button
                        onClick={() => approveTool(currentRequest.id)}
                        className="flex-1 gap-2 bg-primary hover:bg-primary/90"
                    >
                        <Check className="h-4 w-4" />
                        Approve
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
