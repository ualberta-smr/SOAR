So, far we have analyzed [271 repositories](repositories.txt) that uses PyTorch.
The goal was to see whether it is possible to find the reshaping API's used in SOAR (`view`, `permute`, `long`) 
in real client projects.

We found that SOAR only migrates the _model_ classes.
Therefore, we first detected model classes and analyzed them only.
Model classes inherit from `Module` class and has an `__init__` and a `forward` method.

Below is an example from SOAR's result. The results do not produce the actual program 
but this is what the program would look like.

```python
# Original Tensorflow code
def __init__(self, **kwargs):
    self.conv = tf.keras.layers.Conv2D(3, 3, strides=(1, 1))
    self.pool = tf.keras.layers.MaxPool2D(2, 2)

def call(self, x):
    x = self.conv(x)
    x = self.pool(x)
    return x
```

```python
# Migrated to PyTorch
def __init__(self):
    self.v1 = lambda x: x.permute(0,3,1,2)
    self.v2 = torch.nn.Conv2d(1,3,(3,3),stride=(1,1),padding=(0,0))
    self.v3 = torch.nn.MaxPool2d((2,2),stride=(2,2),padding=(0,0))

def forward(self, x):
    x = self.v1(x)
    x = self.v2(x)
    x = self.v3(x)
    return x
```
We could not find any usages of `view`, `permute` and `long` in the `__init__` methods of the model classes.
Therefore, we concluded that we cannot automatically find the reshaping APIs.

However, we then looked into some client code manually and figured that the reshaping APIs are typically used directly inside the 
forward methods. For example, the PyTorch code above will likely be as below.

```python
def __init__(self):
    self.v2 = torch.nn.Conv2d(1,3,(3,3),stride=(1,1),padding=(0,0))
    self.v3 = torch.nn.MaxPool2d((2,2),stride=(2,2),padding=(0,0))

def forward(self, x):
    x = x.permute(0,3,1,2)
    x = self.v2(x)
    x = self.v3(x)
    return x
```

So, we now tried to see which APIs are used in the `forward` but not in `__init__`.
For this we extracted all method calls in the forward method,
and discarded the ones that are not from one of the variables assigned in the `__init__`.
In the example above, we see that `permute`, `v2` and `v3` are the method calls in `forward` 
and `v2` and `v3` are initialized in `__init__`.
Therefore, we conclude that `permute` is a reshaping API.

We run this analysis on all 271 client repositories and logged the reshaping API usages.
The detail results can be found 
[in this spreadsheet](https://docs.google.com/spreadsheets/d/1x-5H1rUOKBbwJQLSwPPbmcPZlDpK4FelMvusVYig9dU/edit#gid=1167016238).
The `diffs` tab has all the occurrences and the `diffs_summary` tab has the frequency and other stats.
The top 23 out of 2714 APIs accounts for 50% occurrences. `view`, `permute` and `long` rank 1st, 9th and 63rd respectively.

Now, we can replace use the top ranked APIs as SOAR's reshaping API to see whether SOAR can synthesize properly.
