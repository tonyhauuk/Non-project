import pandas as pd

filePath = './website.csv'

content = pd.read_csv(filePath, delimiter=',', encoding='utf8')
# print(content)

head = [' 网址 ', ' 英文名称 ', ' 中文拼音 ', ' number ', ' 真假 ']
head1 = ['', 'https://www.google.com', 'google', 'gu ge', '3', 'true']
# data = content.to_csv(filePath, columns=head1, mode='a', index=False)
# print(content.describe())
print(content.info())

for i in range(100):
    print(i)