def read_file(file_name):
    sents = []
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for idx, l in enumerate(lines):
            if l[0] == ';' and lines[idx + 1][0] == '$':
                this_sent = []
            elif l[0] == '$' and lines[idx - 1][0] == ';':
                continue
            elif l[0] == '\n':
                sents.append(this_sent)
            else:
                this_sent.append(tuple(l.split()))
    except:
        try:
            with open(file_name, 'r', encoding='cp949') as f:
                lines = f.readlines()
                for idx, l in enumerate(lines):
                    if l[0] == ';' and lines[idx + 1][0] == '$':
                        this_sent = []
                    elif l[0] == '$' and lines[idx - 1][0] == ';':
                        continue
                    elif l[0] == '\n':
                        sents.append(this_sent)
                    else:
                        this_sent.append(tuple(l.split()))
        except:
            pass
    return sents