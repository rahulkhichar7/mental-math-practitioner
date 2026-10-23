from cli.console import ConsoleCLI
from core.session import TestSession
from distribution.distributor import QuestionDistributor
from reporting.report import ReportGenerator
from topics.registry import TopicRegistry


class MentalMathApplication:

    def __init__(self) -> None:
        self.registry = TopicRegistry()
        self.distributor = QuestionDistributor()
        self.cli = ConsoleCLI(self.registry)
        self.session = TestSession()
        self.reporter = ReportGenerator()

    def run(self) -> None:
        """Run one complete practice session."""
        self.cli.show_welcome()

        selected_nodes = self.cli.select_topics()
        total_questions = self.cli.ask_question_count()

        allocation = self.distributor.allocate_question_counts(
            selected_nodes=selected_nodes,
            total_questions=total_questions,
        )

        self.cli.show_distribution(allocation)
        self.cli.wait_for_start()

        questions = self.registry.create_questions(allocation)
        results = self.session.run(questions)

        self.reporter.print_report(results)

if __name__ == "__main__":
    app = MentalMathApplication()
    app.run()