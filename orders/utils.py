def get_seq(n):
    if n < 1:
        return str(1).zfill(5)
    else:
        return str(n + 1).zfill(5)
