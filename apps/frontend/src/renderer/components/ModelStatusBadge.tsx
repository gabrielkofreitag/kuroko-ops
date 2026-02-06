import { CheckCircle2, XCircle, HelpCircle, Loader2 } from 'lucide-react';
import { cn } from '../lib/utils';
import { Badge } from './ui/badge';
import {
    Tooltip,
    TooltipContent,
    TooltipTrigger,
} from './ui/tooltip';
import type { LLMProfile } from '../stores/llm-profile-store';

interface ModelStatusBadgeProps {
    profile: LLMProfile;
    className?: string;
    showLabel?: boolean;
}

export function ModelStatusBadge({ profile, className, showLabel = false }: ModelStatusBadgeProps) {
    const status = profile.status || 'unverified';

    const statusConfig = {
        verified: {
            icon: CheckCircle2,
            color: 'text-green-500',
            bg: 'bg-green-500/5 dark:bg-green-500/10',
            label: 'Verified',
            animation: 'animate-in zoom-in-50 duration-300'
        },
        unverified: {
            icon: HelpCircle,
            color: 'text-muted-foreground',
            bg: 'bg-muted/50 dark:bg-muted',
            label: 'Unverified',
            animation: ''
        },
        error: {
            icon: XCircle,
            color: 'text-destructive',
            bg: 'bg-destructive/5 dark:bg-destructive/10',
            label: 'Error',
            animation: 'animate-in fade-in slide-in-from-top-1 duration-200'
        },
        loading: {
            icon: Loader2,
            color: 'text-blue-500',
            bg: 'bg-blue-500/5 dark:bg-blue-500/10',
            label: 'Verifying...',
            animation: 'animate-spin'
        }
    };

    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.unverified;
    const Icon = config.icon;

    return (
        <Tooltip>
            <TooltipTrigger asChild>
                <div className={cn(
                    "group relative flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-medium transition-all duration-300 cursor-help border border-transparent hover:border-current/20",
                    config.bg,
                    config.color,
                    className
                )}>
                    <Icon className={cn("h-3 w-3", config.animation)} />
                    {showLabel && (
                        <span className="animate-in fade-in duration-500">
                            {config.label}
                        </span>
                    )}
                    {status === 'verified' && (
                        <div className="absolute inset-0 rounded-full bg-green-500/20 animate-ping [animation-iteration-count:1] [animation-duration:1s]" />
                    )}
                </div>
            </TooltipTrigger>
            <TooltipContent side="bottom" align="center" className="p-3 shadow-xl border-primary/10">
                <div className="text-xs space-y-1.5 min-w-[140px]">
                    <div className="flex items-center justify-between gap-4">
                        <p className="font-semibold text-[13px]">{profile.name}</p>
                        <Badge variant="outline" className="text-[9px] px-1.5 py-0 h-4 uppercase tracking-wider opacity-60">
                            {profile.provider || 'Provider'}
                        </Badge>
                    </div>
                    <p className="text-muted-foreground font-medium">{profile.model}</p>
                    {profile.lastError ? (
                        <div className="mt-2 p-2 rounded bg-destructive/5 border border-destructive/10">
                            <p className="text-destructive font-mono text-[9px] leading-relaxed break-words">
                                {profile.lastError}
                            </p>
                        </div>
                    ) : status === 'verified' && (
                        <p className="text-green-600 dark:text-green-400 text-[10px] flex items-center gap-1 mt-1">
                            <CheckCircle2 className="h-2.5 w-2.5" />
                            Connection secure
                        </p>
                    )}
                </div>
            </TooltipContent>
        </Tooltip>
    );
}
