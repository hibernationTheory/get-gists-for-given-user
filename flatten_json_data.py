import json
import operator
import os

import frontmatter

def categorize_with_tags(data):
	categories = {}
	for item in data:
		tags = item["metadata"]["tags"].split(',')
		tags = [tag_type.strip() for tag_type in tags]
		for tag in tags:
			#tag = str(tag)
			if not categories.get(tag, None):
				categories[tag] = []
			categories[tag].append(item["id"])
	return categories

def run(target_dir, target_file_name):
	"""
	Get all the .json files from the given folder and write their content into a single file.
	"""
	final_data = {}
	gist_data_all = []
	gist_data_all_by_date = {}
	target_file_path = os.path.join(target_dir, target_file_name)

	# collect all the separate md files into one array
	filenames_from_folder = next(os.walk(target_dir))[2]
	for filename in filenames_from_folder:
		if filename.endswith('.json') and filename != target_file_name:
			file_path = os.path.join(target_dir, filename)
			with open(file_path, 'r') as current_json_file:
				gist_data = json.load(current_json_file)
			gist_data_all.append(gist_data)
			gist_data_all_by_date[gist_data["created_at"]] = gist_data

	categories = categorize_with_tags(gist_data_all)
	gist_data_all_by_date__sorted = sorted(gist_data_all_by_date.items(), key=operator.itemgetter(0))
	# add a order index to the sorted .md files to be used on front end.
	gist_data_all__sorted = []
	for index, data in enumerate(gist_data_all_by_date__sorted):
		data = data[1]
		data["sort_index"] = index
		gist_data_all__sorted.append(data)

	final_data["gist_data"] = gist_data_all__sorted
	final_data["categories"] = categories

	with open(target_file_path ,'w') as target_file:
		json.dump(final_data, target_file, indent=True)

