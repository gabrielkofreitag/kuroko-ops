import React, { useState } from 'react';
import {
    Box,
    Button,
    TextField,
    Typography,
    Paper,
    Alert,
    CircularProgress
} from '@mui/material';
import { Key as KeyIcon, CheckCircle as CheckIcon } from '@mui/icons-material';

interface ApiKeySetupProps {
    onValidated: (apiKey: string) => void;
}

export const ApiKeySetup: React.FC<ApiKeySetupProps> = ({ onValidated }) => {
    const [apiKey, setApiKey] = useState('');
    const [isValidating, setIsValidating] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState(false);

    const handleValidate = async () => {
        if (!apiKey.trim()) {
            setError('Por favor, insira uma API Key.');
            return;
        }

        setIsValidating(true);
        setError(null);

        try {
            // Aqui chamaríamos o backend para validar
            // Por enquanto, apenas um mock do fluxo
            const response = await window.api.invoke('auth:validate-key', apiKey);

            if (response.valid) {
                setSuccess(true);
                setTimeout(() => {
                    onValidated(apiKey);
                }, 1500);
            } else {
                setError('API Key inválida ou erro na conexão com OpenRouter.');
            }
        } catch (err: any) {
            setError(`Erro na validação: ${err.message || 'Erro desconhecido'}`);
        } finally {
            setIsValidating(false);
        }
    };

    return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
            <Paper elevation={3} sx={{ p: 4, maxWidth: 400, width: '100%', textAlign: 'center' }}>
                <KeyIcon sx={{ fontSize: 48, mb: 2, color: 'primary.main' }} />
                <Typography variant="h5" gutterBottom>Configuração Kuroko-Ops</Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                    Insira sua OpenRouter API Key para começar.
                </Typography>

                <TextField
                    fullWidth
                    label="OpenRouter API Key"
                    variant="outlined"
                    type="password"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    sx={{ mb: 2 }}
                    placeholder="sk-or-v1-..."
                    disabled={isValidating || success}
                />

                {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                {success && <Alert severity="success" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
                    <CheckIcon sx={{ mr: 1 }} /> API Key validada com sucesso!
                </Alert>}

                <Button
                    fullWidth
                    variant="contained"
                    size="large"
                    onClick={handleValidate}
                    disabled={isValidating || success}
                    startIcon={isValidating ? <CircularProgress size={20} /> : null}
                >
                    {isValidating ? 'Validando...' : 'Validar e Continuar'}
                </Button>

                <Typography variant="caption" sx={{ mt: 2, display: 'block' }} color="text.secondary">
                    Sua chave é salva localmente e nunca é enviada para nossos servidores.
                </Typography>
            </Paper>
        </Box>
    );
};
