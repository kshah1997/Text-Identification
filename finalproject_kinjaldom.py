from porter import create_stem
from math import *

class TextModel:

	def __init__(self, name):
		""" the constructor for the TextModel class
			all dictionaries are started at empty
			the name is just for our own purposes, to keep things 
			organized
		"""
		self.name = name
		self.words = {}   # starts empty
		self.wordlengths = {}
		self.stems = {}
		self.sentencelengths = {}
		self.dialogue = {}
		# you will want another dictionary for your text feature


	def __repr__(self):
		""" this method creates the string version of TextModel objects
		"""
		s  = "\nModel name: " + str(self.name) + "\n"
		s += "    n. of words: " + str(len(self.words))  + "\n"
		s += "    n. of word lengths: " + str(len(self.wordlengths))  + "\n"
		s += "    n. of sentence lengths: " + str(len(self.sentencelengths))  + "\n"
		s += "    n. of stems: " + str(len(self.stems))  + "\n"
		s += "    n. of dialogue lengths: " + str(len(self.dialogue)) + "\n"
		# you will likely want another line for your custom text-feature!
		return s

	def readTextFromFile(self,filename):
		""" input: filename in .txt 
			outpt: all the text in the file as a single large 
					string
		"""

		f = open(filename)
		text = f.read()
		#print text
		f.close()
		return text

	def makeSentenceLengths(self,s):
		""" input: string s from the method readTextFromFile
			output: returns a python dictionary of frequency of 
					sentence lengths
		"""
		LoW = s.split()
		d = {}
		x = 0   # x = index of the first word of any sentence 
		for i in range(len(LoW)):
			if LoW[i][-1] in '.?!':
				sentence_length = i + 1 - x 
				if sentence_length in d.keys():
					d[sentence_length] += 1 
				else:
					d[sentence_length] = 1
				x = i + 1 
		self.sentencelengths = d

	
	def cleanString(self,s):
		""" input: string s 
			output: returns the string with no punctuation/upper 
					case 
		"""
		 
		s1 = '' #new string without punctuation
		for char in range(len(s)):
			if s[char] in "?!.,-;:'()":
				s1 = s1 
			else: 
				s1 = s1 + s[char]
		s = s1.lower()
		return s
	

	def makeWordLengths(self,s):
		""" input: a string s 
			output: creates a pytohon dictionary of words with their 
					frequency
		"""
		s = self.cleanString(s)
		LoW = s.split()
		d = {}
		for i in range(len(LoW)):
			x = len(LoW[i])
			if x in d.keys():
				d[x] += 1
			else:
				d[x] = 1 
		self.wordlengths = d

	def makeWords(self,s):
		""" input: cleaned string s
			output: a dictionary of the frequency of words used in s
		"""
		cs = self.cleanString(s)
		LoW = cs.split()
		
		d = {}
		for i in range(len(LoW)):
			x = LoW[i]
			if x in d.keys():
				d[x] += 1 
			else:
				d[x] = 1
		self.words = d

	def makeStems(self,s):
		""" input: string s 
			output: python dictionary with frequency of stems
		"""
		cs = self.cleanString(s)
		LoW = cs.split()
		
		d = {}
		for i in range(len(LoW)):
			x = create_stem(LoW[i])
			if x in d.keys():
				d[x] += 1
			else:
				d[x] = 1
		self.stems = d

	def makelength_of_dialogue(self,s):
		""" input: string s containing all the text in a  
			file as a single string 
			output: python dictionary of length of dialogues in the 
			text along with its frequency of occurence
		"""

		LoW = s.split()
		d = {}
		x = 0
		for i in range(len(LoW)):
			if LoW[i][0] == '"':	#if the first character of a word is a quote, start counting from 1
				x = 1
			elif LoW[i][-1] == '"':		#elif the last character of a word is a quote, create a key in the dictionary
				x += 1
				if x in d.keys():
					d[x] += 1
				else:
					d[x] = 1
			else:
				x += 1 			#else keep counting by one
		self.dialogue = d


	def printAllDictionaries(self):
		""" input: a string s
			output: the printed dictionaries of sentence lengths,
			word lengths, words, stems, and lengths of dialogues
		"""
		print "self.sentencelengths: ", self.sentencelengths, "\n"
		print "self.words: ", self.words, "\n"  # starts empty
		print "self.wordlengths: ", self.wordlengths, "\n"
		print "self.stems: ", self.stems, "\n"
		print "self.dialoguelengths: ", self.dialogue, "\n"


#test_tm = TextModel( "Milestone test" )
#s = test_tm.readTextFromFile( "test2.txt" )
#test_tm.makelength_of_dialogue(s)
#print test_tm.dialogue


	
	def normalizeDictionary(self,d):
		""" input: a model-dictionary
			output: normalized version, in which values add to 1
		"""
		add = 0
		nd = {}
		for i in d:
			add = add + d[i]
		for i in d:
			nd[i] = d[i]/float(add)
		return nd
		
	def smallestValue(self, nd1, nd2):
		""" input: two model dictionaries
			output: smallest positive value across them both
		"""
		LoV = nd1.values() + nd2.values()
		return min(LoV)
		
	def compareDictionaries(self,d,nd1,nd2):
		""" input: one unnormalized dictionary d and two normalized 
			dictionaries nd1 and nd2
			output: the log-probability that dictionary d arose from the 
			distribution of data in normalized dictionaries nd1 and nd2 
			returns a list 
		"""
		total1 = 0.0
		e = 0.5 * self.smallestValue(nd1,nd2)
		LoK1 = nd1.keys()
		for i in d: 
			if i in LoK1:
				total1 += d[i]*log(nd1[i])
			else: 
				total1 += d[i]*log(e)
		total2= 0.0
		LoK2 = nd2.keys()
		for i in d: 
			if i in LoK2:
				total2 += d[i]*log(nd2[i])
			else: 
				total2 += d[i]*log(e)
		return [total1] + [total2]

	def createAllDictionaries(self, s): 
		""" should create out all five of self's 
			dictionaries in full - for testing and 
			checking how they are working...
		"""
		self.makeSentenceLengths(s)
		new_s = self.cleanString(s)
		self.makeWords(new_s)
		self.makeStems(new_s)
		self.makelength_of_dialogue(s)
		self.makeWordLengths(new_s)

	def compareTextWithTwoModels(self,model1,model2):
		"""
		"""
		print "Model 1 is", model1
		print "Model 2 is", model2

		A1 = self.compareDictionaries(self.words,model1.words,model2.words)[0]
		A2 = self.compareDictionaries(self.words,model1.words,model2.words)[1]
		B1 = self.compareDictionaries(self.wordlengths,model1.wordlengths,model2.wordlengths)[0]
		B2 = self.compareDictionaries(self.wordlengths,model1.wordlengths,model2.wordlengths)[1]
		C1 = self.compareDictionaries(self.sentencelengths,model1.sentencelengths,model2.sentencelengths)[0]
		C2 = self.compareDictionaries(self.sentencelengths,model1.sentencelengths,model2.sentencelengths)[1]
		D1 = self.compareDictionaries(self.stems,model1.stems,model2.stems)[0]
		D2 = self.compareDictionaries(self.stems,model1.stems,model2.stems)[1]
		E1 = self.compareDictionaries(self.dialogue,model1.dialogue,model2.dialogue)[0]
		E2 = self.compareDictionaries(self.dialogue,model1.dialogue,model2.dialogue)[1]

		print "Name               vsTM1               vsTM2"
		print "----               -----               -----"
		print "words              ", str(A1), "    ", str(A2)
		print "wordlengths        ", str(B1), "    ", str(B2)
		print "sentencelengths    ", str(C1), "    ", str(C2)
		print "stems              ", str(D1), "    ", str(D2)
		print "dialogues          ", str(E1), "    ", str(E2), "\n"

		A = [A1, A2]
		B = [B1, B2]
		C = [C1, C2]
		D = [D1, D2]
		E = [E1, E2]
		x = 0
		if max(A) == A1:
			x += 1
		if max(B) == B1:
			x += 1
		if max(C) == C1:
			x += 1
		if max(D) == D1:
			x += 1
		if max(E) == E1:
			x += 1
		print "--> Model 1 wins on", str(x), "features"
		print "--> Model 2 wins on", str(5-x), "features"
		if x > 5-x:
			print "+++++      Model1 is the better match!      +++++"
		else:
			print "+++++      Model2 is the better match!      +++++"






test_tm = TextModel( "Final test" )
d = {'a': 5, 'b':1, 'c':2}
nd = test_tm.normalizeDictionary( d )
print "The original dictionary is"
print d
print "The normalized dictionary is"
print nd


test_tm = TextModel( "Final test" )
d1 = {'a': 5, 'b':1, 'c':2}
nd1 = test_tm.normalizeDictionary( d1 )
d2 = {'a': 15, 'd':1}
nd2 = test_tm.normalizeDictionary( d2 )
print "The normalized dictionaries are"
print nd1
print nd2
sm_va = test_tm.smallestValue( nd1, nd2 )
print "and the smallest value between them is", 
print sm_va 


test_tm = TextModel( "Final test" )
d = {'a':2, 'b':1, 'c':1, 'd':1, 'e':1}
print "The unnormalized dictionary is"
print d
print "\n"
d1 = {'a': 5, 'b':1, 'c':2}
nd1 = test_tm.normalizeDictionary( d1 )
d2 = {'a': 15, 'd':1}
nd2 = test_tm.normalizeDictionary( d2 )
print "The normalized comparison dictionaries are"
print nd1
print nd2


List_of_log_probs = test_tm.compareDictionaries(d, nd1, nd2)
print "The list of log probs is"
print List_of_log_probs

print " +++++++++++ Model1 +++++++++++ "
trained_tm1 = TextModel( "Model1" )
text1 = trained_tm1.readTextFromFile( "test2.txt" )
trained_tm1.createAllDictionaries(text1)  # provided in hw description
trained_tm1.printAllDictionaries()

print " +++++++++++ Model2 +++++++++++ "
trained_tm2 = TextModel( "Model2" )
text2 = trained_tm2.readTextFromFile( "HP5.txt" )
trained_tm2.createAllDictionaries(text2)  # provided in hw description
trained_tm2.printAllDictionaries()

print " +++++++++++ Unknown text +++++++++++ "
unknown_tm = TextModel( "Unknown (trial)" )
text_unk = unknown_tm.readTextFromFile( "HP.txt" )
unknown_tm.createAllDictionaries(text_unk)  # provided in hw description
unknown_tm.printAllDictionaries()

unknown_tm.compareTextWithTwoModels(trained_tm1,trained_tm2)\

print " +++++++++++ Model1 +++++++++++ "
trained_tm1 = TextModel( "Model1" )
text1 = trained_tm1.readTextFromFile( "PJ.txt" )
trained_tm1.createAllDictionaries(text1)  # provided in hw description
trained_tm1.printAllDictionaries()

print " +++++++++++ Model2 +++++++++++ "
trained_tm2 = TextModel( "Model2" )
text2 = trained_tm2.readTextFromFile( "HP5.txt" )
trained_tm2.createAllDictionaries(text2)  # provided in hw description
trained_tm2.printAllDictionaries()

print " +++++++++++ Unknown text +++++++++++ "
unknown_tm = TextModel( "Unknown (trial)" )
text_unk = unknown_tm.readTextFromFile( "PJ2.txt" )
unknown_tm.createAllDictionaries(text_unk)  # provided in hw description
unknown_tm.printAllDictionaries()

unknown_tm.compareTextWithTwoModels(trained_tm1,trained_tm2)\


