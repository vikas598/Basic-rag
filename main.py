from hr_assistant.pipeline import ask, build_hr_assistant

def main():
    print("Building the HR policy assistant...")
    agent = build_hr_assistant()
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

if __name__ == "__main__":
    main()
