from hr_assistant.pipeline import ask, build_hr_assistant
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def main():
    print("Building the HR policy assistant...")
    logger.info("====CLI run started====")
    agent = build_hr_assistant()
    logger.info("HR policy assistant built successfully")
    print("Assistant Ready!\n")

    demo_question = [
        "How many pain annual leave days do I get?",
        "What is the notice period during probation?",
        "Can I work from home every day?"
    ]

    for question in demo_question:
        print("="*60)
        print("QUESTIONS: ",question)
        print("."*60)
        answer = ask(agent, question)
        print("ANSWER :", answer)
        print("="*60)
        print()

        logger.info("====CLI run finished====")

if __name__ == "__main__":
    main()
