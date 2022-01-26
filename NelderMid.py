

def func(x):
    return (1-x[0])**2+100*(x[1]-x[0]**2)**2

def sort(x,f):
    k=1
    while k>0:
        k=0
        for i in range(len(f)-1):
            if f[i]>f[i+1]:
                temp=f[i]
                f[i]=f[i+1]
                f[i+1]=temp
                temp=x[i]
                x[i]=x[i+1]
                x[i+1]=temp
                k+=1

def get_param(f, fct):
    param = 0
    for fi in f:
        param += (fi - fct) ** 2
    param /= len(f)
    param = param ** 0.5
    return param

def get_ct(x):
    xct = []
    for i in x[0]:
        xct.append(0)
    for i in range(len(x)-1):
        for j in range(len(x[0])):
            xct[j] += x[i][j]
    for i in range(len(xct)):
        xct[i]/=(len(x)-1)
    return xct

def NM(x0,alpha=1,beta=2,gamma=-0.5,sigma=0.5,e=0.00001):
    f = []
    for xi in x0:
        f.append(func(xi))
    sort(x0, f)
    xct = get_ct(x0)
    fct = func(xct)
    param = get_param(f, fct)
    while param > e:
        xl = x0[0]
        xg = x0[len(x0)-2]
        xh = x0[len(x0) - 1]
        fl = f[0]
        fg = f[len(x0)-2]
        fh = f[len(x0) - 1]
        xotr = []
        for i in range(len(xct)):
            xotr.append(xct[i]+alpha*(xct[i]-xh[i]))
        fotr = func(xotr)

        if fotr <= fl:
            xrast = []
            for i in range(len(xct)):
                xrast.append(xct[i] + beta * (xct[i] - xh[i]))
            frast = func(xrast)
            if frast<fl:
                f.remove(fh)
                x0.remove(xh)
                f.append(frast)
                x0.append(xrast)
            else:
                f.remove(fh)
                x0.remove(xh)
                f.append(fotr)
                x0.append(xotr)
        elif (fotr > fg) and (fotr <= fh):
            xsgat = []
            for i in range(len(xct)):
                xsgat.append(xct[i] + gamma * (xct[i] - xh[i]))
            fsgat = func(xsgat)
            f.remove(fh)
            x0.remove(xh)
            f.append(fsgat)
            x0.append(xsgat)
        elif (fotr > fl) and (fotr <= fg):
            f.remove(fh)
            x0.remove(xh)
            f.append(fotr)
            x0.append(xotr)
        elif fotr > fh:
            for i in range(1, len(x0)):
                for j in range(len(x0[i])):
                    x0[i][j] = xl[j]+sigma*(x0[i][j]-xl[j])
            f = []
            for xi in x0:
                f.append(func(xi))
        sort(x0, f)
        xct = get_ct(x0)
        fct = func(xct)
        param = get_param(f, fct)
    return x0[0]


