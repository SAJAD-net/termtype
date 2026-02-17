#!/usr/bin/env python3

import curses
import sys
import time
import random
import os
import textwrap
from typing import List, Tuple, Optional, Dict
from enum import Enum
from pathlib import Path

class Category(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    PYTHON = "python"
    CSTYLE = "c_style"
    PRACTICE = "practice"
    CUSTOM = "custom"

class TemplateManager:
    """Manages loading and parsing of template files"""
    
    def __init__(self, templates_dir: str = "templates"):
        # Get the directory where the script is located
        script_dir = Path(__file__).parent.absolute()
        self.templates_dir = script_dir / templates_dir
        self.cache: Dict[Category, List[str]] = {}
        self.category_names = {
            Category.EASY: "Easy Sentences",
            Category.MEDIUM: "Medium (with numbers)",
            Category.HARD: "Hard (complex punctuation)",
            Category.PYTHON: "Python Code",
            Category.CSTYLE: "C/Java/JavaScript",
            Category.PRACTICE: "Practice (common mistakes)",
            Category.CUSTOM: "Custom Templates"
        }
        
    def load_templates(self, category: Category) -> List[str]:
        """Load all templates from a category directory"""
        if category in self.cache:
            return self.cache[category]
        
        templates = []
        category_dir = self.templates_dir / category.value
        
        if not category_dir.exists():
            return [self._get_sample_template(category)]
        
        # Load all .txt files in the directory
        txt_files = sorted(category_dir.glob("*.txt"))
        
        for file_path in txt_files:
            if file_path.name == "README.txt" or file_path.name.startswith("README"):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                    # Skip empty files
                    if not content:
                        continue
                    
                    # Parse templates
                    file_templates = self._parse_template_file(content)
                    templates.extend(file_templates)
                    
            except Exception as e:
                continue
        
        # If no templates found, provide sample
        if not templates:
            templates = [self._get_sample_template(category)]
        
        self.cache[category] = templates
        return templates
    
    def _parse_template_file(self, content: str) -> List[str]:
        """Parse a template file, supporting multiple templates separated by '---'"""
        templates = []
        
        # Split by separator line
        parts = content.split('\n---\n')
        
        for part in parts:
            part = part.strip()
            if part and not part.startswith('#'):
                # Remove any inline comments
                lines = []
                for line in part.split('\n'):
                    if not line.lstrip().startswith('#'):
                        # Preserve the line exactly as is, including indentation
                        lines.append(line)
                
                template = '\n'.join(lines).strip()
                if template:
                    templates.append(template)
        
        return templates
    
    def _get_sample_template(self, category: Category) -> str:
        """Provide a sample template if none exist"""
        samples = {
            Category.EASY: "The quick brown fox jumps over the lazy dog.",
            Category.MEDIUM: "Python 3.12 was released in 2024 with 42 new features.",
            Category.HARD: "Email: user@example.com, Phone: 555-123-4567, Date: 2024-03-15",
            Category.PYTHON: "def hello():\n    print('Hello, World!')",
            Category.CSTYLE: "#include <stdio.h>\n\nint main() {\n    printf('Hello');\n    return 0;\n}",
            Category.PRACTICE: "teh (should be: the)\nrecieve (should be: receive)",
            Category.CUSTOM: "Add your own templates in templates/custom/"
        }
        return samples.get(category, "Sample template")
    
    def get_random_templates(self, category: Category, count: int = 3) -> List[str]:
        """Get random templates from a category"""
        templates = self.load_templates(category)
        
        # Ensure we don't ask for more than available
        count = min(count, len(templates))
        if count == 0:
            return [self._get_sample_template(category)]
        
        return random.sample(templates, count)
    
    def get_category_info(self) -> Dict[Category, Tuple[str, int]]:
        """Get information about all categories"""
        info = {}
        for category in Category:
            templates = self.load_templates(category)
            info[category] = (self.category_names[category], len(templates))
        return info

class TypingTest:
    def __init__(self, category: Category, templates: List[str]):
        self.category = category
        # Store each template as a list of lines to preserve structure
        self.templates = [template.split('\n') for template in templates]
        self.current_template_index = 0
        self.current_line_index = 0
        self.current_template = self.templates[0] if self.templates else []
        self.user_input = []  # List of characters typed for current line
        self.start_time = None
        self.end_time = None
        self.correct_chars = 0
        self.total_chars = 0
        self.wpm_history = []
        self.last_update_time = None
        
        # Calculate total characters for progress
        self.total_chars_all_lines = sum(len(line) for template in self.templates for line in template)
        self.completed_chars = 0
        
    def get_current_line(self) -> str:
        """Get the current line to type"""
        if self.current_template and self.current_line_index < len(self.current_template):
            return self.current_template[self.current_line_index]
        return ""
    
    def is_line_complete(self) -> bool:
        """Check if current line is completely typed"""
        current_line = self.get_current_line()
        return len(self.user_input) >= len(current_line)
    
    def move_to_next_line(self) -> bool:
        """Move to next line in current template. Returns True if template complete."""
        self.current_line_index += 1
        self.user_input = []
        
        if self.current_line_index >= len(self.current_template):
            return self.move_to_next_template()
        return False
    
    def move_to_next_template(self) -> bool:
        """Move to next template. Returns True if all templates complete."""
        self.current_template_index += 1
        self.current_line_index = 0
        
        if self.current_template_index >= len(self.templates):
            return True
        
        self.current_template = self.templates[self.current_template_index]
        return False
    
    def calculate_instant_wpm(self) -> float:
        """Calculate real-time WPM based on current typing speed"""
        if not self.start_time:
            return 0.0
        
        now = time.time()
        elapsed = now - self.start_time
        
        if elapsed > 0 and self.completed_chars > 0:
            minutes = elapsed / 60
            wpm = (self.completed_chars / 5) / minutes
            
            # Update history every second
            if self.last_update_time is None or now - self.last_update_time >= 1.0:
                self.wpm_history.append(wpm)
                self.last_update_time = now
                # Keep last 10 seconds of history
                if len(self.wpm_history) > 10:
                    self.wpm_history.pop(0)
            
            return round(wpm, 1)
        return 0.0
    
    def calculate_average_wpm(self) -> float:
        """Calculate average WPM over the last 10 seconds"""
        if not self.wpm_history:
            return 0.0
        return round(sum(self.wpm_history) / len(self.wpm_history), 1)
    
    def calculate_accuracy(self) -> float:
        """Calculate typing accuracy"""
        if self.total_chars == 0:
            return 100.0
        return round((self.correct_chars / self.total_chars) * 100, 1)
    
    def get_progress(self) -> Tuple[int, int, int, int, int, int]:
        """Return (current_template, total_templates, current_line, total_lines, completed_chars, total_chars)"""
        total_lines_in_template = len(self.current_template) if self.current_template else 0
        current_line = self.current_line_index + 1 if total_lines_in_template > 0 else 0
        
        return (self.current_template_index + 1, len(self.templates),
                current_line, total_lines_in_template,
                self.completed_chars, self.total_chars_all_lines)
    
    def check_character(self, char_pos: int) -> Optional[bool]:
        """Check if character at position is correct"""
        current_line = self.get_current_line()
        
        if not current_line:
            return None
        
        if char_pos >= len(current_line):
            return None
        
        if char_pos >= len(self.user_input):
            return None
        
        return self.user_input[char_pos] == current_line[char_pos]
    
    def submit_line(self) -> bool:
        """Submit current line, return True if test is complete"""
        if not self.user_input:
            return False
        
        current_line = self.get_current_line()
        
        # Start timer on first line
        if self.start_time is None:
            self.start_time = time.time()
            self.last_update_time = time.time()
        
        # Calculate correct characters for this line
        line_correct = 0
        for i, char in enumerate(self.user_input):
            if i < len(current_line) and char == current_line[i]:
                line_correct += 1
        
        self.correct_chars += line_correct
        self.total_chars += len(current_line)
        self.completed_chars += len(current_line)
        
        # Move to next line or template
        is_complete = self.move_to_next_line()
        
        # If test is complete, set end_time
        if is_complete:
            self.end_time = time.time()
        
        return is_complete

def draw_menu(stdscr, height, width, template_manager: TemplateManager) -> Optional[Category]:
    """Draw category selection menu"""
    stdscr.clear()
    
    # Title
    title = "⚡ TERMTYPE - WPM TEST ⚡"
    try:
        stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
        x = max(0, (width // 2) - (len(title) // 2))
        stdscr.addstr(2, x, title)
        stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
    except:
        pass
    
    # Subtitle
    subtitle = "Select Template Category:"
    try:
        x = max(0, (width // 2) - (len(subtitle) // 2))
        stdscr.addstr(4, x, subtitle)
    except:
        pass
    
    # Get category info
    category_info = template_manager.get_category_info()
    
    # Menu items
    menu_items = []
    for i, (category, (name, count)) in enumerate(category_info.items()):
        key = str(i + 1)
        menu_items.append((key, category, name, count))
    
    # Add quit option
    menu_items.append(("q", None, "Quit", 0))
    
    for i, (key, category, name, count) in enumerate(menu_items):
        y = 7 + i * 2
        try:
            stdscr.addstr(y, width // 4, f"[{key}]")
            
            if category:
                color_pair = 2 if count > 0 else 3
                stdscr.attron(curses.color_pair(color_pair) | curses.A_BOLD)
                stdscr.addstr(y, width // 4 + 4, f"{name}")
                stdscr.attroff(curses.color_pair(color_pair) | curses.A_BOLD)
                stdscr.addstr(y, width // 4 + 30, f"({count} templates)")
            else:
                stdscr.attron(curses.color_pair(3))
                stdscr.addstr(y, width // 4 + 4, name)
                stdscr.attroff(curses.color_pair(3))
        except:
            pass
    
    # Instructions
    try:
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(height-3, 2, "Press number key to select category, 'q' to quit")
        stdscr.attroff(curses.color_pair(4))
    except:
        pass
    
    stdscr.refresh()
    
    # Get user input
    while True:
        key = stdscr.getch()
        
        if key == ord('q') or key == ord('Q') or key == 27:
            return None
        
        # Check number keys
        for i, (num_key, category, _, _) in enumerate(menu_items):
            if num_key != "q" and key == ord(num_key):
                return category

def draw_status_bar(stdscr, height, width, test: TypingTest, category_name: str):
    """Draw the status bar at the bottom"""
    instant_wpm = test.calculate_instant_wpm()
    avg_wpm = test.calculate_average_wpm()
    accuracy = test.calculate_accuracy()
    current_template, total_templates, current_line, total_lines, completed_chars, total_chars = test.get_progress()
    
    statusbarstr = f" WPM: {instant_wpm:>5.1f} (avg: {avg_wpm:>5.1f}) | Accuracy: {accuracy:>5.1f}% | Template: {current_template}/{total_templates} | Line: {current_line}/{total_lines} | Chars: {completed_chars}/{total_chars} | {category_name} "
    
    # Clear and draw status bar
    try:
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(height-1, 0, statusbarstr[:width-1])
        stdscr.attroff(curses.color_pair(4))
    except:
        pass

def draw_content(stdscr, test: TypingTest, start_y: int, width: int, height: int):
    """Draw all lines with visual feedback and proper indentation preservation"""
    y = start_y
    
    # Show template header
    current_template, total_templates, current_line, total_lines, _, _ = test.get_progress()
    try:
        stdscr.attron(curses.color_pair(4) | curses.A_BOLD)
        header = f"Template {current_template} of {total_templates} (Line {current_line}/{total_lines})"
        stdscr.addstr(y, 2, header)
        stdscr.attroff(curses.color_pair(4) | curses.A_BOLD)
        y += 2
    except:
        pass
    
    # Show all lines of the current template with proper indentation
    for i, line in enumerate(test.current_template):
        if y >= height - 5:  # Prevent overflow - now height is defined
            try:
                stdscr.addstr(y, 2, "...")
            except:
                pass
            break
        
        if i < test.current_line_index:
            # Completed lines - show in green with checkmark
            try:
                stdscr.addstr(y, 2, "✓ ")
                # Preserve indentation by not stripping the line
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y, 4, line[:width-6])
                stdscr.attroff(curses.color_pair(2))
            except:
                pass
            y += 1
            
        elif i == test.current_line_index:
            # Current line - show with typing feedback
            try:
                stdscr.addstr(y, 2, "▶ ")
                
                # Draw the target line character by character with colors
                x_pos = 4
                for j, char in enumerate(line):
                    if x_pos >= width - 2:
                        y += 1
                        x_pos = 4
                        # Continue on next line
                    
                    char_status = test.check_character(j)
                    
                    try:
                        if char_status is True:
                            stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
                            stdscr.addstr(y, x_pos, char)
                            stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
                        elif char_status is False:
                            stdscr.attron(curses.color_pair(3) | curses.A_BOLD)
                            stdscr.addstr(y, x_pos, char)
                            stdscr.attroff(curses.color_pair(3) | curses.A_BOLD)
                        else:
                            stdscr.addstr(y, x_pos, char)
                    except:
                        pass
                    
                    x_pos += 1
                
                y += 1  # Move past the target line
                
            except:
                y += 1
            
            # Show what user has typed
            if test.user_input:
                try:
                    stdscr.addstr(y, 2, "You: ")
                    user_str = ''.join(test.user_input)
                    
                    # Show user input with proper indentation
                    x_pos = 7
                    for j, char in enumerate(user_str):
                        if x_pos >= width - 2:
                            y += 1
                            x_pos = 2
                        
                        # Check if this character matches the target
                        if j < len(line) and char == line[j]:
                            stdscr.attron(curses.color_pair(2))
                            stdscr.addstr(y, x_pos, char)
                            stdscr.attroff(curses.color_pair(2))
                        else:
                            stdscr.attron(curses.color_pair(3))
                            stdscr.addstr(y, x_pos, char)
                            stdscr.attroff(curses.color_pair(3))
                        
                        x_pos += 1
                    
                    # Show cursor
                    if x_pos < width - 1:
                        stdscr.addstr(y, x_pos, "█")
                    
                    # Show line completion status
                    if test.is_line_complete():
                        stdscr.attron(curses.color_pair(2))
                        stdscr.addstr(y, x_pos + 1, " ✓ Press Enter")
                        stdscr.attroff(curses.color_pair(2))
                    else:
                        remaining = len(line) - len(user_str)
                        if remaining > 0:
                            stdscr.attron(curses.color_pair(4))
                            stdscr.addstr(y, x_pos + 1, f" ({remaining} left)")
                            stdscr.attroff(curses.color_pair(4))
                    
                    y += 1
                except:
                    y += 1
        else:
            # Future lines - show in dim with preserved indentation
            try:
                stdscr.attron(curses.A_DIM)
                stdscr.addstr(y, 4, line[:width-6])
                stdscr.attroff(curses.A_DIM)
            except:
                pass
            y += 1
        
        y += 1  # Add spacing between lines
    
    return y

def draw_progress_bar(stdscr, test: TypingTest, start_y: int, width: int):
    """Draw a progress bar"""
    _, _, _, _, completed_chars, total_chars = test.get_progress()
    percentage = completed_chars / total_chars if total_chars > 0 else 0
    bar_width = min(50, width - 10)
    filled = int(bar_width * percentage)
    
    try:
        stdscr.addstr(start_y, 2, "Progress: [")
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(start_y, 13, "█" * filled)
        stdscr.attroff(curses.color_pair(2))
        stdscr.addstr(start_y, 13 + filled, "░" * (bar_width - filled))
        stdscr.addstr(start_y, 13 + bar_width, f"] {percentage*100:.1f}%")
    except:
        pass

def draw_instructions(stdscr, height: int):
    """Draw instructions at the bottom"""
    try:
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(height-3, 2, "Enter: Submit line | Backspace: Delete | ESC: Menu")
        stdscr.attroff(curses.color_pair(4))
    except:
        pass

def draw_results(stdscr, height, width, test: TypingTest, category_name: str):
    """Draw test results with proper alignment"""
    stdscr.clear()
    
    instant_wpm = test.calculate_instant_wpm()
    avg_wpm = test.calculate_average_wpm()
    accuracy = test.calculate_accuracy()
    
    # Make sure end_time is set
    if test.end_time is None and test.start_time is not None:
        test.end_time = time.time()
    
    total_time = test.end_time - test.start_time if test.end_time and test.start_time else 0
    
    # Create properly aligned box
    results = [
        "╔════════════════════════════╗",
        "║      TEST COMPLETE!        ║",
        "╠════════════════════════════╣",
        f"║  Final WPM:  {instant_wpm:>6.1f}      ║",
        f"║  Avg WPM:    {avg_wpm:>6.1f}      ║",
        f"║  Accuracy:   {accuracy:>6.1f}%      ║",
        f"║  Time:       {total_time:>6.1f}s      ║",
        "╚════════════════════════════╝",
        "",
        "Press any key to continue..."
    ]
    
    # Calculate starting Y position to center vertically
    start_y = max(0, (height // 2) - (len(results) // 2))
    
    for i, line in enumerate(results):
        # Center each line horizontally
        x = max(0, (width // 2) - (len(line) // 2))
        try:
            # Add some styling
            if i == 1:  # Title line
                stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
                stdscr.addstr(start_y + i, x, line)
                stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)
            elif i >= 3 and i <= 6:  # Stats lines
                stdscr.attron(curses.color_pair(4))
                stdscr.addstr(start_y + i, x, line)
                stdscr.attroff(curses.color_pair(4))
            else:
                stdscr.addstr(start_y + i, x, line)
        except curses.error:
            pass
    
    stdscr.refresh()
    stdscr.getch()
    return True


def init_template_directories():
    """Create template directories with sample files"""
    # Get the directory where the script is located
    script_dir = Path(__file__).parent.absolute()
    templates_dir = script_dir / "templates"
    
    # Create directories and sample files if they don't exist
    samples = {
        "easy/01_basic.txt": [
            "# Easy Level - Basic Sentences",
            "",
            "The quick brown fox jumps over the lazy dog.",
            "She sells sea shells by the sea shore.",
            "Peter Piper picked a peck of pickled peppers.",
            "---",
            "How much wood would a woodchuck chuck?",
            "Betty Botter bought some butter.",
            "A proper cup of coffee from a proper copper coffee pot."
        ],
        "easy/02_tongue_twisters.txt": [
            "# Tongue Twisters",
            "",
            "She sells sea shells by the sea shore.",
            "Peter Piper picked a peck of pickled peppers.",
            "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
            "Betty Botter bought some butter but she said the butter's bitter.",
            "I saw Susie sitting in a shoeshine shop.",
            "Fuzzy Wuzzy was a bear. Fuzzy Wuzzy had no hair.",
            "Six slippery snails slid slowly seaward.",
            "Three free throws through three free trees.",
            "A proper cup of coffee from a proper copper coffee pot.",
            "I slit the sheet, the sheet I slit, and on the slitted sheet I sit.",
            "Unique New York, you need New York, you know you need unique New York.",
            "Red lorry, yellow lorry, red lorry, yellow lorry, red lorry, yellow lorry.",
            "Eleven benevolent elephants.",
            "Sheep should sleep in a shed.",
            "Silly Sally swiftly shooed seven silly sheep."
        ],
        "c_style/04_javascript.txt": [
            "# JavaScript/Node.js Examples",
            "",
            "// Async/Await example",
            "function delay(ms) {",
            "    return new Promise(resolve => setTimeout(resolve, ms));",
            "}",
            "",
            "async function fetchUserData(userId) {",
            "    console.log(`Fetching data for user ${userId}...`);",
            "    await delay(1000); // Simulate network delay",
            "    ",
            "    // Simulate API response",
            "    return {",
            "        id: userId,",
            "        name: \"John Doe\",",
            "        email: \"john@example.com\",",
            "        role: \"developer\"",
            "    };",
            "}",
            "",
            "async function processUsers() {",
            "    try {",
            "        let user1 = await fetchUserData(1);",
            "        let user2 = await fetchUserData(2);",
            "        ",
            "        console.log(\"User 1:\", user1);",
            "        console.log(\"User 2:\", user2);",
            "        ",
            "        let team = [user1, user2];",
            "        console.log(`Team has ${team.length} members`);",
            "    } catch (error) {",
            "        console.error(\"Error:\", error);",
            "    }",
            "}",
            "",
            "// Run the async function",
            "processUsers().then(() => console.log(\"Done!\"));",
            "---",
            "// Object-oriented JavaScript",
            "class Person {",
            "    constructor(name, age) {",
            "        this.name = name;",
            "        this.age = age;",
            "        this.hobbies = [];",
            "    }",
            "    ",
            "    addHobby(hobby) {",
            "        this.hobbies.push(hobby);",
            "    }",
            "    ",
            "    introduce() {",
            "        console.log(`Hi, I'm ${this.name} and I'm ${this.age} years old.`);",
            "        console.log(`My hobbies include: ${this.hobbies.join(', ')}`);",
            "    }",
            "    ",
            "    haveBirthday() {",
            "        this.age++;",
            "        console.log(`Happy Birthday! Now I'm ${this.age}`);",
            "    }",
            "}",
            "",
            "// Create and use Person objects",
            "let person = new Person(\"Bob\", 25);",
            "person.addHobby(\"reading\");",
            "person.addHobby(\"gaming\");",
            "person.addHobby(\"coding\");",
            "person.introduce();",
            "person.haveBirthday();"
        ]
    }
    
    for filepath, content in samples.items():
        full_path = templates_dir / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not full_path.exists():
            with open(full_path, 'w') as f:
                f.write('\n'.join(content))
            print(f"Created sample: {filepath}")

def main(stdscr):
    # Setup
    curses.curs_set(0)  # Hide cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    
    # Initialize template manager
    template_manager = TemplateManager()
    
    # Create sample files
    init_template_directories()
    
    while True:
        # Get terminal size
        height, width = stdscr.getmaxyx()
        
        # Check terminal size
        if height < 24 or width < 80:
            stdscr.clear()
            stdscr.addstr(0, 0, "Terminal too small! Please resize to at least 80x24.")
            stdscr.addstr(1, 0, f"Current: {width}x{height}")
            stdscr.addstr(2, 0, "Press any key...")
            stdscr.refresh()
            stdscr.getch()
            continue
        
        # Show menu and get category
        category = draw_menu(stdscr, height, width, template_manager)
        if category is None:
            break
        
        # Get templates for selected category
        templates = template_manager.get_random_templates(category, 2)  # Get 2 templates
        category_name = template_manager.category_names[category]
        
        # Initialize test
        test = TypingTest(category, templates)
        
        # Main typing loop
        while True:
            stdscr.clear()
            
            # Draw UI
            last_y = draw_content(stdscr, test, 3, width, height)
            draw_progress_bar(stdscr, test, last_y + 1, width)
            draw_status_bar(stdscr, height, width, test, category_name)
            draw_instructions(stdscr, height)
            
            stdscr.refresh()
            
            # Get user input
            key = stdscr.getch()
            
            # Handle escape key
            if key == 27:
                break
            
            # Handle backspace
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                if test.user_input:
                    test.user_input.pop()
            
            # Handle enter
            elif key in (curses.KEY_ENTER, 10, 13):
                if test.user_input and test.is_line_complete():
                    if test.submit_line():  # This now sets end_time automatically
                        draw_results(stdscr, height, width, test, category_name)
                        break
                elif test.user_input:
                    try:
                        stdscr.attron(curses.color_pair(3))
                        stdscr.addstr(height-4, 2, "Complete the line first!")
                        stdscr.attroff(curses.color_pair(3))
                        stdscr.refresh()
                    except:
                        pass
                    time.sleep(0.5)
            
            # Handle regular characters
            elif 32 <= key <= 126:
                current_line = test.get_current_line()
                if current_line and len(test.user_input) < len(current_line):
                    test.user_input.append(chr(key))

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)