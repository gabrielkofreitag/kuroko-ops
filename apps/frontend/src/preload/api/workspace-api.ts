import { ipcRenderer } from 'electron';
import { IPC_CHANNELS } from '../../shared/constants';
import type { IPCResult } from '../../shared/types';

export interface WorkspaceAPI {
    getWorkspaceStatus: (projectId: string) => Promise<IPCResult<any>>;
    respondToToolApproval: (requestId: string, approved: boolean) => Promise<IPCResult<any>>;
    onToolApprovalRequest: (callback: (request: any) => void) => () => void;
    onWorkspaceStatusUpdate: (callback: (status: any) => void) => () => void;
}

export const createWorkspaceAPI = (): WorkspaceAPI => ({
    getWorkspaceStatus: (projectId: string): Promise<IPCResult<any>> =>
        ipcRenderer.invoke('workspace:status', projectId),

    respondToToolApproval: (requestId: string, approved: boolean): Promise<IPCResult<any>> =>
        ipcRenderer.invoke('tool:respond', requestId, approved),

    onToolApprovalRequest: (callback: (request: any) => void): (() => void) => {
        const handler = (_event: Electron.IpcRendererEvent, request: any) => callback(request);
        ipcRenderer.on('tool:approval-request', handler);
        return () => {
            ipcRenderer.removeListener('tool:approval-request', handler);
        };
    },

    onWorkspaceStatusUpdate: (callback: (status: any) => void): (() => void) => {
        const handler = (_event: Electron.IpcRendererEvent, status: any) => callback(status);
        ipcRenderer.on('workspace:status-update', handler);
        return () => {
            ipcRenderer.removeListener('workspace:status-update', handler);
        };
    }
});
