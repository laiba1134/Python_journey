import time
import random
import json
from typing import List, Optional
import threading
import requests
import html
import sys

class QuizQuestion:
    def __init__(self, question: str, options: List[str], correct_answer: int, category: str):
        self.question = question
        self.options = options
        self.correct_answer = correct_answer
        self.category = category

class QuizApp:
    def __init__(self):
        self.score = 0
        self.total_questions = 0
        self.timeout_occurred = False
        self.api_base_url = "https://opentdb.com/api.php"
        
        # Expanded categories with IDs from Open Trivia Database
        self.categories = {
            "General Knowledge": 9,
            "Books": 10,
            "Film": 11,
            "Music": 12,
            "Musicals & Theatres": 13,
            "Television": 14,
            "Video Games": 15,
            "Board Games": 16,
            "Science & Nature": 17,
            "Computers": 18,
            "Mathematics": 19,
            "Mythology": 20,
            "Sports": 21,
            "Geography": 22,
            "History": 23,
            "Politics": 24,
            "Art": 25,
            "Celebrities": 26,
            "Animals": 27,
            "Vehicles": 28,
            "Comics": 29,
            "Gadgets": 30,
            "Japanese Anime & Manga": 31,
            "Cartoon & Animations": 32
        }
        
    def check_internet_connection(self) -> bool:
        """Check if internet connection is available"""
        try:
            response = requests.get("https://www.google.com", timeout=5)
            return True
        except:
            return False
    
    def validate_api_availability(self) -> bool:
        """Check if Open Trivia API is available"""
        try:
            response = requests.get("https://opentdb.com/api_category.php", timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def fetch_questions(self, category: str, difficulty: str, num_questions: int) -> List[QuizQuestion]:
        """Fetch questions from Open Trivia Database API with comprehensive error handling"""
        print("\nConnecting to quiz database...")
        
        # Check internet connection first
        if not self.check_internet_connection():
            print("ERROR: No internet connection detected!")
            print("Please check your network and try again.")
            return []
        
        # Check API availability
        if not self.validate_api_availability():
            print("ERROR: Quiz database is currently unavailable!")
            print("The service might be under maintenance. Please try again later.")
            return []
        
        category_id = self.categories.get(category, 9)
        
        try:
            # Build API URL with parameters
            url = f"{self.api_base_url}?amount={num_questions}&category={category_id}&difficulty={difficulty.lower()}&type=multiple"
            
            print("Fetching questions...")
            response = requests.get(url, timeout=15)
            
            # Check HTTP status
            if response.status_code != 200:
                print(f"ERROR: Server error (Status code: {response.status_code})")
                print("Please try again in a moment.")
                return []
            
            data = response.json()
            
            # Handle API response codes
            if data['response_code'] == 0:
                # Success
                questions = []
                for item in data['results']:
                    try:
                        # Combine correct and incorrect answers
                        options = item['incorrect_answers'] + [item['correct_answer']]
                        random.shuffle(options)
                        correct_index = options.index(item['correct_answer'])
                        
                        # Decode HTML entities
                        question_text = html.unescape(item['question'])
                        options = [html.unescape(opt) for opt in options]
                        
                        questions.append(QuizQuestion(
                            question=question_text,
                            options=options,
                            correct_answer=correct_index,
                            category=category
                        ))
                    except Exception as e:
                        print(f"WARNING: Skipped a malformed question")
                        continue
                
                if not questions:
                    print("ERROR: No valid questions were retrieved!")
                    return []
                
                print(f"Successfully loaded {len(questions)} questions!")
                return questions
            
            elif data['response_code'] == 1:
                print("WARNING: Not enough questions available for this combination!")
                print(f"Try one of these:")
                print(f"   - Select fewer questions (try 5-10)")
                print(f"   - Choose a different difficulty level")
                print(f"   - Pick a different category")
                return []
            
            elif data['response_code'] == 2:
                print("ERROR: Invalid parameters sent to the API")
                print("Please restart the app and try again.")
                return []
            
            elif data['response_code'] == 3:
                print("ERROR: Session token error")
                print("Please restart the app.")
                return []
            
            elif data['response_code'] == 4:
                print("WARNING: All questions for this category have been used!")
                print("Try selecting a different category or difficulty.")
                return []
            
            else:
                print(f"ERROR: Unknown API response code: {data['response_code']}")
                return []
            
        except requests.exceptions.Timeout:
            print("ERROR: Request timed out!")
            print("Your connection might be slow. Please try again.")
            return []
        
        except requests.exceptions.ConnectionError:
            print("ERROR: Connection error occurred!")
            print("Please check your internet connection.")
            return []
        
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Network error: {str(e)}")
            print("Please check your connection and try again.")
            return []
        
        except json.JSONDecodeError:
            print("ERROR: Invalid response from server!")
            print("The API might be experiencing issues. Try again later.")
            return []
        
        except KeyError as e:
            print(f"ERROR: Unexpected response format: Missing {str(e)}")
            print("Please try again or contact support.")
            return []
        
        except Exception as e:
            print(f"ERROR: Unexpected error: {str(e)}")
            print("Please try restarting the application.")
            return []
    
    def display_menu(self):
        """Display main menu with organized categories"""
        print("\n" + "="*70)
        print(" "*20 + "QUIZ APPLICATION")
        print("="*70)
        print("\nPowered by Open Trivia Database - Thousands of Questions!")
        
        print("\nAvailable Categories:\n")
        
        # Group categories for better readability
        categories_list = list(self.categories.keys())
        
        # Display in two columns
        mid_point = (len(categories_list) + 1) // 2
        for i in range(mid_point):
            left_idx = i
            right_idx = i + mid_point
            
            left = f"  {left_idx + 1:2d}. {categories_list[left_idx]:<25}"
            
            if right_idx < len(categories_list):
                right = f"{right_idx + 1:2d}. {categories_list[right_idx]}"
                print(f"{left} {right}")
            else:
                print(left)
        
        print(f"\n  {len(categories_list) + 1:2d}. Exit")
    
    def get_time_limit(self, difficulty: str) -> int:
        """Return time limit based on difficulty"""
        time_limits = {
            "easy": 15, 
            "medium": 20, 
            "hard": 30
        }
        return time_limits.get(difficulty.lower(), 20)
    
    def get_user_input_with_timeout(self, prompt: str, timeout: int) -> Optional[str]:
        """Get user input with timeout using threading"""
        self.timeout_occurred = False
        user_input = [None]
        
        def get_input():
            try:
                user_input[0] = input(prompt)
            except:
                pass
        
        input_thread = threading.Thread(target=get_input)
        input_thread.daemon = True
        input_thread.start()
        input_thread.join(timeout)
        
        if input_thread.is_alive():
            self.timeout_occurred = True
            print("\n\nTime's up! Moving to next question...")
            return None
        
        return user_input[0]
    
    def validate_numeric_input(self, prompt: str, min_val: int, max_val: int, allow_cancel: bool = False) -> Optional[int]:
        """Validate numeric input with error handling"""
        while True:
            try:
                user_input = input(prompt).strip()
                
                if allow_cancel and user_input.lower() in ['cancel', 'c', 'back', 'b']:
                    return None
                
                if not user_input.isdigit():
                    print(f"ERROR: Please enter a number between {min_val} and {max_val}")
                    continue
                
                value = int(user_input)
                
                if min_val <= value <= max_val:
                    return value
                else:
                    print(f"ERROR: Please enter a number between {min_val} and {max_val}")
                    
            except KeyboardInterrupt:
                print("\n\nCancelled by user")
                return None
            except Exception as e:
                print(f"ERROR: Invalid input. Please try again.")
    
    def run_quiz(self, category: str, difficulty: str, num_questions: int):
        """Run the quiz with comprehensive error handling"""
        try:
            questions = self.fetch_questions(category, difficulty, num_questions)
            
            if not questions:
                print("\nERROR: Could not load questions.")
                input("\nPress Enter to return to main menu...")
                return
            
            self.score = 0
            self.total_questions = len(questions)
            time_limit = self.get_time_limit(difficulty)
            
            print(f"\n{'='*70}")
            print(f"Category: {category}")
            print(f"Difficulty: {difficulty.upper()}")
            print(f"Time per question: {time_limit} seconds")
            print(f"Total questions: {self.total_questions}")
            print(f"{'='*70}\n")
            
            ready = input("Press Enter to start the quiz (or 'c' to cancel): ").strip().lower()
            if ready == 'c':
                print("Quiz cancelled.")
                return
            
            for i, question in enumerate(questions, 1):
                print(f"\n{'─'*70}")
                print(f"Question {i}/{self.total_questions}")
                print(f"{'─'*70}")
                print(f"\n{question.question}\n")
                
                for j, option in enumerate(question.options):
                    print(f"  {j + 1}. {option}")
                
                start_time = time.time()
                answer = self.get_user_input_with_timeout(
                    f"\nYour answer (1-{len(question.options)}): ", 
                    time_limit
                )
                elapsed_time = time.time() - start_time
                
                if self.timeout_occurred:
                    print(f"INCORRECT: Time's up! Correct answer: {question.options[question.correct_answer]}")
                    continue
                
                if answer and answer.strip().isdigit():
                    user_answer = int(answer.strip()) - 1
                    
                    if 0 <= user_answer < len(question.options):
                        if user_answer == question.correct_answer:
                            self.score += 1
                            print(f"CORRECT! Time: {elapsed_time:.1f}s")
                        else:
                            print(f"INCORRECT! Correct answer: {question.options[question.correct_answer]}")
                    else:
                        print(f"INCORRECT: Invalid option! Correct answer: {question.options[question.correct_answer]}")
                else:
                    print(f"INCORRECT: Invalid input! Correct answer: {question.options[question.correct_answer]}")
                
                time.sleep(1.5)
            
            self.display_results()
            
        except KeyboardInterrupt:
            print("\n\nWARNING: Quiz interrupted by user")
            print(f"Current score: {self.score}/{i if 'i' in locals() else 0}")
            input("\nPress Enter to continue...")
        except Exception as e:
            print(f"\nERROR: An error occurred during the quiz: {str(e)}")
            print("Returning to main menu...")
            input("\nPress Enter to continue...")
    
    def display_results(self):
        """Display quiz results with detailed feedback"""
        accuracy = (self.score / self.total_questions) * 100
        
        print(f"\n{'='*70}")
        print(" "*25 + "QUIZ COMPLETED!")
        print(f"{'='*70}")
        print(f"\nFinal Score: {self.score}/{self.total_questions}")
        print(f"Accuracy: {accuracy:.2f}%")
        print(f"{'─'*70}")
        
        # Performance feedback
        if accuracy == 100:
            print("PERFECT SCORE! Absolutely phenomenal!")
        elif accuracy >= 80:
            print("Excellent work! You're a quiz master!")
        elif accuracy >= 60:
            print("Good job! Solid performance!")
        elif accuracy >= 40:
            print("Fair effort! Keep studying!")
        else:
            print("Keep practicing! You'll improve!")
        
        print(f"{'='*70}\n")
    
    def start(self):
        """Main application loop with error handling"""
        print("\nWelcome to the Interactive Quiz Game!")
        print("Test your knowledge across 24 different categories!\n")
        
        # Check initial connection
        if not self.check_internet_connection():
            print("WARNING: No internet connection detected!")
            print("This app requires internet to fetch questions.\n")
            retry = input("Press Enter to retry or 'q' to quit: ").strip().lower()
            if retry == 'q':
                return
        
        while True:
            try:
                self.display_menu()
                
                categories_list = list(self.categories.keys())
                choice = self.validate_numeric_input(
                    f"\nSelect a category (1-{len(categories_list) + 1}): ",
                    1,
                    len(categories_list) + 1,
                    allow_cancel=True
                )
                
                if choice is None:
                    continue
                
                if choice == len(categories_list) + 1:
                    print("\nThank you for playing! Goodbye!")
                    break
                
                selected_category = categories_list[choice - 1]
                
                print("\nSelect Difficulty Level:")
                print("  1. Easy   (15 seconds per question)")
                print("  2. Medium (20 seconds per question)")
                print("  3. Hard   (30 seconds per question)")
                
                diff_choice = self.validate_numeric_input(
                    "\nYour choice (1-3): ",
                    1,
                    3,
                    allow_cancel=True
                )
                
                if diff_choice is None:
                    continue
                
                difficulty_map = {1: "easy", 2: "medium", 3: "hard"}
                difficulty = difficulty_map[diff_choice]
                
                num_questions = self.validate_numeric_input(
                    "\nHow many questions? (1-50): ",
                    1,
                    50,
                    allow_cancel=True
                )
                
                if num_questions is None:
                    continue
                
                self.run_quiz(selected_category, difficulty, num_questions)
                
                play_again = input("\nPlay again? (y/n): ").strip().lower()
                if play_again != 'y':
                    print("\nThanks for playing! Come back soon!")
                    break
                    
            except KeyboardInterrupt:
                print("\n\nApplication interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nERROR: Unexpected error: {str(e)}")
                print("Returning to main menu...")
                time.sleep(2)

if __name__ == "__main__":
    try:
        quiz_app = QuizApp()
        quiz_app.start()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nERROR: Fatal error: {str(e)}")
        print("Please restart the application.")
        sys.exit(1)