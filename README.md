# DigiTwin Analytics - Modular Version

This is the modularized version of the DigiTwin Analytics application, designed to improve performance and maintainability by separating concerns into logical modules.

## 🏗️ Modular Structure

### Core Modules

1. **`config.py`** - Configuration and constants
   - System prompts
   - Keywords and mappings
   - Model configurations
   - UI styles and constants

2. **`utils.py`** - Utility functions and data processing
   - Logging decorators
   - PDF parsing
   - Data processing functions
   - File upload handling

3. **`visualization.py`** - Visualization and plotting
   - Plant layout drawing functions
   - Matplotlib utilities
   - Chart generation

4. **`llm_models.py`** - AI model interactions
   - Model response generation
   - Provider-specific handlers (OpenAI, Cerebras, HuggingFace)
   - Stream processing

5. **`ui_components.py`** - Streamlit UI components
   - UI setup and styling
   - Tab rendering
   - Sidebar components
   - Chat interface

6. **`app_modular.py`** - Main application orchestrator
   - Coordinates all modules
   - Main application flow
   - Entry point

## 🚀 Performance Improvements

### What's Optimized

1. **Lazy Loading**: Models are only loaded when needed
2. **Caching**: FAISS vectorstore is cached with `@st.cache_resource`
3. **Modular Imports**: Only import what's needed when it's needed
4. **Separated Concerns**: Each module has a single responsibility
5. **Reduced Memory Footprint**: Better memory management through modularization

### Key Optimizations

- **Model Loading**: HuggingFace models are loaded only when the specific agent is selected
- **Vectorstore**: Built only when PDF files are uploaded
- **UI Components**: Separated to reduce re-rendering overhead
- **Data Processing**: Optimized file processing with better error handling

## 📦 Installation

1. Install dependencies:
```bash
pip install -r requirements_modular.txt
```

2. Set up environment variables in `.env`:
```
API_KEY=your_xai_api_key
DEEPSEEK_API_KEY=your_deepseek_api_key
CEREBRAS_API_KEY=your_cerebras_api_key
HF_TOKEN=your_huggingface_token
```

## 🎯 Usage

Run the modular application:
```bash
streamlit run app_modular.py
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all modules are in the same directory
2. **Model Loading**: Check that your API keys are correctly set
3. **Memory Issues**: The modular version should use less memory than the original

### Performance Tips

1. **Use Specific Agents**: Only load the models you need
2. **Limit File Uploads**: Process files in smaller batches
3. **Clear Cache**: Use `st.cache_data.clear()` if needed

## 📊 Comparison with Original

| Aspect | Original | Modular |
|--------|----------|---------|
| File Size | ~535 lines | ~6 files, ~50-200 lines each |
| Memory Usage | Higher | Lower |
| Load Time | Slower | Faster |
| Maintainability | Lower | Higher |
| Debugging | Harder | Easier |

## 🛠️ Development

### Adding New Features

1. **New Models**: Add to `config.py` MODEL_CONFIGS and `llm_models.py`
2. **New Visualizations**: Add to `visualization.py`
3. **New UI Components**: Add to `ui_components.py`
4. **New Data Processing**: Add to `utils.py`

### Testing

Each module can be tested independently:
```python
# Test utils
python -c "from utils import parse_pdf; print('Utils OK')"

# Test config
python -c "from config import PROMPTS; print('Config OK')"
```

## 📈 Benefits

- **Faster Startup**: Only loads what's needed
- **Better Memory Management**: Reduced memory footprint
- **Easier Debugging**: Isolated modules
- **Better Maintainability**: Clear separation of concerns
- **Scalability**: Easy to add new features
- **Reusability**: Modules can be used independently 
