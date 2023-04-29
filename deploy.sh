```bash
#!/bin/bash
set -e

if [ -d "dist" ]; then
    rm -r dist
else
    echo "dist directory not found, skipping removal"
fi

if [ -d "build" ]; then
    rm -r build
else
    echo "build directory not found, skipping removal"
fi

if [ -d "gptop.egg-info" ]; then
    rm -r gptop.egg-info
else
    echo "gptop.egg-info directory not found, skipping removal"
fi

if command -v python &> /dev/null; then
    python setup.py bdist_wheel
else
    echo "Python not found, please install Python and try again"
    exit 1
fi

if command -v twine &> /dev/null; then
    python -m twine upload dist/*
else
    echo "Twine not found, please install Twine and try again"
    exit 1
fi
```