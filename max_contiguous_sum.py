import math
import random
from time import time
from turtle import right
import numpy as np

def solve_with_cum_sum(arr):
	cum_sum = np.zeros((len(arr))).astype(int)
	max_sum = -1000000
	inds = (0, 0)
	for i in range(len(arr)):
		if i==0:
			cum_sum[i] = arr[i]
		else:
			cum_sum[i] = cum_sum[i-1] + arr[i]
		for j in range(i):
			cum_sum_diff = cum_sum[i] - (cum_sum[j] - arr[j])
			# if cum_sum_diff is larger than max_sum, or if cum_sum_diff is equal but uses smaller index range
			if cum_sum_diff > max_sum or (cum_sum_diff == max_sum and i-j < inds[1] - inds[0]):
				max_sum = cum_sum_diff
				inds = (j, i)
	return inds[0], inds[1], max_sum	

def __get_mid_sum(range:range):
	decrement = True if range.stop < range.start else False
	s = 0
	max_sum = -100000
	pos = range.start
	best_pos  = pos
	while((decrement and pos >= range.stop) or (not decrement and pos <= range.stop)):
		s += arr[pos]
		if s > max_sum:
			max_sum = s
			best_pos = pos
		pos = pos - 1 if decrement else pos + 1
	return best_pos, max_sum


def get_mid_sum(arr, i, j):
	mid = (i + j) // 2
	ind_left,  max_sum_left = __get_mid_sum(range(mid, i))
	ind_right, max_sum_right = __get_mid_sum(range(mid, j))
	mid_sum = max_sum_right + max_sum_left - arr[mid]
	return ind_left, ind_right, mid_sum

def solve_with_div_conquer(arr, i, j):
	assert j >= i

	if i == j:
		return i, i, arr[i]
	elif j == i+1:
		if arr[j] >= 0 and arr[i] < 0:
			return j, j, arr[j]
		elif arr[i] >= 0 and arr[j] < 0:
			return i, i, arr[i]
		elif arr[i] > 0 and arr[j] > 0:
			return i, j, arr[i] + arr[j]
		else:
			if arr[i] < arr[j]:
				return j, j, arr[j]
			else:
				return i, i, arr[i]

	ind_left_left, ind_left_right, left_sum = solve_with_div_conquer(arr, i, (i+j)//2)
	ind_mid_left, ind_mid_right, mid_sum = get_mid_sum(arr, i, j)
	ind_right_left, ind_right_right, right_sum = solve_with_div_conquer(arr, i+(j-i)//2, j)

	# Get max of left vs right vs mid: first criteria is max sum, if equal, then look at smallest diff in index (multiplying the diff by -1 and then taking the max does the same thing)
	left = [left_sum, -1 * (ind_left_right-ind_left_left)]
	right = [right_sum, -1 * (ind_right_right-ind_right_left)]
	mid = [mid_sum, -1 * (ind_mid_right-ind_mid_left)]
	terms = {'left': left, 'right': right, 'mid': mid}

	greatest_term = max(terms.items(), key=lambda item: item[1])

	if greatest_term[0] == 'left':
		return ind_left_left, ind_left_right, left_sum
	elif greatest_term[0] == 'right':
		return ind_right_left, ind_right_right, right_sum
	else:
		return ind_mid_left, ind_mid_right, mid_sum

if __name__ == '__main__':
	k = 20000
	numbers = np.linspace(-k, k, k).astype(np.int64)
	arr = random.choices(numbers, k=k//2)

	# print(arr)
	st2 = time()
	ind_left2, ind_right2, sum2 = solve_with_div_conquer(arr, 0, len(arr)-1)
	et2 = round(time() - st2, 3)

	print(f"Div conquer method -- indices: [{ind_left2}, {ind_right2}], sum: {sum2}, runtime: {et2}")

	st1 = time()
	ind_left, ind_right, sum = solve_with_cum_sum(arr)
	et1 = round(time() - st1, 3)
	print(f"Cum sum method -- indices: [{ind_left}, {ind_right}], sum: {sum}, runtime: {et1}")








