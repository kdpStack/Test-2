"""
Story Engine - Generate compelling narratives for logic puzzles
"""

import random

class StoryEngine:
    """Generate story-driven narratives for Murdoku-style puzzles"""
    
    STORY_TEMPLATES = {
        'mystery': [
            {
                'title': 'The Missing Heirloom',
                'intro': 'A precious family heirloom has vanished from the mansion. Five suspects were present at the time of the theft.',
                'categories': ['Suspect', 'Room', 'Time', 'Motive', 'Evidence'],
                'context': 'Detective Morgan must determine which suspect took which item, from which room, at what time, with what motive, and what evidence links them to the crime.'
            },
            {
                'title': 'The Secret Meeting',
                'intro': 'Five spies arranged a secret meeting in different locations across the city.',
                'categories': ['Spy', 'Location', 'Time', 'Cover Story', 'Contact'],
                'context': 'Intelligence agent Sarah needs to match each spy with their meeting location, time, cover story, and contact person.'
            },
            {
                'title': 'The Art Exhibition',
                'intro': 'Five renowned artists submitted their masterpieces to the prestigious gallery exhibition.',
                'categories': ['Artist', 'Artwork', 'Medium', 'Price', 'Buyer'],
                'context': 'Curator James must organize the exhibition by matching each artist with their artwork, medium, selling price, and the buyer who purchased it.'
            }
        ],
        'adventure': [
            {
                'title': 'The Treasure Hunt',
                'intro': 'Five adventurers seek the legendary treasure hidden across mysterious islands.',
                'categories': ['Adventurer', 'Island', 'Tool', 'Clue', 'Challenge'],
                'context': 'Each adventurer visits a different island, uses a unique tool, finds a specific clue, and faces a particular challenge.'
            },
            {
                'title': 'The Space Mission',
                'intro': 'Five astronauts are assigned to different space stations for a critical mission.',
                'categories': ['Astronaut', 'Station', 'Specialty', 'Duration', 'Discovery'],
                'context': 'Mission control must track each astronaut\'s station assignment, specialty, mission duration, and scientific discovery.'
            }
        ],
        'fantasy': [
            {
                'title': 'The Wizard Council',
                'intro': 'Five powerful wizards gather for the annual council meeting.',
                'categories': ['Wizard', 'Magic School', 'Familiar', 'Spell', 'Artifact'],
                'context': 'The archmage must record each wizard\'s school of magic, magical familiar, signature spell, and enchanted artifact.'
            },
            {
                'title': 'The Dragon Riders',
                'intro': 'Five dragon riders prepare for the great aerial tournament.',
                'categories': ['Rider', 'Dragon', 'Color', 'Ability', 'Homeland'],
                'context': 'Each rider bonds with a unique dragon of a specific color, special ability, and originates from a different homeland.'
            }
        ],
        'business': [
            {
                'title': 'The Corporate Merger',
                'intro': 'Five companies are negotiating a major merger deal.',
                'categories': ['Company', 'CEO', 'Industry', 'Valuation', 'Headquarters'],
                'context': 'Business analyst Maria tracks each company\'s CEO, industry sector, valuation, and headquarters location.'
            },
            {
                'title': 'The Product Launch',
                'intro': 'Five innovative products will launch simultaneously in different markets.',
                'categories': ['Product', 'Market', 'Price', 'Feature', 'Target Audience'],
                'context': 'Marketing director Tom coordinates each product\'s target market, price point, key feature, and intended audience.'
            }
        ],
        'everyday': [
            {
                'title': 'The Dinner Party',
                'intro': 'Five friends are hosting a dinner party with multiple courses.',
                'categories': ['Host', 'Course', 'Ingredient', 'Wine', 'Guest'],
                'context': 'Each host prepares a different course using a unique ingredient, paired with a specific wine, for a particular guest.'
            },
            {
                'title': 'The Book Club',
                'intro': 'Five book club members each recommend their favorite novel this month.',
                'categories': ['Member', 'Genre', 'Author', 'Rating', 'Discussion Leader'],
                'context': 'Track each member\'s recommended genre, author, rating, and who leads the discussion.'
            }
        ]
    }
    
    CLUE_PATTERNS = {
        'direct': '{entity_a} is {entity_b}',
        'negative': '{entity_a} is not {entity_b}',
        'comparative': '{entity_a} is {relation} than {entity_b}',
        'positional': '{entity_a} is {position} to {entity_b}',
        'conditional': 'If {entity_a}, then {entity_b}'
    }
    
    def __init__(self):
        self.current_story = None
    
    def get_story_templates(self, category=None):
        """Get available story templates, optionally filtered by category"""
        if category:
            return self.STORY_TEMPLATES.get(category, [])
        all_templates = []
        for templates in self.STORY_TEMPLATES.values():
            all_templates.extend(templates)
        return all_templates
    
    def get_categories(self):
        """Get all available story categories"""
        return list(self.STORY_TEMPLATES.keys())
    
    def select_story(self, category=None, specific_template=None):
        """Select a story template"""
        if specific_template:
            for templates in self.STORY_TEMPLATES.values():
                for template in templates:
                    if template['title'] == specific_template:
                        self.current_story = template.copy()
                        return template
        
        templates = self.get_story_templates(category)
        if templates:
            self.current_story = random.choice(templates).copy()
            return self.current_story
        return None
    
    def generate_clue(self, pattern_type='direct', entities=None):
        """Generate a clue using specified pattern"""
        if entities is None:
            entities = {'entity_a': 'X', 'entity_b': 'Y', 'relation': 'older', 'position': 'next'}
        
        pattern = self.CLUE_PATTERNS.get(pattern_type, self.CLUE_PATTERNS['direct'])
        return pattern.format(**entities)
    
    def generate_clues_for_story(self, num_clues=5, difficulty='medium'):
        """Generate appropriate clues for the current story"""
        if not self.current_story:
            self.select_story()
        
        clues = []
        categories = self.current_story.get('categories', [])
        
        # Adjust clue complexity based on difficulty
        difficulty_settings = {
            'easy': {'direct': 0.7, 'negative': 0.2, 'comparative': 0.1},
            'medium': {'direct': 0.4, 'negative': 0.3, 'comparative': 0.2, 'positional': 0.1},
            'hard': {'direct': 0.2, 'negative': 0.3, 'comparative': 0.3, 'positional': 0.2},
            'expert': {'direct': 0.1, 'negative': 0.2, 'comparative': 0.3, 'positional': 0.3, 'conditional': 0.1}
        }
        
        settings = difficulty_settings.get(difficulty, difficulty_settings['medium'])
        
        for i in range(num_clues):
            pattern_type = random.choices(
                list(settings.keys()),
                weights=list(settings.values())
            )[0]
            
            # Generate sample entities (in real use, these would come from puzzle data)
            entities = {
                'entity_a': f'Item {i+1}',
                'entity_b': f'Category {random.randint(1, len(categories))}',
                'relation': random.choice(['older', 'younger', 'taller', 'shorter', 'earlier', 'later']),
                'position': random.choice(['next', 'before', 'after', 'between'])
            }
            
            clue = self.generate_clue(pattern_type, entities)
            clues.append(clue)
        
        return clues
    
    def customize_story(self, title=None, intro=None, categories=None, context=None):
        """Customize the current story or create a new one"""
        if not self.current_story:
            self.current_story = {}
        
        if title:
            self.current_story['title'] = title
        if intro:
            self.current_story['intro'] = intro
        if categories:
            self.current_story['categories'] = categories
        if context:
            self.current_story['context'] = context
        
        return self.current_story
    
    def create_custom_story(self, title, intro, categories, context):
        """Create a completely custom story"""
        self.current_story = {
            'title': title,
            'intro': intro,
            'categories': categories,
            'context': context
        }
        return self.current_story
    
    def get_story_info(self):
        """Get current story information"""
        return self.current_story if self.current_story else {}
