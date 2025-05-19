from llm import setup_llm, ask


def main():
    print("Welcome!")
    setup_llm()

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "q"]:
            print("See you later!")
            break

        response = ask(user_input)
        print(f"Response: {response}")


if __name__ == "__main__":
    main()
