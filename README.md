# imgtoimg.ai Clone

A professional AI-powered image-to-image transformation platform built with React and FastAPI. Create stunning image variations using Stable Diffusion models with an intuitive, modern interface.

## ✨ Features

- **🎨 Image-to-Image Generation**: Transform images using advanced AI models
- **🤖 Multiple AI Models**: Stable Diffusion 1.5, 2.1, and more
- **⚡ Real-time Progress**: Live generation progress with detailed status
- **🎛️ Advanced Controls**: Fine-tune strength, guidance, steps, and sampling methods
- **📱 Responsive Design**: Beautiful interface that works on all devices
- **🌙 Dark/Light Theme**: Toggle between themes with keyboard shortcuts
- **📊 Batch Processing**: Generate multiple variations at once
- **💾 Easy Downloads**: Download individual images or entire batches
- **❤️ Favorites System**: Mark and organize your best generations

## 🚀 Quick Start

### Option 1: Automated Installation (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd imgtoimg-ai-clone

# Run the automated installer
python install_imgtoimg.py

# Start the application
python start_imgtoimg.py
```

### Option 2: Manual Installation

1. **Prerequisites**
   - Python 3.8+ with pip
   - Node.js 16+ with npm
   - CUDA-compatible GPU (recommended) or CPU

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Start Servers**
   ```bash
   # Terminal 1 - Backend
   cd backend && python main.py
   
   # Terminal 2 - Frontend  
   cd frontend && npm run dev
   ```

5. **Open Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8004
   - API Docs: http://localhost:8004/docs

## 🎯 How to Use

1. **Upload Image**: Drag and drop or click to upload your reference image
2. **Enter Prompt**: Describe what you want to see in the transformed image
3. **Choose Model**: Select from available Stable Diffusion models
4. **Adjust Settings**: Fine-tune strength, guidance scale, and steps
5. **Generate**: Click generate and watch the real-time progress
6. **Download**: Save your favorite results

## ⚙️ Advanced Features

### Generation Controls
- **Strength**: How much the AI modifies the original image (0.1-1.0)
- **Guidance Scale**: How closely the AI follows your prompt (1.0-20.0)
- **Steps**: Number of denoising steps for quality vs speed (20-150)
- **Sampling Methods**: Various algorithms for different styles
- **Batch Generation**: Create multiple variations simultaneously

### Keyboard Shortcuts
- `Ctrl+Enter`: Start generation
- `Ctrl+D`: Toggle dark/light theme

## 🏗️ Architecture

### Frontend (React + TypeScript)
```
frontend/
├── src/
│   ├── components/          # UI components
│   │   ├── Header.tsx       # App header with theme toggle
│   │   ├── ImageUpload.tsx  # Drag-and-drop upload
│   │   ├── GenerationControls.tsx  # Settings panel
│   │   ├── ProgressMonitor.tsx     # Real-time progress
│   │   └── ResultsGallery.tsx      # Results display
│   ├── services/           # API integration
│   ├── types.ts           # TypeScript definitions
│   └── App.tsx           # Main application
```

### Backend (FastAPI + Python)
```
backend/
├── app/
│   ├── api/                # API endpoints
│   │   └── imgtoimg.py    # Main img2img routes
│   ├── services/          # Business logic
│   │   └── imgtoimg_service.py  # AI generation service
│   └── models/           # Data models
└── main.py              # FastAPI application
```

## 🤖 AI Models

### Supported Models
- **Stable Diffusion 1.5**: General purpose, fast and reliable
- **Stable Diffusion 2.1**: Enhanced quality and detail
- **Custom Models**: Easy to add new models

### Model Management
- Automatic model downloading on first use
- Intelligent memory management
- GPU optimization with attention slicing
- CPU fallback support

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Set custom model cache directory
TRANSFORMERS_CACHE=/path/to/model/cache

# Optional: Set device preference
CUDA_VISIBLE_DEVICES=0
```

### Advanced Settings
- Modify `backend/app/services/imgtoimg_service.py` for model configurations
- Adjust memory optimization settings for your hardware
- Configure custom sampling schedulers

## 📊 System Requirements

### Minimum Requirements
- **CPU**: 4+ cores
- **RAM**: 8GB+ 
- **Storage**: 10GB+ free space
- **GPU**: Optional but recommended

### Recommended Requirements
- **CPU**: 8+ cores
- **RAM**: 16GB+
- **Storage**: 50GB+ SSD
- **GPU**: NVIDIA RTX 3060+ with 8GB+ VRAM

## 🐛 Troubleshooting

### Common Issues

**"CUDA out of memory"**
- Reduce batch size or image dimensions
- Enable memory optimization in settings
- Use CPU mode as fallback

**"Model not found"**
- Check internet connection for model downloads
- Verify sufficient disk space
- Clear model cache and retry

**"Generation failed"**
- Check image format (JPEG, PNG, WebP supported)
- Ensure prompt is not empty
- Try different model or settings

### Performance Tips
- Use GPU for 10x faster generation
- Enable xformers for memory efficiency
- Reduce steps for faster generation
- Use smaller image dimensions for speed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Stability AI](https://stability.ai/) for Stable Diffusion models
- [Hugging Face](https://huggingface.co/) for the Diffusers library
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [React](https://reactjs.org/) for the frontend framework

## 📞 Support

- 📖 [Documentation](http://localhost:8004/docs)
- 🐛 [Issue Tracker](https://github.com/your-repo/issues)
- 💬 [Discussions](https://github.com/your-repo/discussions)

---

**⭐ Star this repository if you find it useful!**