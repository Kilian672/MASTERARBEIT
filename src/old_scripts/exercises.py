import numpy as np
import itertools

class Solution(object):
    def uniquePaths(self, m, n):
        """
        :type m: int
        :type n: int
        :rtype: int
        """
        solutions = np.ones((m,n))
        for i in range(1, m): 
            for j in range(1, n): 
                solutions[i][j] = solutions[i-1][j]+solutions[i][j-1]

        return solutions[m-1][n-1]
    
class Solution2(object):
    def zahlenschlange(self):
        
        combinations = list(itertools.permutations([1,2,3,4,5,6,7,8,9]))
        for x in combinations: 
            expression = 'x[0]*10-x[1]/x[2]+x[3]*11/x[4]-x[5]+12*x[6]/x[7]*x[8]-13'
            if eval(expression) == 31: 
                print(x)
                break

class Solution3(object):
    
    def __init__(self): 
        self.mapping = {"A": 1, "B": 2, "C": 3, "D": 4, 
                        "E": 5, "F": 6, "G": 7, "H": 8, 
                        "I": 9, "J": 10, "K": 11, "L": 12, 
                        "M": 13, "N": 14, "O": 15, "P": 16, 
                        "Q": 17, "R": 18, "S": 19, "T": 20, 
                        "U": 21, "V": 22, "W": 23, "X": 24, 
                        "Y": 25, "Z": 26}

        for key, value in self.mapping.items():
            self.mapping[key] = str(value)

    def numDecodings(self, s):
        """
        :type s: str
        :rtype: int
        """
        if s == "": 
            return 0
        
        numbers = list(self.mapping.values())

        numDec = 0
        while s != "":
            if len(s) == 1: 
                if s[0] in numbers: 
                    numDec = numDec + 1
                break

            if s[0] not in numbers and s[0:2] not in numbers: 
                return 0 
            else:  
                if s[1] in numbers: 
                    if s[0:2] in numbers: 
                        numDec = numDec + 2
                    else: 
                        numDec = numDec + 1
                else: 
                    if s[0:2] in numbers: 
                        numDec = numDec + 1
                
                s = s[2:]

        return numDec
    
 
class Solution4(object):
    

    def rotate_list(self, list_): 
        new_list = []
        new_list.append(list_[-1])
        for x in list_[:-1]: 
            new_list.append(x)
        return new_list

    def compute_sum(self, list_): 
        comp_sum = 0
        for i, x in enumerate(list_): 
            comp_sum = comp_sum + x*i
        return comp_sum

    def maxRotateFunction(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        original_nums = nums
        max_sum = self.compute_sum(original_nums)
        nums = self.rotate_list(nums)
        while nums != original_nums:
            current_sum = self.compute_sum(nums)
            if current_sum >= max_sum: 
                max_sum = current_sum

            nums = self.rotate_list(nums)
        
        return max_sum 

class Solution5(object):
    def jump(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        number_of_jumps = 0
        while len(nums) > 1: 
            if nums[0] >= len(nums)-1: 
                return number_of_jumps + 1
            else: 
                current_max = 0
                index = 0
                for i in range(1, nums[0]+1): 
                    if nums[i]+i >= current_max: 
                        current_max = nums[i]+i
                        index = i

                nums = nums[index:]
                number_of_jumps = number_of_jumps + 1
        
        return number_of_jumps


class Solution6(object):
    
    def concat_par_list(self, list1, list2):
        erg = []
        for x in list1: 
            for y in list2: 
                erg.append(x+y)
                erg.append(y+x)

        erg = list(set(erg))
        return erg

    def generateParenthesis(self, n):
        """
        :type n: int
        :rtype: List[str]
        """
        subproblems = [["()"]]
        for i in range(n): 
            subproblems.append(["("+subproblems[i-1][0]+")"])


        for i in range(1, n): 
            subprob = []
            for j in range(i): 
                subprob = self.concat_par_list(subproblems[j], subproblems[-j])
            
            subproblems[i] = subproblems[i] + subprob

        return subproblems[n-1]

class Solution7(object):
    def maxProduct(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        max_prod = 0

        for i in range(len(nums)): 
            curr_small = nums[i]
            curr_big = nums[i]
            for j in range(i+1, len(nums)): 
                if nums[j] == 0: 
                    break 
                if nums[j] < 0: 
                    curr_small = min(curr_small, curr_big*nums[j])
                    curr_big = max(curr_big, curr_small*nums[j])
                if nums[j] > 0: 
                    curr_small = min(curr_small, curr_small*nums[j])
                    curr_big = curr_big * nums[j]
                
            if max_prod < curr_big: 
                max_prod = curr_big

        return max_prod


class Solution8(object):
 

    def countBits(self, n):
        """
        :type n: int
        :rtype: List[int]
        """
        ans = [0, 1]
        i = len(ans)

        while i < n: 
            temp = []
            for x in ans: 
                temp.append(x)
            for x in temp:
                ans.append(1+x)
            i = len(ans)

        return ans[:n]

class Solution9(object):
    def smallerNumbersThanCurrent(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        n = len(nums)
        nums_copy = []
        for num in nums: 
            nums_copy.append(num)

        nums.sort()
        hash_map = {}
        k = n-2
        curr_num = nums[n-1]
        while k >= -1:
            if curr_num == nums[0]: 
                hash_map[curr_num] = 0
                break
            if nums[k] < curr_num: 
                hash_map[curr_num] = k 
                curr_num = nums[k]
            k = k-1

        for k in range(n): 
            nums_copy[k] = hash_map[nums_copy[k]]

        return nums_copy


if __name__ == "__main__": 

    sol = Solution9()
    sol.smallerNumbersThanCurrent([8,1,2,2,3])
    