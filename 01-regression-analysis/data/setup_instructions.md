# Setup Instructions for Your Professor

## Quick Start (Recommended)

1. **Open Terminal** in the project folder

2. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Start Jupyter**:
   ```bash
   jupyter notebook
   ```

4. **Open `regression_analysis.ipynb`** and run all cells

---

## Alternative: Fresh Installation

If the above doesn't work, do a fresh install:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook
```

Then open `regression_analysis.ipynb`

---

## Presentation Mode

When presenting, you can:

1. **Run all cells** before presenting: `Kernel` → `Restart & Run All`
2. **Clear outputs** if you want to show live execution: `Cell` → `All Output` → `Clear`
3. **Use presentation mode**: View → Cell Toolbar → Slideshow (optional)

---

## Troubleshooting

**Problem**: "No module named pandas"
**Solution**: Make sure virtual environment is activated (`source venv/bin/activate`)

**Problem**: Jupyter not found
**Solution**: `pip install jupyter notebook`

**Problem**: Kernel not starting
**Solution**: `python -m ipykernel install --user --name=venv`
