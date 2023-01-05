def h_count(text_with_frequencies): #рахуємо ентропію
    h = 0
    all_frequencies = []
    for i in text_with_frequencies:
        all_frequencies.append(text_with_frequencies[i])
    for i in all_frequencies:
        h += round(-i * math.log2(i), 3)
    return h