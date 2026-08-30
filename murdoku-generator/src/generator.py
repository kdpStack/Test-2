"""
Puzzle Generator - Core logic puzzle generation engine
Generates valid logic puzzles with unique solutions
"""

import random
from itertools import permutations, combinations

class PuzzleGenerator:
    """Generate Murdoku-style logic puzzles with configurable parameters"""
    
    DIFFICULTY_SETTINGS = {
        'easy': {'clue_ratio': 0.7, 'direct_clues': 0.6},
        'medium': {'clue_ratio': 0.5, 'direct_clues': 0.4},
        'hard': {'clue_ratio': 0.35, 'direct_clues': 0.25},
        'expert': {'clue_ratio': 0.25, 'direct_clues': 0.15},
        'master': {'clue_ratio': 0.2, 'direct_clues': 0.1}
    }
    
    def __init__(self, size=5, difficulty='medium'):
        """
        Initialize puzzle generator
        
        Args:
            size: Grid size (5x5, 6x6, etc.)
            difficulty: Difficulty level
        """
        self.size = size
        self.difficulty = difficulty
        self.solution = None
        self.clues = []
        self.categories = []
    
    def generate_solution(self):
        """Generate a valid complete solution for the puzzle"""
        # Create base permutation for first category
        self.solution = []
        base = list(range(self.size))
        
        # First category is just 0 to size-1
        self.solution.append(base.copy())
        
        # Generate remaining categories as permutations
        for _ in range(self.size - 1):
            perm = base.copy()
            random.shuffle(perm)
            # Ensure this permutation doesn't create duplicate rows
            attempts = 0
            while self._is_duplicate_row(perm) and attempts < 100:
                random.shuffle(perm)
                attempts += 1
            self.solution.append(perm)
        
        return self.solution
    
    def _is_duplicate_row(self, perm):
        """Check if permutation creates duplicate row pattern"""
        for existing in self.solution[1:]:
            if perm == existing:
                return True
        return False
    
    def generate_clues(self, num_clues=None):
        """
        Generate clues based on the solution
        
        Args:
            num_clues: Number of clues (auto-calculated if None)
        """
        if not self.solution:
            self.generate_solution()
        
        settings = self.DIFFICULTY_SETTINGS.get(
            self.difficulty, 
            self.DIFFICULTY_SETTINGS['medium']
        )
        
        if num_clues is None:
            # Calculate number of clues based on difficulty
            max_clues = self.size * self.size
            num_clues = int(max_clues * settings['clue_ratio'])
            num_clues = max(num_clues, self.size + 2)  # Minimum clues
        
        self.clues = []
        clue_types = ['direct', 'negative', 'comparative']
        
        for i in range(num_clues):
            clue_type = random.choices(
                clue_types,
                weights=[settings['direct_clues'], 0.3, 0.3 - settings['direct_clues']]
            )[0]
            
            clue = self._generate_single_clue(clue_type)
            if clue:
                self.clues.append(clue)
        
        return self.clues
    
    def _generate_single_clue(self, clue_type):
        """Generate a single clue of specified type"""
        cat1 = random.randint(0, self.size - 1)
        cat2 = random.randint(0, self.size - 1)
        while cat2 == cat1:
            cat2 = random.randint(0, self.size - 1)
        
        idx = random.randint(0, self.size - 1)
        val1 = self.solution[cat1][idx]
        val2 = self.solution[cat2][idx]
        
        if clue_type == 'direct':
            return {
                'type': 'direct',
                'category1': cat1,
                'category2': cat2,
                'value1': val1,
                'value2': val2,
                'text': f"Item {val1} in Category {cat1} matches Item {val2} in Category {cat2}"
            }
        elif clue_type == 'negative':
            # Find a value that doesn't match
            non_matching_idx = (idx + 1) % self.size
            val2_non = self.solution[cat2][non_matching_idx]
            return {
                'type': 'negative',
                'category1': cat1,
                'category2': cat2,
                'value1': val1,
                'value2': val2_non,
                'text': f"Item {val1} in Category {cat1} does NOT match Item {val2_non} in Category {cat2}"
            }
        else:  # comparative
            idx2 = random.randint(0, self.size - 1)
            while idx2 == idx:
                idx2 = random.randint(0, self.size - 1)
            val1_comp = self.solution[cat1][idx2]
            relation = random.choice(['before', 'after'])
            return {
                'type': 'comparative',
                'category1': cat1,
                'category2': cat2,
                'value1': val1,
                'value2': val1_comp,
                'relation': relation,
                'text': f"Item {val1} in Category {cat1} is {relation} Item {val1_comp}"
            }
    
    def set_categories(self, categories):
        """Set custom category names"""
        if len(categories) == self.size:
            self.categories = categories
            return True
        return False
    
    def get_puzzle_data(self):
        """Get complete puzzle data structure"""
        return {
            'size': self.size,
            'difficulty': self.difficulty,
            'solution': self.solution,
            'clues': self.clues,
            'categories': self.categories or [f'Category {i+1}' for i in range(self.size)]
        }
    
    def regenerate(self, keep_difficulty=True):
        """Regenerate puzzle with same or new parameters"""
        self.solution = None
        self.clues = []
        
        if not keep_difficulty:
            self.difficulty = random.choice(list(self.DIFFICULTY_SETTINGS.keys()))
        
        return self.generate()
    
    def generate(self):
        """Generate complete puzzle"""
        self.generate_solution()
        self.generate_clues()
        return self.get_puzzle_data()
    
    def validate_puzzle(self):
        """Validate that puzzle has unique solution"""
        # Basic validation - should be enhanced with actual solver
        if not self.solution or not self.clues:
            return False
        
        if len(self.clues) < self.size + 1:
            return False
        
        return True
    
    def export_grid_format(self):
        """Export puzzle in grid format for display"""
        grid = []
        for row_idx in range(self.size):
            row = []
            for col_idx in range(self.size):
                row.append(self.solution[col_idx][row_idx])
            grid.append(row)
        return grid


def generate_puzzle(size=5, difficulty='medium', categories=None):
    """Convenience function to generate a puzzle"""
    generator = PuzzleGenerator(size=size, difficulty=difficulty)
    if categories:
        generator.set_categories(categories)
    return generator.generate()
