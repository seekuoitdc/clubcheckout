def row_major(alist, sublen):      
  return [alist[i:i+sublen] for i in range(0, len(alist), sublen)]

def col_major(alist, sublen):
  numrows = (len(alist)+sublen-1) // sublen 
  return [alist[i::sublen] for i in range(numrows)]
