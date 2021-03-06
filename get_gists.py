"""
Gets all the Markdown files that has the given prefix (like: '_til_') from a gist account of a given username,
download them into a folder and creates a json metadata file for it as well. if the folder doesn't have that file with the same name AND same size.
Also removes the files in the folder that doesn't match the filename content of the gists of the user.
"""

"""
TO DO: Do I even need the markdown file anymore? I am capturing all the data in the .json file anyway.
"""

#stlib
import os
import json

#3rd party
import frontmatter
import requests

def delete_non_matching_files_from_folder(filename_list, folder_path):
	"""
	given a folder path will compare the given filenames list to the filenames in the folder,
	and delete those files in the folder that doesn't exist in the given list
	"""
	filenames_from_folder = next(os.walk(folder_path))[2]
	for filename in filenames_from_folder:
		if filename not in filename_list:
			file_path = os.path.join(folder_path, filename)
			print('deleting the file: ' + file_path)
			os.remove(file_path)

def get_all_gists_for_user(username):
	"""gets all the gists for the given user from the github gists"""
	website = "https://api.github.com/users/"
	user_gists = website + username + "/gists"
	response = requests.get(user_gists)
	if not response.ok:
		return None
	gists_all = [i for i in response.json()]
	return gists_all

def get_all_gist_filenames(gists_all):
	"""given all the gist data, gets all the gist_filenames"""
	filenames = []
	for gist in gists_all:
		file_dict = gist["files"]
		file_name = file_dict.keys()[0]
		filenames.append(file_name)
	return filenames

def add_json_filenames_to_list(filenames_list):
	json_filenames_list = [filename.replace('.md', '.json') for filename in filenames_list]
	filenames_list.extend(json_filenames_list)

def get_content_data_for_gist(gist, prefix=None):
	"""gets content data from a given gist"""
	if not gist:
		return None
	files_dict = gist["files"]
	gist_id = gist["id"]
	gist_url = gist["html_url"]
	md_content = None

	for file_item in files_dict.iteritems():
		file_name = file_item[0]
		file_item_data = file_item[1]

		language = file_item_data["language"]
		if not prefix:
			conditional = True
		else:
			conditional = file_name.startswith(prefix)

		if language == "Markdown" and conditional:
			return {
				"data":file_item_data,
				"name":file_name,
				"created_at":gist["created_at"],
				"comments_url":gist["comments_url"],
				"id": gist_id,
				"url": gist_url,
			}

def download_markdown_gist(file_path, data):
	"""downloads the file for the given gist to the given path"""
	if os.path.exists(file_path):
		current_size = os.path.getsize(file_path)
		if current_size == data["size"]:
			print("skipping file since file size in disk is same: %s" %file_path)
			return False
	content = download_from_url(data["raw_url"], file_path)
	return content

def download_from_url(url, file_path):
	"""downloads the file at the given url to the given path"""
	r = requests.get(url, stream=True)
	content = ''
	print("downloading the file at: " + url)
	with open(file_path, "wb") as fd:
	    for chunk in r.iter_content(20):
	    	content = content + chunk
	        fd.write(chunk)
	return content

def run(username, save_folder, prefix=None, data_file_name="gist_data.json"):
	gist_all = get_all_gists_for_user(username)
	gist_filenames = get_all_gist_filenames(gist_all)
	add_json_filenames_to_list(gist_filenames)
	delete_non_matching_files_from_folder(gist_filenames, save_folder)

	for gist in gist_all:
		content_data = get_content_data_for_gist(gist, prefix)
		if not content_data:
			continue
		file_path = os.path.join(save_folder, content_data["name"])
		file_data_path = os.path.join(save_folder, content_data["name"].replace('.md', '.json'))
		markdown_content = download_markdown_gist(file_path, content_data["data"])
		if markdown_content:
			gist_frontmatter = frontmatter.loads(markdown_content)
			content = gist_frontmatter.content
			metadata = gist_frontmatter.metadata
			content_data["content"] = content
			content_data["metadata"] = metadata
			with open(file_data_path, 'w') as target_file:
				json.dump(content_data, target_file, indent=True)
