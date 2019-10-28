import pandas as pd 
import xlrd

class Data():
	def __init__(self):
		self.df = pd.read_excel(r"changed_data.xlsx")
	
	def filter_region(self, name): #name type is list as Pandas isin receives only list
		if len(name) > 0:
			return self.df[self.df.Region.isin( name)].to_dict()
		else:
			return "select region to see"

	def get_regions_name(self):
		return self.df.Region.unique()


if __name__ == '__main__':
	b = Data()
	print(b.filter_region(["Süd"]))
	#print(b.get_regions_name())