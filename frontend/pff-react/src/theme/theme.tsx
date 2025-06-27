import { createTheme } from '@mui/material/styles';

export const lightTheme = createTheme({
  palette: {
    primary: { main: '#9cb8d0' },
    secondary: { main: '#de6397' },
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
  },
});

export const darkTheme = createTheme({
  palette: {
    primary: { main: '#37629d' },
    secondary: { main: '#67e5db' },
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
  },
});

