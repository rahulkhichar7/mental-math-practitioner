from core.models import TestResult


class ReportGenerator:
    """Formats a completed test result for the terminal."""

    def print_report(self, result: TestResult) -> None:
        print("\n" + "-" * 72)
        print("FINAL REPORT")
        print("-" * 72)

        print(f"Total questions : {result.total_questions}")
        print(f"Correct         : {result.correct_count}")
        print(f"Incorrect       : {result.incorrect_count}")
        print(f"Accuracy        : {result.accuracy:.2f}%")
        print(f"Total time      : {result.total_time:.2f} s")
        print(f"Average time    : {result.average_time:.2f} s")
        print(f"Fastest         : {result.min_time:.2f} s")
        print(f"Slowest         : {result.max_time:.2f} s")

        wrong = [item for item in result.question_results if not item.is_correct]

        print("\nWRONG QUESTIONS")
        print("-" * 72)

        if not wrong:
            print("None. Excellent!")
        else:
            for index, item in enumerate(wrong, start=1):
                user_answer = (
                    str(item.user_answer)
                    if item.user_answer is not None
                    else "<invalid>"
                )

                print(f"{index}. {item.question.topic_path}")
                print(f"   Question : {item.question.text}")
                print(f"   Your ans : {user_answer}")
                print(f"   Correct   : {item.question.answer}")
                print(f"   Time      : {item.elapsed_seconds:.2f} s")

        print("-" * 72)
