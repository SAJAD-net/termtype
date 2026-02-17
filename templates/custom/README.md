# Custom Templates Directory

Add your own `.txt` files here to create custom typing practice sessions. The program will automatically load all templates from this directory.

## 📁 Directory Structure
```
templates/custom/
├── README.md           # This file
├── my_quotes.txt       # Your custom templates
├── work_emails.txt     # Work-related practice
├── code_snippets.txt   # Your own code examples
└── any_name.txt        # Any .txt file works!
```

## 📝 File Format

### Basic Template File
Each `.txt` file can contain multiple templates. Use `---` on a line by itself to separate templates.

```
# Lines starting with # are comments and will be ignored

This is my first typing template.
It can be any text I want to practice.

---

This is my second template.
It can be multiple lines long.
Perfect for practicing paragraphs.

---

# Third template with some code
def hello_world():
    print("Hello, World!")
    return True
```

### Template Examples

#### 1. Quotes Template (`my_quotes.txt`)
```
# My Favorite Quotes

The only limit to our realization of tomorrow is our doubts of today.
- Franklin D. Roosevelt

---

Life is what happens when you're busy making other plans.
- John Lennon

---

The future belongs to those who believe in the beauty of their dreams.
- Eleanor Roosevelt

---

Success is not final, failure is not fatal: it is the courage to continue that counts.
- Winston Churchill

---

The way to get started is to quit talking and begin doing.
- Walt Disney
```

#### 2. Work Emails Template (`work_emails.txt`)
```
# Common Work Email Phrases

Thank you for your email regarding the project deadline.
I will review the documents and get back to you by Friday.

---

Following up on our meeting yesterday, here are the action items:
1) Update the documentation
2) Review the code changes
3) Schedule the deployment

---

Please find attached the quarterly report for Q3 2024.
Let me know if you have any questions or need clarification.

---

The team meeting has been rescheduled to 2:30 PM on Wednesday.
We will discuss the budget and timeline for the new project.

---

I'm writing to confirm our appointment on March 15th at 10:00 AM.
Please let me know if this time still works for you.
```

#### 3. Code Snippets Template (`code_snippets.txt`)
```
# Python Code Examples

def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Test the function
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
---

# JavaScript Function
function calculateAverage(numbers) {
    const sum = numbers.reduce((acc, val) => acc + val, 0);
    return numbers.length ? sum / numbers.length : 0;
}

const scores = [85, 92, 78, 95, 88];
console.log(`Average: ${calculateAverage(scores)}`);
---

# SQL Query
SELECT 
    u.username,
    COUNT(o.id) as order_count,
    SUM(o.total_amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at >= '2024-01-01'
GROUP BY u.id
HAVING order_count > 5
ORDER BY total_spent DESC;
```

#### 4. Practice Words Template (`practice_words.txt`)
```
# Words I Want to Practice

entrepreneur
unanimously
idiosyncrasy
inconsequential
---

# Technical Terms
asynchronous
encapsulation
polymorphism
inheritance
abstraction
---

# Difficult Spellings
accommodate
embarrass
millennium
occasionally
separate
---

# Programming Terms
asynchronous
callback
closure
debounce
middleware
serialization
```

#### 5. Multi-line Paragraphs Template (`paragraphs.txt`)
```
# Long Paragraphs for Endurance Practice

The art of programming requires not only technical knowledge but also creativity and patience. A good programmer must be able to think logically while also considering the user experience and maintainability of their code. This balance between technical precision and creative problem-solving is what makes programming both challenging and rewarding.

---

In the world of technology, change is the only constant. New frameworks emerge, languages evolve, and best practices shift. Successful developers embrace this constant learning, viewing each new challenge as an opportunity to grow and improve their skills.

---

Effective communication is crucial in software development. Whether you're writing documentation, commenting your code, or explaining technical concepts to non-technical stakeholders, the ability to convey complex ideas clearly and concisely is invaluable.

---

The best code is not just code that works, but code that is readable, maintainable, and efficient. It tells a story to other developers who will read it in the future, making their job easier and reducing the likelihood of bugs and misunderstandings.
```

#### 6. Mixed Practice Template (`mixed_practice.txt`)
```
# Mix of Different Content Types

Regular sentence for warmup.
Numbers: 12345 67890
Special chars: !@#$%^&*()

---

def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
---

The quick brown fox jumps over 13 lazy dogs in 0.5 seconds!
Email: test@example.com
Phone: (555) 123-4567
Date: 2024-03-15
Time: 2:30 PM
URL: https://www.example.com
---

#include <stdio.h>
int main() {
    printf("Hello, C!\n");
    return 0;
}
```

## 🎯 Tips for Best Results

1. **Keep lines under 70 characters** - This ensures they display properly without wrapping
2. **Use only standard keyboard characters** - Avoid Unicode/emoji that might not display correctly
3. **Separate templates with `---`** - Each section between `---` becomes a separate typing test
4. **Use comments for notes** - Lines starting with `#` won't appear in the typing test
5. **Be consistent with indentation** - For code templates, maintain proper indentation (4 spaces recommended)

## 🚀 Quick Start

1. Create a new `.txt` file in this directory
2. Add your content (use the examples above as a guide)
3. Save the file
4. Run TermType and select "Custom Templates" from the menu
5. Start typing!

## 📚 Examples You Can Add

- Song lyrics you want to memorize
- Famous speeches or quotes
- Your own code snippets
- Work-related text you type often
- Foreign language practice
- Technical documentation
- Creative writing pieces
- Interview answers
- Presentation scripts

## ⚠️ Important Notes

- Files are loaded alphabetically
- Empty lines within templates are preserved
- Multiple templates in one file are randomly selected
- You can have as many `.txt` files as you want
- Changes take effect when you restart the program

Happy Typing! 🎉