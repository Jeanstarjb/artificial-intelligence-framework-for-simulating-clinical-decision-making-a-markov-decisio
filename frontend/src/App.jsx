import { Container, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import { teal, deepOrange } from '@mui/material/colors';

const theme = createTheme({
  palette: {
    primary: teal,
    secondary: deepOrange,
    mode: 'light'
  },
  transitions: {
    easing: {
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)'
    }
  }
});

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="xl" sx={{
        minHeight: '100vh',
        background: 'linear-gradient(45deg, #f3f9ff 30%, #f8fbfe 90%)'
      }}>
        <h1 style={{
          color: theme.palette.primary.dark,
          fontWeight: 600,
          textAlign: 'center',
          padding: '2rem',
          animation: 'fadeIn 0.8s ease-in'
        }}>
          Clinical Decision Support Platform
        </h1>
      </Container>
    </ThemeProvider>
  );
}