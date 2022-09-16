import math
import random
from time import time
import numpy as np

def solve_with_dp(arr):
	cur_arr_sum = arr[0]
	max_arr_sum = arr[0]
	start_ind = 0
	inds = [0, 0]
	for i in range(1, len(arr)):
		if cur_arr_sum <= 0:
			cur_arr_sum = arr[i]
			start_ind = i
		else:
			cur_arr_sum += arr[i]

		if cur_arr_sum > max_arr_sum:
			max_arr_sum = cur_arr_sum
			inds = [start_ind, i]
	
	return inds[0], inds[1], max_arr_sum


def solve_with_brute_force(arr):
	max_sum = -math.inf
	for i in range(len(arr)):
		cur_sum = 0
		for j in range(i, len(arr)):
			cur_sum += arr[j]
			if cur_sum >= max_sum:
				inds = (i, j)
				max_sum = cur_sum
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

# return the max mid sum
def get_mid_sum(arr, i, j):
	mid = (i + j) // 2
	ind_left,  max_sum_left = __get_mid_sum(range(mid, i))
	ind_right, max_sum_right = __get_mid_sum(range(mid, j))
	# subtract arr[mid] to not double count it 
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

	ind_left_left, ind_left_right, left_sum = solve_with_div_conquer(arr, i, (i+j)//2 - 1)
	ind_mid_left, ind_mid_right, mid_sum = get_mid_sum(arr, i, j)
	ind_right_left, ind_right_right, right_sum = solve_with_div_conquer(arr, i + (j-i)//2 + 1, j)

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
	n = 500000
	numbers = np.arange(-n, n).astype(np.int64)
	arr = random.choices(numbers, k=n)

	st2 = time()
	ind_left2, ind_right2, sum2 = solve_with_div_conquer(arr, 0, len(arr)-1)
	et2 = round(time() - st2, 4)
	print(f"Div conquer method -- indices: [{ind_left2}, {ind_right2}], sum: {sum2}, runtime: {et2}")

	# st3 = time()
	# ind_left3, ind_right3, sum3 = solve_with_brute_force(arr)
	# et3 = round(time() - st3, 4)
	# print(f"Brute force method -- indices: [{ind_left3}, {ind_right3}], sum: {sum3}, runtime: {et3}")

	st4 = time()
	ind_left4, ind_right4, sum4 = solve_with_dp(arr)
	et4 = round(time() - st4, 4)
	print(f"DP method -- indices: [{ind_left4}, {ind_right4}], sum: {sum4}, runtime: {et4}")

	









