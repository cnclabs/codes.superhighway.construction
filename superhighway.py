from collections import defaultdict
from math import log
from sys import argv
import sys
import argparse

def parse_args():
	'''
	Parses the arguments.
	'''

	parser = argparse.ArgumentParser(description="Superhighway Construction.")

	parser.add_argument('--source_data', nargs='?', default='data/nf_toy',
			help='Input source domain data')

	parser.add_argument('--target_data', nargs='?', default='data/ml_toy',
			help='Input Target domain data')

	parser.add_argument('--alpha', type=float, default=0.9,
			help='Parameter for filtering user by the ratio of overlapped items in each user\'s accessed item list')
	parser.add_argument('--beta', type=float, default=1.0,
			help='Parameter for setting the weight of superhighway')
	parser.add_argument('--output', nargs='?', default='superhighway.edgelist')

	return parser.parse_args()

def LoadEdgelist(f, edgelist, domain):
	user_itemlists = defaultdict(list)	
	item = []
	cnt = 0.0
	print("Preparing...")
	cnt_line = sum(1 for line in open(f))
	with open(f, "r") as f:
		for line in f:
			line = line.strip().split(" ")
			u = line[0]
			i = line[1]
			weight = float(line[2])
			user_itemlists[u].append(i)
			item.append(i)
			edgelist[u][i] = 1

			# Print status
			sys.stdout.write("\rLoading "+domain +" Data: " + str(round(cnt/cnt_line*100, 2)) + " % \r")
			sys.stdout.flush()
			cnt += 1
			#edgelist[user][item] = log(weight)
	sys.stdout.write("\n")

	return edgelist, user_itemlists, item

def BridgePoint_Identification(src_user_itemlists, tar_user_itemlists, src_item, tar_item, alpha):
	overlap_item = list(set(src_item)&set(tar_item))
	selected_src_user = []
	b_cnt = 0.0
	total = float(len(src_user_itemlists.keys()) + len(tar_user_itemlists.keys()))

	for src_user in src_user_itemlists.keys():
		sys.stdout.write("\rIdentifying bridge points: " + str(round(b_cnt/total*100, 2)) + " % \r")
		sys.stdout.flush()
		b_cnt += 1
		if len(list(set(src_user_itemlists[src_user])&set(overlap_item))) > alpha * len(set(src_user_itemlists[src_user])):
			selected_src_user.append(src_user)	

	selected_tar_user = []
	for tar_user in tar_user_itemlists.keys():
		sys.stdout.write("\rIdentifying bridge points: " + str(round(b_cnt/total*100, 2)) + " % \r")
		sys.stdout.flush()
		b_cnt += 1
		if len(list(set(tar_user_itemlists[tar_user])&set(overlap_item))) > alpha * len(set(tar_user_itemlists[tar_user])):
			selected_tar_user.append(tar_user)	
	sys.stdout.write("\n")

	return selected_src_user, selected_tar_user

def main(args):

	f_src = args.source_data
	f_tar = args.target_data
	alpha = float(args.alpha)
	beta = float(args.beta)
	odir = args.output

	edgelist = defaultdict(lambda: defaultdict(int))
	edgelist, src_user_itemlists, src_item = LoadEdgelist(f_src, edgelist, "Source")
	edgelist, tar_user_itemlists, tar_item = LoadEdgelist(f_tar, edgelist, "Target")
	selected_src_user, selected_tar_user = BridgePoint_Identification(src_user_itemlists, tar_user_itemlists, src_item, tar_item, alpha)

	with open(odir,'w') as fw:
		print("Constructing Highways...")
		for src in edgelist.keys():
			for tar in edgelist[src].keys():
				fw.write(str(src)+" "+str(tar)+" "+str(float(edgelist[src][tar]))+"\n")

		print("Constructing Superhighways...")
		for src_user in selected_src_user:
			for tar_user in selected_tar_user:
					o_cnt = len(list(set(src_user_itemlists[src_user])&set(tar_user_itemlists[tar_user])))
					if o_cnt > 0:
						fw.write(str(src_user)+" "+str(tar_user)+" "+str(float(beta*o_cnt))+"\n")

if __name__ == "__main__":
	args = parse_args()
	main(args)	

