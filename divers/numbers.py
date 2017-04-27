from collections import defaultdict

class Trie:
    
    def __init__(self):
        self.root = defaultdict()

    def insert(self, word):
        current = self.root
        for letter in word:
            current = current.setdefault(letter, {})

# Now test the class

test = Trie()
n=int(input())
for i in range(n):
    test.insert(raw_input())
j=0
for i in str(test.root):
    try :
        i=int(i)
        j+=1
    except:pass
print(j)

