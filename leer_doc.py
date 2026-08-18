import win32com.client as win32

word = win32.Dispatch('Word.Application')
word.Visible = False

try:
    doc = word.Documents.Open(r'c:\BotVisasEstudio\Plantilla_plan-empresa-CAST (5).doc')
    text = doc.Content.Text
    doc.Close(False)
finally:
    word.Quit()

with open(r'c:\BotVisasEstudio\plantilla_out.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print("Guardado OK, longitud:", len(text))
