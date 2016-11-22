# Compatible with Python3
# -*- coding: utf-8 -*-
# asterisk-assets-sync - Assets syncer of AsteriskLive.

import os, json, time
from datetime import datetime
import requests

data_dir = "data"
cache_dir = "_cache"
assets_base_url = "http://cdn-01.gameicone.net:10080/cdn/AssetNew/{}"
assets_list_file = "list_v001_download.txt"
assets_places_list_file = "list_v001_android.txt"

if __name__ == "__main__":

	# setup
	os.path.isdir(data_dir) or (os.mkdir(data_dir), os.mkdir("{}/manifests".format(data_dir)), os.mkdir("{}/passed".format(data_dir)), os.mkdir("{}/extracted".format(data_dir)))
	os.path.isdir(cache_dir) or os.mkdir(cache_dir)
	now_str = datetime.now().strftime("%Y-%m-%d_%H-%M")

	# latest assets list download
	assets_list_raw_place = "{}/manifests/{}_assets_list.txt".format(data_dir, now_str)
	with open(assets_list_raw_place, 'wb') as f:
		assets_list_raw = requests.get(assets_base_url.format(assets_list_file))
		f.write(assets_list_raw.content)
	assets_places_list_raw_place = "{}/manifests/{}_assets_place_list.txt".format(data_dir, now_str)
	with open(assets_places_list_raw_place, 'wb') as f:
		assets_places_list_raw = requests.get(assets_base_url.format(assets_places_list_file))
		f.write(assets_places_list_raw.content)
	print("Latest assets list saved:\n->{}\n->{}".format(assets_list_raw_place, assets_places_list_raw_place))

	# convert to array
	assets_list = assets_list_raw.text.split("\n")
	assets_places_list = []
	for asset_datas in assets_places_list_raw.text.split("\n"):
		assets_places_list.append(asset_datas.split(","))

	# load assets list cache
	assets_list_cache_place = "{}/assets_list_cache.json".format(cache_dir)
	try:
		with open(assets_list_cache_place, "r") as f:
			old_assets_list = json.load(f)
	except:
		old_assets_list = []
	assets_place_list_cache_place = "{}/assets_place_list_cache.json".format(cache_dir)
	try:
		with open(assets_place_list_cache_place, "r") as f:
			old_assets_place_list = json.load(f)
	except:
		old_assets_place_list = []
	old_assets_place_list_array = []
	for old_asset_place in old_assets_place_list:
			old_assets_place_list_array.append(old_asset_place[0])

	# check diff and new assets download
	for i in assets_places_list:
		asset_name = i[0].rsplit('/', 1)[1].split('?')[0]
		if asset_name not in old_assets_place_list_array:
			asset_place_url = assets_base_url.format(i[0])
			asset = requests.get(asset_place_url)
			ext = asset_name.split(".")[1]
			# write your processes
			if ext == "acb":
				asset_place = "{}/passed/{}".format(data_dir, asset_name)
				with open(asset_place, "wb") as f:
					f.write(asset.content)
			elif ext == "bin":
				asset_place = "{}/passed/{}".format(data_dir, asset_name)
				with open(asset_place, "wb") as f:
					f.write(asset.content)
			elif ext == "icdata":
				asset_place = "{}/passed/{}".format(data_dir, asset_name)
				with open(asset_place, "wb") as f:
					f.write(asset.content)
			elif ext == "unity3d":
				asset_place = "{}/passed/{}".format(data_dir, asset_name)
				with open(asset_place, "wb") as f:
					f.write(asset.content)
			else:
				asset_place = "{}/passed/{}".format(data_dir, asset_name)
				with open(asset_place, "wb") as f:
					f.write(asset.content)
			print("Saved: \"{}\"".format(asset_place_url))

	# save assets list cache
	with open(assets_list_cache_place, "w") as f:
		f.write(json.dumps(assets_list))
	with open(assets_place_list_cache_place, "w") as f:
		f.write(json.dumps(assets_places_list))