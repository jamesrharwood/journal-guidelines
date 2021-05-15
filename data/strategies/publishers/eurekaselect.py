url = "www.eurekaselect.com/(?P<NODE>\d*)/journal/{ID}$"
extractor_args = dict(restrict_text=[r"instructions\W*for\W*authors"])
template = "https://www.eurekaselect.com/node/{NODE}/{ID}/ifa"
