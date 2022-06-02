import pickle

for cat in ['krealington', 'ksf', 'warble', 'ksf']:

    with open(f'./data/{cat}/history.p', 'rb') as f:
        x = pickle.load(f)
        for elem in x[-5:]:
            print(f'- {str(elem)}')
        answer = input('Do you want to remove the last one? [y/n]')
        print(len(x))
        if answer == 'y':
            del x[-1]
            
    with open(f'./data/{cat}/history.p', 'wb') as file:
        pickle.dumps(x, file)
        print(len(x))