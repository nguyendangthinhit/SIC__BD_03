def check(link):
    with open('links.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if link==line.strip():
                return "trùng rồi"
    return "oke" 
link=input()
print(check(link))

