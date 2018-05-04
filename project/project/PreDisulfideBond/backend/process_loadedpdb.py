# -*-coding:utf-8 -*-
# from __future__ import unicode_literals
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

from . import noSG_extract_unknown_map
from . import noSG_extract_unknown_map2
from . import extract_unknown_map
from . import ssbond_distance_map as sdm
import tensorflow as tf
import sys
import argparse
import numpy as np
from . import noSG_restore_fnn
import operator
from collections import OrderedDict


def find_mutate_rank(dict_result):
	print('****** The probability of the mutate pos ********')
	ssbonds_detect = np.load('/Users/dongxq/Desktop/disulfide/other_test_set/mutational_structrue_bril_flavodoxin/flavodoxin_ssbond.npy')#flavodoxin_ssbond.npy
	k = 1
	rank_dict = OrderedDict()
	# print ssbonds_detect
	for item in dict_result:
		k += 1;
		print item
		temp = item.split('-')

		temp_list = [filter(str.isdigit,temp[0]),filter(str.isdigit,temp[1])]
		if temp_list in ssbonds_detect.tolist():
			print temp_list
			rank_dict[item] = str(float('%.3f'% (k/float(len(dict_result))))*100) + '%'
			
	print rank_dict

def process_pdb(args):

	name = args.split('/')[-1].split('.')[0]
	rf = open(args)
	lines = rf.readlines()
	rf.close()
	temp = None
	length = 0
	for line in lines:
		line_split = line.split()
		if line_split[0] == 'ATOM':
			temp = 'ATOM'
			length = len(line_split)
			break
	# print length,temp
	# print temp == 'ATOM' and length==10
	# print temp == 'ATOM' and length==12
	if temp == 'ATOM' and length==10:

		map_list, map_id ,mol_type_list=noSG_extract_unknown_map.find_map_element(args)
		possible_ssbond, possible_ssbond_id = noSG_extract_unknown_map.make_ssbond_without_repeat(map_list, map_id, mol_type_list)
		full_distance_map = sdm.convert_to_nxn_map(np.array(possible_ssbond))
		print 'canditate bonds',len(full_distance_map)
		predict_path = np.array(full_distance_map)
		predict_ord_path = np.array(possible_ssbond_id)
		result_dict = noSG_restore_fnn.main([predict_path,predict_ord_path,name])
		sorted_result_dict = sorted(result_dict.iteritems(), key=operator.itemgetter(1), reverse=True)  
		final_dict = OrderedDict()
		for item in sorted_result_dict:
			# print item[0],item[1]
			final_dict[item[0]] = item[1]

		# print final_dict
		find_mutate_rank(final_dict)

	elif temp == 'ATOM' and length==12:
		# print 'hi'
		map_list, map_id ,mol_type_list=noSG_extract_unknown_map2.find_map_element(args)
		# print map_list
		possible_ssbond, possible_ssbond_id = noSG_extract_unknown_map2.make_ssbond_without_repeat(map_list, map_id, mol_type_list)
		full_distance_map = sdm.convert_to_nxn_map(np.array(possible_ssbond))
		print 'canditate bonds',len(full_distance_map)
		predict_path = np.array(full_distance_map)
		predict_ord_path = np.array(possible_ssbond_id)
		result_dict = noSG_restore_fnn.main([predict_path,predict_ord_path,name])
		sorted_result_dict = sorted(result_dict.iteritems(), key=operator.itemgetter(1), reverse=True)  
		final_dict = OrderedDict()
		for item in sorted_result_dict:
			# print item[0],item[1]
			final_dict[item[0]] = item[1]

		# print final_dict
		find_mutate_rank(final_dict)
		
	return final_dict

def process_pdb1(args):
	name = args.split('/')[-1].split('.')[0]
	map_list, map_id ,mol_type_list=extract_unknown_map.find_map_element(args)
	if map_list == []:
		print 'no bonds'
		return False
	possible_ssbond, possible_ssbond_id = extract_unknown_map.make_ssbond_without_repeat(map_list, map_id, mol_type_list)
	print possible_ssbond_id
	full_distance_map = sdm.convert_to_nxn_map(np.array(possible_ssbond))
	print 'canditate bonds',len(full_distance_map)
	predict_path = np.array(full_distance_map)
	predict_ord_path = np.array(possible_ssbond_id)
	result_dict = noSG_restore_fnn.main([predict_path,predict_ord_path,name])
	sorted_result_dict = sorted(result_dict.iteritems(), key=operator.itemgetter(1), reverse=True)  
	final_dict = OrderedDict()
	for item in sorted_result_dict:
		# print item[0],item[1]
		final_dict[item[0]] = item[1]

	# print final_dict
	find_mutate_rank(final_dict)
		
	return final_dict

# if __name__ == '__main__':
# 	args = sys.argv[1:]
# 	# print(args[0])
# 	process_pdb(args)
