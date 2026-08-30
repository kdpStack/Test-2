"""
Flask Web Application for Murdoku Puzzle Generator
Browser-based interface for generating, verifying, and exporting puzzles
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import io

from src.generator import PuzzleGenerator, generate_puzzle
from src.solver import PuzzleSolver, verify_puzzle
from src.story_engine import StoryEngine
from src.exporter import Exporter
from src.themes import ThemeManager

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Initialize components
story_engine = StoryEngine()
theme_manager = ThemeManager()

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def api_generate():
    """Generate a single puzzle"""
    data = request.get_json()
    
    size = data.get('size', 5)
    difficulty = data.get('difficulty', 'medium')
    story_category = data.get('story_category', 'mystery')
    story_template = data.get('story_template', None)
    custom_categories = data.get('categories', None)
    
    # Select story
    story = story_engine.select_story(story_category, story_template)
    
    # Generate puzzle
    categories = custom_categories or (story.get('categories', []) if story else None)
    
    if categories and len(categories) != size:
        categories = categories[:size] if len(categories) > size else categories + [f'Category {i+1}' for i in range(len(categories), size)]
    
    generator = PuzzleGenerator(size=size, difficulty=difficulty)
    if categories and len(categories) == size:
        generator.set_categories(categories)
    
    puzzle_data = generator.generate()
    
    # Verify puzzle
    solver = PuzzleSolver(puzzle_data)
    is_valid, solution, message = solver.verify()
    
    response = {
        'success': True,
        'puzzle': puzzle_data,
        'story': story_engine.get_story_info(),
        'verified': is_valid,
        'verification_message': message
    }
    
    return jsonify(response)


@app.route('/api/bulk-generate', methods=['POST'])
def api_bulk_generate():
    """Generate multiple puzzles in bulk"""
    data = request.get_json()
    
    quantity = data.get('quantity', 10)
    size = data.get('size', 5)
    difficulty = data.get('difficulty', 'medium')
    story_category = data.get('story_category', 'mystery')
    export_format = data.get('export_format', 'json')
    
    quantity = min(quantity, 100)  # Limit to 100 puzzles
    
    puzzles = []
    for i in range(quantity):
        story = story_engine.select_story(story_category)
        categories = story.get('categories', []) if story else None
        
        if categories and len(categories) != size:
            categories = categories[:size] if len(categories) > size else categories + [f'Category {i+1}' for i in range(len(categories), size)]
        
        generator = PuzzleGenerator(size=size, difficulty=difficulty)
        if categories and len(categories) == size:
            generator.set_categories(categories)
        
        puzzle_data = generator.generate()
        
        # Verify
        solver = PuzzleSolver(puzzle_data)
        is_valid, _, _ = solver.verify()
        
        if is_valid:
            puzzles.append({
                'id': i + 1,
                'puzzle': puzzle_data,
                'story': story_engine.get_story_info()
            })
    
    # Export if requested
    if export_format == 'json':
        output_file = os.path.join(OUTPUT_DIR, 'bulk_puzzles.json')
        with open(output_file, 'w') as f:
            json.dump({'puzzles': puzzles}, f, indent=2)
        
        return jsonify({
            'success': True,
            'count': len(puzzles),
            'download_url': f'/download/bulk_puzzles.json'
        })
    
    return jsonify({
        'success': True,
        'count': len(puzzles),
        'puzzles': puzzles[:5]  # Return first 5 for preview
    })


@app.route('/api/verify', methods=['POST'])
def api_verify():
    """Verify a puzzle has unique solution"""
    data = request.get_json()
    puzzle_data = data.get('puzzle', {})
    
    solver = PuzzleSolver(puzzle_data)
    is_valid, solution, message = solver.verify()
    
    return jsonify({
        'success': True,
        'valid': is_valid,
        'message': message,
        'solution': solution
    })


@app.route('/api/export', methods=['POST'])
def api_export():
    """Export puzzle to specified format"""
    data = request.get_json()
    puzzle_data = data.get('puzzle', {})
    story_info = data.get('story', {})
    export_format = data.get('format', 'pdf')
    filename = data.get('filename', 'puzzle')
    
    exporter = Exporter(puzzle_data, story_info)
    
    if export_format == 'json':
        filepath = os.path.join(OUTPUT_DIR, f'{filename}.json')
        exporter.to_json(filepath)
    elif export_format == 'png':
        filepath = os.path.join(OUTPUT_DIR, f'{filename}.png')
        exporter.to_png(filepath)
    elif export_format == 'svg':
        filepath = os.path.join(OUTPUT_DIR, f'{filename}.svg')
        exporter.to_svg(filepath)
    elif export_format == 'pdf':
        filepath = os.path.join(OUTPUT_DIR, f'{filename}.pdf')
        exporter.to_pdf(filepath)
    else:
        return jsonify({'success': False, 'error': 'Invalid format'}), 400
    
    return jsonify({
        'success': True,
        'download_url': f'/download/{filename}.{export_format}'
    })


@app.route('/api/stories', methods=['GET'])
def api_get_stories():
    """Get available story templates"""
    category = request.args.get('category', None)
    stories = story_engine.get_story_templates(category)
    return jsonify({
        'success': True,
        'stories': stories
    })


@app.route('/api/story-categories', methods=['GET'])
def api_get_story_categories():
    """Get available story categories"""
    categories = story_engine.get_categories()
    return jsonify({
        'success': True,
        'categories': categories
    })


@app.route('/api/themes', methods=['GET'])
def api_get_themes():
    """Get available themes"""
    themes = theme_manager.list_themes()
    return jsonify({
        'success': True,
        'themes': themes
    })


@app.route('/download/<filename>')
def download_file(filename):
    """Download generated file"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404


@app.route('/api/custom-story', methods=['POST'])
def api_custom_story():
    """Create custom story"""
    data = request.get_json()
    title = data.get('title', 'Custom Puzzle')
    intro = data.get('intro', '')
    categories = data.get('categories', [])
    context = data.get('context', '')
    
    story = story_engine.create_custom_story(title, intro, categories, context)
    
    return jsonify({
        'success': True,
        'story': story
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
