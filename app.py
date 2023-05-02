from cvxpy_prj import cvxpy_func

def handler(event, context):  
    try:
        ret = cvxpy_func(m=event['m'], n=event['n'])
    except:
        print('set default value for m, n = 5, 3')
        ret = cvxpy_func(m=5, n=3)

    print(ret)
    return ret