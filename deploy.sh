rm -r dist
rm -r build
rm -r gptop.egg-info
python setup.py bdist_wheel
python -m twine upload dist/*