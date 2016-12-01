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
					self.support = int(rest.split(',')[0].strip())
					self.confidence = int(rest.split(',')[1].strip())
					
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
	contents = f.read()
	f.close()
	rules = contents.split('\n')
	rules = [Rule(s) for s in rules]
	rules = sorted(rules, key = lambda x: x.get_sort_key(), reverse = True)
	return rules
	
def apply_rules(documents, rules, threshold = 5):
	value ={}
	for doc in documents:
		applicable = [r for r in rules if r <= doc]
		if len(applicable) > threshold:
			applicable = applicable[:threshold]
		topics = set([r.get_topic() for r in applicable])
		value[doc] = topics
	return value
	

