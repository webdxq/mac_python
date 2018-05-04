# -*- coding:utf-8-*-
# from __future__ import unicode_literals
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import sys
import time
import numpy as np
import tensorflow as tf
import argparse
import os
import exceptions
from . import noSG_fnn



# checkpoint_dir = '/Users/dongxq/Desktop/disulfide/noSG_new_train/logs/'
checkpoint_dir = '/Users/dongxq/Sites/project/static/model/'



def predict(args,sess,images,labels,logits,out):

	data = args[0]

	id_ord = args[1]
	name = args[2]
	out_ = sess.run(out,feed_dict={images:data.reshape((len(data),100))})
	count = 0
	result_dict = {}

	# print(name)
	# print(type(result_dict))
	new_list=[]
	new_list_score = []
	
	with open('/Users/dongxq/Desktop/disulfide/predict/%s.txt'%name, 'w') as wf:
		
		for outi in range(len(out_)):
			# print(id_ord[outi],out_[outi])
			if(out_[outi][1] > out_[outi][0]):
				count += 1
				print id_ord[outi],out_[outi]
				# print type(out_[outi][1])
				# result_dict[id_ord[outi]] = out_[outi]
				result_dict[id_ord[outi][0]+'-'+id_ord[outi][1]] = float('%.3f'% out_[outi][1])
				# print(result_dict)
				# print('dict',result_dict[outi])
			# wf.write(id_ord[outi])
			# wf.write(':')
			# wf.write(str(out_[outi]))
			# wf.write('\n')

	# print(len(id_ord),count)
	# print('****** The probability of the mutate pos ********')
	# mutate_pos_ord = [None for i in range(len(id_ord))]
	# print(mutate_pos_ord)
	# with open('/Users/dongxq/Desktop/disulfide/predict/%s.txt'%name, 'a') as wf:
	# 	for i in range(len(id_ord)):
	# 		# if filter(str.isdigit,id_ord[i][0]) == '193' and filter(str.isdigit,id_ord[i][1]) == '233':
	# 		# 	print (filter(str.isdigit,id_ord[i][0]),filter(str.isdigit,id_ord[i][1]))
	# 		# 	break
	# 		mutate_pos_ord[i] = [filter(str.isdigit,id_ord[i][0]),filter(str.isdigit,id_ord[i][1])]
	# 		# wf.write(filter(str.isdigit,id_ord[i][0]) + ',')
	# 		# wf.write(filter(str.isdigit,id_ord[i][1]))
	# 		# wf.write('\n')
	# 		wf.write(id_ord[i][0] + ',')
	# 		wf.write(id_ord[i][1])
	# 		wf.write('\n')
	# 	for ssbonds in ssbonds_detect:
	# 		# try:
	# 		if ssbonds.tolist() in mutate_pos_ord:
	# 			wf.write(ssbonds)
	# 			wf.write(':' + str(out_[mutate_pos_ord.index(ssbonds.tolist())]))
	# 			wf.write('\n')
	# 			print(ssbonds,out_[mutate_pos_ord.index(ssbonds.tolist())])
	# 		else:
	# 			continue
	# 	# 	# rmchr_id_ord.index(ssbonds.tolist())
	# 	# 	# if ssbonds == ['193','233']
			
	# 			# print('probability of the pos (%s,%s) is %0.3f%%'%(ssbonds[0],ssbonds[1],out_[mutate_pos_ord.index(ssbonds.tolist())][1]*100))
	# 		# except ValueError:
	# 		# 	continue
	# # print(result_dict)
	print 'finish predict.'
	return result_dict



def main(args): 
	
	sess=tf.Session() 
	
	ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
	# print(ckpt)
	ckpt_path = ckpt.all_model_checkpoint_paths[-1]
	saver = tf.train.import_meta_graph(ckpt_path + '.meta')
	saver.restore(sess,ckpt_path)
	# saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path + '.meta')
	# saver.restore(sess, ckpt.model_checkpoint_path + '-100')

	graph = tf.get_default_graph()

	images = graph.get_tensor_by_name('image:0')
	labels=graph.get_tensor_by_name('labels:0')

	logits = graph.get_tensor_by_name('softmax_linear/add:0')
	# logits = new_fnn.inference(images, 128, 32)
	out=tf.nn.softmax(logits=logits)

	result_dict = predict(args,sess,images,labels,logits,out)
	return result_dict
	# test(sess,images,labels,logits,out)
	# predict_one_map(sess,images,'/Users/dongxq/Desktop/disulfide/predict_analysis/27_79change5_610.npy',out)

if __name__ == '__main__':
	
	tf.app.run()
