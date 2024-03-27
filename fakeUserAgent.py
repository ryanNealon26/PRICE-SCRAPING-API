import random

def generate_agent():
    rand_first = random.randrange(0, 100)
    rand_second = random.randrange(0, 100)
    rand_third = random.randrange(0, 100)
    rand_four = random.randrange(0, 100)
    template = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.{rand_first}.{rand_second}.{rand_third} Safari/537.36"
    return template