# Frontend Setup Guide

## Quick Start

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

The frontend will start on http://localhost:3000

## Backend Connection

The frontend is configured to connect to the backend on port 8004.
Make sure your backend is running on http://localhost:8004

## Features Working

✅ **Image Upload** - Drag & drop functionality with preview
✅ **Prompt Input** - Text input with character counting
✅ **Model Selection** - Dropdown with available AI models
✅ **Generation Settings** - Aspect ratio, outputs, advanced controls
✅ **Results Display** - Image gallery with download options
✅ **Error Handling** - User-friendly error messages

## Troubleshooting

### Frontend Won't Start
- Make sure Node.js is installed
- Run `npm install` in the frontend directory
- Check if port 3000 is available

### Images Not Showing
- Ensure backend is running on port 8004
- Check browser console for API errors
- Verify the proxy configuration in vite.config.ts

### Generation Not Working
- Check if backend is responding at http://localhost:8004/api/models
- Verify upload functionality first
- Check network tab in browser dev tools

## File Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── ImageUpload.tsx  # File upload component
│   │   ├── PromptInput.tsx  # Prompt input component
│   │   ├── ModelSelection.tsx # Model dropdown
│   │   ├── GenerationSettings.tsx # Settings panel
│   │   └── ResultsGallery.tsx # Results display
│   ├── types/
│   │   └── index.ts         # TypeScript types
│   ├── utils/
│   │   └── api.ts           # API service
│   ├── App.tsx              # Main app component
│   ├── main.tsx             # Entry point
│   └── index.css            # Styles
├── package.json             # Dependencies
├── vite.config.ts           # Vite configuration
└── tailwind.config.js       # Tailwind CSS config
```

## API Endpoints Used

- `GET /api/models` - Get available AI models
- `POST /api/upload` - Upload reference images
- `POST /api/generate` - Start image generation
- `GET /api/jobs/{job_id}` - Get generation status
- `GET /api/download/{image_id}` - Download generated image

## Next Steps

1. Start the backend server on port 8004
2. Start the frontend with `npm run dev`
3. Open http://localhost:3000 in your browser
4. Upload an image and enter a prompt
5. Click "Generate Images" to test the AI functionality

The frontend is now ready and should work perfectly with the backend!