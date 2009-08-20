import dkv_config

def dkv_debug(s, print_nl=True):
	if dkv_config.get('general','debug') == '1':
		if print_nl:
			print s
		else:
			print s,

