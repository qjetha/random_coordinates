import random, csv, os
import geopandas as gpd
from shapely.geometry import Point

def main():

	#-----Set Parameters-----# 
	user = '/Users/qayamjetha/Dropbox (Gorman Consulting)/Polio/Only Gorman Consulting/'
	shapefile = f'{user}/_Mapping_Files/PAK Reconciled/Adm2_PAK_Reconciled.shp'
	number_points = 1500
	min_distance_boundary = 0.1					# in degrees!
	min_distance_point = 0.1					# in degrees!

	geodata = gpd.read_file(shapefile)


	#-----Output CSV With Random Coordinates-----#
	if os.path.exists(f'{user}/_Resources/Dot Density/output/pakistan_admin2.csv'):
		os.remove(f'{user}/_Resources/Dot Density/output/pakistan_admin2.csv')

	with open(f'{user}/_Resources/Dot Density/output/pakistan_admin2.csv', 'w') as file:
		
		writer = csv.writer(file)
		writer.writerow(['district', 'id_district', 'index', 'latitude', 'longitude'])

		# Loop over the length of the geodata
		for unit in range(len(geodata)):
			points = random_points(geodata.iloc[unit].geometry, geodata.iloc[unit].DIST_NAME, number_points, min_distance_boundary, min_distance_point)

			# Loop over the number of random points
			index_id = 1
			for p in points:
				writer.writerow([geodata.iloc[unit].DIST_NAME, geodata.iloc[unit].DIST_ID, index_id, p.y, p.x])
				index_id += 1



#-----Function to Get Random Points Subject to Parameter Constraints-----# 
def random_points(polygon, district_name, number, min_distance_boundary, min_distance_point):
	'''
		Run algorithm for assigning random coordinates within each district
		polygon. Start with very conservative minimum distance to polygon
		boundary and other points. After 10,000 failed coordinates, relax
		parameters slightly. This is not time efficient, but it guarantees
		that points assigned first are "better", which is what we want.
		Returns a list of coordinates that satisfy parameters.
	'''

	min_x, min_y, max_x, max_y = polygon.bounds

	points = list()

	i = 0 		# number of successful coordinates
	j = 1 		# number of unsuccessful coordinates

	while i < number:
	
		print(f'{district_name}, number of successful points = {i}, number of tried points = {j}')

		point = Point(random.uniform(min_x, max_x), random.uniform(min_y, max_y))

		if polygon.contains(point):

			if (j%10000==0) :
				min_distance_boundary = min_distance_boundary - .01
				min_distance_point = min_distance_point - .01
				j+=1
			
			else:

				if polygon.boundary.distance(point) < min_distance_boundary:
					j+=1
					continue
				
				cond_true = True
				for p in points:
					if point.distance(p) < min_distance_point:
						cond_true = False
						break

				if cond_true == True:
					points.append(point)
					i+=1
				else:
					j+=1

	return points



if __name__ == "__main__":
	main()
