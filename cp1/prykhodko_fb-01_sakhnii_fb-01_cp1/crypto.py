from math import log2
file = open('f_without_spaces.txt','r',encoding ="utf-8")
alphabet = [ 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
bygrams = [i+j for i in alphabet for j in alphabet]
alphabet_count = [0]*len(alphabet)
bygrams_count = [0]*len(bygrams)
bygrams_cross_count = [0]*len(bygrams)
all_letters = 0
all_bygrams = 0
all_bygrams_cross = 0
while 1:
    x = file.read(1)
    if not x:
        break
    alphabet_count[alphabet.index(x)] += 1
    all_letters += 1
file.seek(0)
while 1:
    x = file.read(2)
    if not x:
        break
    bygrams_count[bygrams.index(x)] += 1
    all_bygrams += 1
file.seek(0)
all_text = file.read() 
for i in range(len(all_text) - 1):
    x = all_text[i]+all_text[i+1]
    bygrams_cross_count[bygrams.index(x)] += 1
    all_bygrams_cross += 1

alphabet_poss = [i/all_letters for i in alphabet_count]
bygrams_poss = [i/all_bygrams for i in bygrams_count]
bygrams_cross_poss = [i/all_bygrams_cross for i in bygrams_cross_count]
answer = open("answer.txt","w")
#*****************
entropia_for_h1 = -sum([ i*log2(i) for i in alphabet_poss if i > 0 ])
redundancy_for_h1 = 1 - entropia_for_h1/log2(len(alphabet))
#*****************
entropia_for_h2 = -sum([ i*log2(i) for i in bygrams_poss if i > 0 ])/2
redundancy_for_h2 = 1 - entropia_for_h2/log2(len(alphabet))
#*****************
entropia_for_h2_cross = -sum([ i*log2(i) for i in bygrams_cross_poss if i > 0 ])/2
redundancy_for_h2_cross = 1 - entropia_for_h2_cross/log2(len(alphabet))
#*****************
for i in range(len(alphabet)):
    answer.write("\'" + alphabet[i] + "\'" + " " + str(alphabet_poss[i])+'\n')
answer.write("Entropia: "+str(entropia_for_h1)+'\n')
answer.write("Redundancy: "+str(redundancy_for_h1)+'\n')
#*****************
answer.write("\n"*30)
answer.write("For bigrams: \n")
for i in range(len(bygrams)):
    answer.write("\'" + bygrams[i] + "\'" + " " + str(bygrams_poss[i])+'\n')
answer.write("Entropia: "+str(entropia_for_h2)+'\n')
answer.write("Redundancy: "+str(redundancy_for_h2)+'\n')
#*****************
answer.write("\n"*30)
answer.write("For cross-bigrams: \n")
for i in range(len(bygrams)):
    answer.write("\'" + bygrams[i] + "\'" + " " + str(bygrams_cross_poss[i])+'\n')
answer.write("Entropia: "+str(entropia_for_h2_cross)+'\n')
answer.write("Redundancy: "+str(redundancy_for_h2_cross)+'\n')