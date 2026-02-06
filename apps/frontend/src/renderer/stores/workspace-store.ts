import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface WorkspaceStatus {
    active: boolean;
    path: string | null;
    branch: string | null;
}

interface ToolApprovalRequest {
    id: string;
    taskId: string;
    tool: string;
    input: any;
}

interface WorkspaceState {
    status: WorkspaceStatus;
    pendingApprovals: ToolApprovalRequest[];

    setStatus: (status: WorkspaceStatus) => void;
    addApprovalRequest: (request: ToolApprovalRequest) => void;
    removeApprovalRequest: (requestId: string) => void;
}

// Note: electronAPI.ts and preload/api/index.ts have recently been updated 
// workspace:status and tool:respond are the correct IPC channels used in workspace-api.ts
// which is merged into electronAPI. 

export const useWorkspaceStore = create<WorkspaceState>()(
    persist(
        (set) => ({
            status: { active: false, path: null, branch: null },
            pendingApprovals: [],

            setStatus: (status: WorkspaceStatus) => set({ status }),
            addApprovalRequest: (request: ToolApprovalRequest) => set((s: WorkspaceState) => ({
                pendingApprovals: [...s.pendingApprovals, request]
            })),
            removeApprovalRequest: (requestId: string) => set((s: WorkspaceState) => ({
                pendingApprovals: s.pendingApprovals.filter((r: ToolApprovalRequest) => r.id !== requestId)
            })),
        }),
        {
            name: 'kuroko-workspace-store',
        }
    )
);

export async function refreshWorkspaceStatus(projectId: string) {
    const result = await window.electronAPI.getWorkspaceStatus(projectId);
    if (result.success && result.data) {
        useWorkspaceStore.getState().setStatus(result.data);
    }
}

export async function approveTool(requestId: string) {
    const request = useWorkspaceStore.getState().pendingApprovals.find((r: ToolApprovalRequest) => r.id === requestId);
    if (!request) return;

    const result = await window.electronAPI.respondToToolApproval(request.id, true);
    if (result.success) {
        useWorkspaceStore.getState().removeApprovalRequest(requestId);
    }
}

export async function denyTool(requestId: string) {
    const request = useWorkspaceStore.getState().pendingApprovals.find((r: ToolApprovalRequest) => r.id === requestId);
    if (!request) return;

    const result = await window.electronAPI.respondToToolApproval(request.id, false);
    if (result.success) {
        useWorkspaceStore.getState().removeApprovalRequest(requestId);
    }
}
