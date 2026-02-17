from enum import Enum

class Category(Enum):
    EASY = "easy"
    MEDIUM = "medium" 
    HARD = "hard"
    PYTHON = "python"
    CSTYLE = "c_style"
    PRACTICE = "practice"
    CUSTOM = "custom"

CATEGORY_NAMES = {
    Category.EASY: "Easy Sentences",
    Category.MEDIUM: "Medium (with numbers)",
    Category.HARD: "Hard (complex punctuation)",
    Category.PYTHON: "Python Code",
    Category.CSTYLE: "C/Java/JavaScript",
    Category.PRACTICE: "Practice (common mistakes)",
    Category.CUSTOM: "Custom Templates"
}

DEFAULT_TEMPLATE_COUNT = 5
MIN_TERMINAL_HEIGHT = 24
MIN_TERMINAL_WIDTH = 80
WPM_HISTORY_SECONDS = 10