import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface LLMProfile {
  id: string;
  name: string;
  model: string;
  provider?: string;
  apiKey?: string;
  baseUrl?: string;
  active?: boolean;
  status?: 'verified' | 'unverified' | 'error' | 'loading';
  lastError?: string;
}

interface LLMProfileState {
  profiles: LLMProfile[];
  activeProfileId: string | null;
  setActiveProfile: (id: string) => void;
  verifyProfile: (id: string) => Promise<void>;
}

export const useLLMProfileStore = create<LLMProfileState>()(
  persist(
    (set, get) => ({
      profiles: [],
      activeProfileId: null,
      setActiveProfile: (id: string) => set({ activeProfileId: id }),
      verifyProfile: async (id: string) => {
        const profile = get().profiles.find((p: LLMProfile) => p.id === id);
        if (!profile) return;

        set((state: LLMProfileState) => ({
          profiles: state.profiles.map((p: LLMProfile) =>
            p.id === id ? { ...p, status: 'loading' as const } : p
          )
        }));

        try {
          const result = await window.electronAPI.verifyLLMProfile(profile);

          set((state: LLMProfileState) => ({
            profiles: state.profiles.map((p: LLMProfile) =>
              p.id === id ? {
                ...p,
                status: result.success ? 'verified' as const : 'error' as const,
                lastError: result.success ? undefined : result.error
              } : p
            )
          }));
        } catch (error) {
          set((state: LLMProfileState) => ({
            profiles: state.profiles.map((p: LLMProfile) =>
              p.id === id ? {
                ...p,
                status: 'error' as const,
                lastError: error instanceof Error ? error.message : String(error)
              } : p
            )
          }));
        }
      }
    }),
    {
      name: 'llm-profile-storage-v1',
    }
  )
);
