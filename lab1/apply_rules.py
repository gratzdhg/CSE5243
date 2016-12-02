#!/usr/bin/env python
	
class Rule(object):	
	def __init__(self, rule_string):
		self.invalid = False
		if '<-' not in rule_string:
			print 'ERROR: invalid rule string: no "<-"'
			self.invalid = True
		else:
			temp = rule_string.split('<-')
			self.topic = temp[0].strip()
			rest = temp[1].strip()
			if '(' not in rest:
				print 'ERROR: invalid rule string: no "("'
				self.invalid = True
			else:
				temp2 = rest.split('(')
				words = temp2[0].strip().split(' ')
				self.words = set([w.strip() for w in words])
				rest = temp2[1]
				if ',' not in rest or rest[-1] != ')':
					print 'ERROR: invalid rule string: tuple not valid'
					self.invalid = True
				else:
					rest = rest[:-1]
					self.support = float(rest.split(',')[0].strip())
					self.confidence = float(rest.split(',')[1].strip())
					
	def is_valid(self):
		return not self.invalid
		
	def get_word_set(self):
		return self.words
		
	def get_confidence(self):
		return self.confidence
		
	def get_support(self):
		return self.support
		
	def get_sort_key(self):
		return (self.confidence, self.support)
		
	def get_topic(self):
		return self.topic
		
def sort_rules(rule_file):
	f = open(rule_file)
	rules = []
	for s in f:
		r = Rule(s)
		if r.is_valid():
			rules += [r]
	rules = sorted(rules, key = lambda x: x.get_sort_key(), reverse = True)
	f.close()
	return rules
	
def apply_rules(documents, rules, threshold = 5):
	value = []
	for doc in documents:
		count = 0
		applicable = []
		while len(applicable) < threshold and count < len(rules):
			r = rules[count]
			if r.get_word_set() <= doc:
				applicable += [r]
			count += 1
		topics = set([r.get_topic() for r in applicable])
		value.append(topics)
	return value
	

