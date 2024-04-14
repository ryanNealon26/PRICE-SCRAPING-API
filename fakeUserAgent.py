import random
def generate_agent():
    rand_first = random.randrange(0, 100)
    rand_second = random.randrange(0, 100)
    rand_third = random.randrange(0, 100)
    rand_four = random.randrange(0, 100)
    template = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{rand_four}.{rand_first}.{rand_second}.{rand_third} Safari/537.36"
    return template

def random_proxy():
    proxy_list = [
        "157.245.14.43",
        "101.230.172.86",
        "159.65.186.46",
        "190.110.226.162",
        "190.103.177.131"
    ]
    return random.choice(proxy_list)


