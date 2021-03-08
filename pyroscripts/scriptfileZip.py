import zipfile
import os


file_ls = os.listdir("public/csv")
file_name = []
existFile = os.path.isfile("public/result.zip")

if existFile is True :
    os.remove("public/result.zip")
    


for i in file_ls:
    i = "C:/Users/ojh21/OneDrive/바탕 화면/연구원/lastProject/kepco/public/csv/"+ i
    file_name.append(i)



with zipfile.ZipFile("public/result.zip", 'w') as my_zip:
    for i in file_name:
        my_zip.write(i)
    my_zip.close()

for i in file_name:
    os.remove(i)

