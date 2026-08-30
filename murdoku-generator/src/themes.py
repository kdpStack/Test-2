"""
Theme Manager - Handle puzzle themes and visual styles
"""

class ThemeManager:
    """Manage puzzle themes for different visual styles and categories"""
    
    THEMES = {
        'classic': {
            'name': 'Classic',
            'colors': {
                'background': '#FFFFFF',
                'grid_lines': '#000000',
                'clue_background': '#F0F0F0',
                'text': '#000000',
                'highlight': '#FFD700'
            },
            'fonts': {
                'grid': 'Arial',
                'story': 'Georgia'
            }
        },
        'mystery': {
            'name': 'Mystery',
            'colors': {
                'background': '#1a1a2e',
                'grid_lines': '#4a4a6a',
                'clue_background': '#16213e',
                'text': '#e94560',
                'highlight': '#ffd700'
            },
            'fonts': {
                'grid': 'Courier New',
                'story': 'Georgia'
            }
        },
        'nature': {
            'name': 'Nature',
            'colors': {
                'background': '#f5f5dc',
                'grid_lines': '#2d5016',
                'clue_background': '#e8f5e9',
                'text': '#1b5e20',
                'highlight': '#ff9800'
            },
            'fonts': {
                'grid': 'Verdana',
                'story': 'Comic Sans MS'
            }
        },
        'ocean': {
            'name': 'Ocean',
            'colors': {
                'background': '#e0f7fa',
                'grid_lines': '#0277bd',
                'clue_background': '#b3e5fc',
                'text': '#01579b',
                'highlight': '#ff6f00'
            },
            'fonts': {
                'grid': 'Arial',
                'story': 'Verdana'
            }
        },
        'elegant': {
            'name': 'Elegant',
            'colors': {
                'background': '#fafafa',
                'grid_lines': '#424242',
                'clue_background': '#eeeeee',
                'text': '#212121',
                'highlight': '#c0a062'
            },
            'fonts': {
                'grid': 'Times New Roman',
                'story': 'Palatino'
            }
        }
    }
    
    def __init__(self):
        self.current_theme = 'classic'
    
    def get_theme(self, theme_name):
        """Get theme configuration by name"""
        return self.THEMES.get(theme_name, self.THEMES['classic'])
    
    def set_theme(self, theme_name):
        """Set current theme"""
        if theme_name in self.THEMES:
            self.current_theme = theme_name
            return True
        return False
    
    def list_themes(self):
        """List all available themes"""
        return [(key, theme['name']) for key, theme in self.THEMES.items()]
    
    def get_colors(self, theme_name=None):
        """Get color palette for a theme"""
        theme = self.get_theme(theme_name or self.current_theme)
        return theme['colors']
    
    def get_fonts(self, theme_name=None):
        """Get font configuration for a theme"""
        theme = self.get_theme(theme_name or self.current_theme)
        return theme['fonts']
    
    def create_custom_theme(self, name, colors, fonts):
        """Create a custom theme"""
        self.THEMES[name] = {
            'name': name,
            'colors': colors,
            'fonts': fonts
        }
        return True
