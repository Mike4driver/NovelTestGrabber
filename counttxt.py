
string = ""
with open("testtext.txt", "r") as f:
    string = f.read()

print(f"Word count of testtext: {len(string.split())}")