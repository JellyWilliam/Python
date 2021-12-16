import codecs
import matplotlib.pyplot as plt

file = codecs.open('Patient.txt', encoding='utf-8')
i = 1
val1 = 'Фамилия; Имя; Отчество; Пол; Национальность; Рост; Вес; Дата рождения; Номер телефона; Домашний адрес; Номер больницы; Отделение; Номер медицинской карты; Диагноз; Группа крови.'.split('; ') 
val2 = []
val3 = []
for line in file:
    val2.append(i)
    val3.append(line.replace("\n", "").split('; '))
    i += 1
file.close()
   
fig, ax = plt.subplots(figsize=(len(val1),round(i/3))) 
ax.set_axis_off() 
table = ax.table(
    cellText = val3,  
    rowLabels = val2,  
    colLabels = val1, 
    rowColours = ["palegreen"] * len(val1),  
    colColours = ["palegreen"] * len(val1), 
    cellLoc = 'center',  
    loc = 'center')         

ax.axis("off")
table.auto_set_font_size(False)
table.set_fontsize(8)
ax.set_title('Пациенты', 
             fontweight ="bold") 
table.auto_set_column_width(col=list(range(len(val1))))
plt.show() 