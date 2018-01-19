# -*- coding:utf-8-*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import time
import numpy as np
import tensorflow as tf
import argparse
import fnn
import os
import exceptions
import cnn

parser = cnn.parser

parser.add_argument('--test_path', type=str, default='/Users/dongxq/Desktop/disulfide/validation_ssbond/full_nossbonds_distance_map.npy',
                    help='Directory where to write event logs.')
parser.add_argument('--checkpoint_dir', type=str, default='/Users/dongxq/Desktop/disulfide/new_train_cnn/logs/',
                    help='Directory where to read model checkpoints.')

parser.add_argument(
	'--predict_path',
	type=str,
	default='/Users/dongxq/Desktop/disulfide/other_set_map/brilM_ca_full_possible_ssbond_nr.npy',
	help='path with the Validation data.'
)
parser.add_argument(
	'--predict_ord_path',
	type=str,
	default='/Users/dongxq/Desktop/disulfide/other_set_map/brilM_ca_possible_ssbond_id_nr.npy',
	help='path with the Validation data id.'
)
parser.add_argument(
	'--mutate_pos_path',
	type=str,
	# default=os.path.join('/Users/dongxq/Desktop/disulfide/other_set_map','7211_possible_ssbond_id_nr.npy'),
	
	default='/Users/dongxq/Desktop/disulfide/other_test_set/mutational_structrue_bril_flavodoxin/bril_ssbond.npy',
	help='the mutate pos.'
)
parser.add_argument(
	'--test_label',
	type=bool,
	# default=False,
	help='path with the Validation data.'
)

def test(sess,images,labels,logits,out):
	data = np.load(FLAGS.test_path).reshape(-1,12,12,1)
	one_hot_labels=tf.one_hot(labels,axis=-1,depth=2)

	correct_prediction = tf.equal(tf.argmax(out, 1), tf.argmax(one_hot_labels, 1))
	correct_prediction = tf.cast(correct_prediction, tf.float32)
	accuracy = tf.reduce_mean(correct_prediction)

	if FLAGS.test_label:
		make_labels = np.ones(len(data))
	else:
		make_labels=np.zeros(len(data))
	accuracy_,abcd_,out_= sess.run([accuracy,one_hot_labels,out],feed_dict={images:data,labels:make_labels})
	print('accuracy is :%.2f'% accuracy_)

def predict(sess,images,labels,logits,out):

	data = np.load(FLAGS.predict_path)
	name = FLAGS.predict_path.split('/')[-1].split('_')[0]
	ssbonds_detect = np.load(FLAGS.mutate_pos_path)
	print(data.reshape(-1,12,12,1).shape)
	out_ = sess.run(out,feed_dict={images:data.reshape(-1,12,12,1)})
	id_ord = np.load(FLAGS.predict_ord_path)
	count = 0
	with open('/Users/dongxq/Desktop/disulfide/predict/%s.txt'%name, 'w') as wf:
		for outi in range(len(out_)):
			# print(id_ord[outi],out_[outi])
			if(out_[outi][1] > out_[outi][0]):
				count += 1
				print(id_ord[outi],out_[outi])
			# wf.write(id_ord[outi])
			# wf.write(':')
			# wf.write(str(out_[outi]))
			# wf.write('\n')

	print(count)
	print('****** The probability of the mutate pos ********')
	mutate_pos_ord = [None for i in range(len(id_ord))]
	# print(mutate_pos_ord)
	with open('/Users/dongxq/Desktop/disulfide/predict/cnn/%s.txt'%name, 'a') as wf:
		for i in range(len(id_ord)):
			# if filter(str.isdigit,id_ord[i][0]) == '193' and filter(str.isdigit,id_ord[i][1]) == '233':
			# 	print (filter(str.isdigit,id_ord[i][0]),filter(str.isdigit,id_ord[i][1]))
			# 	break
			mutate_pos_ord[i] = [filter(str.isdigit,id_ord[i][0]),filter(str.isdigit,id_ord[i][1])]
			# wf.write(filter(str.isdigit,id_ord[i][0]) + ',')
			# wf.write(filter(str.isdigit,id_ord[i][1]))
			# wf.write('\n')
			wf.write(id_ord[i][0] + ',')
			wf.write(id_ord[i][1])
			wf.write('\n')
		for ssbonds in ssbonds_detect:
			# try:
			if ssbonds.tolist() in mutate_pos_ord:
				wf.write(ssbonds)
				wf.write(':' + str(out_[mutate_pos_ord.index(ssbonds.tolist())]))
				wf.write('\n')
				print(ssbonds,out_[mutate_pos_ord.index(ssbonds.tolist())])
			else:
				continue
		# 	# rmchr_id_ord.index(ssbonds.tolist())
		# 	# if ssbonds == ['193','233']
			
				# print('probability of the pos (%s,%s) is %0.3f%%'%(ssbonds[0],ssbonds[1],out_[mutate_pos_ord.index(ssbonds.tolist())][1]*100))
			# except ValueError:
			# 	continue
	print('finish predict.')

def predict_one_map(sess,images,file,out):
	data = np.load(file).reshape((-1,12,12,1))
	out_ = sess.run(out,feed_dict={images:data})
	print(out_)
	# print(tf.argmax(out, 1))
	

def main(argv=None): 
	sess=tf.Session() 
	
	ckpt = tf.train.get_checkpoint_state(FLAGS.checkpoint_dir)
	print(ckpt)
	ckpt_path = ckpt.all_model_checkpoint_paths[-1]
	saver = tf.train.import_meta_graph(ckpt_path + '.meta')
	saver.restore(sess,ckpt_path)
	# saver = tf.train.import_meta_graph(ckpt.model_checkpoint_path + '.meta')
	# saver.restore(sess, ckpt.model_checkpoint_path + '-100')

	graph = tf.get_default_graph()

	images = graph.get_tensor_by_name('input_2/image:0')
	print (images)
	labels=graph.get_tensor_by_name('input_2/labels:0')

	logits = graph.get_tensor_by_name('softmax_linear/softmax_linear:0')
	# logits = new_fnn.inference(images, 128, 32)
	out=tf.nn.softmax(logits=logits)

	predict(sess,images,labels,logits,out)
	# test(sess,images,labels,logits,out)
	# predict_one_map(sess,images,'/Users/dongxq/Desktop/disulfide/predict_analysis/27_79change5_610.npy',out)

if __name__ == '__main__':
	FLAGS = parser.parse_args()
	tf.app.run()
