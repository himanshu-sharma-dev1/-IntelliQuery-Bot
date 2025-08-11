import re

def parse_faq(file_path):
    """Parses the FAQ.md file and returns a dictionary of questions and answers."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return {}

    questions_answers = {}
    matches = re.findall(r'## (.*?)\n(.*?)(?=\n## |$)', content, re.DOTALL)

    for match in matches:
        question = match[0].strip()
        answer = match[1].strip()
        questions_answers[question] = answer

    return questions_answers

def write_faq(faq_data: dict, file_path: str):
    """Writes the FAQ data to the FAQ.md file, overwriting it."""
    with open(file_path, 'w', encoding='utf-8') as f:
        # Sort by question to maintain a consistent order
        for question, answer in sorted(faq_data.items()):
            f.write(f"## {question}\n")
            f.write(f"{answer}\n\n")
