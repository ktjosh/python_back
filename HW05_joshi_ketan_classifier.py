""" 

File name : HW05_joshi_ketan_Classifier.py
This file is a decision tree program that classifies recipes into cupcakes and muffins

Author: Ketan Joshi (ksj4205)

"""

def Doclassification():


	file1 = open("Recipes_For_VALIDATION_2175_RELEASED_v201.csv","r")
	file = open("HW05_joshi_ketan_MyClassification.csv","w")
	alline = file1.readlines()
	attributes={}
	name = []
	attributes_name = alline[0].split(',')
	for att in attributes_name:
		attributes[att]=0
		name.append(att)
	for index in range(1,len(alline)):
		line = alline[index].split(',')
		line=line[0:26]
		for i in range(1,len(line)):
			attributes[name[i]]= float(line[i])
		if attributes["Sugar"]<=19:
			if attributes["Egg"]<=12:
				if attributes["Butter or Margarine"]<=18:
					if attributes["Baking Powder"]<=2:
						file.write('1\n')
					else:
						if attributes["cinnamon"]<=11:
							file.write('0\n')
						else:
							file.write('1\n')
				else:
					file.write('0\n')
			else:
				file.write('0\n')
		else:
			if attributes["Canned Pumpkin_or_Fruit"]<=26:
				if attributes["Vanilla"]<=6:
					file.write('0\n')
				else:
					file.write('1\n')
			else:
				file.write('1\n')

def main():
	Doclassification()


if __name__ == '__main__':
	main()