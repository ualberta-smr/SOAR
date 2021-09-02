from inspect import getmembers, isfunction

import torch

if __name__ == '__main__':
    apis = filter(lambda api: not api.startswith('_'), map(lambda m: m[0], getmembers(torch.Tensor, isfunction)))
    print('=== with inspect ===')
    print(*list(apis), sep='\n')

    print('\n=== with dir ===')
    apis = filter(lambda api: not api.startswith('_'), dir(torch.Tensor))
    print(*list(apis), sep='\n')
