from os import path
import time

d = path.dirname(__file__)
text  = open(path.join(d, 'data.txt'), encoding = 'utf-8').read()

thousand = ''

t = time.time()
start = int(round(t * 1000))
a = 0
for i in range(1000):
    thousand += text
    a += 1

f = open('new.txt', 'w')
f.write(thousand)
f.close()

t1 = time.time()
end = int(round(t1 * 1000))
print('\nUsed time: ' + str(end - start) + 'ms')

print('\n' + 'process time: ' + str(a))