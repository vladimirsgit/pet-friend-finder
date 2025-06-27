import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import {lightTheme, darkTheme} from "./theme/theme.tsx";

const isDark = true;

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider theme={isDark ? darkTheme : lightTheme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </StrictMode>
);
