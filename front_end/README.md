# Frontend - Hackathon Presentation Generator

React + TypeScript + Vite frontend for the Hackathon Presentation Generator.

## Tech Stack

- **React 19**: Modern UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool and dev server
- **CSS3**: Modern styling with gradients and animations

## Installation

```bash
npm install
```

## Development

Start the development server:

```bash
npm run dev
```

The app will be available at http://localhost:5173

## Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── App.tsx          # Main application component
├── App.css          # Application styles
├── index.css        # Global styles
├── main.tsx         # Entry point
└── assets/          # Static assets
```

## Features

- **Input Form**: URL validation for GitHub and Devpost
- **Loading States**: Multi-stage progress indicators
- **Success View**: Display Canva link and presentation preview
- **Error Handling**: User-friendly error messages
- **Responsive Design**: Works on all screen sizes

## Styling

The app uses:
- CSS custom properties for theming
- Gradient backgrounds
- Glassmorphism effects
- Smooth animations and transitions
- Mobile-first responsive design

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8000`.

CORS is configured to allow requests from `http://localhost:5173`.

## Environment Variables

No environment variables required for development. The backend URL is hardcoded for simplicity.

For production, you may want to use environment variables:

```env
VITE_API_URL=https://your-backend-url.com
```

Then in code:
```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

## Linting

```bash
npm run lint
```

## Code Quality

The project uses:
- ESLint for code linting
- TypeScript for type checking
- React best practices

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## License

MIT
