"""
Exporter - Export puzzles to various formats (PDF, PNG, SVG, JSON)
"""

import io
import json
from PIL import Image, ImageDraw, ImageFont


class Exporter:
    """Export puzzles to different formats"""
    
    def __init__(self, puzzle_data, story_info=None):
        """
        Initialize exporter with puzzle data
        
        Args:
            puzzle_data: Puzzle dictionary from generator
            story_info: Optional story information
        """
        self.puzzle = puzzle_data
        self.story = story_info or {}
        self.size = puzzle_data.get('size', 5)
        self.clues = puzzle_data.get('clues', [])
        self.categories = puzzle_data.get('categories', [])
    
    def to_json(self, filepath=None):
        """Export puzzle as JSON"""
        data = {
            'puzzle': self.puzzle,
            'story': self.story,
            'format_version': '1.0'
        }
        
        json_str = json.dumps(data, indent=2)
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(json_str)
            return filepath
        
        return json_str
    
    def to_png(self, filepath=None, width=800, height=1000, theme='classic'):
        """Export puzzle as PNG image"""
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw title
        title = self.story.get('title', 'Logic Puzzle')
        draw.text((width//2, 30), title, fill='black', anchor='mm')
        
        # Draw story intro
        intro = self.story.get('intro', '')
        y_pos = 60
        self._draw_wrapped_text(draw, intro, (40, y_pos, width-40, y_pos+60))
        
        # Draw grid header
        y_pos = 140
        draw.text((40, y_pos), 'Solution Grid:', fill='black')
        
        # Draw grid
        grid_size = min(width - 100, 500)
        cell_size = grid_size // self.size
        grid_x = (width - grid_size) // 2
        grid_y = y_pos + 30
        
        # Draw grid lines
        for i in range(self.size + 1):
            # Vertical lines
            x = grid_x + i * cell_size
            draw.line([(x, grid_y), (x, grid_y + grid_size)], fill='black', width=2)
            # Horizontal lines
            y = grid_y + i * cell_size
            draw.line([(grid_x, y), (grid_x + grid_size, y)], fill='black', width=2)
        
        # Draw category labels
        for i, cat in enumerate(self.categories[:self.size]):
            x = grid_x + i * cell_size + cell_size // 2
            draw.text((x, grid_y - 20), str(i+1), fill='black', anchor='mm')
        
        # Draw clues section
        y_pos = grid_y + grid_size + 40
        draw.text((40, y_pos), 'Clues:', fill='black')
        
        y_pos += 30
        for i, clue in enumerate(self.clues[:15]):  # Limit clues shown
            clue_text = f"{i+1}. {clue.get('text', '')}"
            self._draw_wrapped_text(draw, clue_text, (40, y_pos, width-40, y_pos+20))
            y_pos += 20
        
        if filepath:
            img.save(filepath, 'PNG')
            return filepath
        
        return img
    
    def to_svg(self, filepath=None, width=800, height=1000):
        """Export puzzle as SVG"""
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
            f'<rect width="{width}" height="{height}" fill="white"/>',
        ]
        
        # Title
        title = self.story.get('title', 'Logic Puzzle')
        svg_parts.append(f'<text x="{width//2}" y="40" text-anchor="middle" font-size="24" font-weight="bold">{title}</text>')
        
        # Story intro
        intro = self.story.get('intro', '')
        svg_parts.append(f'<text x="40" y="70" font-size="14">{intro[:80]}...</text>')
        
        # Grid
        grid_size = min(width - 100, 500)
        cell_size = grid_size // self.size
        grid_x = (width - grid_size) // 2
        grid_y = 100
        
        # Draw grid lines
        for i in range(self.size + 1):
            x = grid_x + i * cell_size
            y = grid_y + i * cell_size
            svg_parts.append(f'<line x1="{x}" y1="{grid_y}" x2="{x}" y2="{grid_y + grid_size}" stroke="black" stroke-width="2"/>')
            svg_parts.append(f'<line x1="{grid_x}" y1="{y}" x2="{grid_x + grid_size}" y2="{y}" stroke="black" stroke-width="2"/>')
        
        # Clues
        y_pos = grid_y + grid_size + 30
        svg_parts.append(f'<text x="40" y="{y_pos}" font-size="16" font-weight="bold">Clues:</text>')
        
        for i, clue in enumerate(self.clues[:12]):
            y_pos += 20
            clue_text = clue.get('text', '')[:70]
            svg_parts.append(f'<text x="40" y="{y_pos}" font-size="12">{i+1}. {clue_text}</text>')
        
        svg_parts.append('</svg>')
        
        svg_content = '\n'.join(svg_parts)
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(svg_content)
            return filepath
        
        return svg_content
    
    def to_pdf(self, filepath=None):
        """Export puzzle as PDF using reportlab"""
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import inch
            
            c = canvas.Canvas(filepath or io.BytesIO(), pagesize=letter)
            width, height = letter
            
            # Title
            title = self.story.get('title', 'Logic Puzzle')
            c.setFont("Helvetica-Bold", 18)
            c.drawCentredString(width/2, height - 1*inch, title)
            
            # Story intro
            intro = self.story.get('intro', '')
            c.setFont("Helvetica", 11)
            text_object = c.beginText(1*inch, height - 1.5*inch)
            text_object.textLines(intro)
            c.drawText(text_object)
            
            # Grid
            grid_size = 5*inch
            cell_size = grid_size / self.size
            grid_x = (width - grid_size) / 2
            grid_y = height - 4*inch
            
            c.setStrokeColorRGB(0, 0, 0)
            c.setLineWidth(2)
            
            for i in range(self.size + 1):
                x = grid_x + i * cell_size
                y = grid_y + i * cell_size
                c.line(grid_x, y, grid_x + grid_size, y)
                c.line(x, grid_y, x, grid_y + grid_size)
            
            # Category labels
            c.setFont("Helvetica", 10)
            for i, cat in enumerate(self.categories[:self.size]):
                x = grid_x + i * cell_size + cell_size / 2
                c.drawCentredString(x, grid_y - 15, str(i+1))
            
            # Clues
            y_pos = grid_y - 0.5*inch
            c.setFont("Helvetica-Bold", 14)
            c.drawString(1*inch, y_pos, "Clues:")
            
            c.setFont("Helvetica", 10)
            y_pos -= 20
            for i, clue in enumerate(self.clues[:15]):
                clue_text = f"{i+1}. {clue.get('text', '')}"
                if y_pos < 1*inch:
                    c.showPage()
                    y_pos = height - 1*inch
                    c.setFont("Helvetica", 10)
                
                c.drawString(1*inch, y_pos, clue_text)
                y_pos -= 15
            
            if filepath and isinstance(filepath, str):
                c.save()
                return filepath
            
            return c
            
        except ImportError:
            # Fallback to PNG if reportlab not available
            png_path = filepath.replace('.pdf', '.png') if filepath else None
            return self.to_png(png_path)
    
    def _draw_wrapped_text(self, draw, text, bbox):
        """Draw text with wrapping"""
        x1, y1, x2, y2 = bbox
        max_width = x2 - x1
        
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            bbox_test = draw.textbbox((0, 0), test_line)
            if bbox_test[2] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        y = y1
        for line in lines:
            draw.text((x1, y), line, fill='black')
            y += 15
    
    def export_all(self, output_dir='output', base_name='puzzle'):
        """Export puzzle in all formats"""
        import os
        
        os.makedirs(output_dir, exist_ok=True)
        
        results = {}
        
        # JSON
        json_path = os.path.join(output_dir, f'{base_name}.json')
        results['json'] = self.to_json(json_path)
        
        # PNG
        png_path = os.path.join(output_dir, f'{base_name}.png')
        results['png'] = self.to_png(png_path)
        
        # SVG
        svg_path = os.path.join(output_dir, f'{base_name}.svg')
        results['svg'] = self.to_svg(svg_path)
        
        # PDF
        pdf_path = os.path.join(output_dir, f'{base_name}.pdf')
        results['pdf'] = self.to_pdf(pdf_path)
        
        return results


def export_puzzle(puzzle_data, filepath, story_info=None):
    """Convenience function to export a puzzle"""
    exporter = Exporter(puzzle_data, story_info)
    
    if filepath.endswith('.json'):
        return exporter.to_json(filepath)
    elif filepath.endswith('.png'):
        return exporter.to_png(filepath)
    elif filepath.endswith('.svg'):
        return exporter.to_svg(filepath)
    elif filepath.endswith('.pdf'):
        return exporter.to_pdf(filepath)
    
    return exporter.to_json(filepath)
