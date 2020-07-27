f = open("temp.txt", "r")
f2 = open("cards.txt", "w")

lines = f.readlines()
for i in range(1, 10):
    if i % 3 == 1:
        f2.write("<div class='card-deck'>\n")
    for line in lines:
        if "{{ " in line:
            line = line.replace("1 }}", str(i) + " }}")
        f2.write(line)
    if i % 3 == 0:
        f2.write("</div>\n")
        f2.write("<br>")
        f2.write("\n\n")
f.close()
f2.close()
