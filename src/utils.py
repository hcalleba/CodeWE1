def sq_dist(x1, y1, x2, y2):
    """
    Returns the square of the distance between two points (x1, y1) and (x2, y2).
    """
    return (x1 - x2)**2 + (y1 - y2)**2

def getIdxF(l, f):
    """
    Get the index of the first element in l that satisfies f.
    Parameters:
    l (list): The list to search in.
    f (function): The function to check. (typically min or max)
    """
    return f(range(len(l)), key=l.__getitem__)