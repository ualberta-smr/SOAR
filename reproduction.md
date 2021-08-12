## What is undocumented
1. Requires a linux machine to reproduce. Reproduced in Ubuntu 20.04 desktop and SMR's server which is also Ubuntu 20.04.
2. The file http://nlp.stanford.edu/data/glove.6B.zip does not exist. I only tried TFIDF so did not face any problem regarding this.
3. Needed to install `runsolver`. Here is how.
   1. `git clone https://github.com/utpalbora/runsolver`
   2. Follow the README of runsolver to install
   3. `sudo apt install libnuma-dev`
   4. Add `runsolver/src` to PATH
4. `pip3 install sentencepiece`

# Results
I only tried the TF-IDF version of SOAR. I used 1 hour timeout and 64GB memory limit as the original authors.
The results are identical to the original one except for the following minor differences.

1. The synthesis time often varied a lot. For some the original was faster and for some mine was faster. 
2. `permute` took arguments in different order. But the end result is same, so it does not matter.
   1. Example: `x.permute(0,2,1)` vs `x.permute(0,1,2)`
3. The following differences were also observed
   1. alexnet
      1. line 15: has an additional `x.permute(0,1,2,3)`.
      2. last line: `Softmax(dim=-1)` instead of `Softmax(dim=1)`
   2. conv_for_text
      1. line 15: `MaxPool1d(2,stride=3,padding=1)` instead of `MaxPool1d(64,stride=3,padding=32)`
      2. line 16: `flatten(x,-2)` instead of `flatten(x,1)`
   3. conv_pool_softmax
      1. `Softmax(dim=None)` instead of `Softmax(dim=1)` 
   4. img_autoencoder
      1. line 11: `Conv2d(32,64,(3,3),stride=(3,3),padding=(0,0))` instead of `Conv2d(32,64,(3,3),stride=(1,1),padding=(0,0))` 
   5. vgg19
      1. line 66: `Softmax(dim=-1)` instead of `Softmax(dim=1)`
   6. line 10: `Embedding(2,1000)` instead of `Embedding(1,1000)`