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
        
        # Available quiz categories
        self.categories = {
            "General Knowledge": 9,
            "Books": 10,
            "Film": 11,
            "Music": 12,
            "Television": 14,
            "Video Games": 15,
            "Science & Nature": 17,
            "Computers": 18,
            "Mathematics": 19,
            "Sports": 21,
            "Geography": 22,
            "History": 23,
            "Animals": 27
        }
        
    def check_internet_connection(self) -> bool:
        """Check if internet connection is available"""
        try:
            response = requests.get("https://www.google.com", timeout=5)
            return True
        except:
            return False
    
    def fetch_questions(self, category: str, difficulty: str, num_questions: int) -> List[QuizQuestion]:
        """Fetch questions from Open Trivia Database API"""
        print("\nConnecting to quiz database...")
        
        if not self.check_internet_connection():
            print("ERROR: No internet connection detected!")
            print("Please check your network and try again.")
            return []
        
        category_id = self.categories.get(category, 9)
        
        try:
            url = f"{self.api_base_url}?amount={num_questions}&category={category_id}&difficulty={difficulty.lower()}&type=multiple"
            
            print("Fetching questions...")
            response = requests.get(url, timeout=15)
            
            if response.status_code != 200:
                print(f"ERROR: Server error (Status code: {response.status_code})")
                print("Please try again in a moment.")
                return []
            
            data = response.json()
            
            if data['response_code'] == 0:
                questions = []
                for item in data['results']:
                    try:
                        options = item['incorrect_answers'] + [item['correct_answer']]
                        random.shuffle(options)
                        correct_index = options.index(item['correct_answer'])
                        
                        question_text = html.unescape(item['question'])
                        options = [html.unescape(opt) for opt in options]
                        
                        questions.append(QuizQuestion(
                            question=question_text,
                            options=options,
                            correct_answer=correct_index,
                            category=category
                        ))
                    except Exception:
                        continue
                
                if not questions:
                    print("ERROR: No valid questions were retrieved!")
                    return []
                
                print(f"Successfully loaded {len(questions)} questions!\n")
                return questions
            
            elif data['response_code'] == 1:
                print("WARNING: Not enough questions available for this combination!")
                print("Try selecting fewer questions or a different difficulty level.")
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
        
        except Exception as e:
            print(f"ERROR: Unexpected error: {str(e)}")
            print("Please try restarting the application.")
            return []
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "=" * 60)
        print("                    QUIZ APPLICATION")
        print("=" * 60)
        print("\nPowered by Open Trivia Database")
        print("\nAvailable Categories:\n")
        
        categories_list = list(self.categories.keys())
        
        for i, category in enumerate(categories_list, 1):
            print(f"  {i:2d}. {category}")
        
        print(f"  {len(categories_list) + 1:2d}. Exit")
    
    def get_time_limit(self, difficulty: str) -> int:
        """Return time limit based on difficulty"""
        time_limits = {
            "easy": 15, 
            "medium": 20, 
            "hard": 30
        }
        return time_limits.get(difficulty.lower(), 20)
    
    def get_user_input_with_timeout(self, prompt: str, timeout: int) -> Optional[str]:
        """Get user input with timeout"""
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
    
    def validate_numeric_input(self, prompt: str, min_val: int, max_val: int) -> Optional[int]:
        """Validate numeric input"""
        while True:
            try:
                user_input = input(prompt).strip()
                
                if not user_input.isdigit():
                    print(f"Please enter a number between {min_val} and {max_val}")
                    continue
                
                value = int(user_input)
                
                if min_val <= value <= max_val:
                    return value
                else:
                    print(f"Please enter a number between {min_val} and {max_val}")
                    
            except KeyboardInterrupt:
                print("\n\nCancelled by user")
                return None
            except Exception:
                print("Invalid input. Please try again.")
    
    def run_quiz(self, category: str, difficulty: str, num_questions: int):
        """Run the quiz"""
        try:
            questions = self.fetch_questions(category, difficulty, num_questions)
            
            if not questions:
                print("\nCould not load questions.")
                input("\nPress Enter to return to main menu...")
                return
            
            self.score = 0
            self.total_questions = len(questions)
            time_limit = self.get_time_limit(difficulty)
            
            print("\n" + "=" * 60)
            print(f"Category: {category}")
            print(f"Difficulty: {difficulty.upper()}")
            print(f"Time per question: {time_limit} seconds")
            print(f"Total questions: {self.total_questions}")
            print("=" * 60 + "\n")
            
            input("Press Enter to start the quiz...")
            
            for i, question in enumerate(questions, 1):
                print(f"\n{'-' * 60}")
                print(f"Question {i}/{self.total_questions}")
                print("-" * 60)
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
                    print(f"INCORRECT! Correct answer: {question.options[question.correct_answer]}")
                    continue
                
                if answer and answer.strip().isdigit():
                    user_answer = int(answer.strip()) - 1
                    
                    if 0 <= user_answer < len(question.options):
                        if user_answer == question.correct_answer:
                            self.score += 1
                            print(f"CORRECT! Time taken: {elapsed_time:.1f} seconds")
                        else:
                            print(f"INCORRECT! Correct answer: {question.options[question.correct_answer]}")
                    else:
                        print(f"Invalid option! Correct answer: {question.options[question.correct_answer]}")
                else:
                    print(f"Invalid input! Correct answer: {question.options[question.correct_answer]}")
                
                time.sleep(1.5)
            
            self.display_results()
            
        except KeyboardInterrupt:
            print("\n\nQuiz interrupted by user")
            print(f"Current score: {self.score}/{i if 'i' in locals() else 0}")
            input("\nPress Enter to continue...")
        except Exception as e:
            print(f"\nAn error occurred during the quiz: {str(e)}")
            print("Returning to main menu...")
            input("\nPress Enter to continue...")
    
    def display_results(self):
        """Display quiz results"""
        accuracy = (self.score / self.total_questions) * 100
        
        print("\n" + "=" * 60)
        print("                   QUIZ COMPLETED!")
        print("=" * 60)
        print(f"\nFinal Score: {self.score}/{self.total_questions}")
        print(f"Accuracy: {accuracy:.2f}%")
        print("-" * 60)
        
        if accuracy == 100:
            print("PERFECT SCORE! Outstanding!")
        elif accuracy >= 80:
            print("Excellent work! Great performance!")
        elif accuracy >= 60:
            print("Good job! Well done!")
        elif accuracy >= 40:
            print("Fair effort! Keep practicing!")
        else:
            print("Keep studying! You'll improve!")
        
        print("=" * 60 + "\n")
    
    def start(self):
        """Main application loop"""
        print("\nWelcome to the Interactive Quiz Game!")
        print("Test your knowledge across multiple categories.\n")
        
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
                    len(categories_list) + 1
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
                    3
                )
                
                if diff_choice is None:
                    continue
                
                difficulty_map = {1: "easy", 2: "medium", 3: "hard"}
                difficulty = difficulty_map[diff_choice]
                
                num_questions = self.validate_numeric_input(
                    "\nHow many questions? (1-20): ",
                    1,
                    20
                )
                
                if num_questions is None:
                    continue
                
                self.run_quiz(selected_category, difficulty, num_questions)
                
                play_again = input("\nPlay again? (y/n): ").strip().lower()
                if play_again != 'y':
                    print("\nThanks for playing! Goodbye!")
                    break
                    
            except KeyboardInterrupt:
                print("\n\nApplication interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nUnexpected error: {str(e)}")
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
        print(f"\nFatal error: {str(e)}")
        print("Please restart the application.")
        sys.exit(1)