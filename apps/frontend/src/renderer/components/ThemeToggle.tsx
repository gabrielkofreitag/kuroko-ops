import { Sun, Moon, Monitor, Palette, Check } from 'lucide-react';
import { useSettingsStore, saveSettings } from '../stores/settings-store';
import { COLOR_THEMES } from '../../shared/constants';
import { Button } from './ui/button';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from './ui/dropdown-menu';
import { cn } from '../lib/utils';
import { useTranslation } from 'react-i18next';

export function ThemeToggle() {
    const { t } = useTranslation('settings');
    const settings = useSettingsStore((state) => state.settings);
    const { theme = 'system' } = settings;
    const colorTheme = settings.colorTheme || 'default';

    const handleThemeChange = (newTheme: 'light' | 'dark' | 'system') => {
        saveSettings({ theme: newTheme });
    };

    const handlePaletteChange = (paletteId: string) => {
        saveSettings({ colorTheme: paletteId as any });
    };

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="h-9 w-9 rounded-full">
                    {theme === 'light' ? (
                        <Sun className="h-4 w-4" />
                    ) : theme === 'dark' ? (
                        <Moon className="h-4 w-4" />
                    ) : (
                        <Monitor className="h-4 w-4" />
                    )}
                    <span className="sr-only">{t('theme.title')}</span>
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
                <DropdownMenuLabel>{t('sections.appearance.title')}</DropdownMenuLabel>
                <DropdownMenuItem onClick={() => handleThemeChange('light')}>
                    <Sun className="mr-2 h-4 w-4" />
                    <span>{t('theme.light')}</span>
                    {theme === 'light' && <Check className="ml-auto h-4 w-4" />}
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => handleThemeChange('dark')}>
                    <Moon className="mr-2 h-4 w-4" />
                    <span>{t('theme.dark')}</span>
                    {theme === 'dark' && <Check className="ml-auto h-4 w-4" />}
                </DropdownMenuItem>
                <DropdownMenuItem onClick={() => handleThemeChange('system')}>
                    <Monitor className="mr-2 h-4 w-4" />
                    <span>{t('theme.system')}</span>
                    {theme === 'system' && <Check className="ml-auto h-4 w-4" />}
                </DropdownMenuItem>

                <DropdownMenuSeparator />
                <DropdownMenuLabel className="flex items-center gap-2">
                    <Palette className="h-4 w-4" />
                    {t('theme.colorTheme')}
                </DropdownMenuLabel>
                <div className="grid grid-cols-2 gap-1 p-1">
                    {COLOR_THEMES.map((palette) => (
                        <button
                            key={palette.id}
                            onClick={() => handlePaletteChange(palette.id)}
                            className={cn(
                                "flex items-center gap-2 rounded-md px-2 py-1.5 text-xs transition-colors hover:bg-accent",
                                colorTheme === palette.id && "bg-accent font-medium text-accent-foreground"
                            )}
                        >
                            <div
                                className="h-3 w-3 rounded-full border border-border"
                                style={{ backgroundColor: palette.previewColors.accent }}
                            />
                            <span className="truncate">{palette.name}</span>
                        </button>
                    ))}
                </div>
            </DropdownMenuContent>
        </DropdownMenu>
    );
}
