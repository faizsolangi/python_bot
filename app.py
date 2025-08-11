#!/usr/bin/env python3
"""
Python Adventure for Kids - Single File Version
Interactive Python learning platform for children aged 6-12
Perfect for deployment on Render, Heroku, or any Python hosting service
"""

import streamlit as st
import json
import sys
import io
import traceback
import contextlib
import ast
import types
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import math
from streamlit_ace import st_ace

# ===== LESSON DATA =====
LESSONS_DATA = {
    "lessons": [
        {
            "id": 1,
            "title": "Hello, Python World!",
            "description": "Learn your first Python commands and say hello to the world!",
            "difficulty": "Beginner",
            "content": [
                {
                    "type": "text",
                    "content": "Welcome to Python! Python is like having a conversation with your computer. When we want to show something on the screen, we use a special command called `print()`."
                },
                {
                    "type": "code_example",
                    "code": "print(\"Hello, World!\")",
                    "explanation": "This tells the computer to display the message 'Hello, World!' on the screen."
                },
                {
                    "type": "text",
                    "content": "You can print anything you want! Try printing your name, your favorite color, or even fun emoji! 🎉"
                },
                {
                    "type": "interactive_demo",
                    "code": "print(\"My name is Python!\")\nprint(\"I love helping kids learn! 🐍\")\nprint(\"Let's be friends! 😊\")"
                }
            ],
            "exercises": [
                {
                    "id": "ex_1_1",
                    "type": "code_completion",
                    "question": "Write a program that prints your name and says hello!",
                    "template": "# Write your code here!\n# Use print() to say hello and tell us your name\n\n",
                    "expected_output": "Hello",
                    "hint": "Use print(\"Hello, my name is [your name]!\")"
                },
                {
                    "id": "ex_1_2",
                    "type": "multiple_choice",
                    "question": "Which command do we use to show text on the screen?",
                    "options": ["show()", "display()", "print()", "write()"],
                    "correct_answer": "print()",
                    "explanation": "The print() function is used to display text and other information on the screen!"
                }
            ]
        },
        {
            "id": 2,
            "title": "Variables - Your Computer's Memory!",
            "description": "Learn how to store information in variables, like boxes that remember things!",
            "difficulty": "Beginner",
            "content": [
                {
                    "type": "text",
                    "content": "Variables are like magical boxes that can store information! You can put numbers, words, or even True/False in these boxes and use them later. Think of them as labels for your stuff!"
                },
                {
                    "type": "code_example",
                    "code": "name = \"Alice\"\nage = 10\nis_student = True",
                    "explanation": "Here we created three variables: 'name' stores text, 'age' stores a number, and 'is_student' stores True or False."
                },
                {
                    "type": "text",
                    "content": "Once you store something in a variable, you can use it anywhere in your code! It's like having a name tag for your data."
                },
                {
                    "type": "interactive_demo",
                    "code": "favorite_animal = \"🐶 Dog\"\nfavorite_number = 7\n\nprint(f\"My favorite animal is: {favorite_animal}\")\nprint(f\"My favorite number is: {favorite_number}\")\nprint(f\"Together they make: {favorite_animal} #{favorite_number}\")"
                }
            ],
            "exercises": [
                {
                    "id": "ex_2_1",
                    "type": "code_completion",
                    "question": "Create variables for your favorite things and print them!",
                    "template": "# Create variables for your favorite color, food, and hobby\n# Then print them out!\n\nfavorite_color = \nfavorite_food = \nfavorite_hobby = \n\n# Print your favorites here!\n",
                    "expected_output": "color",
                    "hint": "Remember to put text in quotes like \"blue\" and use print() to display your variables!"
                }
            ]
        },
        {
            "id": 3,
            "title": "Numbers and Math Magic!",
            "description": "Discover how Python can be your super calculator!",
            "difficulty": "Beginner",
            "content": [
                {
                    "type": "text",
                    "content": "Python is amazing at math! It can add, subtract, multiply, divide, and even do more complex calculations. Let's explore how Python handles numbers!"
                },
                {
                    "type": "code_example",
                    "code": "# Basic math operations\nprint(5 + 3)  # Addition\nprint(10 - 4)  # Subtraction\nprint(6 * 7)   # Multiplication\nprint(15 / 3)  # Division",
                    "explanation": "Python uses +, -, *, and / for basic math operations, just like a calculator!"
                },
                {
                    "type": "text",
                    "content": "You can also use variables in math! This makes your calculations much more flexible and reusable."
                },
                {
                    "type": "interactive_demo",
                    "code": "apples = 12\noranges = 8\ntotal_fruits = apples + oranges\n\nprint(f\"I have {apples} apples\")\nprint(f\"I have {oranges} oranges\")\nprint(f\"In total, I have {total_fruits} fruits! 🍎🍊\")"
                }
            ],
            "exercises": [
                {
                    "id": "ex_3_1",
                    "type": "code_completion",
                    "question": "Create a program that calculates the total cost of your favorite snacks!",
                    "template": "# Let's go shopping for snacks!\nchocolate_price = 2.50\ncookies_price = 3.00\njuice_price = 1.75\n\n# Calculate the total cost\ntotal_cost = \n\nprint(f\"Chocolate costs: ${chocolate_price}\")\nprint(f\"Cookies cost: ${cookies_price}\")\nprint(f\"Juice costs: ${juice_price}\")\nprint(f\"Total cost: ${}\")",
                    "expected_output": "7.25",
                    "hint": "Add all the prices together: chocolate_price + cookies_price + juice_price"
                }
            ]
        },
        {
            "id": 4,
            "title": "Lists - Collections of Awesome Things!",
            "description": "Learn how to store multiple items in lists and work with them!",
            "difficulty": "Beginner",
            "content": [
                {
                    "type": "text",
                    "content": "Lists are like treasure chests that can hold many items! You can store your favorite colors, friends' names, or even numbers in a list. Lists are super useful for organizing information!"
                },
                {
                    "type": "code_example",
                    "code": "# Creating lists\ncolors = [\"red\", \"blue\", \"green\", \"yellow\"]\nnumbers = [1, 5, 10, 15, 20]\nmixed_list = [\"Alice\", 12, True, \"Python\"]",
                    "explanation": "Lists are created using square brackets [ ] and items are separated by commas. You can mix different types of data in one list!"
                },
                {
                    "type": "text",
                    "content": "You can access individual items in a list using their position (starting from 0). You can also add new items or find out how many items are in your list!"
                },
                {
                    "type": "interactive_demo",
                    "code": "favorite_animals = [\"🐶\", \"🐱\", \"🐰\", \"🐸\", \"🦋\"]\n\nprint(f\"My favorite animals: {favorite_animals}\")\nprint(f\"My #1 favorite is: {favorite_animals[0]}\")\nprint(f\"I have {len(favorite_animals)} favorite animals\")\n\n# Add a new favorite\nfavorite_animals.append(\"🐢\")\nprint(f\"Now I have {len(favorite_animals)} favorites!\")"
                }
            ],
            "exercises": [
                {
                    "id": "ex_4_1",
                    "type": "code_completion",
                    "question": "Create a list of your favorite subjects and display information about it!",
                    "template": "# Create a list of your favorite school subjects\nfavorite_subjects = []\n\n# Print the list\nprint(f\"My favorite subjects: {}\")\n\n# Print the first subject\nprint(f\"My most favorite subject is: {}\")\n\n# Print how many subjects you have\nprint(f\"I have {} favorite subjects\")",
                    "expected_output": "subjects",
                    "hint": "Fill in your favorite subjects like ['Math', 'Art', 'Science'] and use the list variable in the print statements!"
                }
            ]
        },
        {
            "id": 5,
            "title": "Loops - Doing Things Over and Over!",
            "description": "Learn how to repeat actions easily with loops!",
            "difficulty": "Beginner",
            "content": [
                {
                    "type": "text",
                    "content": "Sometimes we want to do the same thing many times. Instead of writing the same code over and over, we can use loops! Loops are like telling your computer: 'Do this action multiple times!'"
                },
                {
                    "type": "code_example",
                    "code": "# A simple for loop\nfor i in range(5):\n    print(f\"This is round number {i + 1}!\")",
                    "explanation": "This loop runs 5 times, printing a message each time. The variable 'i' counts from 0 to 4."
                },
                {
                    "type": "text",
                    "content": "You can also loop through lists! This lets you do something with each item in your list automatically."
                },
                {
                    "type": "interactive_demo",
                    "code": "fruits = [\"🍎\", \"🍌\", \"🍊\", \"🍇\"]\n\nprint(\"Welcome to the fruit parade!\")\nfor fruit in fruits:\n    print(f\"Here comes a delicious {fruit}!\")\n\nprint(\"The parade is over! 🎉\")"
                }
            ],
            "exercises": [
                {
                    "id": "ex_5_1",
                    "type": "code_completion",
                    "question": "Create a loop that prints a countdown from 10 to 1, then says 'Blast off!'",
                    "template": "# Countdown loop\nprint(\"Starting countdown...\")\n\nfor i in range(10, 0, -1):\n    print()\n\nprint(\"🚀 Blast off!\")",
                    "expected_output": "Blast off",
                    "hint": "Inside the loop, print the variable 'i' to show each countdown number!"
                }
            ]
        }
    ]
}

# ===== CODE EXECUTOR CLASS =====
class CodeExecutor:
    def __init__(self):
        self.safe_modules = {
            'math': math,
            'random': random,
            'datetime': datetime,
            'json': json,
            'pandas': pd,
            'plotly': {
                'graph_objects': go,
                'express': px
            }
        }
        
        # Safe built-in functions
        self.safe_builtins = {
            'print': print,
            'len': len,
            'range': range,
            'str': str,
            'int': int,
            'float': float,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'set': set,
            'bool': bool,
            'abs': abs,
            'max': max,
            'min': min,
            'sum': sum,
            'sorted': sorted,
            'reversed': reversed,
            'enumerate': enumerate,
            'zip': zip,
            'map': map,
            'filter': filter,
            'round': round,
            'type': type,
            'isinstance': isinstance,
            'hasattr': hasattr,
            'getattr': getattr,
        }
    
    def execute_code(self, code, timeout=5):
        """Execute Python code safely and return results"""
        if not code.strip():
            return {
                'success': True,
                'output': '',
                'error': None,
                'plots': []
            }
        
        # Create a safe execution environment
        safe_globals = {
            '__builtins__': self.safe_builtins,
            'pd': pd,
            'px': px,
            'go': go,
        }
        
        # Add safe modules
        safe_globals.update(self.safe_modules)
        
        # Capture stdout
        old_stdout = sys.stdout
        stdout_capture = io.StringIO()
        
        plots_created = []
        
        try:
            # Check for dangerous operations
            if self._is_code_safe(code):
                sys.stdout = stdout_capture
                
                # Parse and compile the code
                parsed_code = ast.parse(code)
                compiled_code = compile(parsed_code, '<user_code>', 'exec')
                
                # Create a local namespace
                local_namespace = {}
                
                # Execute the code
                exec(compiled_code, safe_globals, local_namespace)
                
                # Capture any plots that were created
                plots_created = self._extract_plots(local_namespace, safe_globals)
                
                output = stdout_capture.getvalue()
                
                return {
                    'success': True,
                    'output': output,
                    'error': None,
                    'plots': plots_created
                }
                
        except SyntaxError as e:
            return {
                'success': False,
                'output': '',
                'error': f"Syntax Error: {str(e)}",
                'plots': []
            }
        except Exception as e:
            error_message = f"{type(e).__name__}: {str(e)}"
            # Provide kid-friendly error messages
            error_message = self._make_error_kid_friendly(error_message)
            
            return {
                'success': False,
                'output': stdout_capture.getvalue(),
                'error': error_message,
                'plots': []
            }
        finally:
            sys.stdout = old_stdout
    
    def _is_code_safe(self, code):
        """Check if code contains potentially dangerous operations"""
        dangerous_keywords = [
            'import os', 'import sys', 'import subprocess',
            'open(', 'file(', 'exec(', 'eval(',
            '__import__', 'globals()', 'locals()',
            'input(', 'raw_input('
        ]
        
        code_lower = code.lower()
        for keyword in dangerous_keywords:
            if keyword in code_lower:
                return False
        
        return True
    
    def _extract_plots(self, local_namespace, global_namespace):
        """Extract any plotly figures that were created"""
        plots = []
        
        # Check both local and global namespaces for plotly figures
        all_vars = {**global_namespace, **local_namespace}
        
        for var_name, var_value in all_vars.items():
            if hasattr(var_value, 'show') and hasattr(var_value, 'data'):
                plots.append(var_value)
        
        return plots
    
    def _make_error_kid_friendly(self, error_message):
        """Convert technical error messages to kid-friendly ones"""
        friendly_messages = {
            'NameError': "Oops! It looks like you're using a word that Python doesn't recognize. Make sure you've spelled everything correctly!",
            'SyntaxError': "There's a small mistake in how you wrote your code. Check for missing quotes, parentheses, or colons!",
            'IndentationError': "Python is very picky about spacing! Make sure your code lines up properly.",
            'TypeError': "You're trying to mix different types of data in a way that doesn't work. Check if you're using numbers and text correctly!",
            'ValueError': "The value you're using isn't quite right for what you're trying to do. Double-check your numbers and text!",
            'ZeroDivisionError': "Whoops! You can't divide by zero - even computers can't do that math trick!",
            'IndexError': "You're trying to access an item in a list that doesn't exist. Remember, lists start counting from 0!",
        }
        
        for error_type, friendly_msg in friendly_messages.items():
            if error_message.startswith(error_type):
                return f"{friendly_msg}\n\nTechnical details: {error_message}"
        
        return f"Something went wrong, but don't worry - debugging is part of learning! 🐛\n\nTechnical details: {error_message}"

# ===== LESSON MANAGER CLASS =====
class LessonManager:
    def __init__(self):
        self.lessons = LESSONS_DATA.get('lessons', [])
    
    def get_all_lessons(self):
        """Get all available lessons"""
        return self.lessons
    
    def get_lesson(self, lesson_id):
        """Get a specific lesson by ID"""
        for lesson in self.lessons:
            if lesson['id'] == lesson_id:
                return lesson
        return None

# ===== PROGRESS TRACKER CLASS =====
class ProgressTracker:
    def __init__(self):
        self.user_progress = self._get_default_progress()
        self.badges = self._initialize_badges()
    
    def _get_default_progress(self):
        """Get default progress structure"""
        return {
            "user_name": "",
            "completed_lessons": [],
            "completed_exercises": [],
            "total_stars": 0,
            "current_streak": 0,
            "lesson_history": [],
            "badges": [],
            "last_active": ""
        }
    
    def _initialize_badges(self):
        """Define all available badges"""
        return {
            "first_lesson": {
                "name": "First Steps",
                "description": "Completed your first lesson!",
                "emoji": "👶",
                "condition": lambda progress: len(progress['completed_lessons']) >= 1
            },
            "three_lessons": {
                "name": "Getting Started",
                "description": "Completed 3 lessons!",
                "emoji": "🚀",
                "condition": lambda progress: len(progress['completed_lessons']) >= 3
            },
            "five_lessons": {
                "name": "Dedicated Learner",
                "description": "Completed 5 lessons!",
                "emoji": "📚",
                "condition": lambda progress: len(progress['completed_lessons']) >= 5
            },
            "star_collector": {
                "name": "Star Collector",
                "description": "Earned 10 stars!",
                "emoji": "⭐",
                "condition": lambda progress: progress['total_stars'] >= 10
            }
        }
    
    def set_user(self, name):
        """Set the user name"""
        self.user_progress['user_name'] = name
        self._update_last_active()
    
    def get_progress(self):
        """Get current progress"""
        return self.user_progress.copy()
    
    def complete_lesson(self, lesson_id):
        """Mark a lesson as completed"""
        if lesson_id not in self.user_progress['completed_lessons']:
            self.user_progress['completed_lessons'].append(lesson_id)
            self.user_progress['total_stars'] += 1
            
            # Add to history
            self.user_progress['lesson_history'].append({
                'lesson_id': lesson_id,
                'completed_at': datetime.now().isoformat(),
                'stars_earned': 1
            })
            
            self._update_streak()
            return True
        return False
    
    def complete_exercise(self, lesson_id, exercise_id):
        """Mark an exercise as completed"""
        exercise_key = f"ex_{lesson_id}_{exercise_id}"
        if exercise_key not in self.user_progress['completed_exercises']:
            self.user_progress['completed_exercises'].append(exercise_key)
            self.user_progress['total_stars'] += 1
            self._update_last_active()
            return True
        return False
    
    def _update_streak(self):
        """Update the learning streak"""
        today = datetime.now().date()
        last_active_str = self.user_progress.get('last_active', '')
        
        if last_active_str:
            try:
                last_active = datetime.fromisoformat(last_active_str).date()
                days_diff = (today - last_active).days
                
                if days_diff == 1:
                    self.user_progress['current_streak'] += 1
                elif days_diff == 0:
                    pass
                else:
                    self.user_progress['current_streak'] = 1
            except ValueError:
                self.user_progress['current_streak'] = 1
        else:
            self.user_progress['current_streak'] = 1
    
    def _update_last_active(self):
        """Update last active timestamp"""
        self.user_progress['last_active'] = datetime.now().isoformat()
    
    def check_badges(self):
        """Check for newly earned badges"""
        earned_badge_names = [badge['name'] for badge in self.user_progress['badges']]
        new_badges = []
        
        for badge_id, badge_info in self.badges.items():
            if badge_info['name'] not in earned_badge_names:
                if badge_info['condition'](self.user_progress):
                    new_badge = {
                        'id': badge_id,
                        'name': badge_info['name'],
                        'description': badge_info['description'],
                        'emoji': badge_info['emoji'],
                        'earned_at': datetime.now().strftime("%Y-%m-%d")
                    }
                    self.user_progress['badges'].append(new_badge)
                    new_badges.append(new_badge)
        
        return new_badges

# ===== STREAMLIT APPLICATION =====

# Configure page
st.set_page_config(
    page_title="🐍 Python Adventure for Kids",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'progress_tracker' not in st.session_state:
    st.session_state.progress_tracker = ProgressTracker()
if 'lesson_manager' not in st.session_state:
    st.session_state.lesson_manager = LessonManager()
if 'code_executor' not in st.session_state:
    st.session_state.code_executor = CodeExecutor()
if 'current_lesson_id' not in st.session_state:
    st.session_state.current_lesson_id = 1
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'playground_history' not in st.session_state:
    st.session_state.playground_history = []

# ===== PAGE FUNCTIONS =====

def display_lesson_content(lesson):
    """Display the main lesson content"""
    st.markdown(f"## {lesson['title']}")
    st.markdown(f"**{lesson['description']}**")
    
    # Lesson content sections
    for section in lesson['content']:
        if section['type'] == 'text':
            st.markdown(section['content'])
        elif section['type'] == 'code_example':
            st.markdown("### 💡 Example:")
            st.code(section['code'], language='python')
            if section.get('explanation'):
                st.markdown(f"**What this does:** {section['explanation']}")
        elif section['type'] == 'interactive_demo':
            st.markdown("### 🎯 Try it yourself:")
            demo_code = section['code']
            result = st.session_state.code_executor.execute_code(demo_code)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.code(demo_code, language='python')
            with col2:
                st.markdown("**Output:**")
                if result['success']:
                    st.success(result['output'])
                else:
                    st.error(result['error'])

def display_exercise(exercise):
    """Display and handle lesson exercises"""
    st.markdown("---")
    st.markdown("### 🎮 Practice Exercise")
    st.markdown(f"**{exercise['question']}**")
    
    if exercise['type'] == 'code_completion':
        st.markdown("Complete the code below:")
        user_code = st_ace(
            value=exercise['template'],
            language='python',
            theme='github',
            key=f"exercise_{st.session_state.current_lesson_id}_{exercise['id']}",
            height=200,
            auto_update=True
        )
        
        if st.button("🔍 Check My Code", type="primary", key=f"check_{exercise['id']}"):
            result = st.session_state.code_executor.execute_code(user_code)
            
            if result['success']:
                expected_output = exercise.get('expected_output', '')
                if expected_output.strip() in result['output'].strip():
                    st.success("🎉 Excellent work! You got it right!")
                    st.balloons()
                    st.session_state.progress_tracker.complete_exercise(
                        st.session_state.current_lesson_id, 
                        exercise['id']
                    )
                else:
                    st.warning(f"Almost there! Expected output: `{expected_output}`")
                    st.info(f"Your output: `{result['output']}`")
            else:
                st.error("Oops! There's an error in your code:")
                st.error(result['error'])
                if exercise.get('hint'):
                    st.info(f"💡 Hint: {exercise['hint']}")
    
    elif exercise['type'] == 'multiple_choice':
        options = exercise['options']
        user_answer = st.radio("Choose the correct answer:", options, key=f"mc_{exercise['id']}")
        
        if st.button("Submit Answer", type="primary", key=f"submit_{exercise['id']}"):
            if user_answer == exercise['correct_answer']:
                st.success("🎉 Correct! Well done!")
                st.balloons()
                st.session_state.progress_tracker.complete_exercise(
                    st.session_state.current_lesson_id, 
                    exercise['id']
                )
            else:
                st.error("Not quite right. Try again!")
                if exercise.get('explanation'):
                    st.info(f"💡 {exercise['explanation']}")

def show_home_page():
    """Display the home page"""
    st.title("🐍 Python Adventure for Kids")
    st.markdown("### Welcome to the most fun way to learn Python!")
    
    # User name input
    if not st.session_state.user_name:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("#### 👋 What's your name, young coder?")
            name = st.text_input("Enter your name:", placeholder="Type your name here...")
            if st.button("Start My Python Adventure! 🚀", type="primary"):
                if name:
                    st.session_state.user_name = name
                    st.session_state.progress_tracker.set_user(name)
                    st.rerun()
                else:
                    st.error("Please enter your name to start!")
    else:
        # Welcome message
        st.markdown(f"### 🎉 Welcome back, {st.session_state.user_name}!")
        
        # Progress overview
        progress_data = st.session_state.progress_tracker.get_progress()
        total_lessons = len(st.session_state.lesson_manager.get_all_lessons())
        completed_lessons = len(progress_data.get('completed_lessons', []))
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🏆 Lessons Completed", f"{completed_lessons}/{total_lessons}")
        with col2:
            st.metric("⭐ Total Stars", progress_data.get('total_stars', 0))
        with col3:
            st.metric("🏅 Badges Earned", len(progress_data.get('badges', [])))
        with col4:
            completion_rate = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
            st.metric("📈 Progress", f"{completion_rate:.0f}%")
        
        # Progress bar
        st.progress(completion_rate / 100)
        
        # Quick navigation
        st.markdown("---")
        st.markdown("### 🎯 What would you like to do today?")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 📚 Learn Python
            Start with lessons and learn Python step by step!
            """)
            if st.button("Go to Lessons 📖", key="lessons_btn", type="primary"):
                st.session_state.current_page = "lessons"
                st.rerun()
        
        with col2:
            st.markdown("""
            #### 🎮 Code Playground  
            Experiment with Python code in a safe environment!
            """)
            if st.button("Open Playground 🎮", key="playground_btn", type="primary"):
                st.session_state.current_page = "playground"
                st.rerun()
        
        with col3:
            st.markdown("""
            #### 🏆 View Progress
            See your achievements, badges, and completed lessons!
            """)
            if st.button("Check Progress 📊", key="progress_btn", type="primary"):
                st.session_state.current_page = "progress"
                st.rerun()

def show_lessons_page():
    """Display the lessons page"""
    st.title("📚 Python Lessons")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🏠 Home"):
            st.session_state.current_page = "home"
            st.rerun()
    
    # Get all lessons
    lessons = st.session_state.lesson_manager.get_all_lessons()
    progress_data = st.session_state.progress_tracker.get_progress()
    completed_lessons = progress_data.get('completed_lessons', [])
    
    # Sidebar for lesson navigation
    st.sidebar.title("📋 Lesson Menu")
    
    for lesson in lessons:
        is_completed = lesson['id'] in completed_lessons
        is_available = lesson['id'] == 1 or (lesson['id'] - 1) in completed_lessons
        
        if is_completed:
            emoji = "✅"
        elif is_available:
            emoji = "▶️"
        else:
            emoji = "🔒"
        
        button_label = f"{emoji} Lesson {lesson['id']}: {lesson['title']}"
        
        if is_available:
            if st.sidebar.button(button_label, key=f"lesson_{lesson['id']}"):
                st.session_state.current_lesson_id = lesson['id']
                st.rerun()
        else:
            st.sidebar.button(button_label, disabled=True, key=f"lesson_{lesson['id']}_disabled")
    
    # Display current lesson
    current_lesson = st.session_state.lesson_manager.get_lesson(st.session_state.current_lesson_id)
    
    if current_lesson:
        # Progress indicator
        lesson_progress = (st.session_state.current_lesson_id - 1) / len(lessons)
        st.progress(lesson_progress)
        st.markdown(f"**Progress: Lesson {st.session_state.current_lesson_id} of {len(lessons)}**")
        
        # Display lesson content
        display_lesson_content(current_lesson)
        
        # Display exercises
        if 'exercises' in current_lesson:
            for exercise in current_lesson['exercises']:
                display_exercise(exercise)
        
        # Lesson completion
        st.markdown("---")
        if st.session_state.current_lesson_id not in completed_lessons:
            if st.button("✨ I've completed this lesson!", type="primary", key="complete_lesson"):
                st.session_state.progress_tracker.complete_lesson(st.session_state.current_lesson_id)
                st.success("🎉 Lesson completed! You earned a star! ⭐")
                st.balloons()
                
                # Check for badges
                badges = st.session_state.progress_tracker.check_badges()
                for badge in badges:
                    st.success(f"🏅 New Badge Earned: {badge['name']} - {badge['description']}")
                
                st.rerun()
        else:
            st.success("✅ You've completed this lesson!")

def show_playground_page():
    """Display the playground page"""
    st.title("🎮 Code Playground")
    st.markdown("### 🚀 Experiment with Python code safely!")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🏠 Home"):
            st.session_state.current_page = "home"
            st.rerun()
    
    # Code examples in sidebar
    st.sidebar.title("📚 Code Examples")
    st.sidebar.markdown("Click on any example to try it!")
    
    examples = {
        "🌟 Hello World": '''print("Hello, World!")
print("My name is Python!")
print("I love coding! 🚀")''',
        
        "🎨 Fun with Variables": '''# Let's create some variables!
name = "Alice"
age = 10
favorite_color = "blue"

print(f"Hi! My name is {name}")
print(f"I am {age} years old")
print(f"My favorite color is {favorite_color}")''',
        
        "🔢 Math Magic": '''# Python can do math!
x = 10
y = 5

print(f"{x} + {y} = {x + y}")
print(f"{x} - {y} = {x - y}")
print(f"{x} * {y} = {x * y}")
print(f"{x} / {y} = {x / y}")''',
        
        "🌈 Colorful Loop": '''# Let's make a rainbow!
colors = ["red", "orange", "yellow", "green", "blue", "purple"]

for color in colors:
    print(f"🌈 {color} is beautiful!")
    
print("What a wonderful rainbow!")'''
    }
    
    for title, code in examples.items():
        if st.sidebar.button(title, key=f"example_{title}"):
            st.session_state.current_code = code
            st.rerun()
    
    # Main playground area
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### ✏️ Write your Python code here:")
        
        # Get initial code
        initial_code = st.session_state.get('current_code', '''# Welcome to the Python Playground! 🎮
# Write your code here and click "Run Code" to see what happens!

print("Hello, young coder! 👋")
print("Let's have some fun with Python!")

# Try changing this message:
message = "Python is awesome!"
print(message)
''')
        
        # Code editor
        user_code = st_ace(
            value=initial_code,
            language='python',
            theme='github',
            key="playground_editor",
            height=400,
            auto_update=True,
            wrap=True,
            font_size=14
        )
        
        # Control buttons
        col_a, col_b = st.columns([1, 1])
        
        with col_a:
            run_button = st.button("🚀 Run Code", type="primary")
        
        with col_b:
            if st.button("🗑️ Clear"):
                st.session_state.current_code = "# Start coding here! 🎉\n"
                st.rerun()
    
    with col2:
        st.markdown("#### 📺 Output:")
        
        if run_button and user_code.strip():
            # Execute the code
            with st.spinner("Running your code... 🔄"):
                result = st.session_state.code_executor.execute_code(user_code)
            
            if result['success']:
                if result['output']:
                    st.success("✅ Code ran successfully!")
                    st.text_area("Output:", value=result['output'], height=300, disabled=True)
                    
                    # Check if there are any plots to display
                    if result.get('plots'):
                        st.markdown("#### 📊 Plots:")
                        for plot in result['plots']:
                            st.plotly_chart(plot, use_container_width=True)
                else:
                    st.info("Code ran successfully, but no output to display.")
            else:
                st.error("❌ Oops! There's an error in your code:")
                st.code(result['error'], language='text')
                
                # Provide helpful hints for common errors
                error_msg = result['error'].lower()
                if 'indentationerror' in error_msg:
                    st.info("💡 **Hint:** Check your indentation! Python is picky about spaces and tabs.")
                elif 'syntaxerror' in error_msg:
                    st.info("💡 **Hint:** Check your syntax! Make sure parentheses, quotes, and colons are balanced.")
                elif 'nameerror' in error_msg:
                    st.info("💡 **Hint:** Make sure all variable names are spelled correctly and defined before use.")
        
        elif not user_code.strip():
            st.info("✏️ Write some code and click 'Run Code' to see the magic happen!")
        
        else:
            st.info("👆 Click 'Run Code' to execute your Python code!")

def show_progress_page():
    """Display the progress page"""
    st.title("🏆 My Python Learning Progress")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🏠 Home"):
            st.session_state.current_page = "home"
            st.rerun()
    
    # Check if user has started learning
    progress_data = st.session_state.progress_tracker.get_progress()
    
    if not progress_data.get('user_name'):
        st.warning("👋 You haven't started your Python journey yet!")
        if st.button("🚀 Go to Home Page"):
            st.session_state.current_page = "home"
            st.rerun()
        return
    
    st.markdown(f"### Welcome back, {progress_data['user_name']}! 👋")
    
    # Overall statistics
    lessons = st.session_state.lesson_manager.get_all_lessons()
    completed_lessons = progress_data.get('completed_lessons', [])
    total_stars = progress_data.get('total_stars', 0)
    badges = progress_data.get('badges', [])
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        completion_rate = (len(completed_lessons) / len(lessons) * 100) if lessons else 0
        st.metric(
            label="📚 Course Progress", 
            value=f"{completion_rate:.1f}%",
            delta=f"{len(completed_lessons)}/{len(lessons)} lessons"
        )
    
    with col2:
        st.metric(
            label="⭐ Total Stars", 
            value=total_stars,
            delta="Keep learning!"
        )
    
    with col3:
        st.metric(
            label="🏅 Badges Earned", 
            value=len(badges),
            delta="Unlock more!"
        )
    
    with col4:
        streak = progress_data.get('current_streak', 0)
        st.metric(
            label="🔥 Learning Streak", 
            value=f"{streak} days",
            delta="Keep it up!"
        )
    
    # Badges section
    if badges:
        st.markdown("---")
        st.markdown("### 🏅 My Badge Collection")
        
        # Display badges in a grid
        badge_cols = st.columns(min(len(badges), 4))
        
        for i, badge in enumerate(badges):
            with badge_cols[i % 4]:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px; border: 2px solid #FFD700; border-radius: 10px; margin: 10px;">
                    <div style="font-size: 3em;">{badge['emoji']}</div>
                    <div style="font-weight: bold; margin-top: 10px;">{badge['name']}</div>
                    <div style="font-size: 0.9em; color: #666;">{badge['description']}</div>
                </div>
                """, unsafe_allow_html=True)

# ===== MAIN APPLICATION =====

def main():
    """Main application logic"""
    # Sidebar navigation
    st.sidebar.title("🐍 Navigation")
    
    # Page navigation buttons
    if st.sidebar.button("🏠 Home", key="nav_home"):
        st.session_state.current_page = "home"
        st.rerun()
    
    if st.sidebar.button("📚 Lessons", key="nav_lessons"):
        st.session_state.current_page = "lessons"
        st.rerun()
    
    if st.sidebar.button("🎮 Playground", key="nav_playground"):
        st.session_state.current_page = "playground"
        st.rerun()
    
    if st.sidebar.button("🏆 Progress", key="nav_progress"):
        st.session_state.current_page = "progress"
        st.rerun()
    
    # Display current page
    if st.session_state.current_page == "home":
        show_home_page()
    elif st.session_state.current_page == "lessons":
        show_lessons_page()
    elif st.session_state.current_page == "playground":
        show_playground_page()
    elif st.session_state.current_page == "progress":
        show_progress_page()

if __name__ == "__main__":
    main()