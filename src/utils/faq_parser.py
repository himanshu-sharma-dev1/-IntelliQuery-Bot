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

