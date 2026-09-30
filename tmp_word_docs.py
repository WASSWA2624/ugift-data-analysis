import win32com.client

word = win32com.client.Dispatch("Word.Application")
print("docs", word.Documents.Count)
for index in range(1, word.Documents.Count + 1):
    doc = word.Documents(index)
    print(index, doc.Saved, doc.FullName)
