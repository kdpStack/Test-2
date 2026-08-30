# Murdoku Puzzle Generator - Premium Story-Driven Logic Puzzles

A premium browser-based tool for generating "Murdoku-style" story-driven logic puzzles with bulk generation, puzzle verification, and complete control over results. Perfect for KDP publishers and puzzle creators.

## Features

### Core Functionality
- **Story-Driven Puzzles**: Generate engaging logic puzzles with compelling narratives
- **Multiple Grid Sizes**: Support for 5x5, 6x6, 7x7, 8x8, 9x9, 10x10, and custom sizes
- **Difficulty Levels**: Easy, Medium, Hard, Expert, and Master with fine-tuned controls
- **Bulk Generation**: Create hundreds of puzzles in minutes with customizable parameters
- **Puzzle Verification**: Built-in solver ensures all puzzles have unique solutions
- **Export Options**: PDF, PNG, SVG, JSON, and print-ready formats for KDP

### Advanced Controls
- **Theme Customization**: Choose from multiple themes or create your own
- **Clue Density Control**: Fine-tune the number and type of clues
- **Story Templates**: Pre-built narrative templates or create custom stories
- **Category Management**: Organize puzzles by category, difficulty, or collection
- **Batch Processing**: Process multiple puzzle configurations simultaneously

### User Experience
- **Intuitive Interface**: Clean, modern browser-based UI
- **Real-time Preview**: See puzzle changes instantly
- **Interactive Solver**: Test puzzles directly in the browser
- **Progress Tracking**: Monitor generation progress for bulk operations
- **Responsive Design**: Works on desktop, tablet, and mobile

## Installation

```bash
cd murdoku-generator
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000 in your browser.

## Quick Start

1. Open the web interface
2. Select grid size and difficulty
3. Choose a theme or story template
4. Click "Generate Puzzle"
5. Verify the solution with built-in solver
6. Export in your preferred format

For bulk generation:
1. Go to "Bulk Generate" tab
2. Set quantity and parameters
3. Configure export options
4. Click "Start Bulk Generation"
5. Download the generated package

## Project Structure

```
murdoku-generator/
├── app.py                  # Flask web application
├── requirements.txt        # Python dependencies
├── src/
│   ├── __init__.py
│   ├── generator.py        # Puzzle generation engine
│   ├── solver.py           # Puzzle verification solver
│   ├── story_engine.py     # Story template system
│   ├── exporter.py         # Export to PDF, PNG, etc.
│   └── themes.py           # Theme definitions
├── templates/
│   ├── index.html          # Main interface
│   └── ...
├── static/
│   ├── css/
│   │   └── style.css       # Styling
│   └── js/
│       └── app.js          # Frontend logic
└── output/                 # Generated puzzles
```

## API Usage

```python
from src.generator import PuzzleGenerator
from src.solver import PuzzleSolver
from src.exporter import Exporter

# Create a puzzle
generator = PuzzleGenerator(size=6, difficulty='medium')
puzzle = generator.generate(theme='mystery')

# Verify solution
solver = PuzzleSolver(puzzle)
is_valid, solution = solver.verify()

# Export
exporter = Exporter(puzzle)
exporter.to_pdf('output/puzzle.pdf')
exporter.to_png('output/puzzle.png')
```

## License

MIT License - See LICENSE file for details

## Support

For questions and support, please open an issue on GitHub.
