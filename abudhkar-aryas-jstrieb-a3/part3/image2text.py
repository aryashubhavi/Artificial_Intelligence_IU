#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: Jacob Striebel (jstrieb), Aishwarya Budhkar (abudhkar), Shubhavi Aryas (aryas)
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import os
import math

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25
CHARACTER_SIZE= CHARACTER_WIDTH * CHARACTER_HEIGHT

test_gold= {
  'test-0-0.png' :'SUPREME COURT OF THE UNITED STATES',
  'test-1-0.png' :'Certiorari to the United States Court of Appeals for the Sixth Circuit',
  'test-2-0.png' :'Nos. 14-556. Argued April 28, 2015 - Decided June 26, 2015',
  'test-3-0.png' :'Together with No. 14-562, Tanco et al. v. Haslam, Governor of',
  'test-4-0.png' :'Tennessee, et al., also on centiorari to the same court.',
  'test-5-0.png' :'Opinion of the Court',
  'test-6-0.png' :'As some of the petitioners in these cases demonstrate, marriage',
  'test-7-0.png' :'embodies a love that may endure even past death.',
  'test-8-0.png' :'It would misunderstand these men and women to say they disrespect',
  'test-9-0.png' :'the idea of marriage.',
  'test-10-0.png':'Their plea is that they do respect it, respect it so deeply that',
  'test-11-0.png':'they seek to find its fulfillment for themselves.',
  'test-12-0.png':'Their hope is not to be condemned to live in loneliness,',
  'test-13-0.png':'excluded from one of civilization\'s oldest institutions.',
  'test-14-0.png':'They ask for equal dignity in the eyes of the law.',
  'test-15-0.png':'The Constitution grants them that right.',
  'test-16-0.png':'The judgement of the Court of Appeals for the Sixth Circuit is reversed.',
  'test-17-0.png':'It is so ordered.',
  'test-18-0.png':'KENNEDY, J., delivered the opinion of the Court, in which',
  'test-19-0.png':'GINSBURG, BREYER, SOTOMAYOR, and KAGAN, JJ., joined.'
}

def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    print(im.size)
    print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    global TRAIN_LETTERS
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

def likelihood(gold_letters, emission_letter):
  diff= list()
  for _, gl in gold_letters.items():
    diff.append(0)
    assert len(gl)==len(emission_letter)
    for i in range(len(gl)):
      assert len(gl[i])==len(emission_letter[i])
      for j in range(len(gl[i])):
        if gl[i][j]!=emission_letter[i][j]:
          diff[-1]+= 1
  return diff

def predict_simple(gold_letters, emission_letters):
  simple= ['~' for letter in emission_letters]
  for i, emission in enumerate(emission_letters):
    least_diff= float('inf')
    differences= likelihood(gold_letters, emission)
    for j, diff in enumerate(differences):
      if diff < least_diff:
        least_diff= diff
        simple[i]= TRAIN_LETTERS[j]
  return simple

class HMM:
  
  def train(self, sentences):
    self.A= dict()
    self.Pi= dict()
    for q0 in TRAIN_LETTERS:
      self.A[q0]= dict()
      self.Pi[q0]= 1E-4
      for q1 in TRAIN_LETTERS:
        self.A[q0][q1]= 1E-8
    for sent in sentences:
      self.Pi[sent[0]]+= 1
      for q0, q1 in zip(sent[:-1], sent[1:]):
        self.A[q0][q1]+= 1
    normPi= math.log2( sum(self.Pi.values()) )
    for q in self.Pi.keys():
      self.Pi[q]= math.log2( self.Pi[q] ) - normPi
    for q0 in self.A.keys():
      normA= math.log2( sum(self.A[q0].values()) )
      for q1 in self.A[q0].keys():
        self.A[q0][q1]= math.log2( self.A[q0][q1] ) - normA
  
  def __init__(self, gold_letters, sentences):
    self.gold_letters_= gold_letters
    self.B_= dict()
    self.train(sentences)
  
  def predict(self, O):
    V= list()
    BT= list()
    for t in range(len(O)):
      V.append(dict())
      BT.append(dict())
      for q in TRAIN_LETTERS:
        V[-1][q]= 0
        BT[-1][q]= -1
    B_= likelihood(self.gold_letters_, O[0])
    B= dict()
    for i, b in enumerate(B_):
      B[TRAIN_LETTERS[i]]= CHARACTER_SIZE - b#math.log2( CHARACTER_SIZE - b ) - math.log2( CHARACTER_SIZE )
    B_sum= sum(B.values())
    for q in B.keys():
      B[q]= math.log2(B[q]) - math.log2(B_sum)
    for q in TRAIN_LETTERS:
      V[0][q]= self.Pi[q] + B[q]
    for t in range(1, len(O)):
      for q1 in TRAIN_LETTERS:
        max_score= float('-inf')
        B_= likelihood(self.gold_letters_, O[t])
        B=dict()
        for i, b in enumerate(B_): 
          B[TRAIN_LETTERS[i]]= CHARACTER_SIZE-b#math.log2( CHARACTER_SIZE - b ) - math.log2( CHARACTER_SIZE )
        B_sum= sum(B.values())
        for q in B.keys():
          B[q]= math.log2(B[q]) - math.log2(B_sum)
        for q0 in TRAIN_LETTERS:
          score= V[t-1][q0] + self.A[q0][q1] + B[q1]
          if max_score < score:
            max_score= score
            V[t][q1]= score
            BT[t][q1]= q0
    max_score= float('-inf')
    max_q= '~'
    for q in TRAIN_LETTERS:
      score= V[len(O)-1][q]
      if max_score < score:
        max_score= score
        max_q= q
    Q= [q]
    for t in range(len(O)-1, 0, -1):
      Q.insert(0, q:=BT[t][q])
    return Q

#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

## Below is just some sample code to show you how the functions above work. 
# You can delete this and put your own code here!

# Each training letter is now stored as a list of characters, where black
#  dots are represented by *'s and white dots are spaces. For example,
#  here's what "a" looks like:
print("\n".join([ r for r in train_letters['P'] ]))

# Same with test letters. Here's what the third letter of the test data
#  looks like:
print("\n".join([ r for r in test_letters[2] ]))

train_txt_file= open(train_txt_fname, 'r')
train_txt= list()
for line in train_txt_file:
  train_txt.append('')
  for i, word in enumerate(line.split()):
    if 0==i%2:
      for char in word:
        if char not in TRAIN_LETTERS:
          word= ''
          break
      if ''==word or "''"==word:
        continue
      if word not in ',.?!':
        train_txt[-1]+= ' '
      train_txt[-1]+= word
  train_txt[-1]= train_txt[-1][1:]
  if ('??'==train_txt[-1][-2:] or
      '!!'==train_txt[-1][-2:]):
    train_txt[-1]= train_txt[-1][:-1]
  if ''==train_txt[-1]:
    train_txt.pop(-1)

hmm= HMM(train_letters, train_txt)

def diff(comp_text, gold_text):
  assert len(comp_text)==len(gold_text)
  diff_cnt= 0
  for a, b in zip(comp_text, gold_text):
    if a==b:
      diff_cnt+= 1
  return diff_cnt

if os.path.isfile(os.path.join('test_images', [k for k in test_gold.keys()][0])):
  letters_total= 0
  letters_correct_total_simple= 0
  letters_correct_total_hmm= 0
  samples_total= 0
  for fname, gold_txt in test_gold.items():
    test_img= load_letters(os.path.join('test_images', fname))
    smpl_txt= ''.join(predict_simple(train_letters, test_img))
    hmmd_txt= ''.join(hmm.predict(test_img))
    samples_total+= 1
    letters_total+= len(gold_txt)
    print('Test sample ', samples_total)
    print('  Gold: ', gold_txt)
    print('Simple: ', smpl_txt)
    print('   HMM: ', hmmd_txt)
    print('')
    print(samples_total, ' of ', len(test_gold), ' test samples scored')
    print(letters_total, ' letters scored')
    letters_correct = diff(smpl_txt, gold_txt)
    letters_correct_total_simple+= letters_correct
    letters_correct = diff(hmmd_txt, gold_txt)
    letters_correct_total_hmm+= letters_correct
    print('Simple: ', letters_correct_total_simple / letters_total)
    print('   HMM: ', letters_correct_total_hmm    / letters_total)
    print('')

fname= os.path.basename(test_img_fname)
if fname in test_gold:
  print("  Gold: " + test_gold[fname])
if True:
# The final two lines of your output should look something like this:
  print("Simple: " + ''.join(predict_simple(train_letters, test_letters)))
  print("   HMM: " + ''.join(hmm.predict(test_letters))) 


